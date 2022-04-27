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

# create table 
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

# check if in lastname doesnt have num or spec char 
def check_lasname(vallastname,err):
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

# check if email is legit 
def check_email(valemail,err):
    pattern = '^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$'

    if re.search(pattern, valemail):
        err[2] = 1
    else:
        err[2] = 0

# check if num is real
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

# check personal id 
def check_persid(valpersid,err):
    #split and chcek brirth date
        lenght = len(valpersid)
        # pers id has 10 num and /
        if valpersid and lenght == 11:
            p = 0
            for i in valpersid:
                if i.isdigit():
                    p = 0
                else:
                    p = 1
            if p == 0:
                # split pers id 
                splited = valpersid.split("/")
                valpersid = splited[0]+splited[1]
                sp1val = splited[0]
                sp2val = splited[1]
                n = 2
                sp1 = [sp1val[i:i + n] for i in range(0, len(sp1val), n)]
                # isolate year month and day 
                year = "20"+sp1[0]
                month = sp1[1]
                # women has +50 on months of birth
                if int(month) > 12:
                    month = int(month) - 50
                day = sp1[2]
                current_year = date.today().year
                # check if date can exist 
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
                                # check last 4 digits 
                                temp = valpersid[1::2]
                                temp = [int(i) for i in temp]
                                temp2 = valpersid[::2]
                                temp2 = [int(i) for i in temp2]
                                res = int(sum(temp)) - int(sum(temp2))
                                lastnumber = int(valpersid[-1])
                                if (lastnumber == 0 and res % 10 != 0) or (lastnumber != 0 and res % 11 != 0):
                                    err[4] = 0
                                else:
                                    err[4] = 1
                else:
                    err[4] = 0
        else:
            err[4] = 0

# get values from entry and check it
def getvals(tk, name_entry, lastname_entry, email_entry, phone_number_entry, personal_id_entry, editstatus, id):
    # err list 
    err = [0,0,0,0,0]

    # reset errors
    name_entry.config(highlightbackground = "white", highlightcolor= "white")
    lastname_entry.config(highlightbackground = "white", highlightcolor= "white")
    email_entry.config(highlightbackground = "white", highlightcolor= "white")
    phone_number_entry.config(highlightbackground = "white", highlightcolor= "white")
    personal_id_entry.config(highlightbackground = "white", highlightcolor= "white")

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

    # delete text areas if everthing is ok 
    for i in err:
        print(i)
        num += 1
        if i == 0:
            if num == 1:
                name_entry.config(highlightbackground = "red", highlightcolor= "red")
            elif num == 2:
                lastname_entry.config(highlightbackground = "red", highlightcolor= "red")
            elif num == 3:
                email_entry.config(highlightbackground = "red", highlightcolor= "red")
            elif num == 4:
                phone_number_entry.config(highlightbackground = "red", highlightcolor= "red")
            elif num == 5:
                personal_id_entry.config(highlightbackground = "red", highlightcolor= "red")
        else:
            status += 1

    if status == 5:
        # check if insert or update data 
        if editstatus == 0:
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

            # alert window 
            alert = Toplevel(tk)
            alert.geometry("295x220")
            alert.title("alert")
            alert.resizable(False, False)
            Label(alert, text='Well done', font='ar 15 bold').place(x=100,y=50)
            Button(alert, text="Go to overview", command= lambda: alertfnc(alert)).place(x=105,y=100)
        else:
            # update
            top.destroy()
            connection = sqlite3.connect('database.db')
            c = connection.cursor()
            c.execute("UPDATE people SET name = :name, lastname = :lastname, email = :email, phone_number = :phone_number, personal_number = :personal_number WHERE id = :id",
             {
                 'name':valname,
                 'lastname':vallastname,
                 'email':valemail,
                 'phone_number':valphone,
                 'personal_number':valpersid,
                 'id':id,
             }
            )
            connection.commit()
            connection.close()
            alertfnc(alert=edit)

# redirect to overview 
def alertfnc(alert):
    global top 
    top = Tk()
    top.destroy()
    alert.after(1000,lambda:alert.destroy())
    overview()

