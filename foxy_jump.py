import sys
import os
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

# --- KONFIGURACE ---
VIDEO_NAME = "foxy1.mp4"         # Jméno souboru
CHECK_INTERVAL_SECONDS = 300   # doba po které proběhne kontrola v sekundách (300 = 5 minut)
CHANCE_PER_CHECK = 0.2        # šance na jumpscare při každé kontrole (0.2 = 20 %)


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_TO_VIDEO = os.path.join(SCRIPT_DIR, VIDEO_NAME)

class VideoJumpscareWindow(QWidget):
    def __init__(self, video_path):
        super().__init__()
        self.setWindowTitle("Jumpscare Overlay")
        

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        



        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Video přehrávač
        self.video_widget = QVideoWidget(self)
        layout.addWidget(self.video_widget)

        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        
        # Hlasitost na 100 % (1.0)
        self.audio_output.setVolume(1.0)
        
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)
        
        # Načtení přesné cesty
        print(f"Načítám video z cesty: {video_path}")
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
    print(f"Kontrola jumpscaru... Hodil jsi: {roll:.2f}")

    if roll < CHANCE_PER_CHECK:
        print("!!! FOXY JUMPSCARE !!!")
        window.trigger_jumpscare()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    jumpscare_win = VideoJumpscareWindow(PATH_TO_VIDEO)


    main_timer = QTimer()
    main_timer.timeout.connect(lambda: check_for_jumpscare(jumpscare_win))
    main_timer.start(CHECK_INTERVAL_SECONDS * 1000)

    print(f"Skript spuštěn. Testovací režim: Jumpscare nastane do {CHECK_INTERVAL_SECONDS} sekund...")
    sys.exit(app.exec())