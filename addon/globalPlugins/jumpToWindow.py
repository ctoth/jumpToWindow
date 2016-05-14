import globalPluginHandler
import ui
import api
import textInfos
import threading
import gui
import winConsoleHandler
import winUser
import controlTypes
from ctypes import windll
import tones
user32 = windll.user32

import wx

def get_text(obj):
	text = obj.makeTextInfo(textInfos.POSITION_ALL).text
	return text

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def script_find_window(self, gesture):
		dlg = wx.TextEntryDialog(gui.mainFrame, _("Search For:"), _("Jump To Window"))

		def callback(result):
			if result == wx.ID_OK:
				wx.CallLater(100, self.find, dlg.GetValue())
		gui.runScriptModalDialog(dlg, callback)

	def find(self, text):
		"""Find a window with the supplied text in its title.
		If the text isn't found in any title, search the text of consoles."""
		consoles = set()
		text = text.lower()
		for c in api.getDesktopObject().children:
			name = c.name
			if name is None:
				continue
			if text in name.lower():
				focus(c.windowHandle)
				return
			elif c.windowClassName == u'ConsoleWindowClass':
				consoles.add(c)

		#We didn't find the search text in the title, start searching consoles
		current_console = winConsoleHandler.consoleObject
		# If our current console is the one with the text in it, presumably we want another one, and if one isn't found, we'll refocus anyway
		if current_console is not None:
			consoles.remove(current_console)
		for console in consoles:
			#We assume this can't fail
			console_text = get_console_text(console)
			if text in console_text.lower():
				focus(console.windowHandle)
				return
		else: #No consoles found
			if current_console:
				winConsoleHandler.connectConsole(current_console)
				if current_console == api.getFocusObject():
					current_console.startMonitoring() #Keep echoing if we didn't switch
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
