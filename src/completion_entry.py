#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class CompletionEntry(gtk.Entry):
	"""docstring for completion_entry"""
	def __init__(self):
		gtk.Entry.__init__(self)