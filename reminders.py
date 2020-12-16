from tkinter import *
from tkinter import messagebox
from time import *
import sys

window = Tk()
window.geometry("735x550+100+100")
window.title('Reminders')
window.resizable(0, 0)
rl = Listbox(window, width=117, height=32,
             relief='flat', highlightthickness=0)
rl.place(x=5, y=5)
scroll = Scrollbar(window)
scroll.place(x=710, y=5, height=510)
rl['yscrollcommand'] = scroll.set
scroll['command'] = rl.yview


def open_1():
    global rlist_compl, rlist_nme, rlist_tme, remnum
    rlist_nme, rlist_tme = [], []
    try:
        with open('rDat.txt') as f:
            text = f.read().strip()
            rlist_compl = text.split('\n')
            rlist_nme.clear()
            rlist_tme.clear()
            for x in rlist_compl:
                rlist_nme.append(x[6:])
                rlist_tme.append(x[0:5])
            remnum = len(rlist_compl)
            rl.delete(0, END)
            if remnum > 0:
                for x, y in enumerate(rlist_compl):
                    if y:
                        item = str(x + 1) + ' ' + y
                        rl.insert('end', item)
                    else:
                        continue
            try:
                rl.select_set(0)
            except:
                pass
    except:
        messagebox.showerror('Err 001', 'No rDat.txt file specified. Please create a blank one. \
            Maybe you can run the attached sh file or bat file.')
        sys.exit(1)


def save():
    with open('rDat.txt', 'w') as f:
        for x in rlist_compl:
            f.write(x+'\n')


def checkTime():
    open_1()
    save()
    cTime = asctime().split()[3][:-3]
    if cTime in rlist_tme:
        index = rlist_tme.index(cTime)
        todo = rlist_nme[index]
        if not todo.endswith('[DONE]'):
            messagebox.showinfo('Hey! Time to ' + todo,
                                'Click the "OK" button to mark it as [DONE].')
            rlist_compl[index] += ' [DONE]'
            open_1()


def add(event=None):
    global tal, tal2, remnum

    tal = []
    for x in range(24):
        if len(str(x)) == 1:
            to_add = '0' + str(x)
        elif len(str(x)) == 2:
            to_add = str(x)
        tal.append(to_add)
    tal = tuple(tal)
    tal2 = []
    for y in range(60):
        if len(str(y)) == 1:
            to_add = '0' + str(y)
        elif len(str(y)) == 2:
            to_add = str(y)
        tal2.append(to_add)
    tal2 = tuple(tal2)
    nrw = Toplevel()
    nrw.title('New')
    nrw.transient(window)
    nrw.geometry('150x125')
    nrw.resizable(0, 0)
    Label(nrw, text='Enter Reminder Name:').pack()
    newName = Entry(nrw)
    newName.pack()
    Label(nrw, text='Select Reminder Time:').pack()
    Label(nrw, text=':').place(y=69, x=68)
    time1 = Spinbox(nrw, values=tal, state='readonly')
    time2 = Spinbox(nrw, values=tal2, state='readonly')

    def cs(event=None):
        global remnum, rlist_nme, rlist_tme
        if newName.get() == '':
            messagebox.showerror('Err 003', 'Empty title')

        elif rlist_nme.count(newName.get()) >= 1:
            messagebox.showerror('Err 004', 'Name found in list. Please use \
                anothor name.')

        elif len(newName.get()) >= 40:
            messagebox.showerror('Err 005', 'Name too long.')

        else:
            remnum += 1
            nr = time1.get() + ':' + time2.get() + ' ' + newName.get()
            rlist_nme.append(newName.get())
            rlist_tme.append(time1.get() + ':' + time2.get())
            rlist_compl.append(nr)
            save()
            open_1()
            nrw.destroy()

    ok_button = Button(nrw, text='OK (Enter)', command=cs, width=7)
    time1.place(x=12, y=71, width=55)
    time2.place(x=80, y=71, width=55)
    ok_button.place(y=95, x=11)
    newName.focus_set()
    open_1()

    def ce(event=None):

        cfirm = messagebox.askyesno('Sure to Exit',
                                    'Do you REALLY want to Exit?\nClick \'Yes\' to Exit, \'No\' to Stay')
        if cfirm == True:

            nrw.destroy()
    canc_button = Button(nrw, text='Cancel', command=ce, width=7)
    canc_button.place(y=95, x=74)

    nrw.bind('<Return>', cs)
    nrw.bind('<F1>', ce)


btn_add = Button(window, text='Add (F1)', command=add)
btn_add.place(x=5, y=520)


def delete(event=None):
    global remnum

    try:
        ck = messagebox.askyesno('Sure?', 'Sure to delete?\nClick \'Yes\' to\
Delete, Or \'No\' to Exit.')

        if ck == True:
            selected = rl.curselection()
            delIndex = selected[0]
            rl.delete(delIndex)
            del rlist_nme[delIndex]
            del rlist_tme[delIndex]
            del rlist_compl[delIndex]
            remnum -= 1
            save()
            open_1()

    except TclError:
        if remnum == 0:
            messagebox.showerror('Err 002', 'Can\'t delete reminder because:\n \
No Items In Your Reminders List.')

        else:
            messagebox.showerror('Err 003', 'Can\'t delete reminder because:\n \
No Items Selected.')


btn_del = Button(window, text='Delete (F2)', command=delete)
btn_del.place(x=65, y=520)


