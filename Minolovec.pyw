import sys

if sys.version_info[0] == 2: #Python 2.7.x
    from Tkinter import *
    import ttk
    import tkMessageBox as messagebox
    import tkFileDialog as filedialog
    from tkColorChooser import askcolor
    import urllib2
else:
    from tkinter import *
    from tkinter import messagebox
    from tkinter import filedialog
    from tkinter.colorchooser import *
    from tkinter import ttk
    import urllib.request as urllib2
import random
import time
import webbrowser

#Konstante
VRSTICE = 10
STOLPCI = 10
MINE = 10
POKAZI = True #False Ne prikazuje števila min, uro v glavnem oknu, True prikazuje.
NEPOKAZI_ST = False

#Barve
C1 = 'green'
C2='green yellow'
C3='blue'
C4='red'

class Gumb:
    def __init__(self, gumb, mina, sosedi, vrstica, stolpec):
        self.gumb = gumb
        self.mina = mina
        self.sosedi = sosedi
        self.vrstica=vrstica
        self.stolpec=stolpec

    def __repr__(self):
        return 'Gumb({0}, {1}, {2}, {3}, {4})'.format(self.gumb, self.mina, self.sosedi, self.vrstica, self.stolpec)

class Minesweeper():
    def __init__(self, master, vrstice,stolpci,mine, nevidne_st, pokazi,c1,c2,c3,c4):
        self.pokazi = pokazi
        self.c1=c1
        self.c2=c2
        self.c3=c3
        self.c4=c4
        self.nevidne_st = nevidne_st
        self.master = master
        self.st_vrstic = vrstice
        self.st_stolpcev = stolpci
        self.mines = mine
        self.sez_praznih = [] #tu notri pospravimo gumbe, ki nimajo min.
        #Nastavi nove vrednosti -Podatke uporabi iz nastavitev
        self.st_vrstic1234 = vrstice
        self.st_stolpcev1234 = stolpci
        self.mines1234=mine
        # Full screen app
        self.state = False
        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Escape>", self.end_fullscreen)

        #konfiguracija menija
        self.menu = Menu(self.master)
        master.config(menu=self.menu)

        # game menu
        filemenu = Menu(self.menu, tearoff=0)
        filemenu.add_command(label="Nova igra", command=self.nova)
        filemenu.add_command(label="Odpri", command=self.file_open)
        filemenu.add_command(label="Shrani", command=self.file_save)
        filemenu.add_separator()
        filemenu.add_command(label="Izhod", command=self.master.destroy)
        self.menu.add_cascade(label="Igra", menu=filemenu)

        # create more pulldown menus
        levelmenu = Menu(self.menu, tearoff=1)
        levelmenu.add_command(label="Po meri", command=self.nastavitve)
        levelmenu.add_command(label="Obrni", command=self.obrni)
        levelmenu.add_separator()
        levelmenu.add_command(label="Lahka", command=self.lahka)
        levelmenu.add_command(label="Srednje težka", command=self.srednja)
        levelmenu.add_command(label="Težka", command=self.tezka)
        levelmenu.add_command(label="Zelo težka", command=self.zelo_tezka)
        self.menu.add_cascade(label="Težavnost", menu=levelmenu)

        netmenu = Menu(self.menu, tearoff=0)
        netmenu.add_command(label='Github',command=self.preveri_posodobitve)
        self.menu.add_cascade(label="Internet", menu=netmenu)

        # display the menu
        self.master.config(menu=self.menu)

        self.nova_igra()

    def preveri_posodobitve(self):
        '''Preveri ali obstajajo posodobitve na githubu'''
        url = 'https://github.com/martincesnovar/Minolovec'
        vir = urllib2.urlopen(url)
        webbrowser.open_new(url)

    def file_save(self):
        '''Shrani gumbe'''
        name=filedialog.asksaveasfile(mode='w',defaultextension=".txt", filetypes=[('Text Files', '*.txt')])
        #self.sez_praznih
        name.write('{0} {1}\n'.format(self.st_vrstic1234, self.st_stolpcev1234))
        for el in self.izbrane_mine:
            text2save=str(el)+ ' '
            name.write(text2save)
        name.close

    def file_open(self):
        '''Naloži igro iz datoteke'''
        file_path = filedialog.askopenfilename(filetypes=[('All', '*.*'),('Text Files', '*.txt')])
        self.nova_igra()
        with open(file_path) as f:
            self.st_vrstic1234, self.st_stolpcev1234 = map(int, f.readline().split())
            self.izbrane_mine = map(int,f.readline().split())
            

    def skrij_uro(self):
        self.pokazi = not self.pokazi

    def nova(self):
        self.t1=time.time()
        self.konec_igre(False)

    def lahka(self):
        '''ustvari 10*10 veliko polje z 10 minami'''
        self.st_vrstic1234 = 10
        self.st_stolpcev1234 = 10
        self.mines1234=10
        self.nevidne_st = False
        self.t1=time.time()
        self.konec_igre(False)

    def srednja(self):
        '''ustvari 15*15 veliko polje z 50 minami'''
        self.st_vrstic1234 = 15
        self.st_stolpcev1234 = 15
        self.mines1234=50
        self.nevidne_st = False
        self.t1=time.time()
        self.konec_igre(False)
        
    def tezka(self):
        '''ustvari 24*30 veliko polje z 688 minami'''
        self.st_vrstic1234 = 24
        self.st_stolpcev1234 = 30
        self.mines1234=668
        self.nevidne_st = False
        self.t1=time.time()
        self.konec_igre(False)

    def zelo_tezka(self):
        '''ustvari 24*30 veliko polje z 688 minami z izklopljenimi številkami'''
        self.tezka()
        self.nevidne_st=True

    def obrni(self):
        '''Obrne število min'''
        polje = self.st_vrstic1234*self.st_stolpcev1234
        self.mines1234 = polje - self.mines1234
        self.t1=time.time()
        self.konec_igre(False)

    def nastavitve(self):
        okno = Nastavitve(self)

    def zbrisi_polje(self):
        '''Zbriše polje'''
        for vrstica in range(self.st_vrstic):
            for stolpec in range(self.st_stolpcev):
                self.buttons[vrstica][stolpec].gumb.destroy()
        self.buttons=None

    def nova_igra(self):
        self.sez_praznih = []
        self.prvic = True
        #Uporabi podatke iz okna nastavitve
        self.mines=self.mines1234
        self.st_vrstic = self.st_vrstic1234
        self.st_stolpcev = self.st_stolpcev1234
        self.buttons = [[None for i in range(self.st_stolpcev)] for j in range(self.st_vrstic)]
        self.izbrane_mine = random.sample([i for i in range(self.st_vrstic * self.st_stolpcev)], self.mines1234)
        self.st_nepoklikanih = self.st_vrstic * self.st_stolpcev
        num_proximity_mines = 0
        frame = Frame(self.master)
        Grid.rowconfigure(self.master, 0, weight=1)
        Grid.columnconfigure(self.master, 0, weight=1)
        
        #Dodamo polje za število min in čas
        
        if self.pokazi: #pokaže/skrije število min in uro.
            var = StringVar()
            var.set('Število min: ' + str(self.mines))
            l = Label(self.master, textvariable=var, anchor=NW, justify=LEFT, wraplength=398)
            l.grid(row=0, column=0, columnspan=10, sticky = N + S + E +W)
            self.now=-1
            self.label = Label(self.master,text=self.now,anchor=NW, justify=LEFT, wraplength=398)
            self.label.grid(row=0, column=2, columnspan=10, sticky = N + S + E +W)
            self.update_clock()
            
        frame.grid(row=1, column=0, sticky = N + S + E + W) if self.pokazi else frame.grid(row=0, column=0, sticky = N + S + E + W)
