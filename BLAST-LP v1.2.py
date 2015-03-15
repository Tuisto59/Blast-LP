# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 201 - 04:24:26
@author: Yoan BOUZIN email : yoan.bouzin@gmail.com
"""

try:
    import time
    import subprocess
    import platform
    import os
    import Tkinter # Python 2
    import ttk
    from tkFileDialog import askopenfilename
    from Tkinter import *
    from tkMessageBox import *
    import threading
except ImportError:
    from tkinter import * # Python 3
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename
    from tkinter.messagebox import *
    import tkinter.font

import time
import threading

###########
# CREDITS #
###########

print("BlastLP v1.0 - 16.02.2015 - 17:43 \n")
print("This software was made to facilitate and automatise local Blast analysis")
print("Please install NCBI Blast+ v2.2.29 or his upgrade")
print("Contact Yoan BOUZIN at yoan.bouzin@gmail.com, Master1 graduates in Bioinformatic, Rennes1 \n")

###########
# PROCESS #
###########

if platform.system() == 'Linux' or platform.system() == 'Darwin':
    chemin = os.getcwd()
    #subprocess.call("cd "+chemin)
    subprocess.call("chmod +x makeblastdb tblastn blastp seqfetch.def.pl", shell=True)

##################
# Graphical User Interface #
##################
    

#fenetre principale
fenetre = Tk()
fenetre.resizable(0,0)

#Titre
fenetre.title("BLAST-LP v1.0")

#Logo
img = PhotoImage(file="logoGUI.png")
Label(fenetre, image=img).grid(rowspan=5, column=0)

#Titre next logo
Label(fenetre, text="BLAST Local Pipeline").grid(row=0, column=1, columnspan=4) 
Label(fenetre, text="version 1.0").grid(row=1, column=1, columnspan=4)
Label(fenetre, text="Application to automatise Blast+ v2.2.30 command").grid(row=2, column=1, columnspan=4)
Label(fenetre, text="By Yoan BOUZIN").grid(row=3, column=1, columnspan=4)
Label(fenetre, text="yoan.bouzin@gmail.com",pady=3).grid(row=4, column=1, columnspan=4)




#Progress Bar the first for partie 1 and 2
progressbar = ttk.Progressbar(orient=HORIZONTAL, length=400, mode='indeterminate', variable=0, maximum=10)

#######
#Partie 1 #
#######

#Titre
a = Label(fenetre, text="Create the library database (makeblastdb)",pady=5).grid(row=5, columnspan=3, sticky="W")
ttk.Separator(fenetre, orient=HORIZONTAL).grid(row=5, columnspan=5, sticky="NEW")
#Variable et création des boutons
var = IntVar()
for item in [1,2]:
    Label(fenetre, text="Type :").grid(row=6, column=0, sticky="W",padx=30)
    if item == 1:
        rb = Radiobutton(fenetre, text='Nucleotides',value=item,variable=var).grid(row=6, column=0,sticky="E")
    if item == 2:
        rb = Radiobutton(fenetre, text='Proteins',value=item,variable=var).grid(row=6, column=1,sticky="W")

#Récuperation de la valeur du bouton radio (Nucleotides/Proteines)
def typeNP():
    return var.get()

#Création d'un objet StringVar() qui contient la valeur de l'Entry
textEntry1 = StringVar()
pathTextEntry1 = StringVar()

#Création du Label File
Label(fenetre, text="Files : ").grid(row=7, column=0, sticky="E")

#Entry file
entry1 = Entry(fenetre, textvariable=textEntry1,state='disabled')
entry1.grid(row=7, column=1)

#entry path
pathEntry1 = Entry(fenetre, textvariable=pathTextEntry1)

#Fonction pour le bouton browse cherche et récupère le nom du fichier

def GetFileToMakeLibraryDatabase():
    import os
    pathfile = askopenfilename(title='Open the Library Datafile')
    textEntry1.set(os.path.split(pathfile)[1])
    pathTextEntry1.set(os.path.split(pathfile)[0])

#Bouton Browse
Button(fenetre, text="Browse",command=GetFileToMakeLibraryDatabase).grid(row=7, column=2)

#Récupère la valeur de entry1
def callback():
    return entry1.get()

def pathCallback():
    return pathEntry1.get()

#fonction de création de la base de données



def makeblastdb():
    """
    create the local library database with your input file
    """
    import subprocess
    import os
    import platform
    from time import strftime, gmtime
    OS = platform.system()
    if OS == 'Linux' or OS == 'Darwin':
        path = pathCallback()+'/'
        print(path)
    if OS == 'Windows':
        path = pathCallback()+'\\'
    DB = callback()
    if os.path.isfile(path+DB) != True:
        progressbar.grid_forget()
        showerror('Error : Missing File !', "You must choose a valid file")
    typ = str(typeNP())
    if typ != '1' and typ != '2':
        progressbar.grid_forget()
        showerror('Error : Missing Type !', "You do not choose your type\n(nucleotides or proteins)")
    t0 = time.time()
    if os.path.isfile(path+DB) == True and typ == '1' or typ == '2':
        if OS == 'Windows':
            if typ == '1':
                process = subprocess.Popen("makeblastdb -in "+path+DB+" -dbtype nucl")
                process.communicate()
                t1 = time.time()
                print("Finish in "+str(strftime("%H hour(s) %M minute(s) %S second(s)", gmtime(t1-t0))))
                progressbar.stop()
                showinfo('Information', "Your job finish in\n"+str(round(t1-t0,2))+" seconds")
            if typ == '2':
                process = subprocess.call("makeblastdb -in "+path+DB+" -dbtype prot", shell=True)
                process.communicate()
                t1 = time.time()
                print("Finish in "+str(strftime("%H hour(s) %M minute(s) %S second(s)", gmtime(t1-t0))))
                progressbar.stop()
                showinfo('Information', "Your job finish in\n"+str(round(t1-t0,2))+" seconds")
        if OS == 'Linux' or OS == 'Darwin':
            if typ == '1':
                subprocess.call("makeblastdb -in "+path+DB+" -dbtype nucl", shell=True)
                t1 = time.time()
                print("Finish in "+str(strftime("%H hour(s) %M minute(s) %S second(s)", gmtime(t1-t0))))
                progressbar.stop()
                showinfo('Information', "Your job finish in\n"+str(round(t1-t0,2))+" seconds")
            if typ == '2':
                subprocess.call("makeblastdb -in "+path+DB+" -dbtype prot", shell=True)
                t1 = time.time()
                print("Finish in "+str(strftime("%H hours %M minute(s) %S second(s)", gmtime(t1-t0))))
                progressbar.stop()
                showinfo('Information', "Your job finish in\n"+str(round(t1-t0,2))+" seconds")
    progressbar.grid_forget()

### Threading progress bar makeblastdb ###

def foo():
    makeblastdb() # simulate some work

def start_foo_thread():
    global foo_thread
    foo_thread = threading.Thread(target=foo)
    foo_thread.daemon = True
    progressbar.grid(row=25,columnspan=4,pady=2,sticky=W+E)
    #progressbar.step(100)
    progressbar.start()
    foo_thread.start()
    fenetre.after(20, check_foo_thread)

def check_foo_thread():
    if foo_thread.is_alive():
        fenetre.after(20, check_foo_thread)
    else:
        progressbar.stop()

Button(fenetre, text="Run",command=start_foo_thread).grid(row=7,column=3)

######
#Partie2#
######

#Variable et création des boutons radio
var2 = IntVar()
for item in [1,2]:
    Label(fenetre, text="Type :").grid(row=9, column=0, sticky="W",padx=30)
    if item == 1:
        rb = Radiobutton(fenetre, text='Nucleotides',value=item,variable=var2).grid(row=9, column=0,sticky="E")
    if item == 2:
        rb = Radiobutton(fenetre, text='Proteins',value=item,variable=var2).grid(row=9, column=1,sticky="W")

#Récuperation de la valeur du bouton radio (Nucleotides/Proteines)
def typeNP2():
    return var2.get()

#objet stringvar
Label(fenetre, text="Blast a file to the library database (Blastp/Blastn)",pady=5).grid(row=8, columnspan=3, sticky="WN")
ttk.Separator(fenetre, orient=HORIZONTAL).grid(row=8, columnspan=5, sticky="NEW")
Label(fenetre, text="Files with sequence(s) : ").grid(row=11, column=0, sticky="E")

textEntry2 = StringVar()
entry2 = Entry(fenetre, textvariable=textEntry2,state='disabled')
entry2.grid(row=10, column=1)

textEntry3 = StringVar()
entry3 = Entry(fenetre, textvariable=textEntry3,state='disabled')
entry3.grid(row=11, column=1)

pathTextEntry2 = StringVar()
pathEntry2 = Entry(fenetre, textvariable=pathTextEntry2)

pathTextEntry3 = StringVar()
pathEntry3 = Entry(fenetre, textvariable=pathTextEntry3)

#Fonction pour le bouton browse cherche et récupère le nom du fichier
def GetLibraryDatabaseFile():
    import os
    pathfile = askopenfilename(title='Open Library Datafile')
    textEntry2.set(os.path.split(pathfile)[1])
    pathTextEntry2.set(os.path.split(pathfile)[0])

def GetSequenceFile():
    import os
    pathfile = askopenfilename(title='Open File with Sequences')
    textEntry3.set(os.path.split(pathfile)[1])
    pathTextEntry3.set(os.path.split(pathfile)[0])

#Récupère la valeur de entry2
def callback2():
    return entry2.get()

def pathCallback2():
    return pathEntry2.get()

#Récupère la valeur de entry3
def callback3():
    return entry3.get()

def pathCallback3():
    return pathEntry3.get()

Button(fenetre, text="Browse", command=GetLibraryDatabaseFile).grid(row=10, column=2)
Button(fenetre, text="Browse",command=GetSequenceFile).grid(row=11, column=2)


Label(fenetre, text="Library Database : ").grid(row=10, column=0,sticky="E")

#fonction OneFile
def OneFile():
    """
    This function is very long, take all the sequences of the input file and blast it to the database
    input : files with your sequences
    output : files with blast results in the same folder
    """
    import subprocess
    import platform
    import time
    OS = platform.system()
    if OS == 'Linux' or OS == 'Darwin':
        pathLibrary = pathCallback2()+'/'
        pathSequence = pathCallback3()+'/'
    if OS == 'Windows':
        pathLibrary = pathCallback2()+'\\'
        pathSequence = pathCallback3()+'\\'
    typ = str(typeNP2())
    if typ != '1' and typ != '2':
        progressbar.stop()
        progressbar.grid_forget()
        showerror('Error : Missing Type !', "You do not choose your type\n(nucleotides or proteins)")
    else:
        library = callback2()
        if os.path.isfile(pathLibrary+library) != True:
            progressbar.stop()
            progressbar.grid_forget()
            showerror('Error : Missing File !', "You must choose a Library Database file")
        else:
            filename = callback3()
            if os.path.isfile(pathSequence+filename) != True:
                progressbar.stop()
                progressbar.grid_forget()
                showerror('Error : Missing File !', "You must choose your sequence file")
            else:
                #evalue = input("Choose your e-value limit : ")
                #if os.path.isfile(pathLibrary+library) == True and os.path.isfile(pathSequence+filename) == True and typ == '1' or typ == '2':
                if typ =="1":
                    typ = "tblastn"
                if typ == "2":
                    typ = "blastp"
                #filename = input("Write the filename : ")
                if OS == 'Linux' or OS == 'Darwin':
                    t0 = time.time()
                    query = str(filename)
                    blast = str(filename)+'_Blast.txt'
                    seqs = str(filename)+'_seqs.txt'
                    subprocess.call(typ+" -query "+pathSequence+query+" -db "+pathLibrary+library+" -evalue 1e-10 -out "+pathSequence+blast, shell=True)
                    print('Fichier n° '+str(1)+' '+str(filename))
                    subprocess.call("grep '\(Sbjct\|>\)' "+pathSequence+blast+" > "+pathSequence+seqs, shell=True)
                    t1 = time.time()
                    progressbar.stop()
                    print('Job finish in '+str(round(t1-t0,2))+' seconds')
                    showinfo('Information', "Your job finish in\n"+str(round(t1-t0,2))+" seconds")
                    showinfo('Information', "The "+blast+" and "+seqs+" have been created in the \n"+pathSequence)
                if OS == 'Windows':
                    t0 = time.time()
                    query = str(filename)
                    blast = str(filename)+'_Blast.txt'
                    seqs = str(filename)+'_seqs.txt'
                    subprocess.call(typ+' -query '+pathSequence+query+' -db '+pathLibrary+library+' -evalue 1e-10 -out '+pathSequence+blast, shell=True)
                    print('Fichier n° '+str(1)+' '+str(filename))
                    subprocess.Popen('findstr "Sbjct >" '+pathSequence+blast+' > '+pathSequence+seqs, shell=True)
                    t1 = time.time()
                    progressbar.stop()
                    print('Job finish in '+str(round(t1-t0,2))+' seconds')
                    showinfo('Information', "Your job finish in\n"+str(round(t1-t0,2))+" seconds")
                    showinfo('Information','The files '+blast+' and '+seqs+"\nhave been created in :\n"+pathSequence)
    progressbar.grid_forget()

### Threading progress bar makeblastdb ###

def foo2():
    OneFile() # simulate some work

def start_foo_thread2():
    global foo_thread
    foo_thread = threading.Thread(target=foo2)
    foo_thread.daemon = True
    progressbar.grid(row=25,columnspan=4,pady=2,sticky=W+E)
    progressbar.start()
    foo_thread.start()
    fenetre.after(20, check_foo_thread2)

def check_foo_thread2():
    if foo_thread.is_alive():
        fenetre.after(20, check_foo_thread2)
    else:
        progressbar.stop()

#Bouton Run pour la fonction OneFile
Button(fenetre, text="Run",command=start_foo_thread2).grid(row=9,column=3,rowspan=2)

#                                           #################
#                                               DISPLAY ALIGNEMENT
#                                           #################

def BlastFile():
    listeFile = []
    if os.path.isfile(pathCallback3()+'/'+callback3()) == True:
        if os.path.isfile(pathCallback3()+'/'+callback3()+"_Blast.txt") == True:
            blastFile = open(pathCallback3()+'/'+callback3()+"_Blast.txt",'r')
            for ligne in blastFile:
                listeFile.append(ligne)
            blastFile.close()
        if os.path.isfile(pathCallback3()+'/'+callback3()+"_Blast.txt") == False:
            blastFile = open(pathCallback3()+'/'+callback3(),'r')
            for ligne in blastFile:
                listeFile.append(ligne)
            blastFile.close()
    return listeFile
    

def getNameSequence():
##    listeFile = []
    listeFile = BlastFile()
    listeName = []
##    blastFile = open(pathCallback3()+'/'+callback3(),'r')
##    for ligne in blastFile:
##        listeFile.append(ligne)
    for ligne in range(len(listeFile)):
        if listeFile[ligne].startswith("Query="):
            if listeFile[ligne].startswith("Query=") and listeFile[ligne+1] != "\n":
                a = re.sub("[\n]","",listeFile[ligne])
                b = re.sub("[\n]","",listeFile[ligne+1])
                listeName.append(a+" "+b)
            else:
                a = re.sub("[\n]","",listeFile[ligne])
                listeName.append(a)
        if listeFile[ligne].startswith(">"):
            if listeFile[ligne].startswith(">") and listeFile[ligne+1] != "\n":
                a = re.sub("[\n]","",listeFile[ligne])
                b = re.sub("[\n]","",listeFile[ligne+1])
                listeName.append(a+" "+b)
            else:
                a = re.sub("[\n]","",listeFile[ligne])
                listeName.append(a)
        if listeFile[ligne].startswith("*"):
                a = re.sub("[\n]","",listeFile[ligne])
                listeName.append(a)
        if listeFile[ligne].startswith(" Frame = "):
            if not listeFile[ligne-6].startswith(">") or listeFile[ligne-5].startswith(">"):
                a = re.sub("[\n]","",listeFile[ligne])
                listeName.append(a)
##    blastFile.close()
    #print("getNameSequence() : ",listeName)
    return listeName

def chercheQueryLength(blastFile):
    """
    crée une liste des longueurs des sequences Query
    """
    lenghtListe = []
##    blastFile = open(pathCallback3()+'/'+callback3(),'r')
    repere = ""
    for ligne in blastFile:
        if ligne.startswith("Query="):
            repere = "Query="
        if ligne.startswith("Length=") and repere == "Query=":
            lenght = ''.join(re.findall("[0-9]",ligne))
            lenghtListe.append(int(lenght))
            repere = ""
##    blastFile.close()
    #print("chercheQueryLength() : ", lenghtListe)
    return lenghtListe

def chercheScore(blastFile):
    """
    crée une liste des Scores en bits
    """
    lenghtListe = []
##    blastFile = open(pathCallback3()+'/'+callback3(),'r')
    for ligne in blastFile:
        if ligne.startswith(" Score ="):
            lenght = float(re.findall(".*?(\\d+)",ligne)[0])
            lenghtListe.append(lenght)
##    blastFile.close()
    if lenghtListe == []:
        lenghtListe.append(0)
    #print("chercheScore() : ", lenghtListe)
    return lenghtListe

def getEValues(blastfile):
    import re
    evalues = []
    for ligne in blastfile:
        if ' Expect = ' in ligne:
            num = re.findall('.*?(\\d+)',ligne)
            evalue = float(num[len(num)-2]+"e-"+num[len(num)-1])
            evalues.append(evalue)
    if evalues == []:
        evalues.append(0)
    #print("getEValues : ", evalues)
    return evalues

def getPosition2(blastFile):
    """
    crée une liste exploitable pour getSbjctWidth
    """
##    blastFile = open(pathCallback3()+'/'+callback3(),'r')
    liste = []
    for ligne in blastFile:
        if not ligne == "\n":
            if ligne.startswith("*"):
                liste.append(ligne)
            if ligne.startswith("Query="):
                liste.append(ligne)
            if ligne.startswith(" Frame = "):
                liste.append(ligne)
            if ligne.startswith(">"):
                liste.append(ligne)
            if ligne.startswith("Query "):
                a = int(re.findall(".*?(\\d+)",ligne)[0])
                b = int(re.findall(".*?(\\d+)",ligne)[1])
                liste.append([a,b])
##    blastFile.close()
    #print("getPosition2() : ", liste)
    return liste

def getSbjctWidth2(blastFile):
    """
    renvois une liste de liste avec les taille des Sbjct trouvé pour chaque sequence Query
    """
    liste = getPosition2(blastFile)
    listeOneSeq = []
    listeOneSeqCopy=[]
    listeTotal = []
    debut = 0
    fin = 0
    for i in range(len(liste)):
        a = liste[i][0]
        if a == " " and liste[i-1][0] == ">" and liste[i-2][0] == "Q":
            debut = liste[i+1][0] #debut, 1er alignement d'un fichier de sequence
        if a == "Q" and type(liste[i-1][0]) == int and i-1>0:
            # Q etant le debut du nouveau Query, la aleur avant sera toujour la valeur fin
            fin = liste[i-1][1]
        if a == " " and type(liste[i-1][0]) == int and type(liste[i+1][0]) == int:
            #dans le cas de plusieur sequence resultat ont à déjà un début au départ ici la fin
            fin = liste[i-1][1]
            #ont ajoute donc les deux valeur pour créé le tuple
            listeOneSeq.append((debut,fin))
            #ont réinitialise à 0
            debut = 0
            fin = 0
            #debut nième alignement d'un fichier de sequence
            debut = liste[i+1][0]
        if a == " " and liste[i-1][0] == ">" and type(liste[i-2][0]) == int:
            fin = liste[i-2][1]
            listeOneSeq.append((debut,fin))
            debut = 0
            fin = 0
            debut = liste[i+1][0]
        if a == '*':
            listeTotal.append([(0,0)])
        if i == len(liste)-1:
            fin = liste[i][1]
        if debut != 0 and fin !=0:
            listeOneSeq.append((debut,fin))
            debut = 0
            fin = 0
        if i == len(liste)-1:
            #modifier ici 12.19 le 2.3.2015
            if listeOneSeq != []:
                listeTotal.append(listeOneSeq)
##            else:
##                listeTotal.append([(0,0)])
        #test listeTotal
        if a == "Q" and i-1>0 and len(listeOneSeq) != 0:
            listeOneSeqCopy=listeOneSeqCopy+listeOneSeq
            listeTotal.append(listeOneSeq)
            listeOneSeq = []
    #print(listeOneSeqCopy)
    #print("getSbjctWidth2() : ", listeTotal)
    return listeTotal
        
def calculdistance(blastFile):
    liste = getSbjctWidth2(blastFile)
    liste1 = []
    liste2 = []
    for i in liste:
        for j in i:
            width = j[1]-j[0]
            #print(width)
            liste2.append(width)
        liste1.append(liste2)
        liste2=[]
    #print("calculdistance() : ", liste1)
    return liste1

def sizePadx():
    #print("Padx running : \n")
    listePadx = []
    longueur = 1000
    blastFile = BlastFile()
    ListeDesPadxSbjct = getSbjctWidth2(blastFile)
    ListeDesLongueurQuery = chercheQueryLength(blastFile)
    ListeDesLongueurSbjct = calculdistance(blastFile)
    ListeDesScores = chercheScore(blastFile)
    ListeEvalues = getEValues(blastFile)
    try:
        MAX = max(ListeDesLongueurQuery)
    except ValueError:
        MAX = longueur
    cpt = 0
    for i in range(len(ListeDesPadxSbjct)):
        #print("boucle : ",cpt)
        listePadx.append([int(round(ListeDesLongueurQuery[i]*longueur/MAX,0)),0])
        for j in range(len(ListeDesPadxSbjct[i])):
            score = ListeDesScores[cpt]
            evalue = ListeEvalues[cpt]
            padx = int(round(ListeDesPadxSbjct[i][j][0]*longueur/MAX,0))
            width = int(round(ListeDesLongueurSbjct[i][j]*longueur/MAX,0))
            if padx != 0 and width != 0:
                listePadx.append([width,padx,score,evalue])
                cpt = cpt + 1
            else:
                listePadx.append([width,padx,0,""])
    #print("sizePadx : ", listePadx)
    return listePadx

###################### END DISPLAY ALIGNEMENT 

def alignement():
    if callback3() == "":
        showerror("Error : Missing File !","Choose your Blast Result")
    if sys.version[0] == '2':
        execfile("displayAlignement.py")
    if sys.version[0] == '3':
        exec(compile(open("displayAlignement.py", "rb").read(), "displayAlignement.py", 'exec'))

Button(fenetre, text="Show\nAlignment",command=alignement).grid(row=11,column=3)

######
#Partie3##################################################################
######
Label(fenetre, text="Create individual query files with a file",pady=5).grid(row=12, columnspan=3, sticky="W")
ttk.Separator(fenetre, orient=HORIZONTAL).grid(row=12, columnspan=5, sticky="NEW")
Label(fenetre, text="Files : ").grid(row=13, column=0,sticky="E")

textEntry4 = StringVar()
entry4 = Entry(fenetre, textvariable=textEntry4,state='disabled')
entry4.grid(row=13, column=1)

pathTextEntry4 = StringVar()
pathEntry4 = Entry(fenetre, textvariable=pathTextEntry4)


#Get the value of entry4
def GetSequenceFile2():
    import os
    pathfile = askopenfilename(title='Open File with Sequences')
    textEntry4.set(os.path.split(pathfile)[1])
    pathTextEntry4.set(os.path.split(pathfile)[0])

#Récupère la valeur de entry4
def callback4():
    return entry4.get()

def pathCallback4():
    return pathEntry4.get()

Button(fenetre, text="Browse",command=GetSequenceFile2).grid(row=13, column=2)

#comand check button
folderVar = StringVar()
folderEntry = Entry(fenetre,width=30, textvariable=folderVar)
def checkButtonEntry():
    if checkButtonVar.get() == 1:
        folderEntry.grid(row = 14, column=1, columnspan=2, sticky="W")
        folderEntry.insert(0, "FolderName")
    else :
        folderEntry.delete(0, END)
        folderEntry.grid_forget()
        
#IntVar du check button
checkButtonVar = IntVar()
checkButton = Checkbutton(fenetre, text="Create a Folder ?", variable=checkButtonVar, command=checkButtonEntry)
checkButton.grid(row=14,column=0)

#recupere le nom du dossier
def getFolderName():
    return folderEntry.get()

#Fonction createQueryFiles

def createQueryFile():
    """
    create individuals sequences files with a single files withs all sequences
    """
    import re
    import time
    liste = []
    seq = []
    fichier = []
    position = []
    OS = platform.system()
    if OS == 'Linux' or OS == 'Darwin':
        #path = os.getcwd()+'/'
        path = pathCallback4()+'/'
    if OS == 'Windows':
        path = pathCallback4()+'\\'
    #Nom du fichier de séquence
    name = callback4()
    if os.path.isfile(path+name) != True:
        showwarning('Warning', "You must choose your sequence file")
    if os.path.isfile(path+name) == True:
        f = open(path+name,'r')
        for i in f:
            fichier.append(i)
        f.close()
        for i in range(len(fichier)):
            if fichier[i][0] == ">":
                position.append(i)
        print("\n They are "+str(len(position))+" sequences in the file \n")
        showinfo('Number of sequences', "They are "+str(len(position))+" sequences in the file")
        for i in range(len(position)):
            if i == len(position)-1:
                for j in range(position[i],len(fichier)):
                    seq.append(fichier[j])
                liste.append(seq)
                seq = []
            else:
                for j in range(position[i],position[i+1]):
                    seq.append(fichier[j])
                liste.append(seq)
                seq = []
        choice = checkButtonVar.get()
        if choice == 0:
            if OS == "Windows":
                tfile = time.time()
                for i in range(len(liste)):
                    a = ''.join(re.findall("[^|]+$",liste[i][0]))
                    b = re.sub('[:/,\s\n]','',a)
                    giN = re.findall("[^|^>]+(?=\|)",liste[i][0])
                    gi = giN[0]+giN[1]
                    seq = open(path+b+"_"+gi+".txt","a")
                    for j in range(len(liste[i])):
                        seq.write(liste[i][j])
                    seq.close()
                    t1d = time.time()
                showinfo('Number of sequences', str(len(position))+" files have been created in "+str(round(t1d-tfile,3))+" seconds")
            if OS == "Linux" or OS == "Darwin":
                tfile = time.time()
                for i in range(len(liste)):
                    a = ''.join(re.findall("[^|]+$",liste[i][0]))
                    b = re.sub('[:/,\s\n]','',a)
                    giN = re.findall("[^|^>]+(?=\|)",liste[i][0])
                    gi = giN[0]+giN[1]
                    seq = open(path+b+"_"+gi,"a")
                    for j in range(len(liste[i])):
                        seq.write(liste[i][j])
                    seq.close()
                t1d = time.time()
                showinfo('Number of sequences', str(len(position))+" files have been created in "+str(round(t1d-tfile,3))+" seconds")
        if choice == 1:
            #RECUPERATION DU NOM DU DOSSIER
            folder = getFolderName()
            if OS == "Windows":
                path = path+"\\"+folder
                if os.path.isdir(path) == True:
                    showwarning('Warning', "The folder already exist \n or they are no folder name !\nChange or get the folder name")
                else:
                    os.mkdir(path)
                    tfile = time.time()
                    for i in range(len(liste)):
                        a = ''.join(re.findall("[^|]+$",liste[i][0]))
                        b = re.sub('[:/,\s\n]','',a)
                        giN = re.findall("[^|^>]+(?=\|)",liste[i][0])
                        gi = giN[0]+giN[1]
                        seq = open(path+"\\"+b+"_"+gi+".txt","a")
                        for j in range(len(liste[i])):
                            seq.write(liste[i][j])
                        seq.close()
                    t1d = time.time()
                    showinfo('Number of sequences', str(len(position))+" files have been created in "+str(round(t1d-tfile,3))+" seconds")
            if OS == "Linux" or OS == "Darwin":
                path = path+"/"+folder
                if os.path.isdir(path) == True:
                    showwarning('Warning', "The folder already exist \n or they are no folder name !\nChange or get the folder name")
                else:
                    os.mkdir(path)
                    tfile = time.time()
                    for i in range(len(liste)):
                        a = ''.join(re.findall("[^|]+$",liste[i][0]))
                        b = re.sub('[:/,\s\n]','',a)
                        giN = re.findall("[^|^>]+(?=\|)",liste[i][0])
                        gi = giN[0]+giN[1]
                        seq = open(path+"/"+b+"_"+gi,"a")
                        for j in range(len(liste[i])):
                            seq.write(liste[i][j])
                        seq.close()
                    t1d = time.time()
                    showinfo('Number of sequences', str(len(position))+" files have been created in "+str(round(t1d-tfile,3))+" seconds")

run = Button(fenetre, text="Run",command=createQueryFile).grid(row=13,column=3)

######
#Partie4#
######

Label(fenetre, text="Extract Reference and Sequences",pady=5).grid(row=15, columnspan=3, sticky="W")
ttk.Separator(fenetre, orient=HORIZONTAL).grid(row=15, columnspan=5, sticky="NEW")
Label(fenetre, text="Blast Result File : ").grid(row=16, column=0,sticky="E")

textEntry5 = StringVar()
entry5 = Entry(fenetre, textvariable=textEntry5,state='disabled')
entry5.grid(row=16, column=1)

pathTextEntry5 = StringVar()
pathEntry5 = Entry(fenetre, textvariable=pathTextEntry5)

textEntry6 = StringVar()
entry6 = Entry(fenetre, textvariable=textEntry6,state='disabled')
entry6.grid(row=17, column=1)

pathTextEntry6 = StringVar()
pathEntry6 = Entry(fenetre, textvariable=pathTextEntry6)

textEntry7 = StringVar()
entry7 = Entry(fenetre, textvariable=textEntry7)
entry7.grid(row=18, column=1)

#Get the value of entry5 blast result
def GetBlastFile():
    import os
    pathfile = askopenfilename(title='Open the file with Blast results')
    textEntry5.set(os.path.split(pathfile)[1])
    pathTextEntry5.set(os.path.split(pathfile)[0])

#Récupère la valeur de entry5 blast result
def callback5():
    return entry5.get()

def pathCallback5():
    return pathEntry5.get()

#Get the value of entry6 library database
def GetLibraryDatabaseFile2():
    import os
    pathfile = askopenfilename(title='Open Library Database')
    textEntry6.set(os.path.split(pathfile)[1])
    pathTextEntry6.set(os.path.split(pathfile)[0])

#Récupère la valeur de entry6 library database
def callback6():
    return entry6.get()

def pathCallback6():
    return pathEntry6.get()

#Récupère la valeur de entry7
def callback7():
    return entry7.get()

Button(fenetre, text="Browse",command=GetBlastFile).grid(row=16, column=2, columnspan=2)

Label(fenetre, text="Library Database : ").grid(row=17, column=0,sticky="E")

Button(fenetre, text="Browse",command=GetLibraryDatabaseFile2).grid(row=17, column=2, columnspan=2)

Label(fenetre, text="Output Filename : ").grid(row=18, column=0,sticky="E")

## Function ##

def extractSbjctSeqAndRef():
    """
    input : file with blast result
    output : file with the reference sequences "Sbjct"
    output2 : file with the sequence of reference "Sbjct"
    """
    import subprocess
    import os
    import re
    import platform
    OS = platform.system()
    if OS == 'Windows':
        path = os.getcwd()+"\\"
        pathBlastResult = pathCallback5()+"\\"
        pathLibrary = pathCallback6()+"\\"
    if OS == 'Linux' or OS == 'Darwin':
        path = os.getcwd()+'/'
        pathBlastResult = pathCallback5()+'/'
        pathLibrary = pathCallback6()+'/'
    liste = []
    file1 = callback5()
    if os.path.isfile(pathBlastResult+file1) != True:
        showerror('Error : Missing File !', "You must choose a Blast-result file")
    else:
        f = open(pathBlastResult+file1,"r")
        for line in f:
            if line[0] == ">":
                if line not in liste:
                    liste.append(line)
        f.close()
        if OS =="Windows":
            file2 = entry7.get()+".txt"
        else:
            file2 = entry7.get()
        if os.path.isfile(pathLibrary+file2) == True:
            showerror('Error',"Your output filename already exist, please change your filename")
        if file2 == '':
            showerror('Error: Missing Filename',"You did not choose the name of the output file")
        else:
            file3 = callback6()
            if file3 == '':
                showerror('Error : Missing File !', "You must choose the Library Database file")
            else:
                f2 = open(pathBlastResult+file2,"a")
                for i in liste:
                    a = re.sub('[>][\s]','',i)
                    f2.write(a)
                f2.close()
                if OS == 'Linux' or OS == 'Darwin':
                    t0 = time.time()
                    process = subprocess.Popen(["perl", "seqfetch.def.pl" , pathBlastResult+file2 , pathLibrary+file3], stdout=subprocess.PIPE)
                    process.communicate()
                    t1 = time.time()
                    showinfo('Time',"Your job finish in "+str(round(t1-t0,3))+" seconds")
                if OS == 'Windows':
                    t0 = time.time()
                    process = subprocess.Popen(["perl", path+"seqfetch.def.pl" , pathBlastResult+file2 , pathLibrary+file3], stdout=subprocess.PIPE)
                    process.communicate()
                    t1 = time.time()
                    showinfo('Time',"Your job finish in "+str(round(t1-t0,3))+" seconds")
                showinfo('Information','The files '+file2+' and '+file2+".seq.txt\nhave been created in :\n"+pathBlastResult)

Button(fenetre, text="Run",command=extractSbjctSeqAndRef).grid(row=18,column=2, columnspan=2)

######
#Partie5#
######

#Variable et création des boutons radio
var5 = IntVar()
for item in [1,2]:
    Label(fenetre, text="Type :").grid(row=20, column=0, sticky="W",padx=30)
    if item == 1:
        rb = Radiobutton(fenetre, text='Nucleotides',value=item,variable=var5).grid(row=20, column=0,sticky="E")
    if item == 2:
        rb = Radiobutton(fenetre, text='Proteins',value=item,variable=var5).grid(row=20, column=1,sticky="W")

#Récuperation de la valeur du bouton radio (Nucleotides/Proteines)
def typeNP5():
    return var5.get()

Label(fenetre, text="Blast all individual Query File",pady=5).grid(row=19, columnspan=3, sticky="W")
ttk.Separator(fenetre, orient=HORIZONTAL).grid(row=19, columnspan=5, sticky="NEW")
Label(fenetre, text="Library Database : ").grid(row=21, column=0,sticky="E")

Label(fenetre, text="Files with sequences : ").grid(row=22, column=0,sticky="E")

textEntry8 = StringVar()
entry8 = Entry(fenetre, textvariable=textEntry8,state='disabled')
entry8.grid(row=21, column=1)

pathTextEntry8 = StringVar()
pathEntry8 = Entry(fenetre, textvariable=pathTextEntry8)

textEntry9 = StringVar()
entry9 = Entry(fenetre, textvariable=textEntry9,state='disabled')
entry9.grid(row=22, column=1)

pathTextEntry9 = StringVar()
pathEntry9 = Entry(fenetre, textvariable=pathTextEntry9)

#Fonction pour le bouton browse cherche et récupère le nom du fichier
def GetLibraryDatabaseFile3():
    import os
    pathfile = askopenfilename(title='Open Library Datafile')
    textEntry8.set(os.path.split(pathfile)[1])
    pathTextEntry8.set(os.path.split(pathfile)[0])

Button(fenetre, text="Browse",command=GetLibraryDatabaseFile3).grid(row=21, column=2)

def GetSequenceFile3():
    import os
    pathfile = askopenfilename(title='Open File with Sequences')
    textEntry9.set(os.path.split(pathfile)[1])
    pathTextEntry9.set(os.path.split(pathfile)[0])

Button(fenetre, text="Browse",command=GetSequenceFile3).grid(row=22, column=2)

#Récupère la valeur de entry8
def callback8():
    return entry8.get()

def pathCallback8():
    return pathEntry8.get()

#Récupère la valeur de entry9
def callback9():
    return entry9.get()

def pathCallback9():
    return pathEntry9.get()

#comand check button
folderVar2 = StringVar()
folderEntry2 = Entry(fenetre,width=30, textvariable=folderVar2)
def checkButtonEntry2():
    if checkButtonVar2.get() == 1:
        folderEntry2.grid(row = 23, column=1, columnspan=2, sticky="W")
        previousFolder = getFolderName()
        folderEntry2.insert(0, previousFolder)
    else :
        folderEntry2.delete(0, END)
        folderEntry2.grid_forget()
        
#IntVar du check button
checkButtonVar2 = IntVar()
checkButton2 = Checkbutton(fenetre, text="In a folder ?", variable=checkButtonVar2, command=checkButtonEntry2)
checkButton2.grid(row=23,column=0)

#recupere le nom du dossier
def getFolderName2():
    return folderEntry2.get()

#####
#fonctions
#####

def Filename(OS):
    import re
    filename1 = []
    filename2 = []
    name = callback9()
    if OS == 'Linux' or OS == 'Darwin':
        #path = os.getcwd()+'/'
        path = pathCallback9()+'/'
    if OS == 'Windows':
        #path = os.getcwd()+'\\'
        path = pathCallback9()+'\\'
    if os.path.isfile(path+name) != True:
        showerror('Error : Missing File !', "You must choose your Sequences file")
    else:
        #f = open(name,'r')
        f = open(path+name,'r')
        for i in f:
            if i[0] == ">":
                filename1.append(i)
        f.close()
        for i in range(len(filename1)):
            a = ''.join(re.findall("[^|]+$",filename1[i]))
            b = re.sub('[:/,\s\n]','',a)
            giN = re.findall("[^|^>]+(?=\|)",filename1[i])
            gi = giN[0]+giN[1]
            filename2.append(b+"_"+gi)
        return filename2

def Blast():
    """
    Blast the Query file into the local database librairy
    """
    import subprocess
    import platform
    import time
    OS = platform.system()
    if OS == 'Linux' or OS == 'Darwin':
        pathLibrary = pathCallback8()+'/'
        pathQuery = pathCallback9()+'/'
        extention = ""
    if OS == 'Windows':
        pathLibrary = pathCallback8()+'\\'
        pathQuery = pathCallback9()+'\\'
        extention = ".txt"
    typ = str(typeNP5())
    if typ != '1' and typ != '2':
        showerror('Error : Missing Type !', "You do not choose your type\n(nucleotides or proteins)")
    else:
        #evalue = input("Choose your e-value limit : ")
        if typ =="1":
            typ = "tblastn"
        else:
            typ = "blastp"
        DB = callback8()
        if os.path.isfile(pathLibrary+DB) != True:
            showerror('Error : Missing File !', "You must choose the Library Database file")
        else:
            filename = Filename(OS)
            if filename != None:
                if os.path.isfile(pathQuery+filename[0]+extention) != True:
                    showerror('Error : Missing File !', "Query file corresponding to sequences were not found.\nChoose Query file or Create Query files with your Sequence file")
                else:
                    #debut bar de progression
                    lab = Label(fenetre, text="Blast in progress...")
                    lab.grid(row=24, columnspan=4)
                    progressbarBlast = ttk.Progressbar(orient=HORIZONTAL, length=400, mode='determinate', variable=1, maximum=0, value=0)
                    progressbarBlast.grid(row=25,columnspan=4,pady=2,sticky=W+E)
                    progressbarBlast["maximum"]=len(filename)
                    progressbarBlast["value"]=0
                    progressbarBlast.update()
                    File = StringVar()
                    nFile = StringVar()
                    nFileLabel = Label(fenetre, textvariable=nFile)
                    nFileLabel.grid(row=26,columnspan=4)
                    fileLabel = Label(fenetre, textvariable=File)
                    fileLabel.grid(row=27,columnspan=4)
                    #fin
                    if OS == 'Linux' or OS == 'Darwin':
                        Dir = checkButtonVar2.get()
                        if Dir == 0: 
                            t0 = time.time()
                            if not os.path.exists(pathQuery+"out-blast"):
                                os.mkdir(pathQuery+"out-blast")
                            if not os.path.exists(pathQuery+"out-seqs"):
                                os.mkdir(pathQuery+"out-seqs")
                            pathBlast = pathQuery+"out-blast/"
                            pathSeqs = pathQuery+"out-seqs/"
                            print(str(len(filename))+" files are being analyzed")
                            for i in range(len(filename)):
                                query = filename[i]
                                blast = filename[i]+'_Blast'
                                seqs = filename[i]+'_seqs'
                                sub1 = time.time()
                                #BARRE DE PROGRESION
                                nFile.set("File "+str(i+1)+"/"+str(len(filename)))
                                File.set(filename[i])
                                progressbarBlast.update()
                                subprocess.call(typ+" -query "+pathQuery+query+" -db "+pathLibrary+DB+" -evalue 1e-10 -out "+pathBlast+blast, shell=True)
                                val = i+1
                                progressbarBlast["value"]= val
                                progressbarBlast.update()
                                #FIN BARRE
                                subprocess.call("grep '\(Sbjct\|>\)' "+pathBlast+blast+" > "+pathSeqs+seqs, shell=True)
                                sub2 = time.time()
                                print('Fichier n° '+str(filename.index(filename[i])+1)+' '+str(filename[i])+' in '+str(sub2-sub1)+' seconds')
                            t1 = time.time()
                            showinfo('Information',"Your job finish in\n"+str(round(t1-t0,3))+" seconds")
                        # QUERY FILES ARE IN A FOLDER
                        # à été corrigé :
                        if Dir == 1:
                            t0 = time.time()
                            folder = getFolderName2()
                            pathQueryFolder = pathQuery+folder+"/" 
                            if not os.path.exists(pathQueryFolder+"out-blast"):
                                os.mkdir(pathQueryFolder+"out-blast")
                            if not os.path.exists(pathQueryFolder+"out-seqs"):
                                os.mkdir(pathQueryFolder+"out-seqs")
                            pathBlast = pathQueryFolder+"out-blast/"
                            pathSeqs = pathQueryFolder+"out-seqs/"
                            for i in range(len(filename)):
                                query = filename[i]
                                blast = filename[i]+'_Blast'
                                seqs = filename[i]+'_seqs'
                                sub1 = time.time()
                                #BARRE DE PROGRESION
                                nFile.set("File "+str(i+1)+"/"+str(len(filename)))
                                File.set(filename[i])
                                progressbarBlast.update()
                                subprocess.call(typ+" -query "+pathQueryFolder+query+" -db "+pathLibrary+DB+" -evalue 1e-10 -out "+pathBlast+blast, shell=True)
                                val = i+1
                                progressbarBlast["value"] = val
                                progressbarBlast.update()
                                #FIN BARRE
                                subprocess.call("grep '\(Sbjct\|>\)' "+pathBlast+blast+" > "+pathSeqs+seqs, shell=True)
                                sub2 = time.time()
                                print('Fichier n° '+str(filename.index(filename[i])+1)+' '+str(filename[i])+' in '+str(sub2-sub1)+' seconds')
                            t1 = time.time()
                            showinfo('Information',"Your job finish in\n"+str(round(t1-t0,3))+" seconds")
                    if OS == 'Windows': 
                        Dir = checkButtonVar2.get()
                        if Dir == 0:
                            t0 = time.time()
                            if not os.path.exists(pathQuery+"out-blast"):
                                os.mkdir(pathQuery+"out-blast")
                            if not os.path.exists(pathQuery+"out-seqs"):
                                os.mkdir(pathQuery+"out-seqs")
                            pathBlast = pathQuery+"out-blast\\"
                            pathSeqs = pathQuery+"out-seqs\\"
                            print(str(len(filename))+" files are being analyzed")
                            for i in range(len(filename)):
                                query = filename[i]+'.txt'
                                blast = filename[i]+'_Blast.txt'
                                seqs = filename[i]+'_seqs.txt'
                                sub1 = time.time()
                                #BARRE DE PROGRESION
                                nFile.set("File "+str(i+1)+"/"+str(len(filename)))
                                File.set(filename[i])
                                progressbarBlast.update()
                                process1 = subprocess.Popen(typ+' -query '+pathQuery+query+' -db '+pathLibrary+DB+' -evalue 1e-10 -out '+pathBlast+blast, shell=True)
                                process1.communicate()
                                val = i+1
                                progressbarBlast["value"]= val
                                progressbarBlast.update()
                                #FIN BARRE
                                process2 = subprocess.Popen('findstr "Sbjct >" '+pathBlast+blast+' > '+pathSeqs+seqs, shell=True)
                                process2.communicate()
                                sub2 = time.time()
                                print('Fichier n° '+str(filename.index(filename[i])+1)+' '+str(filename[i])+' in '+str(sub2-sub1)+' seconds')
                            t1 = time.time()
                            showinfo('Information',"Your job finish in\n"+str(round(t1-t0,3))+" seconds")
                        if Dir == 1:
                            t0 = time.time()
                            folder = getFolderName2()
                            pathQueryFolder = pathQuery+folder+"\\"
                            if not os.path.exists(pathQueryFolder+"out-blast"):
                                os.mkdir(pathQueryFolder+"out-blast")
                            if not os.path.exists(pathQueryFolder+"out-seqs"):
                                os.mkdir(pathQueryFolder+"out-seqs")
                            pathBlast = pathQueryFolder+"out-blast\\"
                            pathSeqs = pathQueryFolder+"out-seqs\\"
                            for i in range(len(filename)):
                                query = filename[i]+'.txt'
                                blast = filename[i]+'_Blast.txt'
                                seqs = filename[i]+'_seqs.txt'
                                sub1 = time.time()
                                #BARRE DE PROGRESION
                                nFile.set("File "+str(i+1)+"/"+str(len(filename)))
                                File.set(filename[i])
                                progressbarBlast.update()
                                process1 = subprocess.Popen(typ+' -query '+pathQueryFolder+query+' -db '+pathLibrary+DB+' -evalue 1e-10 -out '+pathBlast+blast, shell=True)
                                process1.communicate()
                                val = i+1
                                progressbarBlast["value"]= val
                                progressbarBlast.update()
                                #FIN BARRE
                                process2 = subprocess.Popen('findstr "Sbjct >" '+pathBlast+blast+' > '+pathSeqs+seqs, shell=True)
                                process2.communicate()
                                sub2 = time.time()
                                print('Fichier n° '+str(filename.index(filename[i])+1)+' '+str(filename[i])+' in '+str(sub2-sub1)+' seconds')
                            t1 = time.time()
                            print('Job finish in '+str(t1-t0)+' seconds')
                            showinfo('Information',"Your job finish in\n"+str(round(t1-t0,3))+" seconds")
    lab.grid_forget()
    progressbarBlast.grid_forget()
    nFileLabel.grid_forget()
    fileLabel.grid_forget()

Button(fenetre, text="Run",command=Blast).grid(row=21,column=3, rowspan=2)

fenetre.mainloop()
