#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
import os
import sys
import lib_sql as SQL


class App(tk.Tk):
    '''
    Основное окно
    '''
    def __init__(self):
        super().__init__()
        self.time_window = []
        self.add_window = []
        self.title('Master SQLite3')
        self.name_DB_Direct = 'Data_Base'  # вложенная директория базы данных
        self.type_file = ".db"
        self.width = 900
        self.height = 600
        self.num_page = [0, 1, 2, 3, 4]
        self.page = self.num_page[0]
        self.create_or_check_Direct()  # создаем, если еще не существует, директорию для DB
        self.put_frames()
        self.give_all_DB()
        self.minsize(900, 670)
        self.maxsize(900, 670)

    def give_all_DB(self):
        self.direct = f'{os.getcwd()}/{self.name_DB_Direct}'
        self.name_of_tables = os.listdir(self.direct)
        return self.name_of_tables

    def put_frames(self):
        self.change_page = BTNPage1(self).place(x = 0, y = 0, width = 900, height = 50)
        if self.page == 4:
            self.show_page = Start_Page(self).place(x = 0, y = 30, width = self.width, height = self.height)
        elif self.page == 1:
            self.show_page = Create_DB_Tables(self).place(x = 0, y = 30, width = self.width, height = self.height)
        elif self.page == 2:
            self.show_page = SQL_ask(self).place(x = 0, y = 30, width = self.width, height = self.height)
        elif self.page == 3:
            self.show_page = EXEC_COM(self).place(x = 0, y = 30, width = self.width, height = self.height)
        elif self.page == 0:
            self.show_page = View_DB_Tables(self).place(x = 0, y = 30, width = self.width, height = self.height)
        self.form_restrt = FormRestart(self).place(x = self.width - 170, y = self.height + 30)

    def refresh(self):
        all_frames = [f for f in self.children]
        for f_name in all_frames:
            self.nametowidget(f_name).destroy()
        self.put_frames()
        self.give_all_DB()

    def start_page(self):
        self.page = self.num_page[0]
        self.refresh()

    def create_db_tables(self):
        self.page = self.num_page[1]
        self.refresh()

    def sql_ask(self):
        self.page = self.num_page[2]
        self.refresh()

    def exec_page(self):
        self.page = self.num_page[3]
        self.refresh()

    def view_page(self):
        self.page = self.num_page[4]
        self.refresh()

    def create_or_check_Direct(self):
        try:
            os.mkdir(f'{os.getcwd()}/{self.name_DB_Direct}')
        except:
            pass

    def add_data(self):
        self.add_win = AddfWin(self)
        if self.add_window:
            for i in self.add_window:
                i.destroy()
            self.add_window = []
        self.add_window.append(self.add_win)


class BTNPage1(ttk.Frame):
    '''
    Временный фрейм, содержащий кнопки переключения страниц
    '''
    def __init__(self, parent):
        super().__init__(parent)
        btn_1 = ttk.Button(self, text="Черновая страница", command=parent.view_page)
        btn_2 = ttk.Button(self, text="Создание БД и таблиц", command=parent.create_db_tables)
        btn_3 = ttk.Button(self, text="SQL запросы", command=parent.sql_ask)
        btn_4 = ttk.Button(self, text="Команды Python(exec)", command=parent.exec_page)
        btn_5 = ttk.Button(self, text="Отображение таблиц", command=parent.start_page)
        btn_6 = ttk.Button(self, text="Доб./Изм./Уд.", command=parent.add_data)
        btn_1.place(x=595, y=0)
        btn_2.place(x = 160, y = 0)
        btn_3.place(x = 330, y = 0)
        btn_4.place(x=430, y=0)
        btn_5.place(x = 0, y = 0)
        btn_6.place(x=740, y=0)


class FormRestart(ttk.Frame):
    '''
    Временный фрейм, содержащий кнопку обновления
    '''
    def __init__(self, parent):
        super().__init__(parent)
        btn_submit = ttk.Button(self, text="Сбросить", command=parent.refresh)
        btn_submit.grid()


