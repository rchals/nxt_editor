# Builtin
import os
import sys
import logging

# External
from Qt import QtCore, QtWidgets, QtGui

logger = logging.getLogger('nxt.editor')


class DIRECTIONS:
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'


class LoggingSignaler(QtCore.QObject):
    """Qt object used to emit logging messages. This object allows us to make
    thread safe visual loggers.
    """
    signal = QtCore.Signal(logging.LogRecord)


class StringSignaler(QtCore.QObject):
    """Qt object used to emit strings. This object allows us to use Qt
    signals in objects that themselves can't be a QObject.
    """
    signal = QtCore.Signal(str)


def make_resources(qrc_path, result_path):
    import subprocess
    subprocess.call(['pyside2-rcc', qrc_path, '-o', result_path])


try:
    from . import resources
except ImportError:
    this_dir = os.path.dirname(os.path.realpath(__file__))
    qrc_path = os.path.join(this_dir, 'resources/resources.qrc')
    result_path = os.path.join(this_dir, 'resources.py')
    msg = 'First launch nxt resource generation from {} to {}'
    logger.info(msg.format(qrc_path, result_path))
    make_resources(qrc_path, result_path)


def launch_editor(paths=None):
    """Creates a new QApplication with editor main window and shows it.
    """
    # Deferred import since main window relies on us
    from nxt_editor.main_window import MainWindow
    path = None
    if paths is not None:
        path = paths[0]
        paths.pop(0)
    else:
        paths = []
    app = QtWidgets.QApplication(sys.argv)
    app.setEffectEnabled(QtCore.Qt.UI_AnimateCombo, False)
    instance = MainWindow(filepath=path)
    for other_path in paths:
        instance.load_file(other_path)
    pixmap = QtGui.QPixmap(':icons/icons/nxt.svg')
    app.setWindowIcon(QtGui.QIcon(pixmap))
    app.setActiveWindow(instance)
    instance.show()
    return app.exec_()
    sys.exit()