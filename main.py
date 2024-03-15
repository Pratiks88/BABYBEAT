import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from mainwindow import MainWindow
from rppg import RPPG

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Prompt user to select a video file
    file_dialog = QFileDialog()
    video_file_path, _ = file_dialog.getOpenFileName(None, "Select Video File", "", "Video Files (*.mp4 *.avi *.mov)")

    if not video_file_path:
        sys.exit("No video file selected.")

    rppg = RPPG(video=video_file_path, parent=app)  # Pass video file path to RPPG
    win = MainWindow(rppg=rppg)
    win.show()

    rppg.start()
    sys.exit(app.exec_())