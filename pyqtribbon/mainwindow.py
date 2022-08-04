from .framelesswindow import FramelessWindow


class RibbonMainWindow(FramelessWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.titleBar.raise_()