def search(event=None):
    global rlist_nme

    sWin = Toplevel()
    sWin.geometry('165x60')
    sWin.resizable(0, 0)
    sWin.title('Search in Reminders')
    sWin.transient(window)
    searchtxt = Entry(sWin)
    searchtxt.place(x=0, y=0, height=25)
    searchtxt.focus_set()

    def sAction():
        rl.selection_clear(0, END)

        def clear():
            for x in range(remnum):
                rl.itemconfig(x, bg='#ffffff')
        clear()
        sTimes = 0
        for sItem in rlist_compl:
            if (sItem in searchtxt.get()) or (searchtxt.get() in sItem):
                rl.itemconfig(sTimes, bg='#b4eb37')
                sTimes += 1
            else:
                sTimes += 1

    sButton = Button(sWin, text='Search', command=sAction)
    sButton.place(y=27, x=50)


sBtn = Button(window, text='Search (F3)', command=search)
sBtn.place(x=136, y=520)


def properties(event=None):
    try:
        index = rl.curselection()[0]
        name = rlist_nme[index]
        time = rlist_tme[index]
    except (TclError, IndexError):
        if remnum == 0:
            messagebox.showerror('E007', 'Can\'t Show Properties Because:\n\
                No Items In Your Reminders List.')

        else:
            messagebox.showerror('E007', 'Can\'t Show Properties Because:\n\
                Nothing Selected.')

    else:
        pWin = Toplevel()
        pWin.focus()
        pWin.title('Properties of '+name)
        pWin.resizable(0, 0)
        pWin.geometry('200x124')
        pWin.transient(window)
        pBox = Listbox(pWin, height=5, relief='flat', highlightthickness=0)
        pBox.place(x=0, y=0, width=200)

        pBox.insert(END, 'Name: ' + name)
        pBox.insert(END, 'Time: ' + time)
        pBox.select_set(0)

        def edit(event=None):

            def cName():

                ncw = Toplevel()
                ncw.title('New Name')
                ncw.focus()
                ncw.transient(window)
                ncw.resizable(0, 0)
                ncw.geometry('130x70')
                Label(ncw, text='Enter New Name:').place(x=0, y=0)
                cName = Entry(ncw)
                cName.place(x=0, y=20)

                def cnChange(event=None):
                    global remnum, rlist_nme, rlist_tme
                    if cName.get() == '':

                        messagebox.showerror('Err 008', 'Empty title')
                    elif cName in rlist_nme:

                        messagebox.showerror('Err 009', 'Name found in list.\
                         Please use anothor name.')
                    elif len(cName.get()) >= 40:

                        messagebox.showerror('Err 010', 'Name too long.')
                    else:

                        rlist_compl[index] = time + ' ' + cName.get()
                        rlist_nme[index] = cName.get()
                        name = cName.get()
                        save()
                        open_1()
                        ncw.destroy()

                cBtn = Button(ncw, text='OK (Enter)', command=cnChange)
                cBtn.place(x=0, y=40)
                ccBtn = Button(ncw, text='Cancel', command=ncw.destroy)
                ccBtn.place(x=70, y=40, width=54)
                ncw.bind('<Return>', cnChange)
#

            def cTime():
                tal = []
                for x in range(24):
                    if len(str(x)) == 1:
                        to_add = '0' + str(x)
                    elif len(str(x)) == 2:
                        to_add = str(x)
                    tal.append(to_add)
                tal = tuple(tal)
                tal2 = []
                for y in range(60):
                    if len(str(y)) == 1:
                        to_add = '0' + str(y)
                    elif len(str(y)) == 2:
                        to_add = str(y)
                    tal2.append(to_add)
                tal2 = tuple(tal2)
                tcw = Toplevel()
                tcw.transient(window)
                tcw.focus()
                tcw.title('New Time')
                tcw.resizable(0, 0)
                tcw.geometry('150x80')
                Label(tcw, text='Select New Time:').pack()
                cHour = Spinbox(tcw, values=tal, state='readonly')
                cHour.place(x=10, y=20, width=55)
                cMinute = Spinbox(tcw, values=tal2, state='readonly')
                cMinute.place(x=75, y=20, width=55)
                Label(tcw, text=':').place(x=65, y=18)

                def ctChange(event=None):

                    rlist_compl[index] = ' ' + cHour.get() + ':' + \
                        cMinute.get() + ' ' + name
                    rlist_tme[index] = cHour.get() + ':' + cMinute.get()
                    time = cHour.get() + ':' + cMinute.get()
                    save()
                    open_1()
                    tcw.destroy()
                ctBtn = Button(tcw, text='OK (Enter)', command=ctChange)
                ctBtn.place(y=42, x=10, width=60)
                tcw.bind('<Return>', ctChange)
                ccBtn = Button(tcw, text='Cancel', command=tcw.destroy)
                ccBtn.place(y=42, x=70, width=60)
            try:

                action = pBox.get(pBox.curselection())
                if action.startswith('Name'):
                    cName()
                else:
                    cTime()
            except SyntaxError:

                messagebox.showerror('Err 011', 'No Action Selected')

        cButton = Button(pWin, text='Change...(Enter)', command=edit)
        cButton.place(x=2, y=89)
        eButton = Button(pWin, text='Exit', command=pWin.destroy)
        eButton.place(x=100, y=89, width=99)

        pWin.bind('<Return>', edit)


pBtn = Button(window, text='Properties (F4)', command=properties)
pBtn.place(y=520, x=210)


window.bind('<F1>', add)
window.bind('<F2>', delete)
window.bind('<F3>', search)
window.bind('<F4>', properties)

window.after(1000, checkTime)
window.mainloop()
