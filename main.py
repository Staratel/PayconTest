import asyncio
import gi
import api
import csv

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk


class Dialog(Gtk.Dialog):
	def __init__(self, parent):
		super().__init__(self, parent=parent)
		self.set_title("Загрузка данных...")
		self.set_default_size(250, 100)

		self.spinner = Gtk.Spinner()
		self.spinner.set_vexpand(True)
		self.spinner.set_hexpand(True)
		self.vbox.add(self.spinner)
		self.spinner.start()
		self.show_all()

	def complite(self):
		self.vbox.remove(self.spinner)
		label = Gtk.Label()
		label.set_text('Данные загружены')
		self.vbox.pack_start(label, True, True, 0)
		self.show_all()
		GLib.timeout_add(1000, function=self.destroy)


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
		layout.set_size(800, 2350)
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

		# list_name_columns = list(data[0].keys())
		list_name_columns = ['Название']

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

		# types_data = map(type, list(data[0].values()))

		# Добавление в список
		liststore = Gtk.ListStore(str)
		for d in data:
			# liststore.append(list(d.values()))
			liststore.append([d])
		self.treeview.set_model(liststore)

	def on_api_clicked(self, button):
		dialog = Dialog(self)
		data = asyncio.run(api.get_json_data())
		self.create_list(data)
		dialog.complite()

	def on_file_clicked(self, button):
		dialog = Dialog(self)
		data = []
		with open("data.csv", encoding="utf8") as file:
			reader = csv.DictReader(file)
			for row in reader:
				data.append(f"{row['Title']} {row['Price']}")
		self.create_list(data)
		dialog.complite()


def main():
	win = MainWindow()
	win.connect("destroy", Gtk.main_quit)
	win.show_all()
	Gtk.main()


if __name__ == '__main__':
	main()
