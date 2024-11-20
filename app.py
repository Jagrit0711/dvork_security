# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
import cv2
import numpy as np
import sys
import cv2
import numpy as np
import sys
import os
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, 
                             QHBoxLayout, QPushButton, QStackedWidget, QGridLayout,
                             QCheckBox, QFrame, QSplitter, QGraphicsDropShadowEffect,
                             QSystemTrayIcon, QMenu, QAction, QStyle, QInputDialog,
                             QLineEdit, QMessageBox, QGroupBox, QFormLayout, QComboBox,
                             QSlider, QSpinBox, QGraphicsOpacityEffect, QSplashScreen,
                             QDialog, QDialogButtonBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QDateEdit, QFileDialog, QHeaderView,
                             QTextEdit, QScrollArea, QMessageBox, QSizePolicy)
from PyQt5.QtCore import (Qt, QTimer, QThread, pyqtSignal, QPoint, QPointF, QPropertyAnimation, 
                          QEasingCurve, QRect, QRectF, QSize, QSequentialAnimationGroup,
                          QParallelAnimationGroup, QDate)
from PyQt5.QtGui import (QImage, QPixmap, QPalette, QColor, QFont, QPainter, 
                         QPainterPath, QIcon, QLinearGradient, QBrush, QPen)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtNetwork import QTcpSocket
import pandas as pd
from datetime import datetime
from database_handler import DatabaseHandler
import time
from PyQt5.QtCore import QTime, QTimer
import requests
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import cv2
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, 
                             QFileDialog)
from PyQt5.QtCore import QDate
from datetime import datetime
import pandas as pd
from database_handler import DatabaseHandler
from database_sos_message import SOSDatabaseHandler
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QSplashScreen, QLabel, QProgressBar
from PyQt5.QtGui import QPixmap, QColor, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, 
                             QListWidget, QMessageBox)
from attendance import AttendanceProcessor
from PyQt5.QtCore import QTimer
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

PROTOTXT_PATH = r"C:\Users\jagir\CCTV_v.0.2\MobileNetSSD_deploy.prototxt.txt"
MODEL_PATH = resource_path("MobileNetSSD_deploy.caffemodel")

PROTOTXT_PATH = resource_path("MobileNetSSD_deploy.prototxt.txt")
MODEL_PATH = resource_path("MobileNetSSD_deploy.caffemodel")

PROTOTXT_PATH = resource_path("MobileNetSSD_deploy.prototxt.txt")
MODEL_PATH = resource_path("MobileNetSSD_deploy.caffemodel")
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class PersonDetector:
    def __init__(self):
        # Load the MobileNet-SSD model
        self.net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)
class PersonDetector:
    def __init__(self):
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor"]
        self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))
        self.db_handler = DatabaseHandler()

    def detect_people(self, frame):
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                     0.007843, (300, 300), 127.5)
   
        self.net.setInput(blob)
        detections = self.net.forward()
        
        people = []
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                idx = int(detections[0, 0, i, 1])
                if self.CLASSES[idx] == "person":
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    people.append((startX, startY, endX, endY))
                    # Log attendance
                    self.db_handler.log_attendance(person_id=idx, timestamp=datetime.now())
        
        return people
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray, int)

    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self._run_flag = True
        self.person_detector = PersonDetector()

    def run(self):
        cap = cv2.VideoCapture(self.camera_index)
        while self._run_flag:
            ret, frame = cap.read()
            if ret:
                people = self.person_detector.detect_people(frame)
                self.change_pixmap_signal.emit(frame, len(people))
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class WebViewWidget(QWidget):
    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.url = url
        self.layout = QVBoxLayout(self)
        
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl(url))
        self.layout.addWidget(self.web_view)
        
        button_layout = QHBoxLayout()
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_page)
        button_layout.addWidget(self.refresh_button)
        
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close_page)
        button_layout.addWidget(self.close_button)
        
        self.layout.addLayout(button_layout)

    def refresh_page(self):
        self.web_view.reload()

    def close_page(self):
        if isinstance(self.parent, CCTVApp):
            self.parent.show_admin_page()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class LiveMapWidget(QWidget):
    def __init__(self, parent=None, is_preview=False):
        super().__init__(parent)
        self.setMinimumSize(800, 600) if not is_preview else self.setFixedSize(400, 300)
        self.attendance = 0
        self.class_count = 0
        self.is_preview = is_preview

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        scale_x = width / 800
        scale_y = height / 600

        # Draw background
        painter.fillRect(self.rect(), QColor(30, 30, 30))

        # Draw main building outline
        building_color = QColor(100, 100, 100)
        painter.setBrush(QBrush(building_color))
        painter.setPen(QPen(Qt.white, 2))
        painter.drawRect(int(50*scale_x), int(50*scale_y), int(600*scale_x), int(500*scale_y))

        # Draw corridors
        corridor_color = QColor(80, 80, 80)
        painter.fillRect(int(50*scale_x), int(250*scale_y), int(600*scale_x), int(100*scale_y), corridor_color)
        painter.fillRect(int(300*scale_x), int(50*scale_y), int(100*scale_x), int(500*scale_y), corridor_color)

        # Draw classrooms
        self.draw_room(painter, int(75*scale_x), int(75*scale_y), int(200*scale_x), int(150*scale_y), "11A", scale_x, scale_y)
        self.draw_room(painter, int(425*scale_x), int(75*scale_y), int(200*scale_x), int(150*scale_y), "11B", scale_x, scale_y)

        # Draw washroom
        self.draw_room(painter, int(75*scale_x), int(375*scale_y), int(200*scale_x), int(150*scale_y), "Washroom", scale_x, scale_y)

        # Draw playground
        playground_color = QColor(50, 150, 50)
        painter.setBrush(QBrush(playground_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(int(425*scale_x), int(375*scale_y), int(200*scale_x), int(150*scale_y))
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", int(10 * scale_y)))
        painter.drawText(int(475*scale_x), int(460*scale_y), "Playground")

        # Draw construction zone (separate from main building)
        construction_color = QColor(200, 50, 50)
        painter.setBrush(QBrush(construction_color))
        painter.setPen(QPen(Qt.white, 2))
        painter.drawRect(int(675*scale_x), int(50*scale_y), int(100*scale_x), int(100*scale_y))
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", int(8 * scale_y)))
        painter.drawText(int(685*scale_x), int(100*scale_y), "Construction")

        # Draw attendance info for 11A
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", int(10 * scale_y)))
        painter.drawText(int(85*scale_x), int(105*scale_y), f"Attendance: {self.attendance}")
        painter.drawText(int(85*scale_x), int(125*scale_y), f"Class Count: {self.class_count}")

        # Draw students in 11A
        self.draw_students(painter, int(75*scale_x), int(75*scale_y), int(200*scale_x), int(150*scale_y), scale_x, scale_y)

        # Draw "No Camera Connected" text
        painter.setPen(QColor(255, 0, 0))
        painter.setFont(QFont("Arial", int(8 * scale_y)))
        painter.drawText(int(60*scale_x), int(280*scale_y), "No Camera Connected")
        painter.drawText(int(310*scale_x), int(280*scale_y), "No Camera Connected")
        painter.drawText(int(435*scale_x), int(280*scale_y), "No Camera Connected")

        # If it's a preview, don't draw the legend
        if not self.is_preview:
            self.draw_legend(painter, scale_x, scale_y)

    def draw_room(self, painter, x, y, width, height, name, scale_x, scale_y):
        painter.setBrush(QBrush(QColor(50, 50, 50)))
        painter.setPen(QPen(Qt.white, 2))
        painter.drawRect(x, y, width, height)
        painter.setFont(QFont("Arial", int(12 * scale_y)))
        painter.drawText(x + 10, y + 20, name)

    def draw_students(self, painter, x, y, width, height, scale_x, scale_y):
        painter.setBrush(QBrush(QColor(0, 0, 255)))
        painter.setPen(Qt.NoPen)
        max_students_per_row = 8
        student_size = min(int(15 * scale_x), int(15 * scale_y))
        for i in range(self.attendance):
            student_x = x + 20 + (i % max_students_per_row) * (student_size + 5)
            student_y = y + 50 + (i // max_students_per_row) * (student_size + 5)
            painter.drawEllipse(QPointF(student_x, student_y), student_size // 2, student_size // 2)

    def draw_legend(self, painter, scale_x, scale_y):
        legend_x = int(50 * scale_x)
        legend_y = int(560 * scale_y)
        legend_spacing = int(100 * scale_x)

        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", int(10 * scale_y)))
        painter.drawText(legend_x, legend_y, "Legend:")
        
        legend_items = [
            (QColor(0, 0, 255), "Student"),
            (QColor(128, 0, 128), "Teacher"),
            (QColor(255, 0, 0), "Admin Staff")
        ]

        for i, (color, label) in enumerate(legend_items):
            x = legend_x + legend_spacing * (i + 1)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(QPointF(x, legend_y - 5), 5, 5)
            painter.drawText(x + 15, legend_y, label)

    def update_attendance(self, attendance, class_count):
        self.attendance = attendance
        self.class_count = class_count
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()

# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.

class AlwaysOnTopWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(44, 62, 80, 200); border-radius: 10px;")
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.label = QLabel("C: 0 | PP: 4")
        self.label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.label.setAlignment(Qt.AlignCenter)
        
        self.layout.addWidget(self.label)
        
        self.setGeometry(100, 100, 150, 50)
        self.oldPos = self.pos()

    def update_counts(self, camera_count, rfid_count):
        self.label.setText(f"C: {camera_count} | PP: {4}")

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class AnimatedWatermark(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Zylon Security")
        self.setStyleSheet("font-size: 48px; font-weight: bold; color: transparent;")
        self.setAlignment(Qt.AlignCenter)
        self.fill_level = 0

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addText(self.rect().center(), self.font(), self.text())

        gradient = QLinearGradient(0, self.height(), 0, 0)
        gradient.setColorAt(0, QColor(41, 128, 185))  # Light blue
        gradient.setColorAt(1, QColor(52, 152, 219))  # Darker blue

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)

        # Create clipping path for liquid fill effect
        clip_path = QPainterPath()
        clip_path.addRect(0, self.height() * (1 - self.fill_level), self.width(), self.height())
        painter.setClipPath(clip_path)

        painter.drawPath(path)

    def set_fill_level(self, level):
        self.fill_level = level
        self.update()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(180, 40)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #1e1e1e;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 20, 20)
        painter.setClipPath(path)
        super().paintEvent(event)

    def enterEvent(self, event):
        self.animate(True)

    def leaveEvent(self, event):
        self.animate(False)

    def animate(self, hover):
        animation = QPropertyAnimation(self, b"pos")
        animation.setDuration(200)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        start = self.pos()
        if hover:
            end = start + QPoint(5, 0)
        else:
            end = start - QPoint(5, 0)
        
        animation.setStartValue(start)
        animation.setEndValue(end)
        animation.start()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class CCTVApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show_splash_screen()
        self.setWindowTitle("Zylon Security")
        self.setGeometry(100, 100, 1200, 800)
        self.sos_db_handler = SOSDatabaseHandler()
        
        self.attendance_processor = AttendanceProcessor()
        self.attendance_timer = QTimer(self)
        self.attendance_timer.timeout.connect(self.update_attendance_count)
        self.attendance_timer.start(5000)  # Update every 5 seconds

        # Set the application icon
        icon_path = os.path.join(os.path.dirname(__file__), 'app.ico')
        self.setWindowIcon(QIcon(icon_path))
        
        self.apply_theme()
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.create_ui()

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

        self.always_on_top = AlwaysOnTopWindow()
        self.always_on_top.show()

        self.show_watermark()

        # Create system tray icon
        self.create_system_tray()

    def show_splash_screen(self):
        splash_pix = QPixmap('icon.png')  # Use your Zylon logo
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())

        # Add loading text
        loading_label = QLabel("Loading...", splash)
        loading_label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        loading_label.setStyleSheet("color: white; font-size: 18px; margin-bottom: 20px;")

        # Create fade-in/fade-out animation for loading text
        self.fade_animation = QPropertyAnimation(loading_label, b"opacity")
        self.fade_animation.setDuration(1000)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)

        fade_out = QPropertyAnimation(loading_label, b"opacity")
        fade_out.setDuration(1000)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)
        fade_out.setEasingCurve(QEasingCurve.InOutQuad)

        self.fade_sequence = QSequentialAnimationGroup()
        self.fade_sequence.addAnimation(self.fade_animation)
        self.fade_sequence.addAnimation(fade_out)
        self.fade_sequence.setLoopCount(-1)  # Infinite loop

        splash.show()
        self.fade_sequence.start()

        # Simulate loading process
        for i in range(1, 101):
            splash.showMessage(f"Loading... {i}%", Qt.AlignBottom | Qt.AlignHCenter, Qt.white)
            QApplication.processEvents()
            time.sleep(0.03)

        self.fade_sequence.stop()
        splash.finish(self)

    def apply_theme(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #000000;
                color: #ffffff;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #1a1a1a;
                color: #ffffff;
                border: none;
                padding: 12px 24px;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #333333;
            }
            QLineEdit {
                background-color: #1a1a1a;
                border: 2px solid #333333;
                color: #ffffff;
                padding: 10px;
                border-radius: 10px;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
            }
        """)

    def create_ui(self):
        self.button_widget = QWidget()
        self.button_layout = QVBoxLayout(self.button_widget)
        self.button_widget.setStyleSheet("background-color: #121212; border-radius: 15px;")
        self.button_widget.setFixedWidth(220)

        buttons_data = [
            ("Home", "home_icon.png"),
            ("Settings", "settings_icon.png"),
            ("Admin", "admin_icon.png"),
            ("Attendance", "attendance_icon.png"),
            ("Live Camera", "camera_icon.png"),
            ("SOS Message", "sos_icon.png")  # Add this line
        ]

        self.sidebar_buttons = []

        for text, icon_path in buttons_data:
            button = ModernButton(text)
            button.setObjectName("sidebar_button")
            button.setCheckable(True)
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(24, 24))
            self.button_layout.addWidget(button)
            self.sidebar_buttons.append(button)

        self.sidebar_buttons[0].setChecked(True)  # Set Home button as initially checked

        self.button_layout.addStretch()

        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #000000; border-radius: 15px;")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.content_stack.setGraphicsEffect(shadow)

        self.create_home_page()
        self.create_settings_page()
        self.create_admin_page()
        self.create_attendance_page()
        self.create_live_camera_page()
        self.create_sos_message_page()  # Add this line

        for i, button in enumerate(self.sidebar_buttons):
            button.clicked.connect(lambda checked, index=i: self.change_page(index))

        self.main_layout.addWidget(self.button_widget)
        self.main_layout.addWidget(self.content_stack, 1)

    def change_page(self, index):
        self.content_stack.setCurrentIndex(index)
        for i, button in enumerate(self.sidebar_buttons):
            button.setChecked(i == index)
            if i == index:
                self.animate_button_selection(button)

    def animate_button_selection(self, button):
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(300)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        start_geometry = button.geometry()
        end_geometry = start_geometry.adjusted(-10, 0, 0, 0)
        
        animation.setStartValue(start_geometry)
        animation.setEndValue(end_geometry)
        animation.start()

    def create_home_page(self):
        home_widget = QWidget()
        home_layout = QGridLayout(home_widget)
        home_layout.setContentsMargins(20, 20, 20, 20)
        home_layout.setSpacing(20)

        # Welcome message
        welcome_label = QLabel("Welcome, Admin!")
        welcome_label.setStyleSheet("font-size: 24px; color: #3498db; font-weight: bold;")
        home_layout.addWidget(welcome_label, 0, 0, 1, 2)

        # Live Preview
        preview_group = QGroupBox("Live Preview")
        preview_layout = QVBoxLayout(preview_group)
        self.live_preview_label = QLabel()
        self.live_preview_label.setFixedSize(400, 300)
        self.live_preview_label.setStyleSheet("background-color: #2ecc71; border-radius: 10px;")
        preview_layout.addWidget(self.live_preview_label)
        home_layout.addWidget(preview_group, 0, 2, 3, 1)

        # Today's Attendance
        attendance_group = QGroupBox("Today's Attendance")
        attendance_layout = QVBoxLayout(attendance_group)
        self.students_present_label = QLabel("Students present: 0")
        attendance_layout.addWidget(self.students_present_label)
        export_button = QPushButton("Export Attendance")
        export_button.clicked.connect(self.export_attendance)
        attendance_layout.addWidget(export_button)
        home_layout.addWidget(attendance_group, 1, 0)

        # Search User
        search_group = QGroupBox("Search User")
        search_layout = QVBoxLayout(search_group)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter name or ID")
        search_layout.addWidget(self.search_input)
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_user)
        search_layout.addWidget(search_button)
        home_layout.addWidget(search_group, 1, 1)

        # Latest Alerts
        alerts_group = QGroupBox("Latest Alerts")
        alerts_layout = QVBoxLayout(alerts_group)
        self.alerts_text = QTextEdit()
        self.alerts_text.setReadOnly(True)
        alerts_layout.addWidget(self.alerts_text)
        home_layout.addWidget(alerts_group, 2, 0, 1, 2)

        # Send SOS Message
        sos_group = QGroupBox("Send SOS Message")
        sos_layout = QVBoxLayout(sos_group)
        fire_sos_button = QPushButton("Fire SOS")
        fire_sos_button.clicked.connect(lambda: self.send_sos_message("Fire"))
        fire_sos_button.setStyleSheet("background-color: #e74c3c; color: white;")
        earthquake_sos_button = QPushButton("Earthquake SOS")
        earthquake_sos_button.clicked.connect(lambda: self.send_sos_message("Earthquake"))
        earthquake_sos_button.setStyleSheet("background-color: #e67e22; color: white;")
        general_sos_button = QPushButton("General SOS")
        general_sos_button.clicked.connect(lambda: self.send_sos_message("General"))
        general_sos_button.setStyleSheet("background-color: #27ae60; color: white;")
        sos_layout.addWidget(fire_sos_button)
        sos_layout.addWidget(earthquake_sos_button)
        sos_layout.addWidget(general_sos_button)
        home_layout.addWidget(sos_group, 3, 2)

        self.content_stack.addWidget(home_widget)

    # Update live preview
        self.update_live_preview()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def update_live_preview(self):
        if self.video_thread and self.video_thread.current_frame is not None:
            frame = cv2.resize(self.video_thread.current_frame, (400, 300))
            qt_img = self.convert_cv_qt(frame)
            self.live_preview_label.setPixmap(qt_img)

    def export_attendance(self):
        # Implement attendance export functionality
        QMessageBox.information(self, "Export Attendance", "Attendance exported successfully!")

    def search_user(self):
        search_term = self.search_input.text()
        # Implement user search functionality
        QMessageBox.information(self, "Search Result", f"Searching for user: {search_term}")
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
import cv2
import numpy as np
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, 
                             QHBoxLayout, QPushButton, QStackedWidget, QGridLayout,
                             QCheckBox, QFrame, QSplitter, QGraphicsDropShadowEffect,
                             QSystemTrayIcon, QMenu, QAction, QStyle, QInputDialog,
                             QLineEdit, QMessageBox, QGroupBox, QFormLayout, QComboBox,
                             QSlider, QSpinBox, QGraphicsOpacityEffect, QSplashScreen,
                             QDialog, QDialogButtonBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QDateEdit, QFileDialog, QHeaderView,
                             QTextEdit, QScrollArea, QMessageBox, QSizePolicy)
from PyQt5.QtCore import (Qt, QTimer, QThread, pyqtSignal, QPoint, QPointF, QPropertyAnimation, 
                          QEasingCurve, QRect, QRectF, QSize, QSequentialAnimationGroup,
                          QParallelAnimationGroup, QDate)
from PyQt5.QtGui import (QImage, QPixmap, QPalette, QColor, QFont, QPainter, 
                         QPainterPath, QIcon, QLinearGradient, QBrush, QPen)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtNetwork import QTcpSocket
import pandas as pd
from datetime import datetime
from database_handler import DatabaseHandler
import cv2
import numpy as np
import sys
import os
import time
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

PROTOTXT_PATH = r"C:\Users\jagir\CCTV_v.0.2\MobileNetSSD_deploy.prototxt.txt"
MODEL_PATH = resource_path("MobileNetSSD_deploy.caffemodel")

PROTOTXT_PATH = resource_path("MobileNetSSD_deploy.prototxt.txt")
MODEL_PATH = resource_path("MobileNetSSD_deploy.caffemodel")

PROTOTXT_PATH = resource_path("MobileNetSSD_deploy.prototxt.txt")
MODEL_PATH = resource_path("MobileNetSSD_deploy.caffemodel")

class PersonDetector:
    def __init__(self):
        # Load the MobileNet-SSD model
        self.net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor"]
        self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))
        self.db_handler = DatabaseHandler()

    def detect_people(self, frame):
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                     0.007843, (300, 300), 127.5)
        
        self.net.setInput(blob)
        detections = self.net.forward()
        
        people = []
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                idx = int(detections[0, 0, i, 1])
                if self.CLASSES[idx] == "person":
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    people.append((startX, startY, endX, endY))
        
        return people

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray, int)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self._run_flag = True
        self.person_detector = PersonDetector()
        self.grayscale = False
        self.brightness = 0
        self.zoom = 1.0
        self.mirror = False
        self.current_frame = None  # Add this line

    def run(self):
        cap = cv2.VideoCapture(self.camera_index)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                if self.grayscale:
                    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2BGR)
                
                cv_img = cv2.convertScaleAbs(cv_img, alpha=1, beta=self.brightness)
                
                if self.zoom > 1.0:
                    h, w = cv_img.shape[:2]
                    crop_h, crop_w = int(h / self.zoom), int(w / self.zoom)
                    start_y, start_x = (h - crop_h) // 2, (w - crop_w) // 2
                    cv_img = cv_img[start_y:start_y+crop_h, start_x:start_x+crop_w]
                    cv_img = cv2.resize(cv_img, (w, h))
 # Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.               
                if self.mirror:
                    cv_img = cv2.flip(cv_img, 1)
                
                people = self.person_detector.detect_people(cv_img)
                for (startX, startY, endX, endY) in people:
                    cv2.rectangle(cv_img, (startX, startY), (endX, endY), (0, 255, 0), 2)
                
                self.current_frame = cv_img.copy()  # Add this line
                self.change_pixmap_signal.emit(cv_img, len(people))
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

    def set_grayscale(self, value):
        self.grayscale = value

    def set_brightness(self, value):
        self.brightness = value

    def set_zoom(self, value):
        self.zoom = value

    def set_mirror(self, value):
        self.mirror = value
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class LiveMapWidget(QWidget):
    def __init__(self, parent=None, is_preview=False):
        super().__init__(parent)
        self.setMinimumSize(800, 600) if not is_preview else self.setFixedSize(400, 300)
        self.attendance = 0
        self.class_count = 0
        self.is_preview = is_preview

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        scale_x = width / 800
        scale_y = height / 600

        # Draw background
        painter.fillRect(self.rect(), QColor(30, 30, 30))

        # Draw main building outline
        building_color = QColor(100, 100, 100)
        painter.setBrush(QBrush(building_color))
        painter.setPen(QPen(Qt.white, 2))
        painter.drawRect(int(50*scale_x), int(50*scale_y), int(600*scale_x), int(500*scale_y))

        # Draw corridors
        corridor_color = QColor(80, 80, 80)
        painter.fillRect(int(50*scale_x), int(250*scale_y), int(600*scale_x), int(100*scale_y), corridor_color)
        painter.fillRect(int(300*scale_x), int(50*scale_y), int(100*scale_x), int(500*scale_y), corridor_color)

        # Draw classrooms
        self.draw_room(painter, int(75*scale_x), int(75*scale_y), int(200*scale_x), int(150*scale_y), "11A", scale_x, scale_y)
        self.draw_room(painter, int(425*scale_x), int(75*scale_y), int(200*scale_x), int(150*scale_y), "11B", scale_x, scale_y)

        # Draw washroom
        self.draw_room(painter, int(75*scale_x), int(375*scale_y), int(200*scale_x), int(150*scale_y), "Washroom", scale_x, scale_y)

        # Draw playground
        playground_color = QColor(50, 150, 50)
        painter.setBrush(QBrush(playground_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(int(425*scale_x), int(375*scale_y), int(200*scale_x), int(150*scale_y))
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", int(10 * scale_y)))
        painter.drawText(int(475*scale_x), int(460*scale_y), "Playground")

        # Draw construction zone (separate from main building)
        construction_color = QColor(200, 50, 50)
        painter.setBrush(QBrush(construction_color))
        painter.setPen(QPen(Qt.white, 2))
        painter.drawRect(int(675*scale_x), int(50*scale_y), int(100*scale_x), int(100*scale_y))
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", int(8 * scale_y)))
        painter.drawText(int(685*scale_x), int(100*scale_y), "Construction")

        # Draw attendance info for 11A
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", int(10 * scale_y)))
        painter.drawText(int(85*scale_x), int(105*scale_y), f"Attendance: {self.attendance}")
        painter.drawText(int(85*scale_x), int(125*scale_y), f"Class Count: {self.class_count}")

        # Draw students in 11A
        self.draw_students(painter, int(75*scale_x), int(75*scale_y), int(200*scale_x), int(150*scale_y), scale_x, scale_y)

        # Draw "No Camera Connected" text
        painter.setPen(QColor(255, 0, 0))
        painter.setFont(QFont("Arial", int(8 * scale_y)))
        painter.drawText(int(60*scale_x), int(280*scale_y), "No Camera Connected")
        painter.drawText(int(310*scale_x), int(280*scale_y), "No Camera Connected")
        painter.drawText(int(435*scale_x), int(280*scale_y), "No Camera Connected")

        # If it's a preview, don't draw the legend
        if not self.is_preview:
            self.draw_legend(painter, scale_x, scale_y)

    def draw_room(self, painter, x, y, width, height, name, scale_x, scale_y):
        painter.setBrush(QBrush(QColor(50, 50, 50)))
        painter.setPen(QPen(Qt.white, 2))
        painter.drawRect(x, y, width, height)
        painter.setFont(QFont("Arial", int(12 * scale_y)))
        painter.drawText(x + 10, y + 20, name)

    def draw_students(self, painter, x, y, width, height, scale_x, scale_y):
        painter.setBrush(QBrush(QColor(0, 0, 255)))
        painter.setPen(Qt.NoPen)
        max_students_per_row = 8
        student_size = min(int(15 * scale_x), int(15 * scale_y))
        for i in range(self.attendance):
            student_x = x + 20 + (i % max_students_per_row) * (student_size + 5)
            student_y = y + 50 + (i // max_students_per_row) * (student_size + 5)
            painter.drawEllipse(QPointF(student_x, student_y), student_size // 2, student_size // 2)

    def draw_legend(self, painter, scale_x, scale_y):
        legend_x = int(50 * scale_x)
        legend_y = int(560 * scale_y)
        legend_spacing = int(100 * scale_x)

        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", int(10 * scale_y)))
        painter.drawText(legend_x, legend_y, "Legend:")
        
        legend_items = [
            (QColor(0, 0, 255), "Student"),
            (QColor(128, 0, 128), "Teacher"),
            (QColor(255, 0, 0), "Admin Staff")
        ]

        for i, (color, label) in enumerate(legend_items):
            x = legend_x + legend_spacing * (i + 1)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(QPointF(x, legend_y - 5), 5, 5)
            painter.drawText(x + 15, legend_y, label)

    def update_attendance(self, attendance, class_count):
        self.attendance = attendance
        self.class_count = class_count
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()

# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.

class AlwaysOnTopWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(44, 62, 80, 200); border-radius: 10px;")
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.label = QLabel("C: 0 | PP: 4")
        self.label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.label.setAlignment(Qt.AlignCenter)
        
        self.layout.addWidget(self.label)
        
        self.setGeometry(100, 100, 150, 50)
        self.oldPos = self.pos()

    def update_counts(self, camera_count, rfid_count):
        self.label.setText(f"C: {camera_count} | PP: 4-{camera_count}")

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class AnimatedWatermark(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Zylon Security")
        self.setStyleSheet("font-size: 48px; font-weight: bold; color: transparent;")
        self.setAlignment(Qt.AlignCenter)
        self.fill_level = 0

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addText(self.rect().center(), self.font(), self.text())

        gradient = QLinearGradient(0, self.height(), 0, 0)
        gradient.setColorAt(0, QColor(41, 128, 185))  # Light blue
        gradient.setColorAt(1, QColor(52, 152, 219))  # Darker blue

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)

        # Create clipping path for liquid fill effect
        clip_path = QPainterPath()
        clip_path.addRect(0, self.height() * (1 - self.fill_level), self.width(), self.height())
        painter.setClipPath(clip_path)

        painter.drawPath(path)

    def set_fill_level(self, level):
        self.fill_level = level
        self.update()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(180, 40)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #1e1e1e;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 20, 20)
        painter.setClipPath(path)
        super().paintEvent(event)

    def enterEvent(self, event):
        self.animate(True)

    def leaveEvent(self, event):
        self.animate(False)

    def animate(self, hover):
        animation = QPropertyAnimation(self, b"pos")
        animation.setDuration(200)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        start = self.pos()
        if hover:
            end = start + QPoint(5, 0)
        else:
            end = start - QPoint(5, 0)
        
        animation.setStartValue(start)
        animation.setEndValue(end)
        animation.start()

from PyQt5.QtWidgets import QSplashScreen, QLabel, QProgressBar
from PyQt5.QtGui import QPixmap, QColor, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class PremiumSplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Create a sleek, modern background
        pixmap = QPixmap(400, 300)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        gradient = QLinearGradient(0, 0, 400, 300)
        gradient.setColorAt(0, QColor(41, 128, 185))
        gradient.setColorAt(1, QColor(109, 213, 250))
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, 400, 300, 20, 20)
        painter.end()
        self.setPixmap(pixmap)

        # Add a stylish app name
        self.app_name = QLabel("Dvork Security", self)
        self.app_name.setStyleSheet("""
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 28px;
            font-weight: bold;
            color: white;
        """)
        self.app_name.move(20, 20)

        # Add a modern progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(20, 250, 360, 6)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(255, 255, 255, 0.3);
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background-color: white;
                border-radius: 3px;
            }
        """)

        # Add loading text
        self.loading_text = QLabel("Initializing...", self)
        self.loading_text.setStyleSheet("""
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
            color: rgba(255, 255, 255, 0.8);
        """)
        self.loading_text.move(20, 220)

        self.progress = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(30)  # Update every 30ms for smooth animation

    def update_progress(self):
        self.progress += 1
        if self.progress <= 100:
            self.progress_bar.setValue(self.progress)
            if self.progress < 20:
                self.loading_text.setText("Initializing modules...")
            elif self.progress < 40:
                self.loading_text.setText("Loading security protocols...")
            elif self.progress < 60:
                self.loading_text.setText("Establishing connections...")
            elif self.progress < 80:
                self.loading_text.setText("Preparing user interface...")
            else:
                self.loading_text.setText("Finalizing setup...")
        else:
            self.timer.stop()
            self.close()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
