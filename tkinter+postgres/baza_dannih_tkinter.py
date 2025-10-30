import tkinter as tk
from tkinter import messagebox
import psycopg2  

try:
    connection = psycopg2.connect(
        dbname='postgres', user='postgres', password='1111', host='localhost', port="5432"
    )
    cursor = connection.cursor()
except:
    print('Ошибка при подкчении')
    exit()

try:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            city TEXT,
            email TEXT,
            age INTEGER,
            address TEXT
        )
    ''')
    connection.commit()
except:
    print('Не получилось создать базу')

main_window = tk.Tk()
main_window.title('управление пользователями')

name_entry = tk.Entry(main_window, width=20)
name_entry.insert(0, 'Имя')  
name_entry.grid(row=0, column=0)

surname_entry = tk.Entry(main_window, width=20)
surname_entry.insert(0, 'Фамилия')
surname_entry.grid(row=0, column=1)

phone_entry = tk.Entry(main_window, width=20)
phone_entry.insert(0, 'Телефон')
phone_entry.grid(row=0, column=2)

city_entry = tk.Entry(main_window, width=20)
city_entry.insert(0, 'Город')
city_entry.grid(row=0, column=3)

email_entry = tk.Entry(main_window, width=20)
email_entry.insert(0, 'Email')
email_entry.grid(row=1, column=0)

age_entry = tk.Entry(main_window, width=20)
age_entry.insert(0, 'Возраст')
age_entry.grid(row=1, column=1)

addr_entry = tk.Entry(main_window, width=20)
addr_entry.insert(0, 'Адрес')
addr_entry.grid(row=1, column=2)

def add_user():
    fn = name_entry.get()
    ln = surname_entry.get()
    ph = phone_entry.get()
    c = city_entry.get()
    em = email_entry.get()
    ag = age_entry.get()
    ad = addr_entry.get()

    try:
        ag_int = int(ag)
    except ValueError:
        ag_int = None  

    try:
        cursor.execute(
            'INSERT INTO users (first_name,last_name,phone,city,email,age,address) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (fn, ln, ph, c, em, ag_int, ad)
        )
        connection.commit()
        messagebox.showinfo('Успешно', 'Добавлено')
    except Exception as e:
        messagebox.showerror('Ошибка', f'Что-то пошло не так: {e}')


add_button = tk.Button(main_window, text='Добавить', command=add_user)
add_button.grid(row=2, column=0, columnspan=4, pady=10)

query_field = tk.Entry(main_window, width=50)
query_field.grid(row=3, column=0, columnspan=4)

def do_query():
    q = query_field.get()
    try:
        cursor.execute(q)
        res = cursor.fetchall()
        results_text.delete(1.0, tk.END)
        for r in res:
            results_text.insert(tk.END, str(r) + '\n')
    except:
        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, 'Что-то не так с запросом...')

exec_button = tk.Button(main_window, text='Выполнить', command=do_query)
exec_button.grid(row=4, column=0, columnspan=4)

results_text = tk.Text(main_window, width=60, height=10)
results_text.grid(row=5, column=0, columnspan=4)

del_entry = tk.Entry(main_window, width=20)
del_entry.insert(0, 'ID')
del_entry.grid(row=6, column=0)

def delete_user():
    user_id = del_entry.get()
    try:
        cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
        connection.commit()
        messagebox.showinfo('Удалено', "Участник удален")
    except:
        messagebox.showerror('Ошибка', 'Проблемы с удалением')

del_button = tk.Button(main_window, text='Удалить', command=delete_user)
del_button.grid(row=6, column=1)

main_window.mainloop()

connection.close()
