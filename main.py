import time

import gi
import api
import csv

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk


class MainWindow(Gtk.Window):
	def __init__(self):
		super().__init__(title='Download data')
		self.set_default_size(width=800, height=600)

		# Сетка
		self.grid = Gtk.Grid()
		self.grid.set_row_spacing(5)
		self.grid.set_column_spacing(5)

		self.treeview = Gtk.TreeView()
		scrolled_window = Gtk.ScrolledWindow()

		# Слой
		layout = Gtk.Layout()
		layout.set_size(800,2350)
		layout.set_vexpand(True)
		layout.set_hexpand(True)
		layout.add(self.treeview)
		scrolled_window.add(layout)

		self.grid.attach(scrolled_window, 0, 0, 2, 1)

		button_api = Gtk.Button(label='Загрузить из API')
		button_api.connect("clicked", self.on_api_clicked)
		self.grid.attach(button_api, 0, 1, 1, 1)

		button_file = Gtk.Button(label='Загрузить из файла')
		button_file.connect("clicked", self.on_file_clicked)
		self.grid.attach(button_file, 1, 1, 1, 1)

		self.add(self.grid)
		self.columns = []

	def create_list(self, data):
		cellrenderertext = Gtk.CellRendererText()  # Рисует текст

		list_name_columns = list(data[0].keys())

		# Если существуют столбцы - удалить их
		if self.treeview.get_n_columns() != 0:
			for column in self.columns:
				self.treeview.remove_column(column)
			self.columns = []

		# Создание столбцов
		for i, name in enumerate(list_name_columns):
			treeviewcolumn = Gtk.TreeViewColumn(name)
			self.columns.append(treeviewcolumn)
			self.treeview.append_column(treeviewcolumn)
			treeviewcolumn.pack_start(cellrenderertext, True)
			treeviewcolumn.add_attribute(cellrenderertext, "text", i)

		types_data = list(map(type, list(data[0].values())))

		# Добавление в список
		liststore = Gtk.ListStore.new(types_data)
		for d in data:
			liststore.append(list(d.values()))

		self.treeview.set_model(liststore)

	def on_api_clicked(self, button):
		data = api.get_json_data()
		self.create_list(data)

	def on_file_clicked(self, button):
		data = []

		with open("data.csv", encoding="utf8") as file:
			reader = csv.DictReader(file)
			for row in reader:
				data.append(row)
		self.create_list(data)


def main():
	win = MainWindow()
	win.connect("destroy", Gtk.main_quit)
	win.show_all()
	Gtk.main()


if __name__ == '__main__':
	main()
