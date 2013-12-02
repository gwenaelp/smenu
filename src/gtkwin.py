#!/usr/bin/env python

#http://stackoverflow.com/questions/9215649/how-to-really-put-a-window-above-all-others-linux-pygtk
import pygtk
pygtk.require('2.0')
import gtk
import args
import sys

from completion_list import CompletionList
from completion_entry import CompletionEntry
import pprint
import inspect

returnValue = ""

class App:

	def destroy(self, widget, data=None):
		print("destroy signal occurred")
		gtk.main_quit()

	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", self.destroy)

		self.window.set_keep_above(True)
		self.window.show()

		vbox = gtk.VBox()
		vbox.show()
		self.window.add(vbox)

		self.text = gtk.Entry()
		self.text.show()

		if args.get().entries is not None:
			raw_entries = args.get().entries
		elif args.get().file is not None:
			f = open(args.get().file, 'r')
			raw_entries = f.read()
			f.close()

		self.completion_list = CompletionList(self.text, raw_entries, args.get().datatype)
		self.completion_list.show()
		self.completion_list.set_enable_search(False)
		self.completion_list.set_can_focus(False)
		self.text.connect("changed", self.completion_list.apply_filter)
		self.text.connect("activate", self.launch_command)
		self.text.connect('key_press_event', self.on_key_press)

		scrolled_window = gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
		scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		scrolled_window.add(self.completion_list)
		scrolled_window.set_can_focus(False)
		scrolled_window.show()

		vbox.pack_start(self.text, False, True)
		vbox.pack_start(scrolled_window, True, True)
		self.text.set_size_request(20, 20)

		self.text.set_flags(gtk.CAN_DEFAULT)
		self.text.set_receives_default(True)
		self.text.grab_focus()

		pos = args.get().position
		if pos is not None:
			pos = pos.split(",")

			x = int(pos[0])
			y = int(pos[1])

			self.window.move(x, y)

	def on_key_press(self, widget, event):
		keyname = gtk.gdk.keyval_name(event.keyval)
		func = getattr(self, 'keypress_' + keyname, None)

		if func:
			return func()

	def keypress_Escape(self):
		gtk.main_quit()

	def keypress_Up(self):
		self.completion_list.select_prev_column()

	def keypress_Down(self):
		self.completion_list.select_next_column()

	def launch_command(self, entry):
		global returnValue
		returnValue = self.completion_list.get_seleted_value()
		gtk.main_quit()

	def main(self):
		gtk.main()

if __name__ == "__main__":
	theme = args.get().theme
	if theme is not None:
		gtk.rc_parse(theme)

	app = App()
	app.main()

	print(returnValue)
	sys.exit(returnValue)