# ... rest of your existing code ...
class CCTVApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show_splash_screen()
        self.setWindowTitle("Zylon Security")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set the application icon
        icon_path = os.path.join(os.path.dirname(__file__), 'app.ico')
        self.setWindowIcon(QIcon(icon_path))
        
        self.apply_theme()
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.create_ui()

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

        self.always_on_top = AlwaysOnTopWindow()
        self.always_on_top.show()

        self.show_watermark()

        # Create system tray icon
        self.create_system_tray()

    def show_splash_screen(self):
        splash_pix = QPixmap('icon.png')  # Use your Zylon logo
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())

        # Add loading text
        loading_label = QLabel("Loading...", splash)
        loading_label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        loading_label.setStyleSheet("color: white; font-size: 18px; margin-bottom: 20px;")

        # Create fade-in/fade-out animation for loading text
        self.fade_animation = QPropertyAnimation(loading_label, b"opacity")
        self.fade_animation.setDuration(1000)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)

        fade_out = QPropertyAnimation(loading_label, b"opacity")
        fade_out.setDuration(1000)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)
        fade_out.setEasingCurve(QEasingCurve.InOutQuad)

        self.fade_sequence = QSequentialAnimationGroup()
        self.fade_sequence.addAnimation(self.fade_animation)
        self.fade_sequence.addAnimation(fade_out)
        self.fade_sequence.setLoopCount(-1)  # Infinite loop

        splash.show()
        self.fade_sequence.start()

        # Simulate loading process
        for i in range(1, 101):
            splash.showMessage(f"Loading... {i}%", Qt.AlignBottom | Qt.AlignHCenter, Qt.white)
            QApplication.processEvents()
            time.sleep(0.03)

        self.fade_sequence.stop()
        splash.finish(self)

    def apply_theme(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #000000;
                color: #ffffff;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #1a1a1a;
                color: #ffffff;
                border: none;
                padding: 12px 24px;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #333333;
            }
            QLineEdit {
                background-color: #1a1a1a;
                border: 2px solid #333333;
                color: #ffffff;
                padding: 10px;
                border-radius: 10px;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
            }
        """)

    def create_ui(self):
        self.button_widget = QWidget()
        self.button_layout = QVBoxLayout(self.button_widget)
        self.button_widget.setStyleSheet("background-color: #121212; border-radius: 15px;")
        self.button_widget.setFixedWidth(220)

        buttons_data = [
            ("Home", "home_icon.png"),
            ("Settings", "settings_icon.png"),
            ("Admin", "admin_icon.png"),
            ("Attendance", "attendance_icon.png"),
            ("Live Camera", "camera_icon.png"),
            ("SOS Message", "sos_icon.png")  # Add this line
        ]

        self.sidebar_buttons = []

        for text, icon_path in buttons_data:
            button = ModernButton(text)
            button.setObjectName("sidebar_button")
            button.setCheckable(True)
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(24, 24))
            self.button_layout.addWidget(button)
            self.sidebar_buttons.append(button)

        self.sidebar_buttons[0].setChecked(True)  # Set Home button as initially checked

        self.button_layout.addStretch()

        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #000000; border-radius: 15px;")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.content_stack.setGraphicsEffect(shadow)

        self.create_home_page()
        self.create_settings_page()
        self.create_admin_page()
        self.create_attendance_page()
        self.create_live_camera_page()
        self.create_sos_message_page()  # Add this line

        for i, button in enumerate(self.sidebar_buttons):
            button.clicked.connect(lambda checked, index=i: self.change_page(index))

        self.main_layout.addWidget(self.button_widget)
        self.main_layout.addWidget(self.content_stack, 1)

    def change_page(self, index):
        self.content_stack.setCurrentIndex(index)
        for i, button in enumerate(self.sidebar_buttons):
            button.setChecked(i == index)
            if i == index:
                self.animate_button_selection(button)

    def animate_button_selection(self, button):
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(300)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        start_geometry = button.geometry()
        end_geometry = start_geometry.adjusted(-10, 0, 0, 0)
        
        animation.setStartValue(start_geometry)
        animation.setEndValue(end_geometry)
        animation.start()

    def create_home_page(self):
        home_widget = QWidget()
        home_layout = QGridLayout(home_widget)
        home_layout.setContentsMargins(20, 20, 20, 20)
        home_layout.setSpacing(20)

        # Welcome message
        welcome_label = QLabel("Welcome, Admin!")
        welcome_label.setStyleSheet("font-size: 24px; color: #3498db; font-weight: bold;")
        home_layout.addWidget(welcome_label, 0, 0, 1, 2)

        # Live Preview
        preview_group = QGroupBox("Live Preview")
        preview_layout = QVBoxLayout(preview_group)
        self.live_preview_label = QLabel()
        self.live_preview_label.setFixedSize(400, 300)
        self.live_preview_label.setStyleSheet("background-color: #2ecc71; border-radius: 10px;")
        preview_layout.addWidget(self.live_preview_label)
        home_layout.addWidget(preview_group, 0, 2, 3, 1)

        # Today's Attendance
        attendance_group = QGroupBox("Today's Attendance")
        attendance_layout = QVBoxLayout(attendance_group)
        self.students_present_label = QLabel("Students present: 0")
        attendance_layout.addWidget(self.students_present_label)
        export_button = QPushButton("Export Attendance")
        export_button.clicked.connect(self.export_attendance)
        attendance_layout.addWidget(export_button)
        home_layout.addWidget(attendance_group, 1, 0)

        # Search User
        search_group = QGroupBox("Search User")
        search_layout = QVBoxLayout(search_group)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter name or ID")
        search_layout.addWidget(self.search_input)
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_user)
        search_layout.addWidget(search_button)
        home_layout.addWidget(search_group, 1, 1)

        # Latest Alerts
        alerts_group = QGroupBox("Latest Alerts")
        alerts_layout = QVBoxLayout(alerts_group)
        self.alerts_text = QTextEdit()
        self.alerts_text.setReadOnly(True)
        alerts_layout.addWidget(self.alerts_text)
        home_layout.addWidget(alerts_group, 2, 0, 1, 2)

        # Send SOS Message
        sos_group = QGroupBox("Send SOS Message")
        sos_layout = QVBoxLayout(sos_group)
        fire_sos_button = QPushButton("Fire SOS")
        fire_sos_button.clicked.connect(lambda: self.send_sos_message("Fire"))
        fire_sos_button.setStyleSheet("background-color: #e74c3c; color: white;")
        earthquake_sos_button = QPushButton("Earthquake SOS")
        earthquake_sos_button.clicked.connect(lambda: self.send_sos_message("Earthquake"))
        earthquake_sos_button.setStyleSheet("background-color: #e67e22; color: white;")
        general_sos_button = QPushButton("General SOS")
        general_sos_button.clicked.connect(lambda: self.send_sos_message("General"))
        general_sos_button.setStyleSheet("background-color: #27ae60; color: white;")
        sos_layout.addWidget(fire_sos_button)
        sos_layout.addWidget(earthquake_sos_button)
        sos_layout.addWidget(general_sos_button)
        home_layout.addWidget(sos_group, 3, 2)

        self.content_stack.addWidget(home_widget)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    # Update live preview
        self.update_live_preview()

    def update_live_preview(self):
        if self.video_thread and self.video_thread.current_frame is not None:
            frame = cv2.resize(self.video_thread.current_frame, (400, 300))
            qt_img = self.convert_cv_qt(frame)
            self.live_preview_label.setPixmap(qt_img)

    def export_attendance(self):
        # Implement attendance export functionality
        QMessageBox.information(self, "Export Attendance", "Attendance exported successfully!")

    def search_user(self):
        search_term = self.search_input.text()
        # Implement user search functionality
        QMessageBox.information(self, "Search Result", f"Searching for user: {search_term}")

# Update the existing update_image method
    def update_image(self, cv_img, person_count):
        self.students_present_label.setText(f"Students present: {person_count}")
        self.always_on_top.update_counts(person_count, 0)

    def create_settings_page(self):
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.setContentsMargins(20, 20, 20, 20)
        settings_layout.setSpacing(20)
        
        # Camera Settings
        camera_group = QGroupBox("Camera Settings")
        camera_layout = QFormLayout()
        camera_layout.setSpacing(15)
        
        # Camera selection
        self.camera_combo = QComboBox()
        self.update_camera_list()
        self.camera_combo.currentIndexChanged.connect(self.change_camera)
        camera_layout.addRow("Select Camera:", self.camera_combo)
        
        # Camera preview
        self.preview_label = QLabel()
        self.preview_label.setFixedSize(320, 240)
        self.preview_label.setStyleSheet("background-color: #1e1e1e; border: 1px solid #3498db;")
        camera_layout.addRow("Preview:", self.preview_label)

        # Grayscale
        self.grayscale_checkbox = QCheckBox()
        self.grayscale_checkbox.stateChanged.connect(self.update_camera_settings)
        camera_layout.addRow("Grayscale:", self.grayscale_checkbox)
        
        # Brightness
        brightness_layout = QHBoxLayout()
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-100, 100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.valueChanged.connect(self.update_camera_settings)
        self.brightness_label = QLabel("0")
        brightness_layout.addWidget(self.brightness_slider)
        brightness_layout.addWidget(self.brightness_label)
        camera_layout.addRow("Brightness:", brightness_layout)
        
        # Zoom
        zoom_layout = QHBoxLayout()
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(100, 500)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.update_camera_settings)
        self.zoom_label = QLabel("100%")
        zoom_layout.addWidget(self.zoom_slider)
        zoom_layout.addWidget(self.zoom_label)
        camera_layout.addRow("Zoom:", zoom_layout)
        
        # Mirror video
        self.mirror_checkbox = QCheckBox()
        self.mirror_checkbox.stateChanged.connect(self.update_camera_settings)
        camera_layout.addRow("Mirror Video:", self.mirror_checkbox)
        
        camera_group.setLayout(camera_layout)
        settings_layout.addWidget(camera_group)
        
        settings_layout.addStretch()
        self.content_stack.addWidget(settings_widget)

        # Update preview timer
        self.preview_timer = QTimer(self)
        self.preview_timer.timeout.connect(self.update_preview)
        self.preview_timer.start(100)  # Update every 100ms

    def create_admin_page(self):
        admin_widget = QWidget()
        admin_layout = QVBoxLayout(admin_widget)
        admin_layout.setContentsMargins(20, 20, 20, 20)
        admin_layout.setSpacing(20)

        # User Management Section
        user_management_group = QGroupBox("User Management")
        user_management_layout = QVBoxLayout()

        # Add User Form
        add_user_form = QFormLayout()

        self.name_input = QLineEdit()
        self.class_input = QLineEdit()
        self.user_type_input = QComboBox()
        self.user_type_input.addItems(["Student", "Admin", "Staff", "Teacher"])
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()
        self.parent_name_input = QLineEdit()
        self.parent_phone_input = QLineEdit()
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)

        add_user_form.addRow("Name:", self.name_input)
        add_user_form.addRow("Class:", self.class_input)
        add_user_form.addRow("User Type:", self.user_type_input)
        add_user_form.addRow("Phone:", self.phone_input)
        add_user_form.addRow("Email:", self.email_input)
        add_user_form.addRow("Address:", self.address_input)
        add_user_form.addRow("Parent's Name:", self.parent_name_input)
        add_user_form.addRow("Parent's Phone:", self.parent_phone_input)
        add_user_form.addRow("Date of Birth:", self.dob_input)

        # Wrap the form in a scroll area
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(add_user_form)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        user_management_layout.addWidget(scroll_area)

        # Add User Button
        add_user_button = ModernButton("Add User")
        add_user_button.clicked.connect(self.add_user)
        user_management_layout.addWidget(add_user_button)

        user_management_group.setLayout(user_management_layout)
        admin_layout.addWidget(user_management_group)

        self.content_stack.addWidget(admin_widget)

    def add_user(self):
        name = self.name_input.text()
        class_name = self.class_input.text()
        user_type = self.user_type_input.currentText()
        phone = self.phone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()
        parent_name = self.parent_name_input.text()
        parent_phone = self.parent_phone_input.text()
        dob = self.dob_input.date().toString("yyyy-MM-dd")

        try:
            self.db_handler.add_user(name, class_name, user_type, phone, email, address, parent_name, parent_phone, dob)
            QMessageBox.information(self, "Success", "User added successfully.")
            self.clear_user_form()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add user to the database: {str(e)}")

    def clear_user_form(self):
        self.name_input.clear()
        self.class_input.clear()
        self.user_type_input.setCurrentIndex(0)
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()
        self.parent_name_input.clear()
        self.parent_phone_input.clear()
        self.dob_input.setDate(QDate.currentDate())

    def create_attendance_page(self):
        attendance_widget = QWidget()
        attendance_layout = QVBoxLayout(attendance_widget)
        attendance_layout.setContentsMargins(20, 20, 20, 20)
        attendance_layout.setSpacing(20)

        # Date selection
        date_layout = QHBoxLayout()
        date_layout.setSpacing(10)
        
        date_label = QLabel("Select Date:")
        date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        date_layout.addWidget(date_label)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(datetime.now())
        self.date_edit.setStyleSheet("""
            QDateEdit {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #34495e;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QDateEdit::down-arrow {
                image: url(down_arrow.png);
            }
        """)
        date_layout.addWidget(self.date_edit)
        date_layout.addStretch()

        # Search button
        search_button = ModernButton("Search")
        search_button.clicked.connect(self.search_attendance)
        date_layout.addWidget(search_button)

        # Export button
        export_button = ModernButton("Export to Excel")
        export_button.clicked.connect(self.export_to_excel)
        date_layout.addWidget(export_button)

        attendance_layout.addLayout(date_layout)

        # Table
        self.attendance_table = QTableWidget()
        self.attendance_table.setColumnCount(4)
        self.attendance_table.setHorizontalHeaderLabels(["S.No.", "Name", "Roll No.", "Date and Time"])
        self.attendance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.attendance_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                gridline-color: #2c3e50;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            QScrollBar:vertical {
                border: none;
                background: #2c3e50;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #3498db;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        attendance_layout.addWidget(self.attendance_table)

        self.content_stack.addWidget(attendance_widget)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def search_attendance(self):
        selected_date = self.date_edit.date().toString("yyyy-MM-dd")
        
        # Connect to the database
        db = QSqlDatabase.addDatabase("QMYSQL")
        db.setHostName("localhost")
        db.setDatabaseName("your_database_name")
        db.setUserName("your_username")
        db.setPassword("your_password")

        if not db.open():
            QMessageBox.critical(self, "Database Error", "Could not connect to the database.")
            return

        # Fetch data from the database
        query = QSqlQuery()
        query.prepare("SELECT * FROM attendance WHERE DATE(date_time) = :date ORDER BY date_time")
        query.bindValue(":date", selected_date)

        if not query.exec_():
            QMessageBox.critical(self, "Query Error", "Failed to execute the query.")
            return

        # Clear existing table data
        self.attendance_table.setRowCount(0)

        # Populate the table with fetched data
        row = 0
        while query.next():
            self.attendance_table.insertRow(row)
            self.attendance_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.attendance_table.setItem(row, 1, QTableWidgetItem(query.value("name")))
            self.attendance_table.setItem(row, 2, QTableWidgetItem(query.value("roll_no")))
            self.attendance_table.setItem(row, 3, QTableWidgetItem(query.value("date_time").toString()))
            row += 1

        db.close()

    def export_to_excel(self):
        if self.attendance_table.rowCount() == 0:
            QMessageBox.warning(self, "No Data", "There is no data to export.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx)")
        if file_name:
            data = []
            for row in range(self.attendance_table.rowCount()):
                row_data = []
                for col in range(self.attendance_table.columnCount()):
                    item = self.attendance_table.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)

            df = pd.DataFrame(data, columns=["S.No.", "Name", "Roll No.", "Date and Time"])
            df.to_excel(file_name, index=False)
            QMessageBox.information(self, "Export Successful", f"Data exported to {file_name}")

    def create_live_camera_page(self):
        live_camera_widget = QWidget()
        live_camera_layout = QGridLayout(live_camera_widget)
        
        for i in range(4):
            camera_button = QPushButton(f"Camera {i+1}")
            live_camera_layout.addWidget(camera_button, i // 2, i % 2)
        
        self.content_stack.addWidget(live_camera_widget)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
import cv2
import numpy as np
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, 
                             QHBoxLayout, QPushButton, QStackedWidget, QGridLayout,
                             QCheckBox, QFrame, QSplitter, QGraphicsDropShadowEffect,
                             QSystemTrayIcon, QMenu, QAction, QStyle, QInputDialog,
                             QLineEdit, QMessageBox, QGroupBox, QFormLayout, QComboBox,
                             QSlider, QSpinBox, QGraphicsOpacityEffect, QSplashScreen,
                             QDialog, QDialogButtonBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QDateEdit, QFileDialog, QHeaderView,
                             QTextEdit)
from PyQt5.QtCore import (Qt, QTimer, QThread, pyqtSignal, QPoint, QPropertyAnimation, 
                          QEasingCurve, QRect, QRectF, QSize, QSequentialAnimationGroup,
                          QParallelAnimationGroup)
from PyQt5.QtGui import (QImage, QPixmap, QPalette, QColor, QFont, QPainter, 
                         QPainterPath, QIcon, QLinearGradient)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtNetwork import QTcpSocket
import pandas as pd
from datetime import datetime

import cv2
import numpy as np
import sys
import os
import time
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

PROTOTXT_PATH = r"C:\Users\jagir\CCTV_v.0.2\MobileNetSSD_deploy.prototxt.txt"
MODEL_PATH = resource_path("MobileNetSSD_deploy.caffemodel")

PROTOTXT_PATH = resource_path("MobileNetSSD_deploy.prototxt.txt")
MODEL_PATH = resource_path("MobileNetSSD_deploy.caffemodel")

PROTOTXT_PATH = resource_path("MobileNetSSD_deploy.prototxt.txt")
MODEL_PATH = resource_path("MobileNetSSD_deploy.caffemodel")
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class PersonDetector:
    def __init__(self):
        # Load the MobileNet-SSD model
        self.net = cv2.dnn.readNetFromCaffe(PROTOTXT_PATH, MODEL_PATH)
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor"]
        self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw background
        painter.fillRect(self.rect(), QColor(30, 30, 30))

        # Draw corridors
        corridor_color = QColor(100, 100, 100)
        painter.fillRect(50, 50, 700, 100, corridor_color)
        painter.fillRect(350, 150, 100, 300, corridor_color)

        # Draw classrooms
        self.draw_room(painter, 100, 200, 200, 200, "11A")
        self.draw_room(painter, 500, 200, 200, 200, "11B")

        # Draw washroom
        self.draw_room(painter, 100, 450, 150, 100, "Washroom")

        # Draw playground
        playground_color = QColor(50, 150, 50)
        painter.setBrush(QBrush(playground_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(500, 450, 200, 100)
        painter.drawText(580, 505, "Playground")

        # Draw construction zone
        construction_color = QColor(200, 50, 50)
        painter.setBrush(QBrush(construction_color))
        painter.setPen(Qt.NoPen)
        painter.drawRect(650, 50, 100, 100)
        painter.drawText(660, 100, "Construction")

        # Draw attendance info for 11A
        painter.setPen(Qt.white)
        painter.drawText(110, 230, f"Today's Attendance: {self.attendance}")
        painter.drawText(110, 250, f"Class Count: {self.class_count}")

        # Draw students in 11A
        self.draw_students(painter, 100, 200, 200, 200)

        # Draw "No Camera Connected" text
        painter.setPen(QColor(255, 0, 0))
        painter.drawText(60, 80, "No Camera Connected")
        painter.drawText(360, 280, "No Camera Connected")
        painter.drawText(510, 280, "No Camera Connected")

        # Draw legend
        self.draw_legend(painter)

    def draw_room(self, painter, x, y, width, height, name):
        painter.setBrush(QBrush(QColor(50, 50, 50)))
        painter.setPen(QPen(Qt.white, 2))
        painter.drawRect(x, y, width, height)
        painter.drawText(x + 10, y + 30, name)

    def draw_students(self, painter, x, y, width, height):
        painter.setBrush(QBrush(QColor(0, 0, 255)))
        painter.setPen(Qt.NoPen)
        for i in range(self.attendance):
            student_x = x + 20 + (i % 8) * 20
            student_y = y + 50 + (i // 8) * 20
            painter.drawEllipse(QPointF(student_x, student_y), 5, 5)

    def draw_legend(self, painter):
        painter.setPen(Qt.white)
        painter.drawText(50, 580, "Legend:")
        
        painter.setBrush(QBrush(QColor(0, 0, 255)))
        painter.drawEllipse(QPointF(150, 575), 5, 5)
        painter.drawText(160, 580, "Student")

        painter.setBrush(QBrush(QColor(128, 0, 128)))
        painter.drawEllipse(QPointF(250, 575), 5, 5)
        painter.drawText(260, 580, "Teacher")

        painter.setBrush(QBrush(QColor(255, 0, 0)))
        painter.drawEllipse(QPointF(350, 575), 5, 5)
        painter.drawText(360, 580, "Admin Staff")

    def update_attendance(self, attendance, class_count):
        self.attendance = attendance
        self.class_count = class_count
        self.update()

    def detect_people(self, frame):
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                     0.007843, (300, 300), 127.5)
        
        self.net.setInput(blob)
        detections = self.net.forward()
        
        people = []
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                idx = int(detections[0, 0, i, 1])
                if self.CLASSES[idx] == "person":
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    people.append((startX, startY, endX, endY))
        
        return people
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray, int)

    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self._run_flag = True
        self.person_detector = PersonDetector()
        self.grayscale = False
        self.brightness = 0
        self.zoom = 1.0
        self.mirror = False
        self.current_frame = None

    def run(self):
        cap = cv2.VideoCapture(self.camera_index)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                if self.grayscale:
                    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2BGR)
                
                cv_img = cv2.convertScaleAbs(cv_img, alpha=1, beta=self.brightness)
                
                if self.zoom > 1.0:
                    h, w = cv_img.shape[:2]
                    crop_h, crop_w = int(h / self.zoom), int(w / self.zoom)
                    start_y, start_x = (h - crop_h) // 2, (w - crop_w) // 2
                    cv_img = cv_img[start_y:start_y+crop_h, start_x:start_x+crop_w]
                    cv_img = cv2.resize(cv_img, (w, h))
                
                if self.mirror:
                    cv_img = cv2.flip(cv_img, 1)
                
                people = self.person_detector.detect_people(cv_img)
                for (startX, startY, endX, endY) in people:
                    cv2.rectangle(cv_img, (startX, startY), (endX, endY), (0, 255, 0), 2)
                
                self.current_frame = cv_img.copy()
                self.change_pixmap_signal.emit(cv_img, len(people))
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

    def set_grayscale(self, value):
        self.grayscale = value

    def set_brightness(self, value):
        self.brightness = value

    def set_zoom(self, value):
        self.zoom = value

    def set_mirror(self, value):
        self.mirror = value
class LiveCameraThread(QThread):
    update_frame = pyqtSignal(QImage)
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.running = True
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def run(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.error_occurred.emit("Failed to open camera. Is it connected and available?")
            return

        consecutive_failures = 0
        while self.running:
            ret, frame = cap.read()
            if not ret:
                consecutive_failures += 1
                if consecutive_failures > 10:  # Allow for some temporary failures
                    self.error_occurred.emit("Failed to grab frame consistently. Camera might be in use.")
                    break
                continue
            
            consecutive_failures = 0  # Reset the counter on successful frame grab
            
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            scaled_image = qt_image.scaled(640, 480, Qt.KeepAspectRatio)
            self.update_frame.emit(scaled_image)

        cap.release()

    def stop(self):
        self.running = False
        self.wait()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class AlwaysOnTopWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(44, 62, 80, 200); border-radius: 10px;")
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.label = QLabel("C: 0 | PP: 4")
        self.label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.label.setAlignment(Qt.AlignCenter)
        
        self.layout.addWidget(self.label)
        
        self.setGeometry(100, 100, 150, 50)
        self.oldPos = self.pos()
        

    def update_counts(self, camera_count, rfid_count):
        self.number =  4-camera_count
        self.label.setText(f"C: {camera_count} | B: {self.number} | PP: 4")

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class AnimatedWatermark(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Zylon Security")
        self.setStyleSheet("font-size: 48px; font-weight: bold; color: transparent;")
        self.setAlignment(Qt.AlignCenter)
        self.fill_level = 0

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addText(self.rect().center(), self.font(), self.text())

        gradient = QLinearGradient(0, self.height(), 0, 0)
        gradient.setColorAt(0, QColor(41, 128, 185))  # Light blue
        gradient.setColorAt(1, QColor(52, 152, 219))  # Darker blue

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)

        # Create clipping path for liquid fill effect
        clip_path = QPainterPath()
        clip_path.addRect(0, self.height() * (1 - self.fill_level), self.width(), self.height())
        painter.setClipPath(clip_path)

        painter.drawPath(path)

    def set_fill_level(self, level):
        self.fill_level = level
        self.update()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(180, 40)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #1e1e1e;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 20, 20)
        painter.setClipPath(path)
        super().paintEvent(event)

    def enterEvent(self, event):
        self.animate(True)

    def leaveEvent(self, event):
        self.animate(False)

    def animate(self, hover):
        animation = QPropertyAnimation(self, b"pos")
        animation.setDuration(200)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        start = self.pos()
        if hover:
            end = start + QPoint(5, 0)
        else:
            end = start - QPoint(5, 0)
        
        animation.setStartValue(start)
        animation.setEndValue(end)
        animation.start()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class CCTVApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show_splash_screen()
        self.setWindowTitle("Dvork Security")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set the application icon
        self.setWindowIcon(QIcon('app.ico'))  # Changed from 'app.ico' to 'app.ico'
        
        self.apply_theme()
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.create_ui()

        self.video_thread = None
        self.start_video_thread()

        self.always_on_top = AlwaysOnTopWindow()
        self.always_on_top.show()

        self.show_watermark()

        # Create system tray icon
        self.create_system_tray()
        
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.            
        self.sos_db_handler = SOSDatabaseHandler()
        self.sos_update_timer = QTimer(self)
        self.sos_update_timer.timeout.connect(self.update_sos_table)
        self.sos_update_timer.start(5000)  # Update every 5 seconds
        # Start updating live preview
        QTimer.singleShot(100, self.update_live_preview)

    def update_live_preview(self):
        if self.video_thread and self.video_thread.current_frame is not None:
            frame = cv2.resize(self.video_thread.current_frame, (400, 300))
            qt_img = self.convert_cv_qt(frame)
            self.live_preview_label.setPixmap(qt_img)

        # Schedule the next update
        QTimer.singleShot(100, self.update_live_preview)

    def show_splash_screen(self):
        splash_pix = QPixmap('app.ico')  # Changed from 'icon.png' to 'app.ico'
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())

        # Add loading text
        loading_label = QLabel("Loading...", splash)
        loading_label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        loading_label.setStyleSheet("color: white; font-size: 18px; margin-bottom: 20px;")

        # Create fade-in/fade-out animation for loading text
        self.fade_animation = QPropertyAnimation(loading_label, b"opacity")
        self.fade_animation.setDuration(1000)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)

        fade_out = QPropertyAnimation(loading_label, b"opacity")
        fade_out.setDuration(1000)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)
        fade_out.setEasingCurve(QEasingCurve.InOutQuad)

        self.fade_sequence = QSequentialAnimationGroup()
        self.fade_sequence.addAnimation(self.fade_animation)
        self.fade_sequence.addAnimation(fade_out)
        self.fade_sequence.setLoopCount(-1)  # Infinite loop

        splash.show()
        self.fade_sequence.start()

        # Simulate loading process
        for i in range(1, 101):
            splash.showMessage(f"Loading... {i}%", Qt.AlignBottom | Qt.AlignHCenter, Qt.white)
            QApplication.processEvents()
            time.sleep(0.03)

        self.fade_sequence.stop()
        splash.finish(self)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def apply_theme(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #000000;
                color: #ffffff;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #1a1a1a;
                color: #ffffff;
                border: none;
                padding: 12px 24px;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #333333;
            }
            QLineEdit {
                background-color: #1a1a1a;
                border: 2px solid #333333;
                color: #ffffff;
                padding: 10px;
                border-radius: 10px;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
            }
        """)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def create_ui(self):
        self.button_widget = QWidget()
        self.button_layout = QVBoxLayout(self.button_widget)
        self.button_widget.setStyleSheet("background-color: #121212; border-radius: 15px;")
        self.button_widget.setFixedWidth(220)

        buttons_data = [
            ("Home", "home_icon.png"),
            ("Settings", "settings_icon.png"),
            ("Admin", "admin_icon.png"),
            ("Attendance", "attendance_icon.png"),
            ("Live Camera", "camera_icon.png"),
            ("SOS Message", "sos_icon.png")  # Add this line
        ]

        self.sidebar_buttons = []

        for text, icon_path in buttons_data:
            button = ModernButton(text)
            button.setObjectName("sidebar_button")
            button.setCheckable(True)
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(24, 24))
            self.button_layout.addWidget(button)
            self.sidebar_buttons.append(button)

        self.sidebar_buttons[0].setChecked(True)  # Set Home button as initially checked

        self.button_layout.addStretch()

        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #000000; border-radius: 15px;")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.content_stack.setGraphicsEffect(shadow)

        self.create_home_page()
        self.create_settings_page()
        self.create_admin_page()
        self.create_attendance_page()
        self.create_live_camera_page()
        self.create_sos_message_page()  # Add this line

        for i, button in enumerate(self.sidebar_buttons):
            button.clicked.connect(lambda checked, index=i: self.change_page(index))

        self.main_layout.addWidget(self.button_widget)
        self.main_layout.addWidget(self.content_stack, 1)

    def change_page(self, index):
        self.content_stack.setCurrentIndex(index)
        for i, button in enumerate(self.sidebar_buttons):
            button.setChecked(i == index)
            if i == index:
                self.animate_button_selection(button)

    def animate_button_selection(self, button):
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(300)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        start_geometry = button.geometry()
        end_geometry = start_geometry.adjusted(-10, 0, 0, 0)
        
        animation.setStartValue(start_geometry)
        animation.setEndValue(end_geometry)
        animation.start()

    def create_home_page(self):
        home_widget = QWidget()
        home_layout = QGridLayout(home_widget)
        home_layout.setContentsMargins(20, 20, 20, 20)
        home_layout.setSpacing(20)

        # Welcome message
        welcome_label = QLabel("Welcome, Admin!")
        welcome_label.setStyleSheet("font-size: 24px; color: #3498db; font-weight: bold;")
        home_layout.addWidget(welcome_label, 0, 0, 1, 2)

        # Live Preview
        preview_group = QGroupBox("Live Preview")
        preview_layout = QVBoxLayout(preview_group)
        self.live_preview_label = QLabel()
        self.live_preview_label.setFixedSize(400, 300)
        self.live_preview_label.setStyleSheet("background-color: #2ecc71; border-radius: 10px;")
        preview_layout.addWidget(self.live_preview_label)
        home_layout.addWidget(preview_group, 0, 2, 3, 1)

        # Today's Attendance
        attendance_group = QGroupBox("Today's Attendance")
        attendance_layout = QVBoxLayout(attendance_group)
        self.students_present_label = QLabel("Students present: 0")
        attendance_layout.addWidget(self.students_present_label)
        export_button = QPushButton("Export Attendance")
        export_button.clicked.connect(self.export_attendance)
        attendance_layout.addWidget(export_button)
        home_layout.addWidget(attendance_group, 1, 0)

        # Search User
        search_group = QGroupBox("Search User")
        search_layout = QVBoxLayout(search_group)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter name or ID")
        search_layout.addWidget(self.search_input)
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_user)
        search_layout.addWidget(search_button)
        home_layout.addWidget(search_group, 1, 1)

        # Latest Alerts
        alerts_group = QGroupBox("Latest Alerts")
        alerts_layout = QVBoxLayout(alerts_group)
        self.alerts_text = QTextEdit()
        self.alerts_text.setReadOnly(True)
        alerts_layout.addWidget(self.alerts_text)
        home_layout.addWidget(alerts_group, 2, 0, 1, 2)

        # Send SOS Message
        sos_group = QGroupBox("Send SOS Message")
        sos_layout = QVBoxLayout(sos_group)
        fire_sos_button = QPushButton("Fire SOS")
        fire_sos_button.clicked.connect(lambda: self.send_sos_message("Fire"))
        fire_sos_button.setStyleSheet("background-color: #e74c3c; color: white;")
        earthquake_sos_button = QPushButton("Earthquake SOS")
        earthquake_sos_button.clicked.connect(lambda: self.send_sos_message("Earthquake"))
        earthquake_sos_button.setStyleSheet("background-color: #e67e22; color: white;")
        general_sos_button = QPushButton("General SOS")
        general_sos_button.clicked.connect(lambda: self.send_sos_message("General"))
        general_sos_button.setStyleSheet("background-color: #27ae60; color: white;")
        sos_layout.addWidget(fire_sos_button)
        sos_layout.addWidget(earthquake_sos_button)
        sos_layout.addWidget(general_sos_button)
        home_layout.addWidget(sos_group, 3, 2)

        self.content_stack.addWidget(home_widget)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def create_settings_page(self):
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.setContentsMargins(20, 20, 20, 20)
        settings_layout.setSpacing(20)
        
        # Camera Settings
        camera_group = QGroupBox("Camera Settings")
        camera_layout = QFormLayout()
        camera_layout.setSpacing(15)
        
        # Camera selection
        self.camera_combo = QComboBox()
        self.update_camera_list()
        self.camera_combo.currentIndexChanged.connect(self.change_camera)
        camera_layout.addRow("Select Camera:", self.camera_combo)
        
        # Camera preview
        self.preview_label = QLabel()
        self.preview_label.setFixedSize(320, 240)
        self.preview_label.setStyleSheet("background-color: #1e1e1e; border: 1px solid #3498db;")
        camera_layout.addRow("Preview:", self.preview_label)

        # Grayscale
        self.grayscale_checkbox = QCheckBox()
        self.grayscale_checkbox.stateChanged.connect(self.update_camera_settings)
        camera_layout.addRow("Grayscale:", self.grayscale_checkbox)
        
        # Brightness
        brightness_layout = QHBoxLayout()
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-100, 100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.valueChanged.connect(self.update_camera_settings)
        self.brightness_label = QLabel("0")
        brightness_layout.addWidget(self.brightness_slider)
        brightness_layout.addWidget(self.brightness_label)
        camera_layout.addRow("Brightness:", brightness_layout)
        
        # Zoom
        zoom_layout = QHBoxLayout()
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(100, 500)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.update_camera_settings)
        self.zoom_label = QLabel("100%")
        zoom_layout.addWidget(self.zoom_slider)
        zoom_layout.addWidget(self.zoom_label)
        camera_layout.addRow("Zoom:", zoom_layout)
        
        # Mirror video
        self.mirror_checkbox = QCheckBox()
        self.mirror_checkbox.stateChanged.connect(self.update_camera_settings)
        camera_layout.addRow("Mirror Video:", self.mirror_checkbox)
        
        camera_group.setLayout(camera_layout)
        settings_layout.addWidget(camera_group)
        
        settings_layout.addStretch()
        self.content_stack.addWidget(settings_widget)

        # Update preview timer
        self.preview_timer = QTimer(self)
        self.preview_timer.timeout.connect(self.update_preview)
        self.preview_timer.start(100)  # Update every 100ms
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def create_admin_page(self):
        admin_widget = QWidget()
        admin_layout = QVBoxLayout(admin_widget)
        admin_layout.setContentsMargins(20, 20, 20, 20)
        admin_layout.setSpacing(20)

        # User Management Section
        user_management_group = QGroupBox("User Management")
        user_management_layout = QVBoxLayout()

        # Add User Form
        add_user_form = QFormLayout()

        self.name_input = QLineEdit()
        self.class_input = QLineEdit()
        self.user_type_input = QComboBox()
        self.user_type_input.addItems(["Student", "Admin", "Staff", "Teacher"])
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()
        self.parent_name_input = QLineEdit()
        self.parent_phone_input = QLineEdit()
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)

        add_user_form.addRow("Name:", self.name_input)
        add_user_form.addRow("Class:", self.class_input)
        add_user_form.addRow("User Type:", self.user_type_input)
        add_user_form.addRow("Phone:", self.phone_input)
        add_user_form.addRow("Email:", self.email_input)
        add_user_form.addRow("Address:", self.address_input)
        add_user_form.addRow("Parent's Name:", self.parent_name_input)
        add_user_form.addRow("Parent's Phone:", self.parent_phone_input)
        add_user_form.addRow("Date of Birth:", self.dob_input)

        # Wrap the form in a scroll area
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(add_user_form)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        user_management_layout.addWidget(scroll_area)

        # Add User Button
        add_user_button = ModernButton("Add User")
        add_user_button.clicked.connect(self.add_user)
        user_management_layout.addWidget(add_user_button)

        user_management_group.setLayout(user_management_layout)
        admin_layout.addWidget(user_management_group)

        self.content_stack.addWidget(admin_widget)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def add_user(self):
        name = self.name_input.text()
        class_name = self.class_input.text()
        user_type = self.user_type_input.currentText()
        phone = self.phone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()
        parent_name = self.parent_name_input.text()
        parent_phone = self.parent_phone_input.text()
        dob = self.dob_input.date().toString("yyyy-MM-dd")

        # Connect to the database
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("your_database.sqlite")  # Use a file path for SQLite

        if not db.open():
            QMessageBox.critical(self, "Database Error", "Could not connect to the database.")
            return

        # Insert user data into the database
        query = QSqlQuery()
        query.prepare("""
            INSERT INTO users 
            (name, class, user_type, phone, email, address, parent_name, parent_phone, dob) 
            VALUES (:name, :class, :user_type, :phone, :email, :address, :parent_name, :parent_phone, :dob)
        """)
        query.bindValue(":name", name)
        query.bindValue(":class", class_name)
        query.bindValue(":user_type", user_type)
        query.bindValue(":phone", phone)
        query.bindValue(":email", email)
        query.bindValue(":address", address)
        query.bindValue(":parent_name", parent_name)
        query.bindValue(":parent_phone", parent_phone)
        query.bindValue(":dob", dob)

        if query.exec_():
            QMessageBox.information(self, "Success", "User added successfully.")
            self.clear_user_form()
        else:
            QMessageBox.critical(self, "Error", "Failed to add user to the database.")

        db.close()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def clear_user_form(self):
        self.name_input.clear()
        self.class_input.clear()
        self.user_type_input.setCurrentIndex(0)
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()
        self.parent_name_input.clear()
        self.parent_phone_input.clear()
        self.dob_input.setDate(QDate.currentDate())

    def create_attendance_page(self):
        attendance_widget = QWidget()
        attendance_layout = QVBoxLayout(attendance_widget)
        attendance_layout.setContentsMargins(20, 20, 20, 20)
        attendance_layout.setSpacing(20)

        # Date selection
        date_layout = QHBoxLayout()
        date_layout.setSpacing(10)
        
        date_label = QLabel("Select Date:")
        date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        date_layout.addWidget(date_label)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(datetime.now())
        self.date_edit.setStyleSheet("""
            QDateEdit {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #34495e;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QDateEdit::down-arrow {
                image: url(down_arrow.png);
            }
        """)
        date_layout.addWidget(self.date_edit)
        date_layout.addStretch()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
        # Search button
        search_button = ModernButton("Search")
        search_button.clicked.connect(self.search_attendance)
        date_layout.addWidget(search_button)

        # Export button
        export_button = ModernButton("Export to Excel")
        export_button.clicked.connect(self.export_to_excel)
        date_layout.addWidget(export_button)

        attendance_layout.addLayout(date_layout)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
        # Table
        self.attendance_table = QTableWidget()
        self.attendance_table.setColumnCount(4)
        self.attendance_table.setHorizontalHeaderLabels(["S.No.", "Name", "Roll No.", "Date and Time"])
        self.attendance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.attendance_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                gridline-color: #2c3e50;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            QScrollBar:vertical {
                border: none;
                background: #2c3e50;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #3498db;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        attendance_layout.addWidget(self.attendance_table)

        self.content_stack.addWidget(attendance_widget)

    def search_attendance(self):
        selected_date = self.date_edit.date().toString("yyyy-MM-dd")
        
        # Connect to the database
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("your_database.sqlite")  # Use a file path for SQLite

        if not db.open():
            QMessageBox.critical(self, "Database Error", "Could not connect to the database.")
            return

        # Fetch data from the database
        query = QSqlQuery()
        query.prepare("SELECT * FROM attendance WHERE DATE(date_time) = :date ORDER BY date_time")
        query.bindValue(":date", selected_date)

        if not query.exec_():
            QMessageBox.critical(self, "Query Error", "Failed to execute the query.")
            return

        # Clear existing table data
        self.attendance_table.setRowCount(0)

        # Populate the table with fetched data
        row = 0
        while query.next():
            self.attendance_table.insertRow(row)
            self.attendance_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.attendance_table.setItem(row, 1, QTableWidgetItem(query.value("name")))
            self.attendance_table.setItem(row, 2, QTableWidgetItem(query.value("roll_no")))
            self.attendance_table.setItem(row, 3, QTableWidgetItem(query.value("date_time").toString()))
            row += 1

        db.close()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def export_to_excel(self):
        if self.attendance_table.rowCount() == 0:
            QMessageBox.warning(self, "No Data", "There is no data to export.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx)")
        if file_name:
            data = []
            for row in range(self.attendance_table.rowCount()):
                row_data = []
                for col in range(self.attendance_table.columnCount()):
                    item = self.attendance_table.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)

            df = pd.DataFrame(data, columns=["S.No.", "Name", "Roll No.", "Date and Time"])
            df.to_excel(file_name, index=False)
            QMessageBox.information(self, "Export Successful", f"Data exported to {file_name}")

    def create_live_camera_page(self):
        live_camera_widget = QWidget()
        live_camera_layout = QGridLayout(live_camera_widget)
        
        for i in range(4):
            camera_button = QPushButton(f"Camera {i+1}")
            live_camera_layout.addWidget(camera_button, i // 2, i % 2)
        
        self.content_stack.addWidget(live_camera_widget)

    def create_sos_message_page(self):
        sos_widget = QWidget()
        sos_layout = QVBoxLayout(sos_widget)
        sos_layout.setContentsMargins(20, 20, 20, 20)
        sos_layout.setSpacing(20)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
        # Date selection
        date_layout = QHBoxLayout()
        date_layout.setSpacing(10)
        
        date_label = QLabel("Select Date:")
        date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        date_layout.addWidget(date_label)

        self.sos_date_edit = QDateEdit()
        self.sos_date_edit.setCalendarPopup(True)
        self.sos_date_edit.setDate(datetime.now())
        self.sos_date_edit.setStyleSheet("""
            QDateEdit {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #34495e;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QDateEdit::down-arrow {
                image: url(down_arrow.png);
            }
        """)
        date_layout.addWidget(self.sos_date_edit)
        date_layout.addStretch()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
        # Search button
        search_button = ModernButton("Search")
        search_button.clicked.connect(self.search_sos_messages)
        date_layout.addWidget(search_button)

        sos_layout.addLayout(date_layout)

        # SOS History Table
        self.sos_table = QTableWidget()
        self.sos_table.setColumnCount(6)
        self.sos_table.setHorizontalHeaderLabels(["S.No.", "Name", "Type", "Location", "Date and Time", "Source"])
        self.sos_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sos_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                gridline-color: #2c3e50;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            QScrollBar:vertical {
                border: none;
                background: #2c3e50;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #3498db;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        sos_layout.addWidget(self.sos_table)

        # SOS Message Section
        sos_group = QGroupBox("Send SOS Message")
        sos_group_layout = QGridLayout()
        sos_group_layout.setSpacing(15)

        # SOS Buttons
        fire_button = self.create_sos_button("Fire SOS", "fire_icon.png", "#e74c3c")
        earthquake_button = self.create_sos_button("Earthquake SOS", "earthquake_icon.png", "#f39c12")
        evacuation_button = self.create_sos_button("Evacuation SOS", "evacuation_icon.png", "#27ae60")

        fire_button.clicked.connect(lambda: self.send_sos_message("Fire"))
        earthquake_button.clicked.connect(lambda: self.send_sos_message("Earthquake"))
        evacuation_button.clicked.connect(lambda: self.send_sos_message("Evacuation"))

        sos_group_layout.addWidget(fire_button, 0, 0)
        sos_group_layout.addWidget(earthquake_button, 0, 1)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
class CCTVApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show_splash_screen()
        self.setWindowTitle("Dvork Security")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set the application icon
        self.setWindowIcon(QIcon('app.ico'))
        
        self.apply_theme()
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.create_ui()

        self.video_thread = None
        self.start_video_thread()

        self.always_on_top = AlwaysOnTopWindow()
        self.always_on_top.show()

        self.show_watermark()

        # Create system tray icon
        self.create_system_tray()

        # Start updating live preview
        self.update_live_preview()

        # Set the paths for the MobileNetSSD model files
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.prototxt_path = os.path.join(current_dir, "MobileNetSSD_deploy.prototxt.txt")
        self.model_path = os.path.join(current_dir, "MobileNetSSD_deploy.caffemodel")

        # Verify that the files exist
        if not os.path.exists(self.prototxt_path):
            raise FileNotFoundError(f"Prototxt file not found: {self.prototxt_path}")
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
        # Load the MobileNetSSD model
        try:
            self.net = cv2.dnn.readNetFromCaffe(self.prototxt_path, self.model_path)
        except cv2.error as e:
            print(f"Error loading the model: {e}")
            # You might want to handle this error more gracefully, perhaps by showing a message to the user

    def update_live_preview(self):
        if self.video_thread and self.video_thread.current_frame is not None:
            frame = self.video_thread.current_frame
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            scaled_pixmap = QPixmap.fromImage(q_image).scaled(self.live_preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.live_preview_label.setPixmap(scaled_pixmap)
        QTimer.singleShot(100, self.update_live_preview)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def show_splash_screen(self):
        splash_pix = QPixmap('app.ico')
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())

        # Add loading text
        loading_label = QLabel("Loading...", splash)
        loading_label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        loading_label.setStyleSheet("color: white; font-size: 18px; margin-bottom: 20px;")

        # Create fade-in/fade-out animation for loading text
        self.fade_animation = QPropertyAnimation(loading_label, b"geometry")
        self.fade_animation.setDuration(1000)
        self.fade_animation.setStartValue(loading_label.geometry())
        self.fade_animation.setEndValue(loading_label.geometry())
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)

        fade_out = QPropertyAnimation(loading_label, b"geometry")
        fade_out.setDuration(1000)
        fade_out.setStartValue(loading_label.geometry())
        fade_out.setEndValue(loading_label.geometry())
        fade_out.setEasingCurve(QEasingCurve.InOutQuad)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
        self.fade_sequence = QSequentialAnimationGroup()
        self.fade_sequence.addAnimation(self.fade_animation)
        self.fade_sequence.addAnimation(fade_out)
        self.fade_sequence.setLoopCount(-1)  # Infinite loop

        splash.show()
        self.fade_sequence.start()

        # Simulate loading process
        for i in range(1, 101):
            splash.showMessage(f"Loading... {i}%", Qt.AlignBottom | Qt.AlignHCenter, Qt.white)
            QApplication.processEvents()
            time.sleep(0.03)

        self.fade_sequence.stop()
        splash.finish(self)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def apply_theme(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #f0f0f0;
                color: #2c3e50;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit {
                background-color: white;
                border: 2px solid #bdc3c7;
                color: #2c3e50;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
            QLabel {
                color: #2c3e50;
                font-size: 14px;
            }
        """)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def create_ui(self):
        self.button_widget = QWidget()
        self.button_layout = QVBoxLayout(self.button_widget)
        self.button_widget.setStyleSheet("background-color: #121212; border-radius: 15px;")
        self.button_widget.setFixedWidth(220)

        buttons_data = [
            ("Home", "home_icon.png"),
            ("Settings", "settings_icon.png"),
            ("Admin", "admin_icon.png"),
            ("Attendance", "attendance_icon.png"),
            ("Live Camera", "camera_icon.png"),
            ("SOS Message", "sos_icon.png"),
            ("Live Map", "map_icon.png")  # Added this line
        ]

        self.sidebar_buttons = []

        for text, icon_path in buttons_data:
            button = ModernButton(text)
            button.setObjectName("sidebar_button")
            button.setCheckable(True)
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(24, 24))
            self.button_layout.addWidget(button)
            self.sidebar_buttons.append(button)

        self.sidebar_buttons[0].setChecked(True)  # Set Home button as initially checked

        self.button_layout.addStretch()

        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #000000; border-radius: 15px;")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.content_stack.setGraphicsEffect(shadow)

        self.create_home_page()
        self.create_settings_page()
        self.create_admin_page()
        self.create_attendance_page()
        self.create_live_camera_page()
        self.create_sos_message_page()
        self.create_live_map_page()  # Added this line

        for i, button in enumerate(self.sidebar_buttons):
            button.clicked.connect(lambda checked, index=i: self.change_page(index))

        self.main_layout.addWidget(self.button_widget)
        self.main_layout.addWidget(self.content_stack, 1)

    def change_page(self, index):
        self.content_stack.setCurrentIndex(index)
        for i, button in enumerate(self.sidebar_buttons):
            button.setChecked(i == index)
            if i == index:
                self.animate_button_selection(button)

    def animate_button_selection(self, button):
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(300)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        start_geometry = button.geometry()
        end_geometry = start_geometry.adjusted(-10, 0, 0, 0)
        
        animation.setStartValue(start_geometry)
        animation.setEndValue(end_geometry)
        animation.start()

    def create_home_page(self):
        home_widget = QWidget()
        home_layout = QGridLayout(home_widget)
        home_layout.setContentsMargins(20, 20, 20, 20)
        home_layout.setSpacing(20)

        # Set background color for the entire widget
        home_widget.setStyleSheet("background-color: #000000;")

        # Welcome message
        welcome_label = QLabel("Good morning, Admin")
        welcome_label.setStyleSheet("font-size: 32px; color: #ffffff; font-weight: bold; margin-bottom: 10px;")
        home_layout.addWidget(welcome_label, 0, 0, 1, 2)

        # Live preview of camera
        preview_group = QGroupBox("Live Camera Feed")
        preview_group.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                font-weight: bold;
                border: 2px solid #1e90ff;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        preview_layout = QVBoxLayout(preview_group)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.        
        # Create a QLabel for the preview and set its size policy
        self.live_preview_label = QLabel()
        self.live_preview_label.setFixedSize(640, 480)
        self.live_preview_label.setScaledContents(True)
        self.live_preview_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.live_preview_label.setStyleSheet("background-color: #1a1a1a; border-radius: 10px;")
        
        # Create a QScrollArea to contain the preview label
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.live_preview_label)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedSize(660, 500)  # Slightly larger than the label to accommodate scrollbars if needed
        scroll_area.setStyleSheet("background-color: transparent; border: none;")
        
        preview_layout.addWidget(scroll_area)

        switch_camera_button = QPushButton("Switch Camera")
        switch_camera_button.setStyleSheet("""
            QPushButton {
                background-color: #1e90ff;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1a75ff;
            }
        """)
        switch_camera_button.clicked.connect(self.switch_camera)
        preview_layout.addWidget(switch_camera_button)
class CCTVApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show_premium_splash_screen()
        self.setWindowTitle("Dvork Security")
        self.setGeometry(100, 100, 1200, 800)
        self.show_premium_splash_screen()
        # Set the application icon
        self.setWindowIcon(QIcon('app.ico'))
        
        self.apply_theme()
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.create_ui()

        self.video_thread = None
        self.start_video_thread()

        self.always_on_top = AlwaysOnTopWindow()
        self.always_on_top.show()

        self.show_watermark()

        # Create system tray icon
        self.create_system_tray()

        # Start updating live preview
        self.update_live_preview()

        # Set the paths for the MobileNetSSD model files
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.prototxt_path = os.path.join(current_dir, "MobileNetSSD_deploy.prototxt.txt")
        self.model_path = os.path.join(current_dir, "MobileNetSSD_deploy.caffemodel")

        # Verify that the files exist
        if not os.path.exists(self.prototxt_path):
            raise FileNotFoundError(f"Prototxt file not found: {self.prototxt_path}")
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        # Load the MobileNetSSD model
        try:
            self.net = cv2.dnn.readNetFromCaffe(self.prototxt_path, self.model_path)
        except cv2.error as e:
            print(f"Error loading the model: {e}")
            # You might want to handle this error more gracefully, perhaps by showing a message to the user

        self.sos_db_handler = SOSDatabaseHandler()
        # ... rest of the initialization ...
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
        self.attendance_processor = AttendanceProcessor()
        self.attendance_timer = QTimer(self)
        self.attendance_timer.timeout.connect(self.update_attendance_count)
        self.attendance_timer.start(5000)  # Update every 5 seconds

        self.greeting_timer = QTimer(self)
        self.greeting_timer.timeout.connect(self.update_greeting)
        self.greeting_timer.start(60000)  # Update every minute

    def update_live_preview(self):
        if self.video_thread and self.video_thread.current_frame is not None:
            frame = self.video_thread.current_frame
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            scaled_pixmap = QPixmap.fromImage(q_image).scaled(self.live_preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.live_preview_label.setPixmap(scaled_pixmap)
        QTimer.singleShot(100, self.update_live_preview)

    def show_premium_splash_screen(self):
        self.splash = PremiumSplashScreen()
        self.splash.show()

        # Fade-in animation
        self.fade_in_animation = QPropertyAnimation(self.splash, b"windowOpacity")
        self.fade_in_animation.setDuration(1000)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_in_animation.start()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
        # Close splash screen and show main window
        QTimer.singleShot(5000, self.show_main_window)

    def show_main_window(self):
        # Fade-out animation
        self.fade_out_animation = QPropertyAnimation(self.splash, b"windowOpacity")
        self.fade_out_animation.setDuration(1000)
        self.fade_out_animation.setStartValue(1)
        self.fade_out_animation.setEndValue(0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_out_animation.finished.connect(self.splash.close)
        self.fade_out_animation.finished.connect(self.show)
        self.fade_out_animation.start()

    def show_main_window(self):
        # Fade-out animation
        self.fade_out_animation = QPropertyAnimation(self.splash, b"windowOpacity")
        self.fade_out_animation.setDuration(1000)
        self.fade_out_animation.setStartValue(1)
        self.fade_out_animation.setEndValue(0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_out_animation.finished.connect(self.splash.close)
        self.fade_out_animation.finished.connect(self.show)
        self.fade_out_animation.start()

    def apply_theme(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #f0f0f0;
                color: #2c3e50;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLineEdit {
                background-color: white;
                border: 2px solid #bdc3c7;
                color: #2c3e50;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
            QLabel {
                color: #2c3e50;
                font-size: 14px;
            }
        """)

    def create_ui(self):
        self.button_widget = QWidget()
        self.button_layout = QVBoxLayout(self.button_widget)
        self.button_widget.setStyleSheet("background-color: #121212; border-radius: 15px;")
        self.button_widget.setFixedWidth(220)

        buttons_data = [
            ("Home", "home_icon.png"),
            ("Settings", "settings_icon.png"),
            ("Admin", "admin_icon.png"),
            ("Live Location", "location_icon.png"),
            ("Live Camera", "camera_icon.png"),
            ("SOS Message", "sos_icon.png"),
            ("Live Map", "map_icon.png")
        ]

        self.sidebar_buttons = []
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
        for text, icon_path in buttons_data:
            button = ModernButton(text)
            button.setObjectName("sidebar_button")
            button.setCheckable(True)
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(24, 24))
            self.button_layout.addWidget(button)
            self.sidebar_buttons.append(button)

        self.sidebar_buttons[0].setChecked(True)  # Set Home button as initially checked

        self.button_layout.addStretch()

        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: #000000; border-radius: 15px;")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.content_stack.setGraphicsEffect(shadow)

        self.create_home_page()
        self.create_settings_page()
        self.create_admin_page()
        self.create_attendance_page()
        self.create_live_camera_page()
        self.create_sos_message_page()
        self.create_live_map_page()

        for i, button in enumerate(self.sidebar_buttons):
            button.clicked.connect(lambda checked, index=i: self.change_page(index))

        self.main_layout.addWidget(self.button_widget)
        self.main_layout.addWidget(self.content_stack, 1)

    def change_page(self, index):
        self.content_stack.setCurrentIndex(index)
        for i, button in enumerate(self.sidebar_buttons):
            button.setChecked(i == index)
            if i == index:
                self.animate_button_selection(button)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def animate_button_selection(self, button):
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(300)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        start_geometry = button.geometry()
        end_geometry = start_geometry.adjusted(-10, 0, 0, 0)
        
        animation.setStartValue(start_geometry)
        animation.setEndValue(end_geometry)
        animation.start()

    def create_home_page(self):
        home_widget = QWidget()
        home_layout = QGridLayout(home_widget)
        home_layout.setContentsMargins(20, 20, 20, 20)
        home_layout.setSpacing(20)

        # Set background color for the entire widget
        home_widget.setStyleSheet("background-color: #000000;")

        # Greeting
        self.welcome_label = QLabel()
        self.welcome_label.setStyleSheet("font-size: 32px; font-weight: bold; color: white;")
        self.update_greeting()
        home_layout.addWidget(self.welcome_label, 0, 0, 1, 2, Qt.AlignLeft | Qt.AlignTop)

        # Left column
        left_column = QVBoxLayout()

        # Current students in class
        students_group = QGroupBox("Current students in class")
        students_group.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                font-weight: bold;
                border: 2px solid #00ff00;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        students_layout = QVBoxLayout(students_group)
        self.students_label = QLabel("0")
        self.students_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #00ff00; qproperty-alignment: AlignCenter;")
        students_layout.addWidget(self.students_label)
        left_column.addWidget(students_group)

        # Live map
        map_group = QGroupBox("Live Map")
        map_group.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                font-weight: bold;
                border: 2px solid #ffa500;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        map_layout = QVBoxLayout(map_group)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
        # Create a QLabel for the map image
        map_label = QLabel()
        map_pixmap = QPixmap("C:/Users/Jagrit/Documents/CCTV_v.0.8.9/map.png")
        map_label.setPixmap(map_pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        map_label.setAlignment(Qt.AlignCenter)
        map_label.setStyleSheet("background-color: transparent;")

        map_layout.addWidget(map_label)
        left_column.addWidget(map_group)

        # Increase the size of the map group box slightly
        map_group.setMinimumSize(320, 220)

        # SOS button
        self.sos_button = QPushButton("Send SOS")
        self.sos_button.setStyleSheet("""
            QPushButton {
                background-color: #ff0000;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
            QPushButton:pressed {
                background-color: #990000;
            }
        """)
        self.sos_button.clicked.connect(self.send_sos)
        left_column.addWidget(self.sos_button)

        # Download Today's Attendance button
        download_attendance_button = QPushButton("Download Today's Attendance")
        download_attendance_button.setStyleSheet("""
            QPushButton {
                background-color: #32CD32;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #228B22;
            }
            QPushButton:pressed {
                background-color: #006400;
            }
        """)
        download_attendance_button.clicked.connect(self.download_todays_attendance)
        left_column.addWidget(download_attendance_button)

        # Add a button to navigate to SOS Messages page
        sos_button = QPushButton("View SOS Messages")
        sos_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4500;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF6347;
            }
            QPushButton:pressed {
                background-color: #DC143C;
            }
        """)
        sos_button.clicked.connect(self.show_sos_page)
        left_column.addWidget(sos_button)

        # Add left column to main layout
        left_column_widget = QWidget()
        left_column_widget.setLayout(left_column)
        home_layout.addWidget(left_column_widget, 1, 0, 5, 1)

        # Live preview of camera
        preview_group = QGroupBox("Live Camera Feed")
        preview_group.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                font-weight: bold;
                border: 2px solid #1e90ff;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        preview_layout = QVBoxLayout(preview_group)
        
        # Create a QLabel for the preview and set its size policy
        self.live_preview_label = QLabel()
        self.live_preview_label.setFixedSize(640, 480)
        self.live_preview_label.setScaledContents(True)
        self.live_preview_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.live_preview_label.setStyleSheet("background-color: #1a1a1a; border-radius: 10px;")
        
        # Create a QScrollArea to contain the preview label
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.live_preview_label)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedSize(660, 500)  # Slightly larger than the label to accommodate scrollbars if needed
        scroll_area.setStyleSheet("background-color: transparent; border: none;")
        
        preview_layout.addWidget(scroll_area)

# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
        # Add the new text label with more impactful styling
        camera_info_label = QLabel("Currently watching: 11A")
        camera_info_label.setStyleSheet("""
            color: #1e90ff;
            font-size: 18px;
            font-weight: bold;
            margin-top: 15px;
            padding: 10px;
            background-color: rgba(30, 144, 255, 0.1);
            border: 2px solid #1e90ff;
            border-radius: 5px;
        """)
        preview_layout.addWidget(camera_info_label)

        home_layout.addWidget(preview_group, 1, 1, 5, 1)

        self.content_stack.addWidget(home_widget)

        # Set up timer to update greeting
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_greeting)
        self.update_timer.start(60000)  # Update every minute

    def update_date(self):
        current_date = QDate.currentDate()
        self.date_label.setText(current_date.toString("dddd, MMMM d, yyyy"))

    def update_date_and_greeting(self):
        self.update_date()
        self.update_greeting()

    def create_clock_widget(self):
        clock_widget = QWidget()
        clock_layout = QVBoxLayout(clock_widget)
        
        self.day_label = QLabel()
        self.date_label = QLabel()
        self.time_label = QLabel()
        
        for label in [self.day_label, self.date_label, self.time_label]:
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: white; background-color: #1e1e1e; border-radius: 10px; padding: 10px;")
            clock_layout.addWidget(label)
        
        self.day_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.date_label.setFont(QFont("Arial", 16))
        self.time_label.setFont(QFont("Arial", 24, QFont.Bold))
        
        self.update_clock()
        
        # Update clock every second
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        
        return clock_widget

    def update_clock(self):
        current_date = QDate.currentDate()
        current_time = QTime.currentTime()
        
        self.day_label.setText(current_date.toString("dddd"))
        self.date_label.setText(current_date.toString("MMMM d, yyyy"))
        self.time_label.setText(current_time.toString("hh:mm:ss AP"))

    def create_clock_widget(self):
        clock_widget = QWidget()
        clock_layout = QVBoxLayout(clock_widget)
        
        self.day_label = QLabel()
        self.date_label = QLabel()
        self.time_label = QLabel()
        
        for label in [self.day_label, self.date_label, self.time_label]:
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: white; background-color: #1e1e1e; border-radius: 10px; padding: 10px;")
            clock_layout.addWidget(label)
        
        self.day_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.date_label.setFont(QFont("Arial", 16))
        self.time_label.setFont(QFont("Arial", 24, QFont.Bold))
        
        self.update_clock()
        
        # Update clock every second
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        
        return clock_widget

    def update_clock(self):
        current_date = QDate.currentDate()
        current_time = QTime.currentTime()
        
        self.day_label.setText(current_date.toString("dddd"))
        self.date_label.setText(current_date.toString("MMMM d, yyyy"))
        self.time_label.setText(current_time.toString("hh:mm:ss AP"))

    def update_greeting(self):
        current_time = QTime.currentTime()
        hour = current_time.hour()
        
        if 5 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 17:
            greeting = "Good afternoon"
        elif 17 <= hour < 21:
            greeting = "Good evening"
        else:
            greeting = "Good night"
        
        self.welcome_label.setText(f"{greeting},<br>Admin")

    def update_greeting(self):
        current_time = QTime.currentTime()
        hour = current_time.hour()
        
        if 5 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 17:
            greeting = "Good afternoon"
        elif 17 <= hour < 21:
            greeting = "Good evening"
        else:
            greeting = "Good night"
        
        self.welcome_label.setText(f"""
            <div style="font-size: 32px; font-weight: bold; color: white; text-align: right;">
                {greeting},<br>Admin
            </div>
        """)

    def update_greeting(self):
        current_time = QTime.currentTime()
        hour = current_time.hour()
        
        if 5 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 17:
            greeting = "Good afternoon"
        elif 17 <= hour < 21:
            greeting = "Good evening"
        else:
            greeting = "Good night"
        
        self.welcome_label.setText(f"""
            <div style="font-size: 85px; font-weight: bold; color: white; text-align: right;">
                {greeting},<br>Admin
            </div>
        """)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def update_greeting(self):
        current_time = QTime.currentTime()
        hour = current_time.hour()
        
        if 5 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 17:
            greeting = "Good afternoon"
        elif 17 <= hour < 21:
            greeting = "Good evening"
        else:
            greeting = "Good night"
        
        self.welcome_label.setText(f"{greeting},<br>Admin")

    def update_greeting(self):
        current_time = QTime.currentTime()
        hour = current_time.hour()
        
        if 5 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 17:
            greeting = "Good afternoon"
        elif 17 <= hour < 21:
            greeting = "Good evening"
        else:
            greeting = "Good night"
        
        self.welcome_label.setText(f"{greeting},<br>Admin")

    def update_greeting(self):
        current_time = QTime.currentTime()
        hour = current_time.hour()
        
        if 5 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 17:
            greeting = "Good afternoon"
        elif 17 <= hour < 21:
            greeting = "Good evening"
        else:
            greeting = "Good night"
        
        self.welcome_label.setText(f"{greeting},<br>Admin")

    def update_greeting(self):
        current_time = QTime.currentTime()
        hour = current_time.hour()
        
        if 5 <= hour < 12:
            greeting = "Good morning"
        elif 12 <= hour < 17:
            greeting = "Good afternoon"
        elif 17 <= hour < 21:
            greeting = "Good evening"
        else:
            greeting = "Good night"
        
        self.welcome_label.setText(f"{greeting}, Admin")

    def show_sos_page(self):
        # Assuming your content stack index for SOS page is 5
        # Update this index if it's different in your implementation
        self.content_stack.setCurrentIndex(5)
        # Update the sidebar button selection
        for i, button in enumerate(self.sidebar_buttons):
            button.setChecked(i == 5)

    def download_todays_attendance(self):
        today = QDate.currentDate().toString("yyyy-MM-dd")
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Today's Attendance", f"attendance_{today}.xlsx", "Excel Files (*.xlsx)")
        if file_name:
            try:
                # Assuming you have a method in your DatabaseHandler to get today's attendance
                today_attendance = self.db_handler.get_todays_attendance()
                
                df = pd.DataFrame(today_attendance)
                df.to_excel(file_name, index=False)
                QMessageBox.information(self, "Export Successful", f"Today's attendance exported to {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Failed to export today's attendance: {str(e)}")

    def update_attendance_count(self):
        unique_count = self.attendance_processor.get_unique_attendees_count()
        self.attendance_label.setText(str(unique_count))

    def update_attendance_count(self):
        unique_count = self.attendance_processor.get_unique_attendees_count()
        self.attendance_label.setText(str(unique_count))

    def update_attendance_count(self):
        try:
            with open('attendance_output.txt', 'r') as file:
                for line in file:
                    if "Unique attendees today:" in line:
                        count = line.split(':')[1].strip()
                        self.attendance_label.setText(count)
                        break
        except FileNotFoundError:
            print("Attendance output file not found.")
        except Exception as e:
            print(f"Error updating attendance count: {e}")

    def send_sos(self):
        confirm = QMessageBox.question(self, "Confirm SOS", "Are you sure you want to send an emergency alert?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                response = requests.post("http://192.168.225.36/log_beep.php", data={"sos": 1})
                if response.status_code == 200:
                    QMessageBox.information(self, "SOS Sent", "Emergency alert has been sent successfully.")
                    self.sos_button.setText("Stop SOS")
                    self.sos_button.clicked.disconnect()
                    self.sos_button.clicked.connect(self.stop_sos)
                else:
                    QMessageBox.warning(self, "Error", f"Failed to send SOS. Status code: {response.status_code}")
            except requests.RequestException as e:
                QMessageBox.critical(self, "Error", f"Failed to send SOS: {str(e)}")

    def stop_sos(self):
        try:
            response = requests.post("http://192.168.225.36/log_beep.php", data={"sos": 0})
            if response.status_code == 200:
                QMessageBox.information(self, "SOS Stopped", "Emergency alert has been stopped.")
                self.sos_button.setText("Send SOS")
                self.sos_button.clicked.disconnect()
                self.sos_button.clicked.connect(self.send_sos)
            else:
                QMessageBox.warning(self, "Error", f"Failed to stop SOS. Status code: {response.status_code}")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to stop SOS: {str(e)}")
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def switch_camera(self):
        # Implement camera switching logic here
        pass

    def open_sos_dialog(self):
        sos_dialog = QDialog(self)
        sos_dialog.setWindowTitle("Send SOS Alert")
        sos_layout = QVBoxLayout(sos_dialog)

        sos_types = ["Fire", "Earthquake", "Medical", "Security Threat"]
        for sos_type in sos_types:
            sos_button = QPushButton(sos_type)
            sos_button.clicked.connect(lambda checked, t=sos_type: self.send_sos(t, sos_dialog))
            sos_layout.addWidget(sos_button)

        sos_dialog.exec_()

    def send_sos(self, sos_type, dialog):
        # Implement SOS sending logic here
        print(f"Sending {sos_type} SOS alert")
        dialog.accept()

    def export_attendance(self):
        # Implement attendance export logic here
        print("Exporting attendance to Excel")

    def switch_camera(self):
        # Implement camera switching logic here
        pass

    def open_sos_dialog(self):
        sos_dialog = QDialog(self)
        sos_dialog.setWindowTitle("Send SOS Alert")
        sos_layout = QVBoxLayout(sos_dialog)

        sos_types = ["Fire", "Earthquake", "Medical", "Security Threat"]
        for sos_type in sos_types:
            sos_button = QPushButton(sos_type)
            sos_button.clicked.connect(lambda checked, t=sos_type: self.send_sos(t, sos_dialog))
            sos_layout.addWidget(sos_button)

        sos_dialog.exec_()

    def send_sos(self, sos_type, dialog):
        # Implement SOS sending logic here
        print(f"Sending {sos_type} SOS alert")
        dialog.accept()

    def export_attendance(self):
        # Implement attendance export logic here
        print("Exporting attendance to Excel")

    def switch_camera(self):
        # Implement camera switching logic here
        pass

    def open_sos_dialog(self):
        sos_dialog = QDialog(self)
        sos_dialog.setWindowTitle("Send SOS Alert")
        sos_layout = QVBoxLayout(sos_dialog)

        sos_types = ["Fire", "Earthquake", "Medical", "Security Threat"]
        for sos_type in sos_types:
            sos_button = QPushButton(sos_type)
            sos_button.clicked.connect(lambda checked, t=sos_type: self.send_sos(t, sos_dialog))
            sos_layout.addWidget(sos_button)

        sos_dialog.exec_()

    def send_sos(self, sos_type, dialog):
        # Implement SOS sending logic here
        print(f"Sending {sos_type} SOS alert")
        dialog.accept()

    def send_sos(self, sos_type, dialog):
        # Implement SOS sending logic here
        print(f"Sending {sos_type} SOS alert")
        dialog.accept()

    def export_attendance(self):
        # Implement attendance export logic here
        print("Exporting attendance to Excel")

    def create_settings_page(self):
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.setContentsMargins(20, 20, 20, 20)
        settings_layout.setSpacing(20)
        
        # Camera Settings
        camera_group = QGroupBox("Camera Settings")
        camera_layout = QFormLayout()
        camera_layout.setSpacing(15)
        
        # Camera selection
        self.camera_combo = QComboBox()
        self.update_camera_list()
        self.camera_combo.currentIndexChanged.connect(self.change_camera)
        camera_layout.addRow("Select Camera:", self.camera_combo)
        
        # Camera preview
        self.preview_label = QLabel()
        self.preview_label.setFixedSize(320, 240)
        self.preview_label.setStyleSheet("background-color: #1e1e1e; border: 1px solid #3498db;")
        camera_layout.addRow("Preview:", self.preview_label)

        # Grayscale
        self.grayscale_checkbox = QCheckBox()
        self.grayscale_checkbox.stateChanged.connect(self.update_camera_settings)
        camera_layout.addRow("Grayscale:", self.grayscale_checkbox)
        
        # Brightness
        brightness_layout = QHBoxLayout()
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-100, 100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.valueChanged.connect(self.update_camera_settings)
        self.brightness_label = QLabel("0")
        brightness_layout.addWidget(self.brightness_slider)
        brightness_layout.addWidget(self.brightness_label)
        camera_layout.addRow("Brightness:", brightness_layout)
        
        # Zoom
        zoom_layout = QHBoxLayout()
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(100, 500)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.update_camera_settings)
        self.zoom_label = QLabel("100%")
        zoom_layout.addWidget(self.zoom_slider)
        zoom_layout.addWidget(self.zoom_label)
        camera_layout.addRow("Zoom:", zoom_layout)
        
        # Mirror video
        self.mirror_checkbox = QCheckBox()
        self.mirror_checkbox.stateChanged.connect(self.update_camera_settings)
        camera_layout.addRow("Mirror Video:", self.mirror_checkbox)
        
        camera_group.setLayout(camera_layout)
        settings_layout.addWidget(camera_group)
        
        settings_layout.addStretch()
        self.content_stack.addWidget(settings_widget)

        # Update preview timer
        self.preview_timer = QTimer(self)
        self.preview_timer.timeout.connect(self.update_preview)
        self.preview_timer.start(100)  # Update every 100ms

    def create_admin_page(self):
        self.admin_widget = QWidget()
        main_layout = QVBoxLayout(self.admin_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title
        title_label = QLabel("Admin Dashboard")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Center container for buttons
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.setSpacing(20)

        buttons = [
            ("Manage Cameras", self.show_no_camera_popup),
            ("Manage RFID Attendance Devices", self.manage_rfid_devices),
            ("Manage Users", self.manage_users)
        ]

        for text, func in buttons:
            btn = QPushButton(text)
            btn.setFixedSize(300, 60)
            btn.setFont(QFont("Arial", 12, QFont.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2c3e50;
                    color: white;
                    border: none;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #34495e;
                }
                QPushButton:pressed {
                    background-color: #2980b9;
                }
            """)
            btn.clicked.connect(func)
            center_layout.addWidget(btn)

        # Add stretches to center the button container vertically
        main_layout.addStretch(1)
        main_layout.addWidget(center_widget)
        main_layout.addStretch(1)

        self.content_stack.addWidget(self.admin_widget)

    def manage_rfid_devices(self):
        rfid_url = "http://localhost/RFIDATTENDANCE/ManageUsers.php"
        print(f"Opening RFID Devices Management: {rfid_url}")
        rfid_widget = WebViewWidget(rfid_url, self)
        self.content_stack.addWidget(rfid_widget)
        self.content_stack.setCurrentWidget(rfid_widget)

    def manage_users(self):
        users_url = "http://localhost/RFIDATTENDANCE/ManageUsers.php"
        print(f"Opening User Management: {users_url}")
        users_widget = WebViewWidget(users_url, self)
        self.content_stack.addWidget(users_widget)
        self.content_stack.setCurrentWidget(users_widget)

    def manage_rfid_devices(self):
        rfid_url = "http://localhost/RFIDATTENDANCE/ManageUsers.php"
        print(f"Attempting to load URL: {rfid_url}")  # Add this line for debugging
        rfid_widget = WebViewWidget(rfid_url, self)
        self.content_stack.addWidget(rfid_widget)
        self.content_stack.setCurrentWidget(rfid_widget)

    def manage_users(self):
        users_url = "http://localhost/RFIDATTENDANCE/ManageUsers.php"
        print(f"Attempting to load URL: {users_url}")  # Add this line for debugging
        users_widget = WebViewWidget(users_url, self)
        self.content_stack.addWidget(users_widget)
        self.content_stack.setCurrentWidget(users_widget)

    def show_no_camera_popup(self):
        QMessageBox.warning(self, "No Cameras", "No CCTV camera app connected.",
                            QMessageBox.Ok)

    def show_admin_page(self):
        admin_page_index = self.content_stack.indexOf(self.admin_widget)
        self.content_stack.setCurrentIndex(admin_page_index)

    def check_password(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Enter Password")
        dialog.setFixedSize(300, 100)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                background-color: #34495e;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 5px;
            }
        """)

        layout = QVBoxLayout(dialog)
        password_input = QLineEdit(dialog)
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setPlaceholderText("Enter password")
        layout.addWidget(password_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec_() == QDialog.Accepted:
            return password_input.text() == "your_password_here"  # Replace with your actual password
        return False

    def manage_cameras(self):
        print("Managing cameras")
        # Implement camera management functionality here

    def manage_rfid_devices(self):
        print("Managing RFID attendance devices")
        # Implement RFID device management functionality here

    def manage_users(self):
        print("Managing users")
        # Implement user management functionality here

    def manage_id_cards(self):
        print("Managing ID cards")
        # Implement ID card management functionality here

    def manage_cameras(self):
        print("Managing cameras")
        # Implement camera management functionality here

    def manage_rfid_devices(self):
        rfid_url = "http://localhost/RFIDATTENDANCE/ManageUsers.php"
        print(f"Opening RFID Devices Management: {rfid_url}")
        rfid_widget = WebViewWidget(rfid_url, self)
        self.content_stack.addWidget(rfid_widget)
        self.content_stack.setCurrentWidget(rfid_widget)
        # Implement RFID device management functionality here
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def manage_users(self):
        users_url = "http://localhost/RFIDATTENDANCE/ManageUsers.php"
        print(f"Opening User Management: {users_url}")
        users_widget = WebViewWidget(users_url, self)
        self.content_stack.addWidget(users_widget)
        self.content_stack.setCurrentWidget(users_widget)
        # Implement user management functionality here

    def manage_id_cards(self):
        print("Managing ID cards")
        # Implement ID card management functionality here

    def submit_user(self):
        # Collect form data
        user_data = {
            "name": self.name_input.text(),
            "parent_contact": self.parent_contact_input.text(),
            "student_contact": self.student_contact_input.text(),
            "roll_number": self.roll_number_input.text(),
            "address": self.address_input.toPlainText(),
            "blood_group": self.blood_group_input.text(),
            "role": self.role_input.currentText(),
            "mac_address": self.mac_address_input.text()
        }

        # Save to database (you'll need to implement this method in your DatabaseHandler)
        self.db_handler.add_user(user_data)

        # Clear form fields
  # Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.      # Clear form fields
        self.clear_user_form()

        # Refresh the users table
        self.refresh_users_table()

        QMessageBox.information(self, "Success", "User added successfully!")

    def clear_user_form(self):
        self.name_input.clear()
        self.parent_contact_input.clear()
        self.student_contact_input.clear()
        self.roll_number_input.clear()
        self.address_input.clear()
        self.blood_group_input.clear()
        self.role_input.setCurrentIndex(0)
        self.mac_address_input.clear()

    def fetch_data_from_server(self):
        try:
            response = requests.get('http://your_flask_server_ip:port/get_data')
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching data: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return None

    def refresh_users_table(self):
        # Clear existing rows
        self.users_table.setRowCount(0)

        # Fetch users from Flask server
        users = self.fetch_data_from_server()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
        if users:
            for user in users:
                row_position = self.users_table.rowCount()
                self.users_table.insertRow(row_position)
                self.users_table.setItem(row_position, 0, QTableWidgetItem(user['card_uid']))
                self.users_table.setItem(row_position, 1, QTableWidgetItem(user['mac_address']))
                self.users_table.setItem(row_position, 2, QTableWidgetItem(user['name']))
                self.users_table.setItem(row_position, 3, QTableWidgetItem(user['class']))
                self.users_table.setItem(row_position, 4, QTableWidgetItem(user['room_number']))

    def load_user_details(self, item):
        if item.column() == 0:  # Card UID column
            card_uid = item.text()
            user_details = self.fetch_user_details_from_server(card_uid)
            if user_details:
                self.name_input.setText(user_details['name'])
                self.parent_contact_input.setText(user_details['parent_contact'])
                self.student_contact_input.setText(user_details['student_contact'])
                self.roll_number_input.setText(user_details['roll_number'])
                self.address_input.setPlainText(user_details['address'])
                self.blood_group_input.setText(user_details['blood_group'])
                self.role_input.setCurrentText(user_details['role'])
                self.mac_address_input.setText(user_details['mac_address'])

    def fetch_user_details_from_server(self, card_uid):
        try:
            response = requests.get(f'http://your_flask_server_ip:port/get_user/{card_uid}')
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching user details: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Network error: {e}")
            return None
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def view_all_details(self):
        # Implement a new window or dialog to show all user details
        all_users_dialog = QDialog(self)
        all_users_dialog.setWindowTitle("All User Details")
        all_users_dialog.setMinimumSize(800, 600)

        layout = QVBoxLayout(all_users_dialog)

        users_table = QTableWidget()
        users_table.setColumnCount(9)
        users_table.setHorizontalHeaderLabels([
            "Name", "Parent Contact", "Student Contact", "Roll Number",
            "Address", "Blood Group", "Role", "MAC Address", "Attendance"
        ])
        users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Fetch all user details including attendance
        all_users = self.db_handler.get_all_users_with_attendance()

        for user in all_users:
            row_position = users_table.rowCount()
            users_table.insertRow(row_position)
            users_table.setItem(row_position, 0, QTableWidgetItem(user['name']))
            users_table.setItem(row_position, 1, QTableWidgetItem(user['parent_contact']))
            users_table.setItem(row_position, 2, QTableWidgetItem(user['student_contact']))
            users_table.setItem(row_position, 3, QTableWidgetItem(user['roll_number']))
            users_table.setItem(row_position, 4, QTableWidgetItem(user['address']))
            users_table.setItem(row_position, 5, QTableWidgetItem(user['blood_group']))
            users_table.setItem(row_position, 6, QTableWidgetItem(user['role']))
            users_table.setItem(row_position, 7, QTableWidgetItem(user['mac_address']))
            users_table.setItem(row_position, 8, QTableWidgetItem(str(user['attendance'])))

        layout.addWidget(users_table)

        close_button = QPushButton("Close")
        close_button.clicked.connect(all_users_dialog.close)
        layout.addWidget(close_button)

        all_users_dialog.exec_()

    # ... existing code ...

    def create_attendance_page(self):
        attendance_widget = QWidget()
        attendance_layout = QVBoxLayout(attendance_widget)
        attendance_layout.setContentsMargins(20, 20, 20, 20)
        attendance_layout.setSpacing(20)

        # Date selection
        date_layout = QHBoxLayout()
        date_layout.setSpacing(10)
        
        date_label = QLabel("Select Date:")
        date_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        date_layout.addWidget(date_label)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(datetime.now())
        self.date_edit.setStyleSheet("""
            QDateEdit {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #34495e;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QDateEdit::down-arrow {
                image: url(down_arrow.png);
            }
        """)
        date_layout.addWidget(self.date_edit)
        date_layout.addStretch()

        # Search button
        search_button = ModernButton("Search")
        search_button.clicked.connect(self.search_attendance)
        date_layout.addWidget(search_button)

        # Export button
        export_button = ModernButton("Export to Excel")
        export_button.clicked.connect(self.export_to_excel)
        date_layout.addWidget(export_button)

        attendance_layout.addLayout(date_layout)

        # Table
        self.attendance_table = QTableWidget()
        self.attendance_table.setColumnCount(10)
        self.attendance_table.setHorizontalHeaderLabels([
            "ID", "Username", "Serial Number", "Card UID", "Device UID",
            "Device Department", "Check-in Date", "Time In", "Time Out", "Card Out"
        ])
        self.attendance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.attendance_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                gridline-color: #2c3e50;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            QScrollBar:vertical {
                border: none;
                background: #2c3e50;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #3498db;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        attendance_layout.addWidget(self.attendance_table)

        self.content_stack.addWidget(attendance_widget)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def search_attendance(self):
        selected_date = self.date_edit.date().toString("yyyy-MM-dd")
        
        # Fetch data from the database using DatabaseHandler
        db_handler = DatabaseHandler()
        attendance_records = db_handler.get_records_by_date(selected_date)

        # Clear existing table data
        self.attendance_table.setRowCount(0)

        # Populate the table with fetched data
        for record in attendance_records:
            row_position = self.attendance_table.rowCount()
            self.attendance_table.insertRow(row_position)
            self.attendance_table.setItem(row_position, 0, QTableWidgetItem(str(record['id'])))
            self.attendance_table.setItem(row_position, 1, QTableWidgetItem(record['username']))
            self.attendance_table.setItem(row_position, 2, QTableWidgetItem(str(record['serialnumber'])))
            self.attendance_table.setItem(row_position, 3, QTableWidgetItem(str(record['card_uid'])))
            self.attendance_table.setItem(row_position, 4, QTableWidgetItem(record['device_uid']))
            self.attendance_table.setItem(row_position, 5, QTableWidgetItem(record['device_dep']))
            self.attendance_table.setItem(row_position, 6, QTableWidgetItem(str(record['checkindate'])))
            self.attendance_table.setItem(row_position, 7, QTableWidgetItem(str(record['timein'])))
            self.attendance_table.setItem(row_position, 8, QTableWidgetItem(str(record['timeout'])))
            self.attendance_table.setItem(row_position, 9, QTableWidgetItem(str(record['card_out'])))

        if self.attendance_table.rowCount() == 0:
            QMessageBox.information(self, "No Data", f"No attendance records found for {selected_date}")

    def export_to_excel(self):
        if self.attendance_table.rowCount() == 0:
            QMessageBox.warning(self, "No Data", "There is no data to export.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx)")
        if file_name:
            data = []
            headers = []
            for col in range(self.attendance_table.columnCount()):
                headers.append(self.attendance_table.horizontalHeaderItem(col).text())
            data.append(headers)

            for row in range(self.attendance_table.rowCount()):
                row_data = []
                for col in range(self.attendance_table.columnCount()):
                    item = self.attendance_table.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)

            df = pd.DataFrame(data[1:], columns=data[0])
            df.to_excel(file_name, index=False)
            QMessageBox.information(self, "Export Successful", f"Data exported to {file_name}")

    def create_live_camera_page(self):
        live_camera_widget = QWidget()
        live_camera_layout = QVBoxLayout(live_camera_widget)
        live_camera_layout.setContentsMargins(20, 20, 20, 20)
        live_camera_layout.setSpacing(20)

        # Top layout for camera feed and text
        top_layout = QHBoxLayout()
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
        # Large central camera preview
        self.bg_preview_label = QLabel()
        self.bg_preview_label.setFixedSize(800, 600)  # Increased size
        self.bg_preview_label.setStyleSheet("background-color: #1e1e1e; border: 1px solid #3498db;")
        top_layout.addWidget(self.bg_preview_label, 4)  # Give it more space in the layout

        # Text label for "11 A" on the right top
        text_label = QLabel("11 A")
        text_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        text_label.setAlignment(Qt.AlignTop | Qt.AlignRight)
        top_layout.addWidget(text_label, 1)  # Give it less space compared to the camera feed

        live_camera_layout.addLayout(top_layout)

        # Camera selection buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        camera_buttons = ["11 A", "11 B", "11 C", "11 D"]
        for text in camera_buttons:
            camera_button = QPushButton(text)
            camera_button.setFixedSize(150, 50)
            camera_button.clicked.connect(lambda checked, t=text: self.select_camera(t))
            button_layout.addWidget(camera_button)
        
        live_camera_layout.addLayout(button_layout)
        
        self.content_stack.addWidget(live_camera_widget)

        # Start updating the background preview
        self.bg_preview_timer = QTimer(self)
        self.bg_preview_timer.timeout.connect(self.update_bg_preview)
        self.bg_preview_timer.start(33)  # Update at approximately 30 fps

    def select_camera(self, camera):
        if camera == "11 A":
            # Logic to switch to camera 11 A
            print(f"Switched to camera {camera}")
        else:
            QMessageBox.warning(self, "No Camera", "No camera connected for " + camera)

    def update_bg_preview(self):
        if hasattr(self, 'video_thread') and self.video_thread and hasattr(self.video_thread, 'current_frame') and self.video_thread.current_frame is not None:
            frame = self.video_thread.current_frame
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            scaled_pixmap = QPixmap.fromImage(q_image).scaled(self.bg_preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.bg_preview_label.setPixmap(scaled_pixmap)

    def create_sos_message_page(self):
        sos_widget = QWidget()
        sos_layout = QVBoxLayout(sos_widget)
        sos_layout.setContentsMargins(20, 20, 20, 20)
        sos_layout.setSpacing(20)

        # Title
        title_label = QLabel("SOS Messages")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        sos_layout.addWidget(title_label)

        # Add date edit widget
        self.sos_date_edit = QDateEdit()
        self.sos_date_edit.setCalendarPopup(True)
        self.sos_date_edit.setDate(QDate.currentDate())
        sos_layout.addWidget(self.sos_date_edit)

        # SOS History Table
        self.sos_table = QTableWidget()
        self.sos_table.setColumnCount(6)
        self.sos_table.setHorizontalHeaderLabels(["ID", "Message", "MAC Address", "Timestamp", "Status", "Actions"])
        self.sos_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sos_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                gridline-color: #2c3e50;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            QScrollBar:vertical {
                border: none;
                background: #2c3e50;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #3498db;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        sos_layout.addWidget(self.sos_table)

        # Replace multiple SOS buttons with a single "Send SOS" button
        self.sos_button = QPushButton("Send SOS")
        self.sos_button.setStyleSheet("""
            QPushButton {
                background-color: #ff0000;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
            QPushButton:pressed {
                background-color: #990000;
            }
        """)
        self.sos_button.clicked.connect(self.send_sos)
        sos_layout.addWidget(self.sos_button)

        self.content_stack.addWidget(sos_widget)

        # Set up auto-refresh timer
        self.sos_refresh_timer = QTimer(self)
        self.sos_refresh_timer.timeout.connect(self.update_sos_table)
        self.sos_refresh_timer.start(5000)  # Refresh every 5 seconds

    def send_sos(self):
        confirm = QMessageBox.question(self, "Confirm SOS", "Are you sure you want to send an emergency alert?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                response = requests.post("http://192.168.225.36/log_beep.php", data={"sos": 1})
                if response.status_code == 200:
                    QMessageBox.information(self, "SOS Sent", "Emergency alert has been sent successfully.")
                    self.sos_button.setText("Stop SOS")
                    self.sos_button.clicked.disconnect()
                    self.sos_button.clicked.connect(self.stop_sos)
                else:
                    QMessageBox.warning(self, "Error", f"Failed to send SOS. Status code: {response.status_code}")
            except requests.RequestException as e:
                QMessageBox.critical(self, "Error", f"Failed to send SOS: {str(e)}")
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def stop_sos(self):
        try:
            response = requests.post("http://192.168.225.36/log_beep.php", data={"sos": 0})
            if response.status_code == 200:
                QMessageBox.information(self, "SOS Stopped", "Emergency alert has been stopped.")
                self.sos_button.setText("Send SOS")
                self.sos_button.clicked.disconnect()
                self.sos_button.clicked.connect(self.send_sos)
            else:
                QMessageBox.warning(self, "Error", f"Failed to stop SOS. Status code: {response.status_code}")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to stop SOS: {str(e)}")

    def search_sos_messages(self):
        selected_date = self.sos_date_edit.date().toString("yyyy-MM-dd")
        records = self.sos_db_handler.get_records_by_date(selected_date)
        self.update_sos_table(records)

    def update_sos_table(self):
        if hasattr(self, 'sos_date_edit'):
            selected_date = self.sos_date_edit.date().toPyDate()
        else:
            selected_date = datetime.now().date()

        records = self.sos_db_handler.get_records_by_date(selected_date)
        
        # Store the current scroll position
        scroll_position = self.sos_table.verticalScrollBar().value()

        # Clear existing rows
        self.sos_table.setRowCount(0)

        for record in records:
            row_position = self.sos_table.rowCount()
            self.sos_table.insertRow(row_position)
            self.sos_table.setItem(row_position, 0, QTableWidgetItem(str(record['id'])))
            self.sos_table.setItem(row_position, 1, QTableWidgetItem(record['message']))
            self.sos_table.setItem(row_position, 2, QTableWidgetItem(record['mac_address']))
            self.sos_table.setItem(row_position, 3, QTableWidgetItem(str(record['timestamp'])))
            self.sos_table.setItem(row_position, 4, QTableWidgetItem(record.get('status', 'N/A')))

        # Restore the scroll position
        self.sos_table.verticalScrollBar().setValue(scroll_position)

        print(f"SOS table updated with {self.sos_table.rowCount()} records.")

    def create_sos_button(self, text, icon_path, color):
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(32, 32))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 15px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color}cc;
            }}
            QPushButton:pressed {{
                background-color: {color}99;
            }}
        """)
        return button

    def search_sos_messages(self):
        selected_date = self.sos_date_edit.date().toString("yyyy-MM-dd")
        
        try:
            # Fetch data from the database using SOSDatabaseHandler
            sos_messages = self.sos_db_handler.get_records_by_date(selected_date)

            # Clear existing table data
            self.sos_table.setRowCount(0)

            # Populate the table with fetched data
            for row, message in enumerate(sos_messages):
                self.sos_table.insertRow(row)
                self.sos_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                self.sos_table.setItem(row, 1, QTableWidgetItem(message['mac_address']))  # Assuming 'mac_address' is used instead of 'name'
                self.sos_table.setItem(row, 2, QTableWidgetItem(message['message']))  # 'message' instead of 'type'
                self.sos_table.setItem(row, 3, QTableWidgetItem("N/A"))  # Location is not available in the current schema
                self.sos_table.setItem(row, 4, QTableWidgetItem(str(message['timestamp'])))
                self.sos_table.setItem(row, 5, QTableWidgetItem("Database"))  # Source is always "Database" in this case

            if self.sos_table.rowCount() == 0:
                QMessageBox.information(self, "No Data", f"No SOS messages found for {selected_date}")

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to fetch SOS messages: {str(e)}")

        # Debug print statements
        print(f"Selected date: {selected_date}")
        print(f"Number of rows: {self.sos_table.rowCount()}")
        for row in range(self.sos_table.rowCount()):
            print(f"Row {row + 1} data: {self.sos_table.item(row, 1).text()}, {self.sos_table.item(row, 2).text()}, {self.sos_table.item(row, 4).text()}")

    def send_sos_message(self, sos_type):
        mac_address = "Admin"  # Or you could have a way to set the current user's MAC address
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Send message to NodeMCU
        self.send_to_nodemcu(sos_type)

        # Add to the database
        success = self.sos_db_handler.log_sos_message(mac_address, sos_type)

        if success:
            self.search_sos_messages()
            QMessageBox.information(self, "SOS Sent", f"Your {sos_type} SOS message has been sent successfully.")
        else:
            QMessageBox.warning(self, "SOS Failed", f"Failed to send {sos_type} SOS message.")

    def search_sos_messages(self):
        selected_date = self.sos_date_edit.date().toString("yyyy-MM-dd")
        
        try:
            records = self.sos_db_handler.get_records_by_date(selected_date)
            
            # Clear existing table data
            self.sos_table.setRowCount(0)

            # Populate the table with fetched data
            for row, record in enumerate(records):
                self.sos_table.insertRow(row)
                self.sos_table.setItem(row, 0, QTableWidgetItem(str(record['id'])))
                self.sos_table.setItem(row, 1, QTableWidgetItem(record['message']))
                self.sos_table.setItem(row, 2, QTableWidgetItem(record['mac_address']))
                self.sos_table.setItem(row, 3, QTableWidgetItem(str(record['timestamp'])))
                self.sos_table.setItem(row, 4, QTableWidgetItem("Archived"))  # Status column

            if self.sos_table.rowCount() == 0:
                QMessageBox.information(self, "No Data", f"No SOS messages found for {selected_date}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch SOS messages: {str(e)}")

        # Debug print statements
        print(f"Selected date: {selected_date}")
        print(f"Number of rows: {self.sos_table.rowCount()}")
        for row in range(self.sos_table.rowCount()):
            print(f"Row {row + 1} data: {self.sos_table.item(row, 0).text()}, {self.sos_table.item(row, 1).text()}, {self.sos_table.item(row, 2).text()}, {self.sos_table.item(row, 3).text()}, {self.sos_table.item(row, 4).text()}")

    def send_sos_message(self, sos_type):
        mac_address = "Admin"  # Or you could have a way to set the current user's MAC address
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Send message to NodeMCU
        self.send_to_nodemcu(sos_type)

        # Add to the database
        success = self.sos_db_handler.log_sos_message(mac_address, sos_type)

        if success:
            self.search_sos_messages()
            QMessageBox.information(self, "SOS Sent", f"Your {sos_type} SOS message has been sent successfully.")
        else:
            QMessageBox.warning(self, "SOS Failed", f"Failed to send {sos_type} SOS message.")

    def add_sos_to_database(self, name, sos_type, location, date_time, source):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("your_database.sqlite")  # Use a file path for SQLite

        if not db.open():
            QMessageBox.critical(self, "Database Error", "Could not connect to the database.")
            return

        query = QSqlQuery()
        query.prepare("INSERT INTO sos_messages (name, type, location, date_time, source) VALUES (:name, :type, :location, :date_time, :source)")
        query.bindValue(":name", name)
        query.bindValue(":type", sos_type)
        query.bindValue(":location", location)
        query.bindValue(":date_time", date_time)
        query.bindValue(":source", source)

        if not query.exec_():
            QMessageBox.critical(self, "Database Error", "Failed to add SOS message to the database.")

        db.close()

    def send_to_nodemcu(self, sos_type):
        socket = QTcpSocket(self)
        socket.connectToHost("NodeMCU_IP_ADDRESS", 80)  # Replace with your NodeMCU's IP address

        if socket.waitForConnected(3000):  # Wait up to 3 seconds for connection
            if sos_type == "Fire":
                socket.write(b"FIRE")
            elif sos_type == "Earthquake":
                socket.write(b"EARTHQUAKE")
            elif sos_type == "Evacuation":
                socket.write(b"EVACUATION")
            
            socket.waitForBytesWritten(1000)
            socket.disconnectFromHost()
        else:
            QMessageBox.warning(self, "Connection Error", "Failed to connect to NodeMCU")

    def update_camera_list(self):
        self.camera_combo.clear()
        for i in range(10):  # Check first 10 camera indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                self.camera_combo.addItem(f"Camera {i}")
                cap.release()

    def change_camera(self, index):
        if self.video_thread is not None:
            self.video_thread.stop()
        self.video_thread = VideoThread(index)
        self.video_thread.change_pixmap_signal.connect(self.update_image)
        self.video_thread.start()

    def update_camera_settings(self):
        if self.video_thread is not None:
            self.video_thread.set_grayscale(self.grayscale_checkbox.isChecked())
            brightness = self.brightness_slider.value()
            self.video_thread.set_brightness(brightness)
            self.brightness_label.setText(str(brightness))
            zoom = self.zoom_slider.value()
            self.video_thread.set_zoom(zoom / 100)
            self.zoom_label.setText(f"{zoom}%")
            self.video_thread.set_mirror(self.mirror_checkbox.isChecked())
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def update_image(self, cv_img, person_count):
        qt_img = self.convert_cv_qt(cv_img)
        
        # Scale the image to fit the label while maintaining aspect ratio
        scaled_pixmap = qt_img.scaled(self.live_preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.live_preview_label.setPixmap(scaled_pixmap)
        
        self.students_label.setText(str(person_count))
        self.attendance_label.setText(str(person_count))  # This should be updated with actual attendance logic
        self.always_on_top.update_counts(person_count, 0)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(convert_to_Qt_format)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(convert_to_Qt_format)

    def update_image(self, cv_img, person_count):
        qt_img = self.convert_cv_qt(cv_img)
        
        # Scale the image to fit the label while maintaining aspect ratio
        scaled_pixmap = qt_img.scaled(self.live_preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.live_preview_label.setPixmap(scaled_pixmap)
        
        self.students_label.setText(str(person_count))
        self.current_person_count = person_count  # Store the count in a class variable if needed
        
        # If you have a label for current students in class, update that instead:
        if hasattr(self, 'students_label'):
            self.students_label.setText(str(person_count))
        
        self.always_on_top.update_counts(person_count, 0)
        self.update_live_map()  # Add this line

    def show_watermark(self):
        self.watermark = AnimatedWatermark(self)
        self.watermark.resize(self.width(), self.height())
        
        self.opacity_effect = QGraphicsOpacityEffect(self.watermark)
        self.watermark.setGraphicsEffect(self.opacity_effect)

        self.fill_animation = QPropertyAnimation(self.watermark, b"fill_level")
        self.fill_animation.setDuration(3000)
        self.fill_animation.setStartValue(0)
        self.fill_animation.setEndValue(1)
        self.fill_animation.setEasingCurve(QEasingCurve.InOutCubic)

        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(1000)
        self.opacity_animation.setStartValue(1)
        self.opacity_animation.setEndValue(0)
        self.opacity_animation.setEasingCurve(QEasingCurve.InOutCubic)

        self.fill_animation.start()
        self.fill_animation.finished.connect(self.opacity_animation.start)
        self.opacity_animation.finished.connect(self.watermark.deleteLater)

    def create_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        tray_menu = QMenu()
        show_action = QAction("Show", self)
        quit_action = QAction("Quit", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.confirm_quit)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)

        self.tray_icon.show()

    def confirm_quit(self):
        password, ok = QInputDialog.getText(self, 'Password', 'Enter password to quit:', QLineEdit.Password)
        if ok:
            if password == "jagrit":
                QCoreApplication.quit()
            else:
                QMessageBox.warning(self, "Incorrect Password", "The password you entered is incorrect.")

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.activateWindow()

    def closeEvent(self, event):
        self.sos_db_handler.close()
        super().closeEvent(event)
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Zylon Security",
            "Application minimized to tray",
            QSystemTrayIcon.Information,
            2000
        )

    def quit_app(self):
        if self.show_password_dialog():
            if self.video_thread is not None:
                self.video_thread.stop()
            self.always_on_top.close()
            self.tray_icon.hide()
            QApplication.quit()
        else:
            # If the password is incorrect, we don't quit the app
            pass

    def show_password_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Enter Password")
        dialog.setStyleSheet("""
            QDialog {
                background-color: #000000;
            }
            QLineEdit {
                background-color: #1a1a1a;
                border: 2px solid #333333;
                color: #ffffff;
                padding: 10px;
                border-radius: 10px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
            }
        """)

        layout = QVBoxLayout(dialog)
        password_input = QLineEdit(dialog)
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setPlaceholderText("Enter password")
        layout.addWidget(password_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.button(QDialogButtonBox.Ok).setText("OK")
        button_box.button(QDialogButtonBox.Cancel).setText("Cancel")

        for button in button_box.buttons():
            button.setStyleSheet("""
                QPushButton {
                    background-color: #1a1a1a;
                    color: #ffffff;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 15px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3498db;
                }
                QPushButton:pressed {
                    background-color: #2980b9;
                }
            """)

        layout.addWidget(button_box)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            return password_input.text() == "your_password_here"  # Replace with your actual password check
        return False

    def update_preview(self):
        if self.video_thread is not None and self.video_thread.isRunning():
            frame = self.video_thread.current_frame
            if frame is not None:
                preview_frame = cv2.resize(frame, (320, 240))
                preview_image = self.convert_cv_qt(preview_frame)
                self.preview_label.setPixmap(preview_image)

    def start_video_thread(self):
        if self.video_thread is not None:
            self.video_thread.stop()
        self.video_thread = VideoThread()
        self.video_thread.change_pixmap_signal.connect(self.update_image)
        self.video_thread.start()

    def export_attendance(self):
        # Implement attendance export logic here
        print("Exporting attendance to Excel")

    def search_user(self):
        # Implement your user search logic here
        search_term = self.search_input.text()
        print(f"Searching for user: {search_term}")
        # For now, we'll just show a message box
        QMessageBox.information(self, "User Search", f"Searching for user: {search_term}")
    def create_live_map_page(self):
        live_map_widget = QWidget()
        live_map_layout = QVBoxLayout(live_map_widget)
        live_map_layout.setContentsMargins(0, 0, 0, 0)
        
        self.live_map = LiveMapWidget()
        live_map_layout.addWidget(self.live_map)
        
        self.content_stack.addWidget(live_map_widget)

    def update_live_map(self):
        if hasattr(self, 'live_map'):
            attendance = int(self.students_label.text())
            class_count = attendance  # For now, we'll assume class count is the same as attendance
            self.live_map.update_attendance(attendance, class_count)

    def update_live_map(self):
        if hasattr(self, 'live_map'):
            attendance = int(self.students_label.text())
            class_count = attendance  # For now, we'll assume class count is the same as attendance
            self.live_map.update_attendance(attendance, class_count)

    def update_bg_preview(self):
        if hasattr(self, 'video_thread') and self.video_thread and hasattr(self.video_thread, 'current_frame') and self.video_thread.current_frame is not None:
            frame = self.video_thread.current_frame
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            scaled_pixmap = QPixmap.fromImage(q_image).scaled(self.bg_preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.bg_preview_label.setPixmap(scaled_pixmap)

def create_live_camera_page(self):
    live_camera_widget = QWidget()
    live_camera_layout = QHBoxLayout(live_camera_widget)
    live_camera_layout.setContentsMargins(20, 20, 20, 20)
    live_camera_layout.setSpacing(20)

    # Left column
    left_column = QVBoxLayout()

    # Live preview of camera
    preview_group = QGroupBox("Live Camera Feed")
    preview_group.setStyleSheet("""
        QGroupBox {
            font-size: 18px;
            font-weight: bold;
            border: 2px solid #1e90ff;
            border-radius: 10px;
            margin-top: 10px;
            padding-top: 10px;
            color: #ffffff;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
    """)
    preview_layout = QVBoxLayout(preview_group)
    
    # Create a QLabel for the preview and set its size policy
    self.live_camera_preview_label = QLabel()
    self.live_camera_preview_label.setFixedSize(640, 480)
    self.live_camera_preview_label.setScaledContents(True)
    self.live_camera_preview_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
    self.live_camera_preview_label.setStyleSheet("background-color: #1a1a1a; border-radius: 10px;")
    
    # Create a QScrollArea to contain the preview label
    scroll_area = QScrollArea()
    scroll_area.setWidget(self.live_camera_preview_label)
    scroll_area.setWidgetResizable(True)
    scroll_area.setFixedSize(660, 500)
    scroll_area.setStyleSheet("background-color: transparent; border: none;")
    
    preview_layout.addWidget(scroll_area)
    left_column.addWidget(preview_group)

    # Class label
    self.class_label = QLabel("Current Class: Class 11A")
    self.class_label.setStyleSheet("color: white; font-size: 18px;")
    left_column.addWidget(self.class_label)
    
    # Class buttons
    class_buttons_layout = QHBoxLayout()
    for class_name in ["Class 11A", "Class 11B", "Class 11C"]:
        btn = QPushButton(class_name)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)
        btn.clicked.connect(lambda checked, name=class_name: self.select_class(name))
        class_buttons_layout.addWidget(btn)
    left_column.addLayout(class_buttons_layout)
    
    live_camera_layout.addLayout(left_column, 2)

    # Right side - Class list
    class_list_layout = QVBoxLayout()
    class_list_label = QLabel("Class List")
    class_list_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
    class_list_layout.addWidget(class_list_label)
    
    self.class_list = QListWidget()
    self.class_list.setStyleSheet("""
        QListWidget {
            background-color: #2c3e50;
            color: white;
            border: none;
            border-radius: 5px;
        }
        QListWidget::item {
            padding: 10px;
        }
        QListWidget::item:selected {
            background-color: #3498db;
        }
    """)
    for i in range(1, 13):
        self.class_list.addItem(f"Class {i}")
    self.class_list.itemClicked.connect(self.on_class_selected)
    class_list_layout.addWidget(self.class_list)
    
    live_camera_layout.addLayout(class_list_layout, 1)

    self.content_stack.addWidget(live_camera_widget)

    # Connect the video thread to update the live camera preview
    if hasattr(self, 'video_thread'):
        self.video_thread.change_pixmap_signal.connect(self.update_live_camera_preview)

def update_live_camera_preview(self, cv_img, person_count):
    qt_img = self.convert_cv_qt(cv_img)
    scaled_pixmap = qt_img.scaled(self.live_camera_preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    self.live_camera_preview_label.setPixmap(scaled_pixmap)

def select_class(self, class_name):
    if class_name == "Class 11A":
        QMessageBox.information(self, "Camera Status", "Already rolling 11A")
    else:
        QMessageBox.warning(self, "No Camera", f"No camera connected for {class_name}")

def on_class_selected(self, item):
    selected_class = item.text()
    if selected_class == "Class 11":
        QMessageBox.information(self, "Camera Status", "Already rolling 11A")
    else:
        QMessageBox.warning(self, "No Camera", f"No camera connected for {selected_class}")

    def select_class(self, class_name):
        if class_name == "Class 11A":
            QMessageBox.information(self, "Camera Status", "Already rolling 11A")
        else:
            QMessageBox.warning(self, "No Camera", f"No camera connected for {class_name}")

    def on_class_selected(self, item):
        selected_class = item.text()
        if selected_class == "Class 11":
            QMessageBox.information(self, "Camera Status", "Already rolling 11A")
        else:
            QMessageBox.warning(self, "No Camera", f"No camera connected for {selected_class}")

        # Don't start the video thread here

    def select_class(self, class_name):
        if class_name == "Class 11A":
            self.current_class = class_name
            self.update_class_display()
            if not self.video_thread.isRunning():
                self.video_thread.start()
        else:
            self.show_no_camera_message(class_name)
            self.camera_preview.clear()
            self.camera_preview.setText("No Camera Connected")

    def on_class_selected(self, item):
        selected_class = item.text()
        if selected_class in ["Class 11", "Class 11A"]:
            self.current_class = "Class 11A"
            self.update_class_display()
            if not self.video_thread.isRunning():
                self.video_thread.start()
        else:
            self.show_no_camera_message(selected_class)
            self.camera_preview.clear()
            self.camera_preview.setText("No Camera Connected")

    def update_camera_preview(self, image):
        if self.current_class == "Class 11A":
            self.camera_preview.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        if hasattr(self, 'video_thread'):
            self.video_thread.stop()
        super().closeEvent(event)

    def select_class(self, class_name):
        if class_name == "Class 11A":
            self.current_class = class_name
            self.update_class_display()
            if not self.live_camera_thread.isRunning():
                self.live_camera_thread.start()
        else:
            self.show_no_camera_message(class_name)
            if self.live_camera_thread.isRunning():
                self.live_camera_thread.stop()
            self.camera_preview.clear()
            self.camera_preview.setText("No Camera Connected")

    def on_class_selected(self, item):
        selected_class = item.text()
        if selected_class in ["Class 11", "Class 11A"]:
            self.current_class = "Class 11A"
            self.update_class_display()
            if not self.live_camera_thread.isRunning():
                self.live_camera_thread.start()
        else:
            self.show_no_camera_message(selected_class)
            if self.live_camera_thread.isRunning():
                self.live_camera_thread.stop()
            self.camera_preview.clear()
            self.camera_preview.setText("No Camera Connected")

    def update_class_display(self):
        self.class_label.setText(f"Current Class: {self.current_class}")

    def show_no_camera_message(self, class_name):
        QMessageBox.warning(self, "No Camera", f"No camera connected for {class_name}")

    def update_camera_preview(self, image):
        self.camera_preview.setPixmap(QPixmap.fromImage(image))

    def handle_camera_error(self, error_message):
        QMessageBox.warning(self, "Camera Error", error_message)
        self.camera_preview.setText("Camera Error: " + error_message)

    def closeEvent(self, event):
        if hasattr(self, 'live_camera_thread'):
            self.live_camera_thread.stop()
        super().closeEvent(event)

    def handle_camera_error(self, error_message):
        QMessageBox.warning(self, "Camera Error", error_message)
        self.camera_preview.setText("Camera Error: " + error_message)

    def select_class(self, class_name):
        if class_name == "Class 11A":
            self.current_class = class_name
            self.update_class_display()
            if not self.live_camera_thread.isRunning():
                self.live_camera_thread.start()
        else:
            self.show_no_camera_message(class_name)
            if self.live_camera_thread.isRunning():
                self.live_camera_thread.stop()
            self.camera_preview.clear()
            self.camera_preview.setText("No Camera Connected")

    def on_class_selected(self, item):
        selected_class = item.text()
        if selected_class in ["Class 11", "Class 11A"]:
            self.current_class = "Class 11A"
            self.update_class_display()
            if not self.live_camera_thread.isRunning():
                self.live_camera_thread.start()
        else:
            self.show_no_camera_message(selected_class)
            if self.live_camera_thread.isRunning():
                self.live_camera_thread.stop()
            self.camera_preview.clear()
            self.camera_preview.setText("No Camera Connected")

    def update_class_display(self):
        self.class_label.setText(f"Current Class: {self.current_class}")

    def show_no_camera_message(self, class_name):
        QMessageBox.warning(self, "No Camera", f"No camera connected for {class_name}")

    def update_camera_preview(self, image):
        self.camera_preview.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        if hasattr(self, 'live_camera_thread'):
            self.live_camera_thread.stop()
        super().closeEvent(event)

    def select_class(self, class_name):
        if class_name == "Class 11A":
            self.current_class = class_name
            self.update_class_display()
            if not self.live_camera_thread.isRunning():
                self.live_camera_thread.start()
        else:
            self.show_no_camera_message(class_name)
            if self.live_camera_thread.isRunning():
                self.live_camera_thread.stop()
            self.camera_preview.clear()
            self.camera_preview.setText("No Camera Connected")

    def on_class_selected(self, item):
        selected_class = item.text()
        if selected_class in ["Class 11", "Class 11A"]:
            self.current_class = "Class 11A"
            self.update_class_display()
            if not self.live_camera_thread.isRunning():
                self.live_camera_thread.start()
        else:
            self.show_no_camera_message(selected_class)
            if self.live_camera_thread.isRunning():
                self.live_camera_thread.stop()
            self.camera_preview.clear()
            self.camera_preview.setText("No Camera Connected")

    def update_class_display(self):
        self.class_label.setText(f"Current Class: {self.current_class}")

    def show_no_camera_message(self, class_name):
        QMessageBox.warning(self, "No Camera", f"No camera connected for {class_name}")

    def update_camera_preview(self, image):
        self.camera_preview.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        if hasattr(self, 'live_camera_thread'):
            self.live_camera_thread.stop()
        super().closeEvent(event)

    def select_class(self, class_name):
        if class_name == "Class 11A":
            self.current_class = class_name
            self.update_class_display()
            if not self.video_thread.isRunning():
                self.video_thread.start()
        else:
            self.show_no_camera_message(class_name)
            if self.video_thread.isRunning():
                self.video_thread.stop()
            self.camera_preview.clear()
            self.camera_preview.setText("No Camera Connected")

    def on_class_selected(self, item):
        selected_class = item.text()
        if selected_class in ["Class 11", "Class 11A"]:
            self.current_class = "Class 11A"
            self.update_class_display()
            if not self.video_thread.isRunning():
                self.video_thread.start()
        else:
            self.show_no_camera_message(selected_class)
            if self.video_thread.isRunning():
                self.video_thread.stop()
            self.camera_preview.clear()
            self.camera_preview.setText("No Camera Connected")

    def update_camera_preview(self, image):
        self.camera_preview.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        self.video_thread.stop()
        super().closeEvent(event)

    def select_class(self, class_name):
        if class_name == "Class 11A":
            self.current_class = class_name
            self.update_class_display()
            if not self.camera_timer.isActive():
                self.camera_timer.start(30)
        else:
            self.show_no_camera_message(class_name)
            self.camera_timer.stop()
            self.camera_preview.clear()
            self.camera_preview.setText("No Camera Connected")

    def on_class_selected(self, item):
        selected_class = item.text()
        if selected_class == "Class 11":
            self.current_class = "Class 11A"
            self.update_class_display()
            if not self.camera_timer.isActive():
                self.camera_timer.start(30)
        elif selected_class == "Class 11A":
            self.current_class = selected_class
            self.update_class_display()
            if not self.camera_timer.isActive():
                self.camera_timer.start(30)
        else:
            self.show_no_camera_message(selected_class)
            self.camera_timer.stop()
            self.camera_preview.clear()
            self.camera_preview.setText("No Camera Connected")

    def update_class_display(self):
        self.class_label.setText(f"Current Class: {self.current_class}")

    def show_no_camera_message(self, class_name):
        QMessageBox.warning(self, "No Camera", f"No camera connected for {class_name}")

    def update_camera_preview(self):
        if self.camera is not None and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                scaled_pixmap = pixmap.scaled(self.camera_preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.camera_preview.setPixmap(scaled_pixmap)

    def closeEvent(self, event):
        if self.camera is not None:
            self.camera.release()
        super().closeEvent(event)

    def select_class(self, class_name):
        if class_name == "Class 11A":
            self.current_class = class_name
            self.update_class_display()
        else:
            self.show_no_camera_message(class_name)

    def on_class_selected(self, item):
        selected_class = item.text()
        if selected_class == "Class 11":
            self.current_class = "Class 11A"
            self.update_class_display()
        elif selected_class == "Class 11A":
            self.current_class = selected_class
            self.update_class_display()
        else:
            self.show_no_camera_message(selected_class)

    def update_class_display(self):
        self.class_label.setText(f"Current Class: {self.current_class}")

    def show_no_camera_message(self, class_name):
        QMessageBox.warning(self, "No Camera", f"No camera connected for {class_name}")

    def update_camera_preview(self):
        if self.camera is not None:
            ret, frame = self.camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                scaled_pixmap = pixmap.scaled(self.camera_preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.camera_preview.setPixmap(scaled_pixmap)

    def closeEvent(self, event):
        if self.camera is not None:
            self.camera.release()
        super().closeEvent(event)

    def select_class(self, class_name):
        if class_name in ["Class 11A", "Class 11B", "Class 11C"]:
            self.start_camera_preview(class_name)
        else:
            self.stop_camera_preview()
            QMessageBox.warning(self, "No Camera", "No camera connected for this class.")

    def on_class_selected(self, item):
        selected_class = item.text()
        if selected_class == "Class 11":
            QMessageBox.information(self, "Class Selection", "Please select a specific section (A, B, or C)")
        elif selected_class in ["Class 11A", "Class 11B", "Class 11C"]:
            self.start_camera_preview(selected_class)
        else:
            self.stop_camera_preview()
            QMessageBox.warning(self, "No Camera", "No camera connected for this class.")

    def start_camera_preview(self, class_name):
        if self.camera is None:
            self.camera = cv2.VideoCapture(0)  # Use 0 for default camera
        if not self.camera_timer.isActive():
            self.camera_timer.start(30)  # Update every 30ms
        self.camera_preview.setText(f"Live Feed: {class_name}")

    def stop_camera_preview(self):
        if self.camera_timer.isActive():
            self.camera_timer.stop()
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        self.camera_preview.clear()
        self.camera_preview.setText("No Camera Connected")

    def update_camera_preview(self):
        if self.camera is not None:
            ret, frame = self.camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                scaled_pixmap = pixmap.scaled(self.camera_preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.camera_preview.setPixmap(scaled_pixmap)

    def closeEvent(self, event):
        self.stop_camera_preview()
        super().closeEvent(event)

    def select_class(self, class_name):
        if class_name in ["Class 11A", "Class 11B", "Class 11C"]:
            self.start_camera_preview()
            QMessageBox.information(self, "Class Selection", f"Showing live preview for {class_name}")
        else:
            self.stop_camera_preview()
            QMessageBox.warning(self, "No Camera", "No camera connected for this class.")

    def on_class_selected(self, item):
        selected_class = item.text()
        if selected_class in ["Class 11", "Class 11A", "Class 11B", "Class 11C"]:
            self.start_camera_preview()
            QMessageBox.information(self, "Class Selection", f"Showing live preview for {selected_class}")
        else:
            self.stop_camera_preview()
            QMessageBox.warning(self, "No Camera", "No camera connected for this class.")

    def start_camera_preview(self):
        if self.camera is None:
            self.camera = cv2.VideoCapture(0)  # Use 0 for default camera
        if not self.camera_timer.isActive():
            self.camera_timer.start(30)  # Update every 30ms

    def stop_camera_preview(self):
        if self.camera_timer.isActive():
            self.camera_timer.stop()
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        self.camera_preview.clear()
        self.camera_preview.setText("No Camera Connected")

    def update_camera_preview(self):
        if self.camera is not None:
            ret, frame = self.camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.camera_preview.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        self.stop_camera_preview()
        super().closeEvent(event)

    def select_class(self, class_name):
        if class_name == "Class 11A":
            QMessageBox.information(self, "Camera Status", "Already rolling 11A")
        else:
            QMessageBox.warning(self, "No Camera", f"No camera connected for {class_name}")

    def on_class_selected(self, item):
        selected_class = item.text()
        if selected_class.startswith("Class 11"):
            QMessageBox.information(self, "Class Selection", "Camera already opened for this class.")
        else:
            QMessageBox.warning(self, "No Camera", "No camera connected for this class.")

    def update_bg_preview(self):
        if hasattr(self, 'video_thread') and self.video_thread and hasattr(self.video_thread, 'current_frame') and self.video_thread.current_frame is not None:
            frame = self.video_thread.current_frame
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            scaled_pixmap = QPixmap.fromImage(q_image).scaled(self.bg_preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Create a new pixmap with the fixed size of the label
            display_pixmap = QPixmap(self.bg_preview_label.size())
            display_pixmap.fill(Qt.black)  # Fill with black background
            
            # Draw the scaled image centered on the display pixmap
            painter = QPainter(display_pixmap)
            painter.drawPixmap((display_pixmap.width() - scaled_pixmap.width()) // 2,
                               (display_pixmap.height() - scaled_pixmap.height()) // 2,
                               scaled_pixmap)
            painter.end()
            
            self.bg_preview_label.setPixmap(display_pixmap)

    def select_camera(self, camera):
        self.class_label.setText(camera.split()[-1])
        if camera == "Class 11A":
            # Logic to switch to camera 11A
            print(f"Switched to {camera}")
        else:
            QMessageBox.warning(self, "Camera Disconnected", f"Camera for {camera} is disconnected.")

    def switch_class(self):
        # Implement the logic for switching class here
        print("Switching class")

    def update_bg_preview(self):
        if hasattr(self, 'video_thread') and self.video_thread and hasattr(self.video_thread, 'current_frame') and self.video_thread.current_frame is not None:
            frame = self.video_thread.current_frame
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            scaled_pixmap = QPixmap.fromImage(q_image).scaled(self.bg_preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.bg_preview_label.setPixmap(scaled_pixmap)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def update_bg_preview(self):
        if hasattr(self, 'video_thread') and self.video_thread and hasattr(self.video_thread, 'current_frame') and self.video_thread.current_frame is not None:
            frame = self.video_thread.current_frame
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            scaled_pixmap = QPixmap.fromImage(q_image).scaled(self.bg_preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Create a new pixmap with the fixed size of the label
            display_pixmap = QPixmap(self.bg_preview_label.size())
            display_pixmap.fill(Qt.black)  # Fill with black background
            
            # Draw the scaled image centered on the display pixmap
            painter = QPainter(display_pixmap)
            painter.drawPixmap((display_pixmap.width() - scaled_pixmap.width()) // 2,
                               (display_pixmap.height() - scaled_pixmap.height()) // 2,
                               scaled_pixmap)
            painter.end()
            
            self.bg_preview_label.setPixmap(display_pixmap)
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
    def select_camera(self, camera):
        if camera == "11 A":
            # Logic to switch to camera 11 A
            print(f"Switched to camera {camera}")
        else:
            QMessageBox.warning(self, "No Camera", "No camera connected for " + camera)

    def select_camera(self, camera):
        if camera == "11 A":
            # Logic to switch to camera 11 A
            print(f"Switched to camera {camera}")
        else:
            QMessageBox.warning(self, "No Camera", "No camera connected for " + camera)

    # ... rest of your class methods ...
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("System tray not available on this system")
        sys.exit(1)

    QApplication.setQuitOnLastWindowClosed(False)
    
    window = CCTVApp()
    window.show()
    
    sys.exit(app.exec_())
    # Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
    # All rights reserved.