import os
import random
import sys
import threading
import keyboard
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget

# --- KONFIGURACE ---
VIDEO_NAME = "foxy1.mp4"  # Jméno souboru s videem
CHECK_INTERVAL_SECONDS = 300  # Doba, po které proběhne kontrola (300 sekund = 5 minut)
CHANCE_PER_CHECK = 0.2  # Šance na jumpscare při každé kontrole (0.2 = 20 %)



def get_resource_path(relative_path):
    """Vrátí absolutní cestu k souboru (funguje v dev režimu i uvnitř PyInstaller .exe)"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


PATH_TO_VIDEO = get_resource_path(VIDEO_NAME)



def setup_hotkey():
    # Stisknutím Ctrl+Alt+K se aplikace okamžitě vypne
    keyboard.add_hotkey('ctrl+alt+k', lambda: os._exit(0))
    keyboard.wait()



threading.Thread(target=setup_hotkey, daemon=True).start()


class VideoJumpscareWindow(QWidget):

    def __init__(self, video_path):
        super().__init__()
        self.setWindowTitle('Jumpscare Overlay')

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)


        self.video_widget = QVideoWidget(self)
        layout.addWidget(self.video_widget)

        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)

        # Hlasitost na 100 % (1.0)
        self.audio_output.setVolume(1.0)

        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)


        self.media_player.setSource(QUrl.fromLocalFile(video_path))
        self.media_player.mediaStatusChanged.connect(self.on_status_changed)

    def trigger_jumpscare(self):
        self.showFullScreen()
        self.media_player.setPosition(0)
        self.media_player.play()

    def on_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.hide()


def check_for_jumpscare(window):
    roll = random.random()
    if roll < CHANCE_PER_CHECK:
        window.trigger_jumpscare()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    jumpscare_win = VideoJumpscareWindow(PATH_TO_VIDEO)

    main_timer = QTimer()
    main_timer.timeout.connect(lambda: check_for_jumpscare(jumpscare_win))
    main_timer.start(CHECK_INTERVAL_SECONDS * 1000)

    sys.exit(app.exec())