##        self.label1 = Label(frame, text="Minesweeper")
##        self.label1.grid(row=0, column=0, columnspan=10)
        st = 0
        for vrstica in range(self.st_vrstic):
            Grid.rowconfigure(frame, vrstica, weight=1)
            for stolpec in range(self.st_stolpcev):
                Grid.columnconfigure(frame, stolpec, weight=1)
                mine = False
                if st in self.izbrane_mine:
                    mine = True                   
  
                gumb = Gumb(Button(frame, bg=self.c1, width=3), mine, num_proximity_mines, vrstica, stolpec)  # Objekt

                if mine == False: #Prazne mine doda v seznam - da "premaknem" mino.
                    self.sez_praznih.append(gumb)               

                self.buttons[vrstica][stolpec] = gumb
                # GLUPI PYTHON NAROBE DELA SPREMENLJIVKE V LAMBDAH
                self.buttons[vrstica][stolpec].gumb.bind('<Button-1>',
                                                         (lambda v, s: lambda e: self.lclick(v, s))(vrstica, stolpec))
                self.buttons[vrstica][stolpec].gumb.bind('<Button-3>',
                                                         (lambda v, s: lambda e: self.rclick(v, s))(vrstica, stolpec))
                self.buttons[vrstica][stolpec].gumb.grid(row=vrstica, column=stolpec, sticky=N + S + E + W)
                st+=1

        for v in range(self.st_vrstic):
            for s in range(self.st_stolpcev):
                self.buttons[v][s].sosedi = self.sosednje_mine(v, s)

        self.master.attributes("-topmost", True)

    def update_clock(self):
        if not self.prvic:
            self.now = -1
        self.now += 1
        
        self.label.configure(text=self.now)
        if self.prvic:
            self.label.after(1000, self.update_clock)
        
    def sosedi(self, vrstica, stolpec):
        sez = [(vrstica - 1, stolpec - 1), (vrstica - 1, stolpec), (vrstica - 1, stolpec + 1),
               (vrstica, stolpec - 1), (vrstica, stolpec + 1),
               (vrstica + 1, stolpec - 1), (vrstica + 1, stolpec), (vrstica + 1, stolpec + 1)]
        return [(v, s) for (v, s) in sez if 0 <= v < self.st_vrstic and 0 <= s < self.st_stolpcev]

    def sosednje_mine(self, vrstica, stolpec):
        """Stevilo sosednjih polj, ki so mina"""
        m = 0
        for (v, s) in self.sosedi(vrstica, stolpec):
            if self.buttons[v][s].mina == 1: m += 1
        return m

    def lclick(self, vrstica, stolpec, preveri_konec=True):
        prva = self.st_nepoklikanih == self.st_vrstic*self.st_stolpcev #ali je prva poteza?
        if prva: self.t1 = time.time()

        sez = self.buttons[vrstica][stolpec]
        if sez.gumb["bg"] == self.c1:
            # polje se ni odkrito, ga odkrijemo
            self.st_nepoklikanih -= 1
            sez.sosedi = self.sosednje_mine(vrstica, stolpec)
            #Stopimo na mino v 1. koraku
            #Na igralnem polju je 1 mina manj.
            if sez.mina == True and prva == True:
                sez.mina= False
                #self.mines-=1

                #Dodamo še 1 mino, ker smo jo kliknili v 1. potezi
                izbrana = random.choice(self.sez_praznih)
                izbrana.mina = True
                sez.sosedi = self.sosednje_mine(vrstica, stolpec)
                #self.mines += 1
                
                m = sez.sosedi  # stevilo sosednjih min
                if m != 0 or sys.platform =="darwin":
                    if self.nevidne_st == False:
                        sez.gumb.config(text=str(m))
                    else:
                        sez.gumb.config(text='')
                        
                sez.gumb.config(bg=self.c2)
            elif sez.mina == 1:
                # stopili smo na mino
                for i in range(len(self.buttons)):
                    for x in range(len(self.buttons[i])):
                        if self.buttons[i][x].mina == 1:
                            self.buttons[i][x].gumb.config(bg=self.c4, text='*')
                            preveri_konec = False
                self.konec_igre(False)
            else:
                # polje je bilo prazno
                m = sez.sosedi  # stevilo sosednjih min
                if m != 0 or sys.platform == "darwin":
                    if self.nevidne_st == False:
                        sez.gumb.config(text=str(m))
                    else:
                        sez.gumb.config(text='')
                        if m == 0 and sys.platform == "darwin": #Označi odprte
                            sez.gumb.config(text=str(m))
                        
                sez.gumb.config(bg=self.c2)
                if m == 0:
                    for (v, s) in self.sosedi(vrstica, stolpec):
                        self.lclick(v, s, preveri_konec=False)

        # ali je konec igre?
        if preveri_konec and self.st_nepoklikanih-self.mines == 0:
            self.konec_igre(True)
            
    def rclick(self, vrstica, stolpec):
        sez = self.buttons[vrstica][stolpec]
        if sez.gumb["bg"] == self.c1:
            sez.gumb.config(bg=self.c3, text=chr(9873) if sys.version_info[0] == 3 and TkVersion >= 8.6 else ':)')
            self.st_nepoklikanih -= 1
            if sez.mina == True:
                self.mines -= 1

        elif sez.gumb["bg"] == self.c3:
            if sez.mina == True:
                self.mines += 1
            self.st_nepoklikanih += 1
            sez.gumb.config(bg=self.c1, text="")

        if self.st_nepoklikanih == 0 and self.mines == 0:
            self.konec_igre(True)

    def konec_igre(self, od_kje):
        self.prvic = False
        self.t2 = time.time()
        if od_kje:
            result = messagebox.askyesno('Winner!', 'Igram znova?\nČas igranja {0}'.format(int(self.t2-self.t1)))
        else:
            result = messagebox.askyesno('Looser!', 'Igram znova?\nČas igranja {0}'.format(int(self.t2-self.t1)))
        if result:
            self.zbrisi_polje()
            self.nova_igra()
        else:
            self.master.destroy()

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.master.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.master.attributes("-fullscreen", False)
        return "break"

