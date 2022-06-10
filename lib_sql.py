import sqlite3


def createrDB(name_db = None):
    '''
    Данная функция создает БД (если ее не было) и подключается к ней
    '''
    if not name_db:
        name_db = input("Укажите имя БД(расширение .db - не указывать): ") + ".db"
    else:
        name_db = name_db
    connect = sqlite3.connect(name_db)  # создает БД если ее не было и подключается к ней
    return connect


def pullCommandSQL(text_order, name_db = None):
    '''
    Данная функция создает запросы SQL
    '''
    print(text_order)
    connect = createrDB(name_db)  # подключаемся к БД
    cursor = connect.cursor()
    cursor.execute(text_order)
    answer = cursor.fetchall()
    return answer


def pullNamesFromTable(name_db = None):
    '''
    Данная функция получает в качестве ответа SQL комманды, с помощью которых создавались таблицы.
    В данных коммандах есть вся информация о названиях столбцов и типах данных.
    '''
    connect = createrDB(name_db)  # подключаемся к БД
    cursor = connect.cursor()
    text_order = '''SELECT * FROM sqlite_master'''
    cursor.execute(text_order)
    result = cursor.fetchall()
    return result

def pushOneCommandSQL(text, name_db = None):
    '''
    Данная функция выполняет команду SQL (создание/удаление объектов)
    '''
    connect = createrDB(name_db)  # подключаемся к БД
    cursor = connect.cursor()
    text_order = text
    cursor.execute(text_order)
    connect.commit()


def createrTable_easy(name_db = None):
    '''
    Данная функция создает новую таблицу, без команд SQL
    '''
    connect = createrDB(name_db)#подключаемся к БД
    cursor = connect.cursor()
    text_order = '''CREATE TABLE IF NOT EXISTS ''' + input('Введите название таблицы: ') + ' ('
    inf_column = ['Имя колонки: ', 'Тип данных: ', 'PRIMARY KEY(Y/N): ']
    big_flag = True
    while big_flag:
        my_text = ""
        for i in range(3):
            text = input(inf_column[i])
            if i == 2 and (text == 'Y' or text == 'y'):
                my_text += ' PRIMARY KEY'
            elif i == 2 and (text == 'N' or text == 'n'):
                pass
            else:
                my_text += ' ' + text
        while True:
            flag = input('Таблица готова? (Y/N): ')
            if flag in 'Yy':
                text_order += my_text + ');'
                big_flag = False
                break
            elif flag in 'Nn':
                text_order += my_text + ','
                break
            else:
                print('Введите корректный ответ.')
    print(text_order)
    cursor.execute(text_order)
    connect.commit()


def pushManyCommandSQL(my_list_tuple, name_db = None):
    '''
    Данная функция выполняет команду SQL (множественное присвоение).
    В качестве аргумента принимает список кортежей
    cursor.executemany("INSERT INTO users VALUES(?, ?, ?, ?);", my_list_tuple)
    '''
    connect = createrDB(name_db)  # подключаемся к БД
    cursor = connect.cursor()
    text_order = input('''Введите команду SQL (множественное присвоение):\n''')
    print(text_order)
    cursor.executemany(text_order, my_list_tuple)
    connect.commit()


def pullTables(name_db = None):
    '''
    Данная функция получает названия таблиц в конкретной БД
    '''
    connect = createrDB(name_db)  # подключаемся к БД
    cursor = connect.cursor()
    text_order = '''SELECT name from sqlite_master where type= "table"'''
    cursor.execute(text_order)
    print(f'В базе данных содержатся следующие таблицы: {cursor.fetchall()}')



