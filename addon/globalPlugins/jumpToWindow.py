import re
import threading
from ctypes import windll

import 	api
import controlTypes
import globalPluginHandler
import gui
import textInfos
import tones
import ui
import winConsoleHandler
import winUser

user32 = windll.user32

import wx


def get_text(obj):
	text = obj.makeTextInfo(textInfos.POSITION_ALL).text
	return text

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _("Jump to Window")

	def script_find_window(self, gesture):
		dlg = wx.TextEntryDialog(parent=gui.mainFrame, message=_("Search Term (or regexp):"), caption=_("Jump To Window"))

		def callback(result):
			if result == wx.ID_OK:
				wx.CallLater(50, self.find, dlg.GetValue())
		gui.runScriptModalDialog(dlg, callback)

	script_find_window.__doc__ = _("""Focus a window whose title or console text matches the supplied value or regular expression""")

	def find(self, text):
		"""Find a window whose title matches the provided regexp.
		If no title matches, search the text of consoles."""
		consoles = []
		regexp = re.compile(text, re.IGNORECASE)
		windows = reversed(list(api.getDesktopObject().children))
		for w in windows:
			name = w.name
			if name is None:
				continue
			if regexp.search(name) is not None:
				focus(winConsoleHandler.windowHandle)
				return
			elif w.windowClassName == u'ConsoleWindowClass':
				consoles.append(w)

		#We didn't find the search text in the title, start searching consoles
		current_console = winConsoleHandler.consoleObject
		# While we would refocus our current console if there were no text found, the UI would still give an error beep
		# And therefore we wouldn't know if the text is in the console.
		if current_console is not None:
			consoles.remove(current_console)
			consoles.append(current_console)
		for console in consoles:
			try:
				console_text = get_console_text(console)
				if text in console_text.lower():
					focus(console.windowHandle)
					return
			except:
					continue
		else: #No consoles found
			if current_console:
				winConsoleHandler.connectConsole(current_console)
				if current_console == api.getFocusObject():
					current_console.startMonitoring() #Keep echoing if we didn't switch
		self.did_fail()

	def did_fail(self):
		tones.beep(300, 150)

	__gestures = {
		"kb:NVDA+\\": "find_window",
	}

def focus(hwnd):
	"""Try whatever we can to focus this window."""
	if user32.IsIconic(hwnd):
		user32.ShowWindow(hwnd, 9) #SW_RESTORE
	winUser.setForegroundWindow(hwnd)

def get_console_text(console):
	"""Gets the text of a console. The caller is responsible for
	reconnecting the current console if needed."""
	child = [child for child in console.children if child.role == controlTypes.ROLE_TERMINAL][0]
	if winConsoleHandler.consoleObject is not child: #We need to connect it
		if winConsoleHandler.consoleObject:
			winConsoleHandler.disconnectConsole()
		winConsoleHandler.connectConsole(child)
	console_text = get_text(child)
	if winConsoleHandler.consoleObject:
		winConsoleHandler.disconnectConsole()
	return console_text
