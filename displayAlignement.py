# -*- coding: utf-8 -*-
"""
Created on Wed March 4 2015 - 11:36:13
@author: Yoan BOUZIN email : yoan.bouzin@gmail.com
"""

try:
    import re
    import Tkinter # Python 2
    import ttk
    from tkFileDialog import askopenfilename
    from Tkinter import *
    from tkMessageBox import *
except ImportError:
    from tkinter import * # Python 3
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename
    from tkinter.messagebox import *
    import tkinter.font

root = Tk()
vsb = Scrollbar(root, orient=VERTICAL)
vsb.grid(row=0, column=1, sticky=N+S)
hsb = Scrollbar(root, orient=HORIZONTAL)
hsb.grid(row=1, column=0, sticky=E+W)
c = Canvas(root,yscrollcommand=vsb.set, xscrollcommand=hsb.set)
c.grid(row=0, column=0, sticky="news")
vsb.config(command=c.yview)
hsb.config(command=c.xview)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
fr = Frame(c,bg="white")
#On ajoute des widgets :
liste = sizePadx()
liste2 = getNameSequence()
for i in range(len(liste2)):
    row=i//1
    col=i%1
    if liste2[i].startswith(">") or liste2[i].startswith(" Frame"):
        Label(fr,text=liste2[i],relief=RIDGE,anchor='w',bg="white",borderwidth=0).grid(row=row, column=col, sticky="EW")
    if liste2[i].startswith("*"):
        Label(fr,text=liste2[i],relief=RIDGE,bg="LightSalmon",borderwidth=0).grid(row=row, column=col, sticky="EW")
    if liste2[i].startswith("Query="):
        Label(fr,text=liste2[i],anchor='w',relief=RAISED).grid(row=row, column=col, sticky="EW")
for i in range(len(liste)):
    row=i//1
    col=i%1
    if liste[i][0] != 0 and liste[i][1] == 0:
        Frame(fr, width=liste[i][0],height=6, bg="black").grid(row=row, column=col+3, pady=4, padx=10,sticky="W")
    else:
        Label(fr,text=liste[i][3],bg='white',borderwidth=0).grid(row=row,column=col+1,sticky="EW")
        Label(fr,text=liste[i][2],bg='white',borderwidth=0).grid(row=row,column=col+2,sticky="EW")
        if liste[i][2] < 40:
            Frame(fr, width=liste[i][0],height=4, bg="black",bd=2).grid(row=row, column=col+3, pady=2, padx=liste[i][1]+10, sticky="W")
        if liste[i][2] >= 40 and liste[i][2] <50:
            Frame(fr, width=liste[i][0],height=4, bg="blue2",bd=2).grid(row=row, column=col+3, pady=2, padx=liste[i][1]+10, sticky="W")
        if liste[i][2] >= 50 and liste[i][2] <80:
            Frame(fr, width=liste[i][0],height=4, bg="green2",bd=2).grid(row=row, column=col+3, pady=2, padx=liste[i][1]+10, sticky="W")
        if liste[i][2] >= 80 and liste[i][2] <200:
            Frame(fr, width=liste[i][0],height=4, bg="maroon1",bd=2).grid(row=row, column=col+3, pady=2, padx=liste[i][1]+10, sticky="W")
        if liste[i][2] > 200:
            Frame(fr, width=liste[i][0],height=4, bg="red",bd=2).grid(row=row, column=col+3, pady=2, padx=liste[i][1]+10, sticky="W")
hauteur = 20 * len(liste2)
Frame(fr,width=1,height=hauteur,bg="black").grid(row=0,column=0,rowspan=len(liste2),sticky="NE")
Label(fr,text="E-value",anchor='w',relief=RAISED).grid(row=0, column=1, sticky="EW")
Frame(fr,width=1,height=hauteur,bg="black").grid(row=0,column=1,rowspan=len(liste2),sticky="NE")
##sep = ttk.Separator(fr, orient=VERTICAL).grid(column=1, columnspan=5, sticky="NSE")
##style = ttk.Style()
##style.configure("sep.Separator", background="black")
##sep.configure(style="sep.TCheckbutton")

Label(fr,text="Score",anchor='w',relief=RAISED).grid(row=0, column=2, sticky="EW")
Frame(fr,width=1,height=hauteur,bg="black").grid(row=0,column=2,rowspan=len(liste2),sticky="NE")
c.create_window(0, 0,  window=fr)
fr.update_idletasks()
c.config(scrollregion=c.bbox("all"))
root.mainloop()
