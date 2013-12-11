import pygtk
pygtk.require('2.0')
import gtk
from fuzzywuzzy import fuzz
import json

class CompletionList(gtk.TreeView):

	"""the widget with the list of available choices"""
	def __init__(self, entry, completions, datatype):

		print str(type(completions))
		
		if datatype == "json":
			completions = json.loads(completions)
		elif datatype == "plain_newlines":
			completions = completions.split("\n")
		else:
			completions = completions.split(",")

		if datatype == "json":
			self.liststore = gtk.TreeStore(int, str, gtk.gdk.Pixbuf)

			for completion in completions:
				icon = gtk.gdk.pixbuf_new_from_file("/usr/share/icons/Mint-X/apps/24/firefox.png")
				self.liststore.append(None, [0, completion["text"], icon])
		else:
			self.liststore = gtk.TreeStore(int, str)

			for completion in completions:
				self.liststore.append(None, [0, completion])

		self.modelfilter = self.liststore.filter_new()

		gtk.TreeView.__init__(self, self.liststore)
		self.set_headers_visible(False)

		self.entry = entry

		self.buildColumns(datatype)

		self.modelfilter.set_visible_func(self.visible_function, "")
		self.modelsort = gtk.TreeModelSort(child_model=self.modelfilter)
		self.modelsort.set_sort_column_id(0, gtk.SORT_DESCENDING)
		self.set_model(self.modelsort)

		self.set_cursor(0)

	def buildColumns(self, datatype):
		if datatype == "json":
			self.col_icon = gtk.TreeViewColumn('Icon')
			self.append_column(self.col_icon)
			cellIcon = gtk.CellRendererPixbuf()
			self.col_icon.pack_start(cellIcon, False)
			self.col_icon.add_attribute(cellIcon, "pixbuf", 2)

		self.tvcol_score = gtk.TreeViewColumn('Score')
		self.cellScore = gtk.CellRendererText()
		self.append_column(self.tvcol_score)
		self.tvcol_score.pack_start(self.cellScore, True)
		self.tvcol_score.add_attribute(self.cellScore, 'text', 0)

		self.tvcol_completions = gtk.TreeViewColumn('Completion')
		self.append_column(self.tvcol_completions)
		self.cellCompletion = gtk.CellRendererText()
		self.tvcol_completions.pack_start(self.cellCompletion, True)
		self.tvcol_completions.add_attribute(self.cellCompletion, 'text', 1)

	def visible_function(self, model, iter, data):
		score = model.get_value(iter, 0)
		if len(self.entry.get_text()) == 0:
			return True
		else:
			return score > 0

	def set_scores(self, text):
		iter = self.liststore.get_iter_first()
		while iter:
			ratio = fuzz.partial_ratio(self.liststore.get_value(iter, 1), text.get_text())
			self.liststore.set_value(iter, 0, ratio)
			iter = self.liststore.iter_next(iter)

	def apply_filter(self, text):
		self.set_scores(text)
		self.modelfilter.refilter()
		self.set_cursor(0)

	def get_seleted_value(self):
		selectedIter = self.modelsort.get_iter(self.get_cursor()[0])
		return self.modelsort.get_value(selectedIter, 1)

	def select_prev_column(self):
		selectedIter = self.modelsort.get_iter(self.get_cursor()[0])
		selectedIter = self.iter_prev(selectedIter)
		self.set_cursor(self.modelsort.get_path(selectedIter))

	def select_next_column(self):
		selectedIter = self.modelsort.get_iter(self.get_cursor()[0])
		selectedIter = self.iter_next(selectedIter)
		self.set_cursor(self.modelsort.get_path(selectedIter))

	def iter_next(self, iter):
		return self.modelsort.iter_next(iter)

	def iter_prev(self, iter):
		path = self.modelsort.get_path(iter)
		position = path[-1]
		if position == 0:
			return None
		prev_path = list(path)[:-1]
		prev_path.append(position - 1)
		prev = self.modelsort.get_iter(tuple(prev_path))
		return prev
