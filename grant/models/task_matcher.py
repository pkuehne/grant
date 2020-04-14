""" Matches a task node against various inputs """

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject


class TaskMatcher(QObject):
    """ Allows the setting of various filters and then matches a task against them """
    filters_updated = pyqtSignal()

    def __init__(self):
        super(TaskMatcher, self).__init__()
        self._text_filter = ""
        self._result_filter = ""

    def text_filter(self, text):
        """ Sets the text filter """
        self._text_filter = text
        self.filters_updated.emit()

    def result_filter(self, text):
        """ Sets the result filter  """
        self._result_filter = text
        self.filters_updated.emit()

    def match_result_filter(self, task):
        """ Determines whether the node matches the result filter """
        if self._result_filter == "":
            return True

        if self._result_filter == "open" and task.result is None:
            return True

        return self._result_filter in str(task.result)

    def match(self, task):
        """ Checks the task against the given filters """
        if task is None:
            return False
            
        result = True
        result = result and self._text_filter in task.source
        result = result and self.match_result_filter(task)
        return result
