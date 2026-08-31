from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DirectoryMonitorHandler(FileSystemEventHandler):
    """Custom handler for directory monitoring."""

    def __init__(self, log_function):
        """
        Initialize the handler.
        :param log_function: Function to call for logging messages.
        """
        self.log_function = log_function

    def normalize_path(self, path):
        """Normalize the path for consistent formatting."""
        return Path(path).as_posix()

    def on_created(self, event):
        """Log file or directory creation events."""
        normalized_path = self.normalize_path(event.src_path)
        if event.is_directory:
            self.log_function(f"Folder created: {normalized_path}")
        else:
            self.log_function(f"File created: {normalized_path}")

    def on_deleted(self, event):
        """Log file or directory deletion events."""
        normalized_path = self.normalize_path(event.src_path)
        if event.is_directory:
            self.log_function(f"Folder deleted: {normalized_path}")
        else:
            self.log_function(f"File deleted: {normalized_path}")

    def on_moved(self, event):
        """Log file or directory renaming events."""
        normalized_src_path = self.normalize_path(event.src_path)
        normalized_dest_path = self.normalize_path(event.dest_path)
        if event.is_directory:
            self.log_function(
                f"Folder renamed from: {normalized_src_path} to: {normalized_dest_path}"
            )
        else:
            self.log_function(
                f"File renamed from: {normalized_src_path} to: {normalized_dest_path}"
            )


class DirectoryMonitor:
    """Directory monitoring logic using watchdog."""

    def __init__(self, log_function):
        """
        Initialize the directory monitor.
        :param log_function: Function to call for logging messages.
        """
        self.observer = None
        self.log_function = log_function

    def start(self, directory_to_monitor):
        """Start monitoring the given directory."""
        dir_path = Path(directory_to_monitor)
        if not dir_path.is_dir():
            self.log_function("Error: Selected path is not a valid directory.")
            return

        self.observer = Observer()
        event_handler = DirectoryMonitorHandler(self.log_function)
        self.observer.schedule(event_handler, str(dir_path), recursive=True)
        self.observer.start()
        self.log_function(f"Started monitoring directory: {dir_path.as_posix()}")

    def stop(self):
        """Stop monitoring."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.log_function("Stopped directory monitoring.")
