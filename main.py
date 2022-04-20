import sqlite3
from tkinter import *
import re

#c.execute("CREATE TABLE people (name text,lastname text, email text, phone_number text, perosnal_number text)") /create
#c.execute("INSERT INTO people VALUES ('tomas','dokoupil','idk@sad.com','888999777','041125/5338')") /insert
#c.execute("SELECT * FROM people") / select
#print(c.fetchall())


#connection = sqlite3.connect('database.db')
#c = connection.cursor()
#connection.commit()
#connection.close()



def check_name(valname):
    status = 0
    for char in valname:
        val = char.isdigit()
        if val == True:
            status = 1
        else:
            pass
    if status == 0:
        name_entry.delete(0, END)
        name_entry.insert(0, "SUCCES")
    else:
        name_entry.delete(0, END)
        name_entry.insert(0, "ERROR")

def check_lasname(vallastname):
    status = 0

    for char in vallastname:
        val = char.isdigit()
        if val == True:
            status = 1
        else:
            pass

    if status == 0:
        lastname_entry.delete(0, END)
        lastname_entry.insert(0, "SUCCES")
    else:
        lastname_entry.delete(0, END)
        lastname_entry.insert(0, "ERROR")

def check_email(valemail):
    pattern = '^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$'

    if re.search(pattern, valemail):
        email_entry.delete(0, END)
        email_entry.insert(0, "SUCCES")
    else:
        email_entry.delete(0, END)
        email_entry.insert(0, "ERROR")

def check_phone(valphone):
    status = 0
    lenght = len(valphone)
    print(lenght)
    if lenght == 9:
        for char in valphone:
            val = char.isdigit()
            if val == True:
                pass
            else:
                status = 1

        if status == 0:
            phone_number_entry.delete(0, END)
            phone_number_entry.insert(0, "SUCCES")
        else:
            phone_number_entry.delete(0, END)
            phone_number_entry.insert(0, "ERROR")
    else:
        phone_number_entry.delete(0, END)
        phone_number_entry.insert(0, "ERROR")

def check_persid(valpersid):
    #split and chcek brirth date
    if valpersid:
        personal_id_entry.delete(0, END)
        personal_id_entry.insert(0, "SUCCES")
    else:
        personal_id_entry.delete(0, END)
        personal_id_entry.insert(0, "ERROR")


def getvals():
    valname = name_entry.get()
    check_name(valname)
    vallastname = lastname_entry.get()
    check_lasname(vallastname)
    valemail = email_entry.get()
    check_email(valemail)
    valphone = phone_number_entry.get()
    check_phone(valphone)
    valpersid = personal_id_entry.get()
    check_persid(valpersid)



tk = Tk()
tk.geometry("295x200")
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


