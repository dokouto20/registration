import sqlite3
from tkinter import *
import re
from textwrap import wrap
from datetime import date

#c.execute("CREATE TABLE people (name text,lastname text, email text, phone_number text, perosnal_number text)") /create
#c.execute("INSERT INTO people VALUES ('tomas','dokoupil','idk@sad.com','888999777','041125/5338')") /insert
#c.execute("SELECT * FROM people") / select
#print(c.fetchall())


#connection = sqlite3.connect('database.db')
#c = connection.cursor()
#connection.commit()
#connection.close()

def check_name(valname,err):
    if valname != "OK" or valname != "ERROR":
        if valname:
            status = 0
            for char in valname:
                val = char.isdigit()
                if val == True:
                    status = 1
                else:
                    pass
            if status == 0:
                err[0] = 1
            else:
                err[0] = 0
        else:
            err[0] = 0
    else:
        err[0] = 0

def check_lasname(vallastname,err):
    if vallastname != "OK" or vallastname != "ERROR":
        if vallastname:
            status = 0

            for char in vallastname:
                val = char.isdigit()
                if val == True:
                    status = 1
                else:
                    pass

            if status == 0:
                err[1] = 1
            else:
                err[1] = 0
        else:
            err[1] = 0
    else:
        err[1] = 0

def check_email(valemail,err):
    pattern = '^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$'

    if re.search(pattern, valemail):
        err[2] = 1
    else:
        err[2] = 0

def check_phone(valphone,err):
    status = 0
    lenght = len(valphone)
    if lenght == 9:
        for char in valphone:
            val = char.isdigit()
            if val == True:
                pass
            else:
                status = 1

        if status == 0:
            err[3] = 1
        else:
            err[3] = 0
    else:
        err[3] = 0

def check_persid(valpersid,err):
    #split and chcek brirth date
    if valpersid != "OK" or valpersid != "ERROR":
        if valpersid:
            splited = valpersid.split("/")
            sp1val = splited[0]
            n = 2
            sp1 = [sp1val[i:i + n] for i in range(0, len(sp1val), n)]
            year = "20"
            month = None
            day = None
            if sp1[0] != "ER":
                year = year+sp1[0]
            if sp1[1] != "RO":
                month = sp1[1]
                if int(month) > 12:
                    month - 50
            if sp1[2] != "R":
                day = sp1[2]
            current_year = date.today().year
            if year and month and day:
                if int(year) > current_year:
                    err[4] = 0
                else:
                    if int(month) > 12:
                        err[4] = 0
                    else:
                        if int(day) > 31:
                            err[4] = 0
                        else:
                            err[4] = 1
            else:
                err[4] = 0
        else:
            err[4] = 0
    else:
        err[4] = 0

def getvals():
    err = [0,0,0,0,0]
    valname = name_entry.get()
    check_name(valname,err)
    vallastname = lastname_entry.get()
    check_lasname(vallastname,err)
    valemail = email_entry.get()
    check_email(valemail,err)
    valphone = phone_number_entry.get()
    check_phone(valphone,err)
    valpersid = personal_id_entry.get()
    check_persid(valpersid,err)

    num = 0
    status = 0
    for i in err:
        print(i)
        num += 1
        if i == 0:
            if num == 1:
                name_entry.delete(0, END)
                name_entry.insert(0, "ERROR")
            elif num == 2:
                lastname_entry.delete(0, END)
                lastname_entry.insert(0, "ERROR")
            elif num == 3:
                email_entry.delete(0, END)
                email_entry.insert(0, "ERROR")
            elif num == 4:
                phone_number_entry.delete(0, END)
                phone_number_entry.insert(0, "ERROR")
            elif num == 5:
                personal_id_entry.delete(0, END)
                personal_id_entry.insert(0, "ERROR")
        else:
            status += 1

    if status == 5:
        print("insert")







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


