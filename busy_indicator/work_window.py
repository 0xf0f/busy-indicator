from busy_indicator.work import Work
from busy_indicator.work_thread import WorkThread
import PyQt5.Qt as qt


class WorkWindow(qt.QWidget):
    def __init__(self, work: Work):
        super().__init__()

        self.indicator_gif = qt.QMovie('busy-indicator.gif')
        self.indicator_gif.jumpToFrame(0)

        self.indicator_label = qt.QLabel()
        self.indicator_label.setMovie(self.indicator_gif)
        self.indicator_label.setAlignment(qt.Qt.AlignCenter)

        self.progress_label = qt.QLabel()
        self.progress_label.setAlignment(qt.Qt.AlignCenter)

        self.message_label = qt.QLabel()
        self.message_label.setAlignment(qt.Qt.AlignCenter)

        self.pause_button = qt.QPushButton()
        self.pause_button.setText('Pause')
        self.pause_button.clicked.connect(self.toggle_pause)

        self.close_checkbox = qt.QCheckBox()
        self.close_checkbox.setText('Close after completion')
        self.close_checkbox.setChecked(True)

        layout = qt.QVBoxLayout()
        # layout.setAlignment(qt.qt.AlignCenter)
        layout.addWidget(self.indicator_label)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.message_label)
        layout.addWidget(self.close_checkbox)
        layout.addWidget(self.pause_button)
        self.setLayout(layout)

        self.work_thread = WorkThread(work)
        self.work_thread.update_message.connect(self.update_message)
        self.work_thread.update_progress.connect(self.update_progress)
        self.work_thread.started.connect(self.started)
        self.work_thread.finished.connect(self.finished)

        self.fade = None

    @qt.pyqtSlot(str, name='update_progress')
    def update_progress(self, progress):
        self.progress_label.setText(progress)

    @qt.pyqtSlot(str, name='update_message')
    def update_message(self, message):
        self.message_label.setText(message)

    def started(self):
        # print('started')
        self.indicator_gif.start()

    def finished(self):
        self.message_label.setText('Complete.')
        self.indicator_gif.setPaused(True)

        self.pause_button.setEnabled(False)

        if self.close_checkbox.isChecked():
            self.close()

    def toggle_pause(self):
        if self.work_thread.is_paused():
            self.work_thread.resume()
            self.indicator_gif.setPaused(False)
            self.pause_button.setText('Pause')
        else:
            self.work_thread.pause()
            self.indicator_gif.setPaused(True)
            self.pause_button.setText('Resume')

    def start(self):
        self.work_thread.start()
