import sqlite3
from tkinter import *

#c.execute("CREATE TABLE people (name text,lastname text, email text, phone_number text, perosnal_number text)") /create
#c.execute("INSERT INTO people VALUES ('tomas','dokoupil','idk@sad.com','888999777','041125/5338')") /insert
#c.execute("SELECT * FROM people") / select
#print(c.fetchall())


#connection = sqlite3.connect('database.db')
#c = connection.cursor()
#connection.commit()
#connection.close()

def getvals():
    print('jdeto')


tk = Tk()
tk.geometry("270x200")
tk.resizable(False, False)

Label(tk, text='registration', font='ar 15 bold').grid(row=0, column=3)

name = Label(tk, text='name')
lastname = Label(tk, text='lastname')
email = Label(tk, text='email')
phone_number = Label(tk, text='phone number')
presonal_id = Label(tk, text='personal id')

name.grid(row=1 ,column=2)
lastname.grid(row=2 ,column=2)
email.grid(row=3 ,column=2)
phone_number.grid(row=4 ,column=2)
presonal_id.grid(row=5 ,column=2)

name_value = StringVar
lastname_value = StringVar
email_value = StringVar
phone_number_value = StringVar
personal_id_value = StringVar

name_entry = Entry(tk, textvariable= name_value)
lastname_entry = Entry(tk, textvariable= lastname_value)
email_entry = Entry(tk, textvariable= email_value)
phone_number_entry = Entry(tk, textvariable= phone_number_value)
personal_id_entry = Entry(tk, textvariable= personal_id_value)

name_entry.grid(row=1, column=3)
lastname_entry.grid(row=2, column=3)
email_entry.grid(row=3, column=3)
phone_number_entry.grid(row=4, column=3)
personal_id_entry.grid(row=5, column=3)

Button(text="submit", command=getvals).grid(row=7, column=3)

tk.mainloop()


