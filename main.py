import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk


class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title='Download data')
        self.set_default_size(width = 800, height = 600)

        # Сетка
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)

        # СкроллОкно
        scrolled_window = Gtk.ScrolledWindow()
        grid.attach(scrolled_window,0,0,2,1)

        # Список
        # Product_id,Title,Price,quantity,weight?,Category,Picture
        liststore = Gtk.ListStore(str,str,int,str,str,int)
        for data in [["318","Хлеб фруктово-медовый", 96.0], ["336","Сыр полутвердый \"Российский\"", 740.0 ], ["352","Творог детский \"Клубника\" 4,2%", 38.0 ], ["356","Морс брусничный стекло", 131.0 ], ["357","Морс черника стекло", 48.0 ], ["358","Морс облепиха стекло", 135.0 ], ["360","Морс клюква стекло", 131.0 ], ["365","Нектар тыквенно-яблочный,1л., ЗиЗ", 2.0 ], ["366","Сок томатный, 1 л", 100.0 ], ["369","Нектар морковно-яблочный, 1л.,ЗиЗ", 132.0 ], ["371","Вода родниковая, 500 мл", 29.0 ], ["372","Вода родниковая, 5 л", 87.0 ], ["373","Вода родниковая, 1,5 л", 45.0 ], ["401","Кальмар тушка, замороженная", 327.0 ], ["414","Кижуч стейк свежемороженный", 900.0 ], ["417","Горбуша натуральная, 250 г", 177.0 ], ["420","Скумбрия натуральная", 105.0 ], ["484","Тушка цыпленка-бройлера, охлажденная", 203.0 ], ["487","Окорочок цыпленка", 226.0 ], ["488","Филе грудки цыпленка", 336.0 ], ["489","Голень цыпленка", 251.0 ], ["501","Говядина лопатка, без кости", 780.0 ], ["511","Окорок свиной охлажденный", 405.0 ], ["541","Колбаса \"Краковская\" полукопченая", 720.0 ], ["542","Пельмени с говядиной и свининой", 470.0 ], ["557","Вареники с творогом", 217.0 ], ["559","Вареники с картофелем и грибами", 194.0 ], ["598","Яйцо перепелиное", 100.0 ], ["599","Яйцо куриное домашнее 1 дес", 140.0 ], ["602","Капуста белокочанная", 25.0 ], ["605","Лук репчатый", 40.0 ], ["606","Морковь", 138.0 ], ["608","Перец сладкий", 140.0 ], ["609","Огурцы короткоплодные", 180.0 ], ["611","Свекла", 52.0 ], ["615","Черешня", 300.0 ], ["617","Клубника", 525.0 ], ["619","Кабачки", 78.0 ], ["626","Капуста цветная", 180.0 ], ["629","Сумка \"ВкусВилл\", шт", 18.0 ], ["646","Пакет-майка \"Избёнка\" большой", 7.0 ], ["647","Пакет-майка \"Избёнка\" малый", 6.0 ], ["654","Персик", 215.0 ], ["655","Нектарин", 190.0 ], ["659","Груша Конференция", 232.0 ], ["662","Редис молодой пучок, 300 г", 115.0 ], ["673","Батон нарезной", 26.0 ], ["674","Хлеб \"Украинский Новый\", нарезка", 20.0 ], ["675","Хлеб \"Бородинский\"", 40.0 ], ["682","Пирожок с капустой", 78.0 ], ["685","Пряник \"Паломник\"", 226.0 ], ["690","Слива красная", 155.0 ], ["692","Хлеб \"Рождественский\", половинка", 47.0 ], ["696","Окунь филе на коже замороженное", 620.0 ], ["697","Кальмар филе очищенное, замороженное", 557.0 ], ["698","Судак филе на коже замороженное", 648.0 ], ["716","Хлеб \"Казанский\", половинка", 56.0 ], ["729","Апельсины", 100.0 ], ["730","Лимоны", 158.0 ], ["731","Бананы", 88.0 ], ["732","Бифилайф детский \"Малина-шиповник\" 2,5%", 38.0 ], ["736","Мандарины", 187.0 ], ["744","Пряник \"Игрушка\"", 46.0 ], ["752","Нерка малосоленая филе- кусок, 250 г", 385.0 ], ["755","Пельмени с говядиной и зеленью", 505.0 ], ["775","Пюре из моркови", 31.0 ], ["776","Пюре из яблок и клубники", 37.0 ], ["778","Пюре из яблок и черники", 65.0 ] ]:
            liststore.append(data)

        # Слой
        layout = Gtk.Layout()
        layout.set_size(800,600)
        layout.set_vexpand(True)
        layout.set_hexpand(True)

        treeview = Gtk.TreeView()
        treeview.set_model(liststore)

        layout.add(treeview)
        scrolled_window.add(layout)


        cellrenderertext = Gtk.CellRendererText()

        list_name_columns = ["id","name","price"] # Заменить на заголовки из API Json или файла CSV по заданию
        for i in range(3):
            treeviewcolumn = Gtk.TreeViewColumn(list_name_columns[i])
            treeview.append_column(treeviewcolumn)
            treeviewcolumn.pack_start(cellrenderertext, True)
            treeviewcolumn.add_attribute(cellrenderertext, "text", i)

        button_api = Gtk.Button(label='Загрузить из API')
        button_api.connect("clicked", self.on_api_clicked)
        grid.attach(button_api,0,1,1,1)

        button_file = Gtk.Button(label='Загрузить из файла')
        button_file.connect("clicked", self.on_file_clicked)
        grid.attach(button_file,1,1,1,1)
        self.add(grid)

    def on_api_clicked(self, button):
        print('Hello')

    def on_file_clicked(self, button):
        print('file')

def main():
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()