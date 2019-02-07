from TestStack.White.Configuration import CoreAppXmlConfiguration
from TestStack.White import AutomationException
from WhiteLibrary.keywords.librarycomponent import LibraryComponent
from WhiteLibrary.keywords.robotlibcore import keyword
from TestStack.White.UIItems.WindowItems import Window   # noqa: F401
from TestStack.White import Desktop
from robot.api import logger    # noqa: F401


class WindowKeywords(LibraryComponent):

    @keyword
    def get_title(self):
        """Returns title of the currently attached window. Does not use parameters.
        Assumes some window is already attached.
        """
        return self.state.window.Title

    @keyword
    def attach_window(self, window_title):
        """Attach WhiteLibrary to a window of already attached application.

        See `Attach Application By Id`, `Attach Application By Name` or
        `Launch application` for more details.

        ``window_title`` is the title of the window.
        """

        self.state.window = self._get_window(window_title)

    @keyword
    def list_application_windows(self):
        """Returns a list of all main windows in belonging to an application. Does not return modal windows.
        """
        return list(self.state.app.GetWindows())

    @keyword
    def attach_window_by_index(self, window_index):
        """Attaches WhiteLibrary to a window by its index.
        ``window_index`` is the index of the window.
        """
        self.state.window = self.state.app.GetWindows()[window_index]
        logger.debug("Attached to window {}".format(self.state.window))

    @keyword
    def list_desktop_windows(self):
        """Returns a list of all main windows on the desktop. Does not return modal windows.
        """
        return list(Desktop.Instance.Windows())

    @keyword
    def attach_desktop_window_by_name(self, name):
        """Attaches WhiteLibrary to a window by its name.
        ``name`` is the name of the window.
        """
        for win in Desktop.Instance.Windows():
            if win.Name == name:
                self.state.window = win
                logger.debug("Attached to window {}".format(self.state.window))
                return
        raise AssertionError("Window with name {} not found".format(name))

    @keyword
    def attach_desktop_window_by_id(self, id):
        """Attaches WhiteLibrary to a window by its automation id.
        ``id`` is the automation id of the window.
        """
        for win in Desktop.Instance.Windows():
            if win.Id == id:
                self.state.window = win
                logger.debug("Attached to window {}".format(self.state.window))
                return
        raise AssertionError("Window with id {} not found".format(id))


    @keyword
    def select_modal_window(self, window_title):
        """Select modal window.

        ``window_title`` is the title of the window.
        """
        self.state.window = self.state.window.ModalWindow(window_title)

    @keyword
    def close_window(self, window_title=None):
        """Closes a window.

        ``window_title`` is the title of the window (optional).

        If title is not given, the currently attached window is closed.
        See `Attach Window` for more details.
        """
        if window_title is not None:
            window = self._get_window(window_title)
            window.Close()
        else:
            self.state.window.Close()

    def _get_window(self, window_title):
        try:
            return self.state.app.GetWindow(window_title)
        except AutomationException as error_msg:
            error_msg = str(error_msg)
            replaced_text = "after waiting for {0} seconds".format(int(CoreAppXmlConfiguration.Instance.FindWindowTimeout / 1000))
            raise AutomationException(error_msg.replace("after waiting for 30 seconds", replaced_text), "")
        except AttributeError as error_msg:
            error_msg = str(error_msg)
            if "NoneType" in error_msg:
                error_msg = "No application attached."
            raise AttributeError(error_msg)
