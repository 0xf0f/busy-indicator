from busy_indicator.work import Work
import PyQt5.Qt as qt
import threading


class WorkThread(qt.QThread):
    update_progress = qt.pyqtSignal(str)
    update_message = qt.pyqtSignal(str)
    paused = qt.pyqtSignal(bool)

    def __init__(self, work: Work):
        super().__init__()

        self.work = work

        self.started.connect(self.work.started)
        self.finished.connect(self.work.finished)

        self.paused_event = threading.Event()
        self.paused_event.set()

    def run(self):
        self.paused_event.wait()
        self.work.started()
        while not self.work.complete():
            self.paused_event.wait()
            self.update_message.emit(self.work.status())
            self.update_progress.emit(self.work.progress())
            self.work.iterate()
            self.paused_event.wait()
        self.work.finished()

    def pause(self):
        self.paused_event.clear()
        self.paused.emit(True)

    def resume(self):
        self.paused_event.set()
        self.paused.emit(False)

    def is_paused(self):
        return not self.paused_event.is_set()

