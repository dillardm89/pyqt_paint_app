from PyQt6.QtWidgets import (QLabel, QFileDialog, QMessageBox, QSizePolicy,
                             QColorDialog)
from PyQt6.QtGui import (QMouseEvent, QPixmap, QPainter, QPaintEvent,
                         QResizeEvent, QPen, QColor)
from PyQt6.QtCore import (Qt, QPoint, QRect)
import random


class PaintCanvas(QLabel):
    """ A class to represent a Paint Canvas

        ...

        Attributes
        ----------
        QLabel : class
            PaintCanvas inherits from this PyQt6 class

        Methods
        ----------
        init_UI():
            Sets up initial state of the object
        resizeEvent(event: QResizeEvent):
            Event handler allows window to be resized
            while maintaining user drawing on canvas
        mouseMoveEvent(event: QMouseEvent):
            Event handler tracks mouse movement on canvas,
            updates location in status bar, and calls
            draw function
        mousePressEvent(event: QMouseEvent):
            Event handler updates drawing status and last
            mouse location on canvas when mouse pressed
        mouseReleaseEvent(event: QMouseEvent):
            Event handler updates drawing status when
            mouse released
        draw(points):
            Handles mouse location input to generate drawing
            on canvas based on drawing status, eraser status,
            and tool type selected
        paintEvent(event: QPaintEvent):
            Event handler updates pixmap to render drawing
            on canvas
        select_tool_size(self, tool, size):
            Sets variables for eraser status, tool type,
            pen width, and tool color based on user selection
            then updates status bar
        new_file():
            Generates new blank canvas after prompting user
            to save existing drawing
        open_file():
            Allows user to open existing image file
        save_file_as():
            Allows user to save drawing not previously saved
        save_file():
            Allows user to update saving a previously
            saved drawing
        exit_programs():
            Exits app after prompting user to save drawing
    """

    def __init__(self, parent):
        """
        Constructs all the attributes for the object

        Parameters
        ----------
            parent : class
                Attributes and methods of the parent class
                'AppWindow' in which the object instance is created
        """
        super().__init__(parent)
        self.parent_window = parent
        self.init_UI()

    def init_UI(self):
        """
        Sets up initial state of the object
        """

        # Set up and configure pixmap
        self.pixmap = QPixmap(400, 400)
        self.pixmap.fill(Qt.GlobalColor.white)
        self.setPixmap(self.pixmap)
        self.setMinimumSize(10, 10)
        self.setMouseTracking(True)

        # Set initial variables & statuses
        self.eraser_status = False
        self.drawing_status = False
        self.eraser_size = 4
        self.last_mouse_position = QPoint()
        self.mouse_label = QLabel()
        self.tool_label = QLabel()
        self.tool_selected = 'Pencil'
        self.pen_color = QColor(0, 0, 0)
        self.color_selected = self.pen_color.getRgb()
        self.pen_width = 2
        self.current_file = None

    def resizeEvent(self, event: QResizeEvent):
        """
        Event handler allows window to be resized
        while maintaining user drawing on canvas

        Parameters
        ----------
        event : QResizeEvent
            Inherits from PyQt6 QResizeEvent method
            for handling window resize event
        """
        old_img = self.pixmap
        scaled = old_img.scaled(self.width(), self.height(),
                                Qt.AspectRatioMode.IgnoreAspectRatio,
                                Qt.TransformationMode.SmoothTransformation)
        self.setSizePolicy(QSizePolicy.Policy.Preferred,
                           QSizePolicy.Policy.Preferred)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pixmap = scaled
        self.setPixmap(self.pixmap)

    def mouseMoveEvent(self, event: QMouseEvent):
        """
        Event handler tracks mouse movement on canvas,
        updates location in status bar, and calls
        draw function

        Parameters
        ----------
        event : QMouseEvent
            Inherits from PyQt6 QMouseEvent method
            for handling mouse events
        """
        self.mouse_position = event.pos()

        # Update status bar
        mouse_text = (f'     Mouse at {self.mouse_position.x()}, ' +
                      f'{self.mouse_position.y()}     ')
        self.mouse_label.setText(mouse_text)
        self.parent_window.statusBar.addPermanentWidget(self.mouse_label)

        tool_text = (f'     Tool: {self.tool_selected}, ' +
                     f'Size: {self.pen_width}px, ' +
                     f'Color: {self.color_selected}     ')
        self.tool_label.setText(tool_text)
        self.parent_window.statusBar.addWidget(self.tool_label)

        # Call draw method
        if ((event.buttons() and Qt.MouseButton.LeftButton)
                and self.drawing_status):
            self.draw(self.mouse_position)

    def mousePressEvent(self, event: QMouseEvent):
        """
        Event handler updates drawing status and last
        mouse location on canvas when mouse pressed

        Parameters
        ----------
        event : QMouseEvent
            Inherits from PyQt6 QMouseEvent method
            for handling mouse events
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_mouse_position = self.mouse_position
            self.drawing_status = True

    def mouseReleaseEvent(self, event: QMouseEvent):
        """
        Event handler updates drawing status when
        mouse released

        Parameters
        ----------
        event : QMouseEvent
            Inherits from PyQt6 QMouseEvent method
            for handling mouse events
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing_status = False

    def draw(self, points):
        """
        Handles mouse location input to generate drawing
        on canvas based on drawing status, eraser status,
        and tool type selected

        Parameters
        ----------
        points : QPoint
            Inherits from PyQt6 QPoint class
            containing attributes and methods for mouse
            position on canvas
        """
        painter = QPainter(self.pixmap)

        # Set drawing type based on tool selected and
        # eraser status
        if (self.eraser_status is False and
                self.tool_selected != 'Spray Paint'):
            pen = QPen(self.pen_color, self.pen_width)
            painter.setPen(pen)
            painter.drawLine(self.last_mouse_position, points)
            self.last_mouse_position = points
        elif (self.eraser_status is False and
                self.tool_selected == 'Spray Paint'):
            pen = QPen(self.pen_color, 1)
            painter.setPen(pen)

            spray_particles = self.pen_width * 2
            spray_diameter = self.pen_width

            for n in range(spray_particles):
                x_point = points.x() + round(random.gauss(0, spray_particles))
                y_point = points.y() + round(random.gauss(0, spray_diameter))
                painter.drawPoint(int(x_point), int(y_point))
        else:
            eraser = QRect(points.x(), points.y(),
                           self.eraser_size, self.eraser_size)
            painter.eraseRect(eraser)
        self.update()

    def paintEvent(self, event: QPaintEvent):
        """
        Event handler updates pixmap to render drawing
        on canvas

        Parameters
        ----------
        points : QPaintEvent
            Inherits from PyQt6 QPoint method for handling
            pixmap update events

        """
        painter = QPainter(self)
        target_rectangle = QRect()
        target_rectangle = event.rect()
        painter.drawPixmap(target_rectangle, self.pixmap, target_rectangle)
        painter.end()

    def select_tool_size(self, tool, size):
        """
        Sets variables for eraser status, tool type,
        pen width, and tool color based on user selection
        then updates status bar

        Parameters
        ----------
        tool : str
            Tool type selected by user
        size : int
            Tool size selected by user

        """
        if tool == 'Spray':
            self.eraser_status = False
            self.tool_selected = 'Spray Paint'
            self.pen_width = 2 * size
        elif tool in ('Pencil', 'Brush'):
            self.eraser_status = False
            self.tool_selected = tool
            self.pen_width = 2 * size
        elif tool == 'Colors':
            self.eraser_status = False
            self.pen_color = QColorDialog.getColor()
            self.color_selected = QColor.getRgb(self.pen_color)
        elif tool == 'Eraser':
            self.eraser_status = True
            self.tool_selected = 'Eraser'
            self.eraser_size = 4 * size

        # Update status bar with tool / size selection
        tool_text = (f'     Tool: {self.tool_selected}, ' +
                     f'Size: {self.pen_width}px, ' +
                     f'Color: {self.color_selected}     ')
        self.tool_label.setText(tool_text)
        self.parent_window.statusBar.addWidget(self.tool_label)

    def new_file(self):
        """
        Generates new blank canvas after prompting user
        to save existing drawing
        """
        message_text = 'Do you want to save before starting a new canvas?'
        new_msg = QMessageBox.question(self, 'Save File', message_text,
                                       QMessageBox.StandardButton.Save |
                                       QMessageBox.StandardButton.Discard,
                                       QMessageBox.StandardButton.Save)

        if new_msg == QMessageBox.StandardButton.Save:
            print('Save File')
            self.save_file()
        else:
            print('File Not Saved')

        self.pixmap.fill(Qt.GlobalColor.white)
        self.current_file = None
        self.update()

    def open_file(self):
        """
        Allows user to open existing image file
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Open File', '',
            'All Files(*);; PNG Files(*.png);; JPG Files(*.jpg)')

        if file_path:
            new_img = QPixmap(file_path)
            scaled = new_img.scaled(self.width(),
                                    self.height(),
                                    Qt.AspectRatioMode.KeepAspectRatio,
                                    Qt.TransformationMode.SmoothTransformation)
            self.pixmap = scaled
            self.setPixmap(self.pixmap)

    def save_file_as(self):
        """
        Allows user to save drawing not previously saved
        """
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save File', '',
            'All Files(*);; PNG Files(*.png);; JPG Files(*.jpg)')

        if file_path:
            self.current_file = file_path
            self.pixmap.save(file_path)
            print('File Saved')

    def save_file(self):
        """
        Allows user to update saving a previously
        saved drawing
        """
        if self.current_file is not None:
            self.pixmap.save(self.current_file)
            print('File Saved')
        else:
            print('Save File As')
            self.save_file_as()

    def exit_program(self):
        """
        Exits app after prompting user to save drawing
        """
        if self.current_file is not None:
            self.save_file()
        else:
            message_text = 'Do you want to save before exiting?'
            exit_msg = QMessageBox.question(self, 'Save File', message_text,
                                            QMessageBox.StandardButton.Yes |
                                            QMessageBox.StandardButton.No,
                                            QMessageBox.StandardButton.Yes)

            if exit_msg == QMessageBox.StandardButton.Yes:
                print('Saving File')
                self.save_file_as()
            else:
                print('File Not Saved')

        print('Exiting File...')
        self.parent_window.close()
