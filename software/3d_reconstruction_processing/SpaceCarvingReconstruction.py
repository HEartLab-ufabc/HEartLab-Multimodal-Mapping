"""HEartLab rotational silhouette-based 3D reconstruction.

This program implements the reconstruction-processing stage described for the
HEartLab rotating-heart workflow:

1. Load MC-Calib camera parameters.
2. Load and undistort the rotational image sequence.
3. Generate and, if required, manually correct binary silhouettes.
4. Intersect the silhouettes in a rotating voxel volume (visual-hull / space
   carving approximation for a fixed camera and rotating object).
5. Convert the carved voxel volume to a triangular surface with marching cubes.

Camera calibration itself is intentionally not implemented here. Follow the
upstream MC-Calib project and supply its ``calibrated_cameras_data.yml`` output.

IMPORTANT
---------
The carved volume is expressed in voxel coordinates. Camera focal length alone
is not a valid conversion from voxel coordinates to millimetres. Apply a metric
scale only when a validated spatial calibration for the reconstruction volume is
available.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
import tkinter as tk
from tkinter import Scale, Toplevel, filedialog, messagebox, simpledialog

import cv2
import numpy as np
import psutil
import pyvista as pv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.path import Path as MPath
from matplotlib.widgets import PolygonSelector
from scipy.ndimage import binary_erosion, rotate
from skimage import measure


DEFAULT_ANGLE_DEG = 3.6
DEFAULT_VOXEL_SIZE = 500


def _set_high_priority_if_supported() -> None:
    """Best-effort process-priority increase; safe on non-Windows systems."""
    try:
        process = psutil.Process(os.getpid())
        if os.name == "nt" and hasattr(psutil, "HIGH_PRIORITY_CLASS"):
            process.nice(psutil.HIGH_PRIORITY_CLASS)
    except (psutil.Error, PermissionError, OSError):
        pass


def _natural_key(path: Path):
    """Sort filenames in human/numeric order (image_2 before image_10)."""
    return [int(part) if part.isdigit() else part.lower()
            for part in re.split(r"(\d+)", path.name)]


def _mc_node_real(node, default=0.0):
    try:
        if node is None or node.empty():
            return default
        return node.real()
    except Exception:
        return default


class SpaceCarvingApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("HEartLab 3D Space-Carving Reconstruction")

        self.images: list[np.ndarray] = []
        self.image_paths: list[Path] = []
        self.silhouettes: list[np.ndarray] = []
        self.current_image_index = 0

        self.camera_params = {
            "intrinsic": None,
            "distortion": None,
            "distortion_type": 0,
            "camera_pose": None,
            "camera_index": None,
        }

        self.voxel_size = DEFAULT_VOXEL_SIZE
        self.voxel_matrix = np.ones(
            (self.voxel_size, self.voxel_size, self.voxel_size), dtype=bool
        )
        self.surface_mesh: pv.PolyData | None = None

        self.save_dir: Path | None = None
        self.silhouette_dir: Path | None = None
        self.matrix_dir: Path | None = None
        self.mesh_dir: Path | None = None

        self.drawing = False
        self.adding_to_silhouette = True
        self.brush_size = 5
        self.conditional_threshold = True
        self.invert_silhouette = False
        self.polygon_selector = None
        self.polygon_mode_active = False
        self.show_polygon_message = True

        self._build_controls()
        self._create_display_window()

    # ------------------------------------------------------------------ UI --
    def _build_controls(self):
        tk.Button(
            self.root, text="Load MC-Calib Camera Parameters",
            command=self.load_camera_params_from_yaml
        ).pack()
        tk.Button(
            self.root, text="Load Images from Folder",
            command=self.load_images_from_folder
        ).pack()
        tk.Button(
            self.root, text="Select Save Directory",
            command=self.select_save_directory
        ).pack()

        tk.Button(
            self.root, text="Toggle Threshold Mode",
            command=self.toggle_threshold_mode
        ).pack()

        self.invert_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            self.root, text="Invert silhouette",
            variable=self.invert_var,
            command=self.toggle_invert
        ).pack()

        self.threshold_slider = Scale(
            self.root, from_=0, to=255, orient=tk.HORIZONTAL,
            label="Threshold / offset", command=self.update_silhouette
        )
        self.threshold_slider.pack()

        tk.Label(self.root, text="Angle between images (degrees)").pack()
        self.angle_entry = tk.Entry(self.root, width=10)
        self.angle_entry.insert(0, str(DEFAULT_ANGLE_DEG))
        self.angle_entry.pack()

        tk.Button(self.root, text="Next Image (carve)", command=self.next_image).pack()
        tk.Button(self.root, text="Skip Image", command=self.skip_image).pack()
        tk.Button(
            self.root, text="Toggle Add/Erase",
            command=self.toggle_drawing_mode
        ).pack()

        self.brush_size_slider = Scale(
            self.root, from_=1, to=20, orient=tk.HORIZONTAL,
            label="Brush Size", command=self.update_brush_size
        )
        self.brush_size_slider.set(5)
        self.brush_size_slider.pack()

        tk.Button(self.root, text="Draw Polygon", command=self.activate_polygon_mode).pack()
        tk.Button(
            self.root, text="Load Existing Silhouettes",
            command=self.choose_existing_silhouettes
        ).pack()
        tk.Button(
            self.root, text="Save Current Voxel Matrix",
            command=self.save_voxel_matrix
        ).pack()
        tk.Button(self.root, text="Load Voxel Matrix", command=self.load_voxel_matrix).pack()
        tk.Button(self.root, text="Generate Mesh", command=self.voxel_to_mesh).pack()
        tk.Button(self.root, text="Smooth Mesh", command=self.refine_mesh).pack()
        tk.Button(self.root, text="Save Current Mesh", command=self.save_current_mesh).pack()
        tk.Button(self.root, text="Show 3D Preview", command=self.show_3d_preview).pack()

        self.image_counter_label = tk.Label(self.root, text="Image 0/0")
        self.image_counter_label.pack()

    def _create_display_window(self):
        self.display_window = Toplevel(self.root)
        self.display_window.title("Image and Silhouette Display")
        self.figure = Figure(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, self.display_window)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect("button_press_event", self.on_mouse_press)
        self.canvas.mpl_connect("button_release_event", self.on_mouse_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)

    # ---------------------------------------------------------- calibration --
    def load_camera_params_from_yaml(self):
        file_path = filedialog.askopenfilename(
            title="Select MC-Calib calibrated_cameras_data.yml",
            filetypes=[("YAML files", "*.yml *.yaml")],
        )
        if not file_path:
            return

        fs = cv2.FileStorage(file_path, cv2.FILE_STORAGE_READ)
        if not fs.isOpened():
            messagebox.showerror("Error", "Could not open the calibration file.")
            return

        try:
            nb_node = fs.getNode("nb_camera")
            num_cameras = int(_mc_node_real(nb_node, 0))
            if num_cameras <= 0:
                messagebox.showerror(
                    "Error", "No cameras were found in the MC-Calib calibration file."
                )
                return

            selected = simpledialog.askinteger(
                "Select Camera",
                f"Enter camera number (0 to {num_cameras - 1})",
                minvalue=0,
                maxvalue=num_cameras - 1,
            )
            if selected is None:
                return

            cam_node = fs.getNode(f"camera_{selected}")
            intrinsic = cam_node.getNode("camera_matrix").mat()
            distortion = cam_node.getNode("distortion_vector").mat()
            pose = cam_node.getNode("camera_pose_matrix").mat()
            distortion_type = int(_mc_node_real(cam_node.getNode("distortion_type"), 0))

            if intrinsic is None or distortion is None:
                messagebox.showerror(
                    "Error", f"Missing intrinsic/distortion parameters for camera_{selected}."
                )
                return

            self.camera_params.update({
                "intrinsic": intrinsic,
                "distortion": distortion,
                "distortion_type": distortion_type,
                "camera_pose": pose,
                "camera_index": selected,
            })
            messagebox.showinfo(
                "Calibration",
                f"MC-Calib parameters loaded for camera_{selected}."
            )
        finally:
            fs.release()

    def undistort_image(self, image: np.ndarray) -> np.ndarray:
        k = self.camera_params["intrinsic"]
        d = self.camera_params["distortion"]
        distortion_type = self.camera_params["distortion_type"]
        h, w = image.shape[:2]

        if distortion_type == 1:
            # MC-Calib: 1 = Kannala/fisheye model.
            d = np.asarray(d, dtype=np.float64).reshape(-1, 1)
            return cv2.fisheye.undistortImage(
                image, np.asarray(k, dtype=np.float64), d,
                Knew=np.asarray(k, dtype=np.float64), new_size=(w, h)
            )

        # MC-Calib: 0 = Brown/perspective model.
        new_k, _ = cv2.getOptimalNewCameraMatrix(k, d, (w, h), 1, (w, h))
        return cv2.undistort(image, k, d, None, new_k)

    # --------------------------------------------------------------- images --
    def load_images_from_folder(self):
        if self.camera_params["intrinsic"] is None:
            messagebox.showerror(
                "Error", "Load the MC-Calib camera parameters before loading images."
            )
            return

        folder = filedialog.askdirectory(title="Select Rotational Image Folder")
        if not folder:
            return

        extensions = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp"}
        paths = sorted(
            [p for p in Path(folder).iterdir() if p.is_file() and p.suffix.lower() in extensions],
            key=_natural_key,
        )
        if not paths:
            messagebox.showerror("Error", "No supported image files were found.")
            return

        images = []
        valid_paths = []
        for path in paths:
            image = cv2.imread(str(path), cv2.IMREAD_COLOR)
            if image is None:
                print(f"Warning: could not read {path}")
                continue
            images.append(self.undistort_image(image))
            valid_paths.append(path)

        if not images:
            messagebox.showerror("Error", "None of the selected images could be read.")
            return

        self.images = images
        self.image_paths = valid_paths
        self.current_image_index = 0
        self.silhouettes = [self.generate_silhouette(image) for image in self.images]
        self.reset_voxel_matrix()
        self.update_image_counter()
        self.show_image()

    def generate_silhouette(self, image: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold = self.threshold_slider.get()

        if self.conditional_threshold:
            threshold = np.clip(float(np.mean(gray)) + threshold, 0, 255)

        mode = cv2.THRESH_BINARY_INV if self.invert_silhouette else cv2.THRESH_BINARY
        _, bw = cv2.threshold(gray, threshold, 255, mode)

        # Keep the largest connected foreground region as the initial heart mask.
        labels = measure.label(bw > 0, connectivity=2)
        props = measure.regionprops(labels)
        if not props:
            return bw.astype(np.uint8)

        largest = max(props, key=lambda p: p.area)
        return (labels == largest.label).astype(np.uint8) * 255

    def update_silhouette(self, _value=None):
        if not self.images:
            return
        self.silhouettes[self.current_image_index] = self.generate_silhouette(
            self.images[self.current_image_index]
        )
        self.show_image()

    def toggle_threshold_mode(self):
        self.conditional_threshold = not self.conditional_threshold
        mode = "mean + offset" if self.conditional_threshold else "absolute"
        messagebox.showinfo("Threshold Mode", f"Threshold mode: {mode}")
        self.update_silhouette()

    def toggle_invert(self):
        self.invert_silhouette = bool(self.invert_var.get())
        self.update_silhouette()

    # ---------------------------------------------------------- mask editing --
    def show_image(self):
        if not self.silhouettes or not self.images:
            return
        image = self.images[self.current_image_index]
        mask = self.silhouettes[self.current_image_index]
        overlay = image.copy()
        overlay[mask == 255] = (255, 0, 0)
        blended = cv2.addWeighted(image, 0.7, overlay, 0.3, 0)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.imshow(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))
        ax.axis("off")
        self.figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.canvas.draw()

    def toggle_drawing_mode(self):
        self.adding_to_silhouette = not self.adding_to_silhouette
        messagebox.showinfo(
            "Drawing Mode", "Mode: " + ("Add" if self.adding_to_silhouette else "Erase")
        )

    def update_brush_size(self, value):
        self.brush_size = int(float(value))

    def on_mouse_press(self, event):
        if not self.polygon_mode_active:
            self.drawing = True
            self.modify_silhouette(event)

    def on_mouse_release(self, _event):
        if not self.polygon_mode_active:
            self.drawing = False

    def on_mouse_move(self, event):
        if self.drawing and not self.polygon_mode_active:
            self.modify_silhouette(event)

    def modify_silhouette(self, event):
        if not self.silhouettes or event.xdata is None or event.ydata is None:
            return
        x, y = int(event.xdata), int(event.ydata)
        mask = self.silhouettes[self.current_image_index]
        if not (0 <= x < mask.shape[1] and 0 <= y < mask.shape[0]):
            return
        color = 255 if self.adding_to_silhouette else 0
        cv2.circle(mask, (x, y), self.brush_size, color, -1)
        self.show_image()

    def activate_polygon_mode(self):
        if not self.silhouettes:
            messagebox.showerror("Error", "No silhouette is available to edit.")
            return
        self.polygon_mode_active = True
        self.drawing = False
        self.polygon_selector = PolygonSelector(
            self.figure.gca(), self.on_polygon_complete,
            useblit=True, props=dict(color="red", linewidth=2, linestyle="--")
        )
        if self.show_polygon_message:
            messagebox.showinfo(
                "Polygon Mode", "Select a polygon and close it to apply the edit."
            )
            self.show_polygon_message = False

    def on_polygon_complete(self, vertices):
        self.polygon_mode_active = False
        mask = self.silhouettes[self.current_image_index]
        height, width = mask.shape
        poly_path = MPath(vertices)
        x, y = np.meshgrid(np.arange(width), np.arange(height))
        points = np.column_stack((x.ravel(), y.ravel()))
        selected = poly_path.contains_points(points).reshape(height, width)
        mask[selected] = 255 if self.adding_to_silhouette else 0
        self.show_image()
        if self.polygon_selector is not None:
            self.polygon_selector.disconnect_events()
            self.polygon_selector = None

    # ---------------------------------------------------------- space carve --
    def get_angle_step(self) -> float | None:
        try:
            angle = float(self.angle_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter a valid angle between images.")
            return None
        if angle == 0:
            messagebox.showerror("Error", "The angular increment cannot be zero.")
            return None
        return angle

    def reset_voxel_matrix(self):
        self.voxel_matrix = np.ones(
            (self.voxel_size, self.voxel_size, self.voxel_size), dtype=bool
        )
        self.surface_mesh = None

    def silhouette_to_voxel_projection(self, silhouette: np.ndarray) -> np.ndarray:
        """Resize and center a silhouette in the square voxel projection plane."""
        h, w = silhouette.shape
        scale = min(self.voxel_size / w, self.voxel_size / h)
        new_w = max(1, int(round(w * scale)))
        new_h = max(1, int(round(h * scale)))
        resized = cv2.resize(
            silhouette, (new_w, new_h), interpolation=cv2.INTER_NEAREST
        )
        centered = np.zeros((self.voxel_size, self.voxel_size), dtype=bool)
        y0 = (self.voxel_size - new_h) // 2
        x0 = (self.voxel_size - new_w) // 2
        centered[y0:y0 + new_h, x0:x0 + new_w] = resized > 0
        return centered

    def carve_silhouette(self, silhouette: np.ndarray):
        projection = self.silhouette_to_voxel_projection(silhouette)
        # Broadcasting avoids allocating an explicit V x V x V repeated mask.
        self.voxel_matrix &= projection[:, :, np.newaxis]

    @staticmethod
    def rotate_voxel_matrix(matrix: np.ndarray, angle: float) -> np.ndarray:
        # Rotation axis follows the original HEartLab implementation.
        rotated = rotate(
            matrix, angle=angle, axes=(1, 2), reshape=False,
            order=0, mode="constant", cval=0, prefilter=False
        )
        return rotated.astype(bool, copy=False)

    def current_absolute_angle(self) -> float:
        angle = self.get_angle_step()
        if angle is None:
            return 0.0
        return self.current_image_index * angle

    def next_image(self):
        if not self.images:
            messagebox.showerror("Error", "Load images first.")
            return
        angle_step = self.get_angle_step()
        if angle_step is None:
            return

        idx = self.current_image_index
        self.carve_silhouette(self.silhouettes[idx])
        self.save_silhouette(idx, idx * angle_step)

        if idx >= len(self.images) - 1:
            self.update_image_counter()
            messagebox.showinfo("Reconstruction", "Last image carved.")
            return

        self.voxel_matrix = self.rotate_voxel_matrix(self.voxel_matrix, angle_step)
        self.current_image_index += 1
        self.update_image_counter()
        self.show_image()

    def skip_image(self):
        if not self.images:
            return
        angle_step = self.get_angle_step()
        if angle_step is None:
            return
        if self.current_image_index >= len(self.images) - 1:
            messagebox.showinfo("Reconstruction", "Already at the final image.")
            return
        self.voxel_matrix = self.rotate_voxel_matrix(self.voxel_matrix, angle_step)
        self.current_image_index += 1
        self.update_image_counter()
        self.show_image()

    def update_image_counter(self):
        total = len(self.images)
        if total:
            angle_step = self.get_angle_step()
            angle = self.current_image_index * angle_step if angle_step is not None else 0
            self.image_counter_label.config(
                text=f"Image {self.current_image_index + 1}/{total} — {angle:.1f}°"
            )
        else:
            self.image_counter_label.config(text="Image 0/0")

    # -------------------------------------------------------------- storage --
    def select_save_directory(self):
        selected = filedialog.askdirectory(title="Select Directory to Save Reconstruction")
        if not selected:
            return
        self.save_dir = Path(selected)
        self.silhouette_dir = self.save_dir / "silhouettes"
        self.matrix_dir = self.save_dir / "voxel_matrix"
        self.mesh_dir = self.save_dir / "mesh"
        for directory in (self.silhouette_dir, self.matrix_dir, self.mesh_dir):
            directory.mkdir(parents=True, exist_ok=True)
        messagebox.showinfo("Save Directory", str(self.save_dir))

    def ensure_save_directory(self) -> bool:
        if self.save_dir is None:
            self.select_save_directory()
        return self.save_dir is not None

    def save_silhouette(self, index: int, absolute_angle: float):
        if not self.ensure_save_directory():
            return
        filename = f"st_{index:03d}_{absolute_angle:.1f}.png"
        output = self.silhouette_dir / filename
        if not cv2.imwrite(str(output), self.silhouettes[index]):
            messagebox.showerror("Error", f"Could not save {output}")

    def choose_existing_silhouettes(self):
        folder = filedialog.askdirectory(title="Select Existing Silhouette Folder")
        if not folder:
            return
        files = sorted(Path(folder).glob("st_*.png"), key=_natural_key)
        if not files:
            messagebox.showerror("Error", "No st_*.png silhouettes found.")
            return
        self.reconstruct_from_saved_silhouettes(files)

    def reconstruct_from_saved_silhouettes(self, files: list[Path]):
        pattern = re.compile(r"st_(\d+)_(-?\d+(?:\.\d+)?)\.png$", re.IGNORECASE)
        records = []
        for path in files:
            match = pattern.match(path.name)
            if not match:
                continue
            image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
            if image is not None:
                records.append((int(match.group(1)), float(match.group(2)), image))
        records.sort(key=lambda item: item[0])
        if not records:
            messagebox.showerror("Error", "No valid saved silhouettes were found.")
            return

        self.reset_voxel_matrix()
        previous_angle = records[0][1]
        if abs(previous_angle) > 1e-9:
            self.voxel_matrix = self.rotate_voxel_matrix(self.voxel_matrix, previous_angle)

        for i, (_idx, absolute_angle, silhouette) in enumerate(records):
            if i > 0:
                delta = absolute_angle - previous_angle
                self.voxel_matrix = self.rotate_voxel_matrix(self.voxel_matrix, delta)
            self.carve_silhouette(silhouette)
            previous_angle = absolute_angle

        messagebox.showinfo(
            "Reconstruction", f"Carved {len(records)} saved silhouettes."
        )

    def save_voxel_matrix(self):
        if not self.ensure_save_directory():
            return
        path = self.matrix_dir / "visual_hull_voxels.npy"
        np.save(path, self.voxel_matrix)
        messagebox.showinfo("Saved", str(path))

    def load_voxel_matrix(self):
        file_path = filedialog.askopenfilename(
            title="Select Voxel Matrix", filetypes=[("NumPy files", "*.npy")]
        )
        if not file_path:
            return
        matrix = np.load(file_path)
        if matrix.ndim != 3 or not (matrix.shape[0] == matrix.shape[1] == matrix.shape[2]):
            messagebox.showerror("Error", "Voxel matrix must be cubic and 3-dimensional.")
            return
        self.voxel_size = matrix.shape[0]
        self.voxel_matrix = matrix.astype(bool)
        self.surface_mesh = None
        messagebox.showinfo("Loaded", f"Loaded {self.voxel_size}³ voxel matrix.")

    # --------------------------------------------------------------- mesh --
    def extract_surface_voxels(self) -> np.ndarray:
        eroded = binary_erosion(self.voxel_matrix)
        surface = self.voxel_matrix & ~eroded
        return np.array(np.where(surface)).T

    def show_3d_preview(self):
        points = self.extract_surface_voxels()
        if points.size == 0:
            messagebox.showinfo("Preview", "No carved surface is available.")
            return
        plotter = pv.Plotter(window_size=(800, 600))
        # Decimate preview points if the surface is very large.
        if len(points) > 250_000:
            step = int(np.ceil(len(points) / 250_000))
            points = points[::step]
        plotter.add_points(points.astype(np.float32), point_size=2)
        plotter.show_grid()
        plotter.show(title="Visual-Hull Surface Voxels")

    def voxel_to_mesh(self):
        if not np.any(self.voxel_matrix):
            messagebox.showerror("Error", "The voxel volume is empty.")
            return
        try:
            vertices, faces, _normals, _values = measure.marching_cubes(
                self.voxel_matrix.astype(np.uint8), level=0.5
            )
            pv_faces = np.hstack(
                (np.full((faces.shape[0], 1), 3, dtype=np.int64), faces.astype(np.int64))
            ).ravel()
            self.surface_mesh = pv.PolyData(vertices, pv_faces).clean()
            plotter = pv.Plotter(window_size=(800, 600))
            plotter.add_mesh(self.surface_mesh, color="lightblue", show_edges=False)
            plotter.show_bounds(
                grid="back", location="outer",
                xlabel="X (voxel)", ylabel="Y (voxel)", zlabel="Z (voxel)"
            )
            plotter.show(title="HEartLab Visual-Hull Mesh")
        except Exception as exc:
            messagebox.showerror("Mesh Generation", f"Mesh generation failed: {exc}")

    def refine_mesh(self):
        if self.surface_mesh is None:
            messagebox.showerror("Error", "Generate a mesh first.")
            return
        try:
            self.surface_mesh = self.surface_mesh.clean().smooth(
                n_iter=20, relaxation_factor=0.05
            )
            plotter = pv.Plotter(window_size=(800, 600))
            plotter.add_mesh(self.surface_mesh, color="lightblue", show_edges=False)
            plotter.show(title="Smoothed HEartLab Mesh")
        except Exception as exc:
            messagebox.showerror("Mesh Refinement", str(exc))

    def save_current_mesh(self):
        if self.surface_mesh is None:
            messagebox.showerror("Error", "No mesh is available to save.")
            return
        if not self.ensure_save_directory():
            return
        file_path = filedialog.asksaveasfilename(
            initialdir=str(self.mesh_dir),
            title="Save Mesh",
            defaultextension=".ply",
            filetypes=[("PLY", "*.ply"), ("STL", "*.stl"), ("OBJ", "*.obj")],
        )
        if not file_path:
            return
        self.surface_mesh.save(file_path)
        messagebox.showinfo(
            "Saved",
            "Mesh saved in voxel coordinates. Apply metric scaling only after a validated spatial calibration."
        )


if __name__ == "__main__":
    _set_high_priority_if_supported()
    root = tk.Tk()
    app = SpaceCarvingApp(root)
    root.mainloop()