# print frame
def print_frame(top):

    # create mainframe 
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

    # db connect 
    connection = sqlite3.connect('database.db')
    c = connection.cursor()
    c.execute("SELECT * FROM people")
    result = c.fetchall()

    lenght = range(len(result))
    j = 4
    delY = 60
    ediY = 20

    # print information
    for i in lenght:

        Textarea = Text(secondframe, width=70, height=5,)
        Textarea.grid(row=j,column=0,padx=10,pady=10)
        Textarea.insert(END, "\n" +"Name: "+result[i][1]+" Lastname: "+result[i][2])
        Textarea.insert(END, "\n" +"Email: "+result[i][3]+" Phone number: "+result[i][4])
        Textarea.insert(END, "\n" +"Personal id: "+result[i][5])
        Textarea.configure(state='disabled')

        functionedit = partial(editfnc, id=result[i][0])
        edit = Button(secondframe, text="  Edit  ", command=functionedit).place(x=520,y=ediY)
        functiondelete = partial(delete, id=result[i][0])
        deletebutton = Button(secondframe, text="Delete", command=functiondelete)
        deletebutton.place(x=520,y=delY)

        delY += 104
        ediY += 104
        j += 1

    connection.commit()
    connection.close()

# alertdelete registration from database
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

# overview
def overview():
    global top 
    top = Tk()
    top.geometry("610x600")
    top.title("Overview")
    top.resizable(False, False)

    #print scrollable frame 
    print_frame(top)

    top.mainloop()

# edit
def editfnc(id):
    global edit
    edit = Tk()
    edit.geometry("295x220")
    edit.title("Edit")
    edit.resizable(False, False)

    Label(edit, text='Edit', font='ar 15 bold').grid(row=0, column=3)

    # entry
    name = Label(edit, text='Name')
    lastname = Label(edit, text='Lastname')
    email = Label(edit, text='Email')
    phone_number = Label(edit, text='Phone number')
    presonal_id = Label(edit, text='Personal id')

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

    # select specific information by id 
    connection = sqlite3.connect('database.db')
    c = connection.cursor()
    c.execute("SELECT * FROM people WHERE id ="+str(id)+"")
    result = c.fetchall()
    print (result)
    connection.commit()
    connection.close()

    name_entry = Entry(edit, textvariable= name_value,highlightthickness=2)
    name_entry.insert(0,result[0][1])
    lastname_entry = Entry(edit, textvariable= lastname_value,highlightthickness=2)
    lastname_entry.insert(0,result[0][2])
    email_entry = Entry(edit, textvariable= email_value,highlightthickness=2)
    email_entry.insert(0,result[0][3])
    phone_number_entry = Entry(edit, textvariable= phone_number_value,highlightthickness=2)
    phone_number_entry.insert(0,result[0][4])
    personal_id_entry = Entry(edit, textvariable= personal_id_value,highlightthickness=2)
    personal_id_entry.insert(0,result[0][5])

    name_entry.grid(row=1, column=3)
    lastname_entry.grid(row=2, column=3)
    email_entry.grid(row=3, column=3)
    phone_number_entry.grid(row=4, column=3)
    personal_id_entry.grid(row=5, column=3)

    # buttons 
    Button(edit, text="submit", command= lambda:getvals(edit, name_entry, lastname_entry, email_entry, phone_number_entry, personal_id_entry, editstatus=1, id = id)).grid(row=7, column=3)
    
    edit.mainloop()

# main window
def main(tk):
    # registration window 
    tk.geometry("295x220")
    tk.resizable(False, False)
    tk.title("Registration")


    Label(tk, text='Registration', font='ar 15 bold').grid(row=0, column=3)

    # entry
    name = Label(tk, text='Name')
    lastname = Label(tk, text='Lastname')
    email = Label(tk, text='Email')
    phone_number = Label(tk, text='Phone number')
    presonal_id = Label(tk, text='Personal id')

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

    name_entry = Entry(tk, textvariable= name_value,highlightthickness=2)
    lastname_entry = Entry(tk, textvariable= lastname_value,highlightthickness=2)
    email_entry = Entry(tk, textvariable= email_value,highlightthickness=2)
    phone_number_entry = Entry(tk, textvariable= phone_number_value,highlightthickness=2)
    personal_id_entry = Entry(tk, textvariable= personal_id_value,highlightthickness=2)

    name_entry.grid(row=1, column=3)
    lastname_entry.grid(row=2, column=3)
    email_entry.grid(row=3, column=3)
    phone_number_entry.grid(row=4, column=3)
    personal_id_entry.grid(row=5, column=3)

    # buttons 
    Button(tk, text="Submit", command= lambda:getvals(tk, name_entry, lastname_entry, email_entry, phone_number_entry, personal_id_entry, editstatus=0, id = 0)).grid(row=7, column=3)
    Button(tk, text="Overview", command= lambda:overview()).grid(row=8, column=3)


    tk.mainloop()


#create main 
tk = Tk()
main(tk)


