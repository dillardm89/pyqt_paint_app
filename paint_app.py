from PyQt6.QtWidgets import (QMainWindow, QApplication, QStatusBar)
from PyQt6.QtGui import (QAction, QIcon)
from canvas import PaintCanvas

""" This is a PyQt6 Paint Application.
    User can create new, open existing, and save drawings
    using a variety of tools (pencil, brush, spray paint,
    and eraser) in a variety of tool sizes, as well as
    select different tool colors.
"""


class AppWindow(QMainWindow):
    """ A class to represent the AppWindow

        ...

        Attributes
        ----------
        QMainWindow : class
            AppWindow inherits from this PyQt6 class

        Methods
        ----------
        init_UI():
            Sets up initial state of the object

    """

    def __init__(self):
        """
        Constructs all the attributes for the object
        """
        super().__init__()
        self.init_UI()

    def init_UI(self):
        """
        Sets up initial state of the object
        """
        self.setMinimumSize(500, 500)
        self.setWindowTitle('PyQt Paint App')

        # Create a PaintCanvas class instance
        canvas = PaintCanvas(self)
        self.setCentralWidget(canvas)

        # Create a status bar using QStatusBar class
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        # Create menu bar with drop-down fields and tool icons
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        # Add a 'File' drop-down to menu bar
        file_menu = menu_bar.addMenu('File')
        menu_bar.addMenu(QIcon('Icons/separator.png'), '|')

        # Add an open icon to menu bar
        self.open_icon = QAction(QIcon('Icons/open.png'), 'Open')
        self.open_icon.triggered.connect(canvas.open_file)
        menu_bar.addAction(self.open_icon)

        # Add a new icon to menu bar
        self.new_icon = QAction(QIcon('Icons/new.png'), 'New')
        self.new_icon.triggered.connect(canvas.new_file)
        menu_bar.addAction(self.new_icon)

        # Add a save icon to menu bar
        self.save_icon = QAction(QIcon('Icons/save.png'), 'Save')
        self.save_icon.triggered.connect(canvas.save_file)
        menu_bar.addAction(self.save_icon)

        # Add pencil, brush, spray paint, and eraser icons
        # with drop-downs to menu bar
        menu_bar.addMenu(QIcon('Icons/separator.png'), '|')
        pencil_menu = menu_bar.addMenu(QIcon('Icons/pencil.png'), 'Pencil')
        brush_menu = menu_bar.addMenu(QIcon('Icons/brush.png'), 'Brush')
        spray_menu = menu_bar.addMenu(QIcon('Icons/spray.png'), 'Spray')
        eraser_menu = menu_bar.addMenu(QIcon('Icons/eraser.png'), 'Eraser')

        # Add a color selector icon to menu bar
        self.colors_icon = QAction(QIcon('Icons/colors.png'), 'Colors')
        self.colors_icon.triggered.connect(
            lambda: canvas.select_tool_size('Colors', 0))
        menu_bar.addAction(self.colors_icon)

        # Create actions (new, open, save, save as, exit) to file menu
        self.new_action = QAction(QIcon('Icons/new.png'), 'New')
        self.new_action.triggered.connect(canvas.new_file)
        file_menu.addAction(self.new_action)

        self.open_action = QAction(QIcon('Icons/open.png'), 'Open')
        self.open_action.triggered.connect(canvas.open_file)
        file_menu.addAction(self.open_action)

        self.save_action = QAction(QIcon('Icons/save.png'), 'Save')
        self.save_action.triggered.connect(canvas.save_file)
        file_menu.addAction(self.save_action)

        self.save_as_action = QAction(QIcon('Icons/save_as.png'), 'Save As')
        self.save_as_action.triggered.connect(canvas.save_file_as)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()

        self.exit_action = QAction(QIcon('Icons/exit.png'), 'Exit')
        self.exit_action.triggered.connect(canvas.exit_program)
        file_menu.addAction(self.exit_action)

        # Create actions to select size to pencil menu
        self.pencil1x_action = QAction(QIcon('Icons/2px.png'), 'Pencil 2px')
        self.pencil1x_action.triggered.connect(
            lambda: canvas.select_tool_size('Pencil', 1))
        pencil_menu.addAction(self.pencil1x_action)

        self.pencil2x_action = QAction(QIcon('Icons/4px.png'), 'Pencil 4px')
        self.pencil2x_action.triggered.connect(
            lambda: canvas.select_tool_size('Pencil', 2))
        pencil_menu.addAction(self.pencil2x_action)

        self.pencil3x_action = QAction(QIcon('Icons/6px.png'), 'Pencil 6px')
        self.pencil3x_action.triggered.connect(
            lambda: canvas.select_tool_size('Pencil', 3))
        pencil_menu.addAction(self.pencil3x_action)

        self.pencil4x_action = QAction(QIcon('Icons/8px.png'), 'Pencil 8px')
        self.pencil4x_action.triggered.connect(
            lambda: canvas.select_tool_size('Pencil', 4))
        pencil_menu.addAction(self.pencil4x_action)

        # Create actions to select size to brush menu
        self.brush1x_action = QAction(QIcon('Icons/4px.png'), 'Brush 4px')
        self.brush1x_action.triggered.connect(
            lambda: canvas.select_tool_size('Brush', 2))
        brush_menu.addAction(self.brush1x_action)

        self.brush2x_action = QAction(QIcon('Icons/8px.png'), 'Brush 8px')
        self.brush2x_action.triggered.connect(
            lambda: canvas.select_tool_size('Brush', 4))
        brush_menu.addAction(self.brush2x_action)

        self.brush3x_action = QAction(QIcon('Icons/12px.png'), 'Brush 12px')
        self.brush3x_action.triggered.connect(
            lambda: canvas.select_tool_size('Brush', 6))
        brush_menu.addAction(self.brush3x_action)

        self.brush4x_action = QAction(QIcon('Icons/16px.png'), 'Brush 16px')
        self.brush4x_action.triggered.connect(
            lambda: canvas.select_tool_size('Brush', 8))
        brush_menu.addAction(self.brush4x_action)

        # Create actions to select size to spray menu
        self.spray1x_action = QAction(QIcon('Icons/S_4px.png'), 'Spray 2px')
        self.spray1x_action.triggered.connect(
            lambda: canvas.select_tool_size('Spray', 1))
        spray_menu.addAction(self.spray1x_action)

        self.spray2x_action = QAction(QIcon('Icons/S_4px.png'), 'Spray 4px')
        self.spray2x_action.triggered.connect(
            lambda: canvas.select_tool_size('Spray', 2))
        spray_menu.addAction(self.spray2x_action)

        self.spray3x_action = QAction(QIcon('Icons/S_6px.png'), 'Spray 6px')
        self.spray3x_action.triggered.connect(
            lambda: canvas.select_tool_size('Spray', 3))
        spray_menu.addAction(self.spray3x_action)

        self.spray4x_action = QAction(QIcon('Icons/S_8px.png'), 'Spray 8px')
        self.spray4x_action.triggered.connect(
            lambda: canvas.select_tool_size('Spray', 4))
        spray_menu.addAction(self.spray4x_action)

        # Create actions to select size eraser menu
        self.eraser1x_action = QAction(
            QIcon('Icons/E_16px.png'), 'Eraser 16px')
        self.eraser1x_action.triggered.connect(
            lambda: canvas.select_tool_size('Eraser', 4))
        eraser_menu.addAction(self.eraser1x_action)

        self.eraser2x_action = QAction(
            QIcon('Icons/E_24px.png'), 'Eraser 24px')
        self.eraser2x_action.triggered.connect(
            lambda: canvas.select_tool_size('Eraser', 6))
        eraser_menu.addAction(self.eraser2x_action)

        self.eraser3x_action = QAction(
            QIcon('Icons/E_32px.png'), 'Eraser 32px')
        self.eraser3x_action.triggered.connect(
            lambda: canvas.select_tool_size('Eraser', 8))
        eraser_menu.addAction(self.eraser3x_action)

        self.eraser4x_action = QAction(
            QIcon('Icons/E_40px.png'), 'Eraser 40px')
        self.eraser4x_action.triggered.connect(
            lambda: canvas.select_tool_size('Eraser', 10))
        eraser_menu.addAction(self.eraser4x_action)

        # Add keyboard shortcuts for new, open, and save actions
        self.new_action.setShortcut('Ctrl+N')
        self.open_action.setShortcut('Ctrl+O')
        self.save_as_action.setShortcut('Ctrl+S')


def main():
    """ Create instance of QApplication class and
        instance of AppWindow class then call methods
        to display application on desktop screen
    """
    app = QApplication([])
    window = AppWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
