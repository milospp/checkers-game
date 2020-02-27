from PySide2.QtWidgets import QBoxLayout, QSpacerItem, QWidget


#https://stackoverflow.com/questions/30005540/keeping-the-aspect-ratio-of-a-sub-classed-qwidget-during-resize
class AspectRatioWidget(QWidget):
    def __init__(self, widget, parent):
        super().__init__(parent)
        self.setStyleSheet("background:#222; padding:0; margin:0")
        self.setLayout(QBoxLayout(QBoxLayout.LeftToRight, self))
        self.layout().setMargin(0)
        #  add spacer, then widget, then spacer
        self.layout().addItem(QSpacerItem(0, 0))
        self.layout().addWidget(widget)
        self.layout().addItem(QSpacerItem(0, 0))

    def resizeEvent(self, e):
        w = e.size().width()
        h = e.size().height()

        if w > h:  # too wide
            self.layout().setDirection(QBoxLayout.LeftToRight)
            widget_stretch = h
            outer_stretch = (w - h) / 2
        else:  # too tall
            self.layout().setDirection(QBoxLayout.TopToBottom)
            widget_stretch = w
            outer_stretch = (h - w) / 2

        self.layout().setStretch(0, outer_stretch)
        self.layout().setStretch(1, widget_stretch)
        self.layout().setStretch(2, outer_stretch)