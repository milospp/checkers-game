from PySide2.QtWidgets import QBoxLayout, QSpacerItem, QWidget


# https://stackoverflow.com/questions/30005540/keeping-the-aspect-ratio-of-a-sub-classed-qwidget-during-resize
class AspectRatioWidget(QWidget):
    def __init__(self, widget, side_widget, parent):
        super().__init__(parent)
        self.setParent(parent)
        self.setStyleSheet("background:#222; color:#fff; padding:0; margin:0")
        self.setLayout(QBoxLayout(QBoxLayout.LeftToRight, self))

        self.main_widget = widget
        self.side_widget = side_widget

        self.centerWrapper = QWidget()
        self.centerWrapperLayout = QBoxLayout(QBoxLayout.LeftToRight)
        self.centerWrapperLayout.setMargin(0)
        self.centerWrapperLayout.setSpacing(0)
        self.centerWrapper.setLayout(self.centerWrapperLayout)
        self.centerWrapperLayout.addWidget(self.main_widget)
        self.centerWrapperLayout.addWidget(self.side_widget)

        self.layout().setMargin(0)
        #  add spacer, then widget, then spacer
        self.layout().addItem(QSpacerItem(0, 0))
        self.layout().addWidget(self.centerWrapper)
        # self.layout().addWidget(side_widget)
        self.layout().addItem(QSpacerItem(0, 0))

    def resizeEvent(self, e):
        w = e.size().width()
        h = e.size().height()
        side_width = self.side_widget.width()

        if w - 100 > h:  # too wide
            self.layout().setDirection(QBoxLayout.LeftToRight)
            widget_stretch = h + side_width
            outer_stretch = (w - h - side_width) / 2
        else:  # too tall
            self.layout().setDirection(QBoxLayout.TopToBottom)
            widget_stretch = w - side_width
            outer_stretch = (h - w + side_width) / 2

        self.layout().setStretch(0, outer_stretch)
        self.layout().setStretch(1, widget_stretch)
        self.layout().setStretch(2, outer_stretch)
