"""Optional PCA-based alignment of HEartLab silhouette images.

This utility estimates the dominant long axis of the UNION of all silhouettes,
rotates that axis to vertical, and translates the common silhouette centroid to
the horizontal image centre. It is intended as an optional preprocessing aid
when the rotational image set is slightly tilted in the image plane.

It is NOT a replacement for camera calibration and should not be described as
estimating camera pose. For rigorous geometric correction, use a known physical
reference/rotation axis.
"""

from pathlib import Path
import re
import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA


def natural_key(path: Path):
    return [int(x) if x.isdigit() else x.lower() for x in re.split(r"(\d+)", path.name)]


def load_silhouettes(folder: Path):
    pattern = re.compile(r"st_(\d+)_(-?\d+(?:\.\d+)?)\.png$", re.IGNORECASE)
    records = []
    for path in sorted(folder.glob("st_*.png"), key=natural_key):
        match = pattern.match(path.name)
        if not match:
            continue
        image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        if image is None:
            continue
        _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        records.append((path, int(match.group(1)), float(match.group(2)), image))
    return records


def estimate_alignment(union_image: np.ndarray):
    ys, xs = np.where(union_image > 0)
    if len(xs) < 3:
        raise ValueError("The union silhouette contains too few foreground pixels.")

    coords = np.column_stack((xs, ys))
    centroid = coords.mean(axis=0)

    # First PCA component = axis of greatest variance (dominant silhouette axis).
    pca = PCA(n_components=2)
    pca.fit(coords)
    axis = pca.components_[0]

    # In image coordinates (+y downward), theta is the dominant-axis angle from +x.
    theta_deg = np.degrees(np.arctan2(axis[1], axis[0]))

    # cv2.getRotationMatrix2D causes an image-coordinate line angle theta to become
    # theta - correction. Therefore correction = theta - 90° aligns it vertically.
    correction_deg = theta_deg - 90.0

    # PCA axis direction is sign-ambiguous; choose the smallest equivalent rotation.
    while correction_deg > 90.0:
        correction_deg -= 180.0
    while correction_deg < -90.0:
        correction_deg += 180.0

    return (float(centroid[0]), float(centroid[1])), float(correction_deg)


def align_image(image: np.ndarray, correction_deg: float, rotation_point):
    rows, cols = image.shape
    matrix = cv2.getRotationMatrix2D(rotation_point, correction_deg, 1.0)
    rotated = cv2.warpAffine(
        image, matrix, (cols, rows), flags=cv2.INTER_NEAREST, borderValue=0
    )

    # Rotate the chosen reference point, then move it to the horizontal centre.
    px, py = rotation_point
    new_x = matrix[0, 0] * px + matrix[0, 1] * py + matrix[0, 2]
    shift_x = cols / 2.0 - new_x
    translation = np.float32([[1, 0, shift_x], [0, 1, 0]])
    return cv2.warpAffine(
        rotated, translation, (cols, rows), flags=cv2.INTER_NEAREST, borderValue=0
    )


def main():
    root = tk.Tk()
    root.withdraw()

    input_dir = filedialog.askdirectory(title="Select silhouette folder")
    if not input_dir:
        return
    output_dir = filedialog.askdirectory(title="Select output folder")
    if not output_dir:
        return

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    records = load_silhouettes(input_dir)
    if not records:
        messagebox.showerror("Alignment", "No valid st_*.png silhouettes were found.")
        return

    shape = records[0][3].shape
    if any(record[3].shape != shape for record in records):
        messagebox.showerror("Alignment", "All silhouettes must have the same dimensions.")
        return

    union = np.zeros(shape, dtype=np.uint8)
    for _path, _idx, _angle, image in records:
        union = cv2.bitwise_or(union, image)

    rotation_point, correction_deg = estimate_alignment(union)
    print(f"Estimated in-plane alignment correction: {correction_deg:.3f}°")

    aligned_union = np.zeros_like(union)
    for path, _idx, _angle, image in records:
        aligned = align_image(image, correction_deg, rotation_point)
        cv2.imwrite(str(output_dir / path.name), aligned)
        aligned_union = cv2.bitwise_or(aligned_union, aligned)

    plt.figure()
    plt.imshow(aligned_union, cmap="gray")
    plt.title(f"Aligned silhouette union ({correction_deg:.2f}° correction)")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    main()