class View_DB_Tables(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.name_db = ''
        self.name_tbl = []
        self.name_col = []
        self.collumn = []
        self.lst = []
        self.place_page = tk.Frame(self, width=parent.width, height=parent.height)
        lbl_check_db = tk.Label(self.place_page, text='Выберите для подключения: БД')
        self.combobox_db = ttk.Combobox(self.place_page, state="readonly", values=os.listdir(f'{os.getcwd()}/{self.parent.name_DB_Direct}'))
        btn_db = ttk.Button(self.place_page, text="Подключиться к БД", command=self.connect_db)
        lbl_check_tbl = tk.Label(self.place_page, text='Таблицу')
        self.combobox_tbl = ttk.Combobox(self.place_page, state="readonly", values=self.name_tbl)
        btn_tbl = ttk.Button(self.place_page, text="Показать результат", command=self.show_text)
        self.view_table()
        lbl_check_db.place(x=10, y=0)
        self.combobox_db.place(x=245, y=0)
        btn_db.place(x=450, y=0)
        lbl_check_tbl.place(x=180, y=35)
        self.combobox_tbl.place(x=245, y=35)
        btn_tbl.place(x=450, y=35)
        self.place_page.grid()

    def view_table(self):
        self.table = ttk.Treeview(self.place_page, show='headings')  # по умолчанию в show = 'tree headings'
        self.table['columns'] = self.collumn
        for header in self.collumn:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center', width = 20)
        for row in self.lst:
            self.table.insert('', tk.END, values=row)
        self.scroll_panel = ttk.Scrollbar(self.place_page, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscrollcommand=self.scroll_panel.set)
        self.scroll_panel.place(x=850, y=70, height=490)
        self.table.place(x=0, y=70, width=850, height=490)

    def connect_db(self):
        if self.combobox_db.get():
            self.name_db = self.combobox_db.get()
            self.name_tbl = []
            self.name_col = []
            text = SQL.pullNamesFromTable(f'{self.parent.name_DB_Direct}/{self.combobox_db.get()}')
            self.flag = True
            for i in text:
                if i[0] == 'table':
                    if i[1] == 'sqlite_sequence':
                        continue
                    self.name_tbl.append(i[1])
                    self.name_col.append(i[4].split('(')[1][:-1].split(', '))
            self.combobox_tbl.destroy()
            self.combobox_tbl = ttk.Combobox(self.place_page, state="readonly", values=self.name_tbl)
            self.combobox_tbl.place(x=245, y=35)

    def show_text(self):
        self.collumn = self.run_the_command()
        self.lst = SQL.pullCommandSQL(f'SELECT * FROM {self.combobox_tbl.get()}',
                                  f'{self.parent.name_DB_Direct}/{self.combobox_db.get()}')
        self.table.destroy()
        self.scroll_panel.destroy()
        self.view_table()

    def run_the_command(self):
        if self.name_db == self.combobox_db.get():
            if self.combobox_tbl.get():
                text = self.create_name_col()
                return text

    def create_name_col(self):
        for i in range(len(self.name_tbl)):
            if self.name_tbl[i] == self.combobox_tbl.get():
                text = []
                for j in self.name_col[i]:
                    text.append(j.split(' ')[0])
                text = [i.lstrip() for i in text]
                return text


class Start_Page(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.name_db = ''
        self.name_tbl = []
        self.name_col = []
        self.place_page = tk.Frame(self, width = parent.width, height = parent.height)
        lbl_name_page = tk.Label(self.place_page, text='Обзорная страница для просмотра содержимого таблиц.')
        lbl_check_db = tk.Label(self.place_page, text='Выберите для подключения: БД')
        self.combobox_db = ttk.Combobox(self.place_page, state="readonly", values=os.listdir(f'{os.getcwd()}/{self.parent.name_DB_Direct}'))
        btn_db = ttk.Button(self.place_page, text="Подключиться к БД", command=self.connect_db)
        lbl_check_tbl = tk.Label(self.place_page, text='Таблицу')
        self.combobox_tbl = ttk.Combobox(self.place_page, state="readonly", values=self.name_tbl)
        btn_tbl = ttk.Button(self.place_page, text="Показать результат", command=self.show_text)
        self.answer = tk.Text(self.place_page, state=tk.DISABLED)
        self.scroll_pane = ttk.Scrollbar(self.place_page, command=self.answer.yview)
        lbl_name_page.place(x=10, y=5)
        lbl_check_db.place(x=10, y=35)
        self.combobox_db.place(x=245, y=35)
        lbl_check_tbl.place(x=10, y=70)
        btn_db.place(x=450, y=30)
        self.combobox_tbl.place(x=80, y=70)
        btn_tbl.place(x=285, y=67)
        self.answer.place(x=10, y=100, width=700, height=490)
        self.scroll_pane.place(x=710, y=100, height=490)
        self.place_page.grid()
        self.flag = False

    def show_text(self):
        self.result = self.run_the_command()
        if self.result:
            self.answer.destroy()
            self.scroll_pane.destroy()
            self.answer = tk.Text(self.place_page, state=tk.NORMAL)
            self.answer.place(x=10, y=100, width=700, height=490)
            self.answer.insert(tk.END, self.result)
            text = SQL.pullCommandSQL(f'SELECT * FROM {self.combobox_tbl.get()}', f'{self.parent.name_DB_Direct}/{self.combobox_db.get()}')
            for i in text:
                self.answer.insert(tk.END, i)
                self.answer.insert(tk.END, '\n')
            self.answer.insert(tk.END, '='*50)
            self.answer.insert(tk.END, '\n')
            self.scroll_pane = ttk.Scrollbar(self.place_page, command=self.answer.yview)
            self.answer.configure(state=tk.DISABLED, yscrollcommand=self.scroll_pane.set)
            self.scroll_pane.place(x=710, y=100, height=490)

    def connect_db(self):
        if self.combobox_db.get():
            self.name_db = self.combobox_db.get()
            self.name_tbl = []
            self.name_col = []
            text = SQL.pullNamesFromTable(f'{self.parent.name_DB_Direct}/{self.combobox_db.get()}')
            self.flag = True
            for i in text:
                if i[0] == 'table':
                    if i[1] == 'sqlite_sequence':
                        continue
                    self.name_tbl.append(i[1])
                    self.name_col.append(i[4].split('(')[1][:-1].split(', '))
            self.combobox_tbl.destroy()
            self.combobox_tbl = ttk.Combobox(self.place_page, state="readonly", values=self.name_tbl)
            self.combobox_tbl.place(x=80, y=70)

    def create_name_col(self):
        for i in range(len(self.name_tbl)):
            if self.name_tbl[i] == self.combobox_tbl.get():
                text = ''
                for j in self.name_col[i]:
                    text += j.split(' ')[0] + '\t'
                text = text.split('\n')
                text = ''.join(text)
                return text + '\n' + '-'*50 + '\n'
        return ''

    def run_the_command(self):
        if self.name_db == self.combobox_db.get():
            if self.combobox_tbl.get():
                text = self.create_name_col()
                return text


class Create_DB_Tables(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.face = ''
        self.place_page = tk.Frame(self, width = parent.width, height = parent.height)
        lbl = tk.Label(self.place_page, text='Страница для создания баз данных и таблиц')
        btn_bd = ttk.Button(self.place_page, text="База данных", command=self.create_db)
        btn_tbl = ttk.Button(self.place_page, text="Таблица", command=self.create_tbl)
        btn_create = ttk.Button(self.place_page, text="Создать", command=self.create)
        lbl.place(x=10, y=5)
        btn_bd.place(x = 10, y = 40)
        btn_tbl.place(x=10, y=70)
        btn_create.place(x=700, y=40)
        self.place_page.grid()

    def create_db(self):
        if self.face == 'Table':
            self.change_place.destroy()
        self.face = 'Base'
        self.change_place = tk.Frame(self.place_page, width=850, height=480)
        self.name_db = tk.Entry(self.change_place, justify=tk.CENTER)
        self.lbl = tk.Label(self.change_place, text='')
        self.name_db.place(x=250, y=0)
        self.lbl.place(x=250, y=50)
        self.change_place.place(x=10, y=100)

    def creater_db_sql(self):
        self.lbl.destroy()
        db = self.name_db.get()
        if db:
            if db.isalnum():
                db += '.db'
                if not os.path.exists(f'{self.parent.name_DB_Direct}/{db}'):
                    SQL.createrDB(f'{self.parent.name_DB_Direct}/{db}')
                    self.lbl = tk.Label(self.change_place, text='База Данных создана!')
                else:
                    self.lbl = tk.Label(self.change_place, text = 'Такая БД уже существует')
            else:
                self.lbl = tk.Label(self.change_place, text='Имя базы должно состоять из букв и(или) цифр')
        else:
            self.lbl = tk.Label(self.change_place, text='Укажите имя БД')
        self.lbl.place(x = 250, y = 50)

    def create_tbl(self):
        if self.face == 'Base':
            self.change_place.destroy()
        self.col_type = ['INTEGER', 'TEXT', 'DATE']
        self.col_key = ['PRIMARY KEY', '']
        self.col_autoin = ['AUTOINCREMENT', '']
        self.col_null = ['NOT NULL', '']
        self.face = 'Table'
        self.create_tbl_zone()

    def create_tbl_zone(self):
        self.all_comboboxes = []
        self.num_line = 0
        selecting_db = self.parent.give_all_DB()
        self.change_place = tk.Frame(self.place_page, width=850, height=480)
        self.lbl_name_change_db = tk.Label(self.change_place, text='Выберите БД')
        self.combobox_tbl_zone = ttk.Combobox(self.change_place, state="readonly", values=selecting_db, width=10)
        self.lbl_name_tbl = tk.Label(self.change_place, text='Название таблицы')
        self.name_tbl = tk.Entry(self.change_place, justify=tk.LEFT, width=10)
        self.lbl_tbl_inf_error = tk.Label(self.change_place, text='')
        self.combobox_tbl_zone.place(x = 110, y = 0)
        self.lbl_name_change_db.place(x = 10, y = 0)
        self.lbl_name_tbl.place(x = 230, y = 0)
        self.name_tbl.place(x = 370, y = 0)
        self.lbl_tbl_inf_error.place(x=500, y=0)
        self.add_col()
        self.change_place.place(x=10, y=100)

    def add_col(self):
        if self.num_line > 0:
            self.btn_add.destroy()
        self.btn_add = ttk.Button(self.change_place, text='Добавить колонку', command=self.add_col)
        entry = tk.Entry(self.change_place, justify=tk.LEFT, width=10)
        combobox_1 = ttk.Combobox(self.change_place, state="readonly", values=self.col_type, width=10)
        combobox_2 = ttk.Combobox(self.change_place, state="readonly", values=self.col_key, width=10)
        combobox_3 = ttk.Combobox(self.change_place, state="readonly", values=self.col_autoin, width=13)
        combobox_4 = ttk.Combobox(self.change_place, state="readonly", values=self.col_null, width=10)
        self.btn_add.place(x=0, y=self.num_line * 35 + 70)
        entry.place(x =0, y = self.num_line * 35 + 35)
        combobox_1.place(x = 110, y = self.num_line * 35 + 35)
        combobox_2.place(x=225, y=self.num_line * 35 + 35)
        combobox_3.place(x=340, y=self.num_line * 35 + 35)
        combobox_4.place(x=480, y=self.num_line * 35 + 35)
        self.all_comboboxes.append((entry, combobox_1, combobox_2, combobox_3, combobox_4))
        self.num_line += 1

    def create(self):
        command = ''
        if self.face == 'Base':
            print(self.face)
            self.creater_db_sql()
        elif self.face == 'Table':
            self.lbl_tbl_inf_error.destroy()
            name_table = self.name_tbl.get().title()
            if not self.combobox_tbl_zone.get():
                self.create_lbl_error('Необходимо выбрать базу данных')
                return
            if not name_table:
                self.create_lbl_error('Отсутствует название таблицы')
                return
            if not name_table.isalnum():
                self.create_lbl_error('Имя таблицы дожно сотоять из букв и(или) цифр')
                return
            text = SQL.pullNamesFromTable(f'{self.parent.name_DB_Direct}/{self.combobox_tbl_zone.get()}')
            names_tbl = []
            for i in text:
                if i[0] == 'table':
                    names_tbl.append(i[1])
            if name_table in names_tbl:
                self.create_lbl_error('Такая таблица уже существует')
                return
            command += f'CREATE TABLE IF NOT EXISTS {name_table} ('
            for i in self.all_comboboxes:
                if i[0].get() == '' or i[1].get() == '':
                    self.create_lbl_error('2-е первых колонки обязательны к заполнению')
                    return
                if not i[0].get().isalnum():
                    self.create_lbl_error('Название 1-й колонки должно состоять из букв и(или) цифр')
                    return
                if i != self.all_comboboxes[0]:
                    command += ', '
                command += f'\n{i[0].get()} {i[1].get()} {i[2].get()} {i[3].get()} {i[4].get()}'
            command += ');'
            print(f'{self.parent.name_DB_Direct}/{self.combobox_tbl_zone.get()}')
            try:
                SQL.pushOneCommandSQL(command, f'{self.parent.name_DB_Direct}/{self.combobox_tbl_zone.get()}')
            except:
                self.create_lbl_error(sys.exc_info()[:2])
            self.all_comboboxes = []
            self.change_place.destroy()
            self.create_tbl_zone()
        else:
            pass

    def create_lbl_error(self, text):
        self.lbl_tbl_inf_error = tk.Label(self.change_place, text=text)
        self.lbl_tbl_inf_error.place(x=500, y=0)


class SQL_ask(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.place_page = tk.Frame(self, width = parent.width, height = parent.height)
        lbl = tk.Label(self.place_page, text='Страница для работы с SQL запросами.       Выберите БД для подключения')
        self.combobox = ttk.Combobox(self.place_page, state="readonly", values=os.listdir(f'{os.getcwd()}/{self.parent.name_DB_Direct}'))
        self.sql_command = tk.Text(self.place_page)
        btn = ttk.Button(self.place_page, text="Выполнить запрос", command=self.show_text)
        self.restart_answer()
        lbl.place(x = 10, y = 5)
        self.combobox.place(x = 550, y = 5)
        self.sql_command.place(x = 10, y = 35, width = 700, height = 120)
        btn.place(x = 730, y = 35)
        self.place_page.grid()

    def show_text(self):
        self.result = self.run_the_command()
        self.answer.configure(state=tk.NORMAL)
        for i in self.result:
            self.answer.insert(tk.END, i)
            self.answer.insert(tk.END, '\n')
        self.answer.configure(state=tk.DISABLED)

    def run_the_command(self):
        if self.combobox.get():
            if self.sql_command.get('1.0', tk.END):
                self.scroll_pane.destroy()
                self.answer.destroy()
                self.restart_answer()
                try :
                    text = SQL.pullCommandSQL(self.sql_command.get('1.0', tk.END), f'{self.parent.name_DB_Direct}/{self.combobox.get()}')
                    return text or ['Пустое значение']
                except SQL.sqlite3.OperationalError:
                    return ['Ошибка - OperationalError']
                except:
                    return ['ОШИБКА новая', sys.exc_info()[:2]]
            return ''
        return ['ОШИБКА - не выбрана база данных']

    def restart_answer(self):
        self.answer = tk.Text(self.place_page, state=tk.DISABLED)
        self.scroll_pane = ttk.Scrollbar(self.place_page, command=self.answer.yview)
        self.answer['yscrollcommand'] = self.scroll_pane.set
        self.answer.place(x=10, y=170, width=700, height=420)
        self.scroll_pane.place(x=710, y=170, height=420)


class EXEC_COM(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.place_page = tk.Frame(self, width=parent.width, height=parent.height)
        lbl = tk.Label(self.place_page, text='Страница для программной обработки файлов.')
        btn_run = ttk.Button(self.place_page, text="Запустить фрагмент кода", command=self.command_exec)
        btn_give = ttk.Button(self.place_page, text="Загрузить", command=self.give_code)
        btn_save = ttk.Button(self.place_page, text="Сохранить", command=self.save_code)
        self.answer = tk.Text(self.place_page)
        scroll_panel = ttk.Scrollbar(self.place_page, command=self.answer.yview)
        self.answer['yscrollcommand'] = scroll_panel.set
        self.answer.place(x=10, y=70, width=700, height=500)
        lbl.place(x=10, y=5)
        btn_run.place(x=10, y=35)
        btn_give.place(x=310, y=35)
        btn_save.place(x=410, y=35)
        scroll_panel.place(x=710, y=70, height=500)
        self.place_page.grid()

    def command_exec(self):
        try:
            exec(self.answer.get('1.0', tk.END))
        except:
            self.inf_win = InfWin('My error' + str(sys.exc_info()[0]))

    def give_code(self):
        with open('SAVE.txt', 'r', encoding='utf-8') as file:
            self.answer.destroy()
            self.answer = tk.Text(self.place_page)
            self.answer.place(x=10, y=70, width=700, height=500)
            text = file.read()
            self.answer.insert('1.0', text[:-1])

    def save_code(self):
        with open('SAVE.txt', 'w', encoding='utf-8') as file:
            file.write(self.answer.get('1.0', tk.END))
            self.inf_win = InfWin('Информация сохранена')
            if self.parent.time_window:
                for i in self.parent.time_window:
                    i.destroy()
                self.parent.time_window = []
            self.parent.time_window.append(self.inf_win)


class InfWin(tk.Toplevel):
    def __init__(self, text):
        super().__init__()
        text = text
        lbl = tk.Label(self, text=text)
        self.title('Информация')
        btn = ttk.Button(self, text="Ok", command=self.destroy)
        lbl.pack()
        btn.pack()
        self.geometry('300x50+200+100')
        self.maxsize(300, 50)


class AddfWin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title('Добавить данные')
        lbl = tk.Label(self, text="Выберите БД для подключения")
        self.combobox = ttk.Combobox(self, state="readonly", values=os.listdir(f'{os.getcwd()}/{self.parent.name_DB_Direct}'))
        self.text_sql = tk.Text(self)
        btn_create = ttk.Button(self, text="Добавить", command=self.command_sql)
        btn_close = ttk.Button(self, text="Закрыть", command=self.destroy)
        lbl.place(x=20, y=10)
        self.combobox.place(x=250, y=10)
        self.text_sql.place(x=10, y=40, width=480, height=290)
        btn_create.place(x=10, y=350)
        btn_close.place(x=400, y=350)
        self.geometry('500x400+200+100')
        self.maxsize(500, 400)

    def command_sql(self):
        try:
            SQL.pushOneCommandSQL(self.text_sql.get('1.0', tk.END), f'{self.parent.name_DB_Direct}/{self.combobox.get()}')
        except:
            self.inf_win = InfWin(sys.exc_info()[0])
            if self.parent.time_window:
                for i in self.parent.time_window:
                    i.destroy()
                self.parent.time_window = []
            self.parent.time_window.append(self.inf_win)


app = App().mainloop()

