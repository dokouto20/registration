from cgi import print_form
import sqlite3
from tkinter import *
from tkinter import ttk
import re
from textwrap import wrap
from datetime import date
from tkinter.messagebox import YESNOCANCEL
from turtle import delay, width
from functools import partial
import os


#c.executescript("""
#REATE TABLE people(
#    id INTEGER PRIMARY KEY,
#    name VARCHAR(500),
#    lastname VARCHAR(500),
#    email VARCHAR(500),
#    phone_number VARCHAR(500),
#    personal_number VARCHAR(500)
#
#);
#""")


# check if in name doesnt have num or spec char 
def check_name(valname,err):
    if valname != "OK" or valname != "ERROR":
        if valname:
            status = 0
            for char in valname:
                val = char.isdigit()
                valalpha = char.isalpha()
                if val == True or valalpha == False:
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

# check if in lastname doesnt have num or spec char 
def check_lasname(vallastname,err):
    if vallastname != "OK" or vallastname != "ERROR":
        if vallastname:
            status = 0

            for char in vallastname:
                val = char.isdigit()
                valalpha = char.isalpha()
                if val == True or valalpha == False:
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

#check if email is legit 
def check_email(valemail,err):
    pattern = '^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$'

    if re.search(pattern, valemail):
        err[2] = 1
    else:
        err[2] = 0

#check if num is real
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

#check personal id 
def check_persid(valpersid,err):
    #split and chcek brirth date
    if valpersid != "OK" or valpersid != "ERROR":
        lenght = len(valpersid)
        #pers id has 10 num and /
        if valpersid and lenght == 11:
            p = 0
            for i in valpersid:
                if i.isdigit():
                    p = 0
                else:
                    p = 1
            if p == 0:
                #split pers id 
                splited = valpersid.split("/")
                sp1val = splited[0]
                n = 2
                sp1 = [sp1val[i:i + n] for i in range(0, len(sp1val), n)]
                print(sp1)
                # isolate year month and day 
                year = "20"+sp1[0]
                month = sp1[1]
                #womens has +50 on their birth month
                if int(month) > 12:
                    month = int(month) - 50
                day = sp1[2]
                current_year = date.today().year
                #check if date can exist 
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

#get vals form entry and check it 
def getvals(tk, name_entry, lastname_entry, email_entry, phone_number_entry, personal_id_entry):
    # err list 
    err = [0,0,0,0,0]
    # val check 
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
    #delete text areas if everthing is ok 
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
        # inset into database 
        connection = sqlite3.connect('database.db')
        c = connection.cursor()
        c.execute("INSERT INTO people (name, lastname, email, phone_number, personal_number) VALUES (?,?,?,?,?)", (valname,vallastname,valemail,valphone,valpersid,))
        name_entry.delete(0, END)
        lastname_entry.delete(0, END)
        email_entry.delete(0, END)
        phone_number_entry.delete(0, END)
        personal_id_entry.delete(0, END)
        connection.commit()
        connection.close()
        #alert window 
        alert = Toplevel(tk)
        alert.geometry("295x220")
        alert.title("alert")
        Label(alert, text='regisrace uspesna', font='ar 15 bold').grid(row=0, column=3)
        Button(alert, text="přejit na prehled", command= lambda: alertfnc(alert, tk)).grid(row=3, column=3)

#redirect to prehled 
def alertfnc(alert, tk):
    alert.after(3000,lambda:alert.destroy())
    overview(tk)

# print frame
def print_frame(top):

    global mainframe
    mainframe = Frame(top)
    mainframe.pack(fill=BOTH, expand=1)

    mycanvas = Canvas(mainframe)
    mycanvas.pack(side=LEFT, fill=BOTH, expand=1 )

    myscrollbar = ttk.Scrollbar(mainframe, orient=VERTICAL, comman=mycanvas.yview)
    myscrollbar.pack(side=RIGHT, fill=Y)

    mycanvas.configure(yscrollcommand=myscrollbar.set)
    mycanvas.bind('<Configure>', lambda e:mycanvas.configure(scrollregion=mycanvas.bbox('all')))

    secondframe = Frame(mycanvas)
    mycanvas.create_window((0,0), window=secondframe, anchor="nw")

    connection = sqlite3.connect('database.db')
    c = connection.cursor()
    c.execute("SELECT * FROM people")
    result = c.fetchall()

    lenght = range(len(result))
    j = 4
    delY = 60
    ediY = 20

    for i in lenght:

        Textarea = Text(secondframe, width=70, height=5,)
        Textarea.grid(row=j,column=0,padx=10,pady=10)
        Textarea.insert(END, "\n" +"name: "+result[i][1]+" lastname: "+result[i][2])
        Textarea.insert(END, "\n" +"email: "+result[i][3]+" phone num: "+result[i][4])
        Textarea.insert(END, "\n" +"personal id: "+result[i][5])
        Textarea.configure(state='disabled')

        edit = Button(secondframe, text="  edit  ", command=editfnc(tk)).place(x=520,y=ediY)
        function = partial(delete, id=result[i][0])
        deletebutton = Button(secondframe, text="delete", command=function)
        deletebutton.place(x=520,y=delY)

        delY += 104
        ediY += 104
        j += 1

    connection.commit()
    connection.close()

#delete from database
def delete(id):
    valid = id 
    print(valid)
    connection = sqlite3.connect('database.db')
    c = connection.cursor()
    c.execute("DELETE FROM people WHERE id = :id", {'id': valid})
    connection.commit()
    connection.close()
    mainframe.destroy()
    print_frame(top)

#prehled 
def overview(tk):
    global top
    top = Tk()
    top.geometry("600x600")
    top.title("prehled")
    top.resizable(False, False)

    print_frame(top)

    top.mainloop()

def editfnc(tk):
    print("upravit veme id = otevre okno a tam text pole s submit - update")

# main win
def main(tk):
    # registration window 
    tk.geometry("295x220")
    tk.resizable(False, False)
    tk.title("reg")


    Label(tk, text='registration', font='ar 15 bold').grid(row=0, column=3)

    # colums
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

    # buttons 
    Button(tk, text="submit", command= lambda:getvals(tk, name_entry, lastname_entry, email_entry, phone_number_entry, personal_id_entry)).grid(row=7, column=3)
    Button(tk, text="preheled", command= lambda:overview(tk)).grid(row=8, column=3)


    tk.mainloop()

tk = Tk()
main(tk)

# upravit veme id = otevre okno a tam text pole s submit - update