class Nastavitve():
    def __init__(self, minesweeper):
        self.minesweeper = minesweeper
        self.minesweeper.prvic = False #Štoparica
        self.top = Toplevel()
        self.top.title("Nastavi")
        self.top.attributes("-topmost", True)

        frame = Frame(self.top)

        frame.pack()

        Label(frame, text="Število vrstic").grid(row=0, column=0, sticky=W)
        Label(frame, text="Število stolpcev").grid(row=1, column=0, sticky=W)
        Label(frame, text="Število min").grid(row=2, column=0, sticky=W)
        self.e1 = ttk.Entry(frame)
        self.e2 = ttk.Entry(frame)
        self.e3 = ttk.Entry(frame)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)

        self.var = IntVar()
        c = ttk.Checkbutton(self.top, text="Skrij številke", variable=self.var)
        c.pack()


        c1 = Button(self.top, text = 'Neodkriti', command = self.getColor1, bg = self.minesweeper.c1)
        c1.pack()

        c2 = Button(self.top, text = 'Odkriti', command = self.getColor2, bg = self.minesweeper.c2)
        c2.pack()

        c3 = Button(self.top, text = 'Zastava', command = self.getColor3, bg = self.minesweeper.c3)
        c3.pack()

        c4 = Button(self.top, text = 'Mina', command = self.getColor4, bg = self.minesweeper.c4)
        c4.pack()
        
        b = ttk.Button(self.top, text="OK", command=self.callback)
        self.top.bind("<Return>", self.callback)
        b.pack()


    def getColor1(self):
        self.minesweeper.c1 = askcolor()[1]
    def getColor2(self):
        self.minesweeper.c2 = askcolor()[1]
    def getColor3(self):
        self.minesweeper.c3 = askcolor()[1]
    def getColor4(self):
        self.minesweeper.c4 = askcolor()[1]

    def callback(self,event=None):
        '''Dobi podatke iz okna če obstajajo, sicer ohrani stare vrednosti'''
                
        self.e1.get1 = self.e1.get() or self.minesweeper.st_vrstic1234
        self.e2.get2 = self.e2.get() or self.minesweeper.st_stolpcev1234
        self.e3.get3 = self.e3.get() or self.minesweeper.mines1234
        
        self.minesweeper.st_vrstic1234 = max(int(self.e1.get1),1)
        self.minesweeper.st_stolpcev1234 = max(int(self.e2.get2),1)
        self.minesweeper.mines1234 = max(min(int(self.e3.get3),self.minesweeper.st_stolpcev1234*self.minesweeper.st_vrstic1234 - 1),0) #Število min ne sme biti večje od velikosti igralnega polja
        self.minesweeper.nevidne_st = self.var.get()

        self.top.destroy()
        
        self.minesweeper.zbrisi_polje()
        self.minesweeper.nova_igra()

#Glavni program
root = Tk()
root.title('Minolovec')
minesweeper = Minesweeper(root,VRSTICE,STOLPCI,MINE, NEPOKAZI_ST, POKAZI,C1,C2,C3,C4)
root.mainloop()
