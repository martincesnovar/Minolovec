import sys

if sys.version_info[0] == 2: #Python 2.7.x
    from Tkinter import *
    import tkMessageBox as messagebox
else:
    from tkinter import *
    from tkinter import messagebox
import random
import time

#Zdaj iz msgbox-a in iz okna nastavitve čas teče pravilno, popraviti še iz težavnosti

#Konstante
VRSTICE = 10
STOLPCI = 10
MINE = 10
POKAZI = True #False Ne prikazuje števila min, uro v glavnem oknu, True prikazuje.
POKAZI_ST = False

class Gumb:
    def __init__(self, gumb, mina, sosedi):
        self.gumb = gumb
        self.mina = mina
        self.sosedi = sosedi

    def __repr__(self):
        return 'Gumb({0}, {1}, {2})'.format(self.gumb, self.mina, self.sosedi)

class Minesweeper():
    def __init__(self, master, vrstice,stolpci,mine, vidne_st, pokazi):
        self.POKAZI = pokazi
        self.vidne_st = vidne_st
        self.master = master
        self.st_vrstic = vrstice
        self.st_stolpcev = stolpci
        self.mines = mine
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
        filemenu.add_command(label="Nova igra", command=self.nova_igra)
        filemenu.add_command(label="Štoparica", command=self.stoparica)
        filemenu.add_separator()
        filemenu.add_command(label="Izhod", command=self.master.destroy)
        self.menu.add_cascade(label="Igra", menu=filemenu)

        # create more pulldown menus
        levelmenu = Menu(self.menu, tearoff=1)
        levelmenu.add_command(label="Po meri", command=self.nastavitve)
        levelmenu.add_separator()
        levelmenu.add_command(label="Lahka", command=self.lahka)
        levelmenu.add_command(label="Srednje težka", command=self.srednja)
        levelmenu.add_command(label="Težka", command=self.tezka)
        levelmenu.add_command(label="Zelo težka", command=self.zelo_tezka)
        self.menu.add_cascade(label="Težavnost", menu=levelmenu)

        # display the menu
        self.master.config(menu=self.menu)

        self.nova_igra()

    def lahka(self):
        '''ustvari 10*10 veliko polje z 10 minami'''
        self.prvic = False
        self.st_vrstic1234 = 10
        self.st_stolpcev1234 = 10
        self.mines1234=10
        self.vidne_st = False
        self.nova_igra()

    def srednja(self):
        '''ustvari 15*15 veliko polje z 50 minami'''
        self.prvic = False
        self.st_vrstic1234 = 15
        self.st_stolpcev1234 = 15
        self.mines1234=50
        self.vidne_st = False
        self.nova_igra()
        
    def tezka(self):
        '''ustvari 24*30 veliko polje z 688 minami'''
        self.prvic = False
        self.st_vrstic1234 = 24
        self.st_stolpcev1234 = 30
        self.mines1234=668
        self.vidne_st = False
        self.nova_igra()

    def zelo_tezka(self):
        '''ustvari 24*30 veliko polje z 688 minami z izklopljenimi številkami'''
        self.prvic = False
        self.st_vrstic1234 = 24
        self.st_stolpcev1234 = 30
        self.mines1234=668
        self.vidne_st = True #Skrij številke
        self.prvic = False
        self.nova_igra()

    def stoparica(self):
        okno = Timer(self)

    def nastavitve(self):
        okno = Nastavitve(self)

    def zbrisi_polje(self):
        '''Zbriše polje'''
        for vrstica in range(self.st_vrstic):
            for stolpec in range(self.st_stolpcev):
                self.buttons[vrstica][stolpec].gumb.destroy()
        self.buttons=None

    def nova_igra(self):
        self.prvic = True
        #Uporabi podatke iz okna nastavitve
        self.mines=self.mines1234
        self.st_vrstic = self.st_vrstic1234
        self.st_stolpcev = self.st_stolpcev1234
        self.buttons = [[None for i in range(self.st_stolpcev)] for j in range(self.st_vrstic)]
        self.izbrane_mine = random.sample([i for i in range(self.st_vrstic * self.st_stolpcev)], self.mines1234)
        self.st_poklikanih = self.st_vrstic * self.st_stolpcev
        # print("nova igra")
        num_proximity_mines = 0
        frame = Frame(self.master)
        Grid.rowconfigure(self.master, 0, weight=1)
        Grid.columnconfigure(self.master, 0, weight=1)
        
        #Dodamo polje za število min in čas
        
        if self.POKAZI:
            var = StringVar()
##            var.trace("w", callback)
            var.set('Število min: ' + str(self.mines))
##            self.label2 = Label(frame, variable = var)
            
            l = Label(self.master, textvariable=var, anchor=NW, justify=LEFT, wraplength=398)
            l.grid(row=0, column=0, columnspan=10, sticky = N + S + E +W)
##            self.label2.pack()
##            self.label2.grid(row=0, column=0, columnspan=10, sticky = N + S + E +W)
            self.now=0
            self.label = Label(self.master,text=self.now,anchor=NW, justify=LEFT, wraplength=398)
            self.label.grid(row=0, column=2, columnspan=10, sticky = N + S + E +W)
            self.update_clock()

    

            
##            self.label2.grid(row = 0, column = 0, columnspan = 10)

        
        frame.grid(row=1, column=0, sticky = N + S + E + W) if self.POKAZI else frame.grid(row=0, column=0, sticky = N + S + E + W)
        self.label1 = Label(frame, text="Minesweeper")
        self.label1.grid(row=0, column=0, columnspan=10)
        st = 0
        for vrstica in range(self.st_vrstic):
            Grid.rowconfigure(frame, vrstica, weight=1)
            for stolpec in range(self.st_stolpcev):
                Grid.columnconfigure(frame, stolpec, weight=1)
                mine = False
                if st in self.izbrane_mine:
                    mine = True

                gumb = Gumb(Button(frame, bg="green", width=3), mine, num_proximity_mines)  # Objekt

                self.buttons[vrstica][stolpec] = gumb
                # GLUPI PYTHON NAROBE DELA SPREMENLJIVKE V LAMBDAH
                self.buttons[vrstica][stolpec].gumb.bind('<Button-1>',
                                                         (lambda v, s: lambda e: self.lclick(v, s))(vrstica, stolpec))
                self.buttons[vrstica][stolpec].gumb.bind('<Button-2>',
                                                         (lambda v, s: lambda e: self.sclick(v, s))(vrstica, stolpec))
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
            self.now = 0
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
        prva = self.st_poklikanih == self.st_vrstic*self.st_stolpcev
        if prva: self.t1 = time.time()

        sez = self.buttons[vrstica][stolpec]
        # print(sez)
        if sez.gumb["bg"] == "green":
            # polje se ni odkrito, ga odkrijemo
            self.st_poklikanih -= 1
            #Stopimo na mino v 1. koraku
            #Na igralnem polju je 1 mina manj
            if sez.mina == 1 and prva == True:
                sez.mina=0
                self.mines-=1
                m = sez.sosedi  # stevilo sosednjih min
                if m != 0 or sys.platform =="darwin":
                    if self.vidne_st == False:
                        sez.gumb.config(text=str(m))
                    else:
                        sez.gumb.config(text='')
                        
                sez.gumb.config(bg="green yellow")
            elif sez.mina == 1:
                # stopili smo na mino
                for i in range(len(self.buttons)):
                    for x in range(len(self.buttons[i])):
                        if self.buttons[i][x].mina == 1:
                            self.buttons[i][x].gumb.config(bg="red", text='*')
                            preveri_konec = False
                self.konec_igre(False)
            else:
                # polje je bilo prazno
                m = sez.sosedi  # stevilo sosednjih min
                if m != 0 or sys.platform == "darwin":
                    if self.vidne_st == False:
                        sez.gumb.config(text=str(m))
                    else:
                        sez.gumb.config(text='')
                        
                sez.gumb.config(bg="green yellow")
                if m == 0:
                    # print ("odpiramo sosede od {0}".format((vrstica,stolpec)))
                    for (v, s) in self.sosedi(vrstica, stolpec):
                        self.lclick(v, s, preveri_konec=False)

        # ali je konec igre?
        if preveri_konec and self.st_poklikanih-self.mines == 0:
            self.konec_igre(True)
        return True

    def sclick(self, vrstica, stolpec):
        '''Odpira še sosednje mine Experimentalno'''
        self.lclick(vrstica, stolpec,False)
        self.lclick(vrstica-1, stolpec,False)
        self.lclick(vrstica, stolpec-1,False)
        self.lclick(vrstica-1, stolpec-1,False)
        self.lclick(vrstica+1, stolpec,False)
        self.lclick(vrstica, stolpec+1,False)
        self.lclick(vrstica+1, stolpec+1,False)
        self.lclick(vrstica+1, stolpec-1,False)
        self.lclick(vrstica-1, stolpec+1,False)

    def rclick(self, vrstica, stolpec):
        sez = self.buttons[vrstica][stolpec]
        if sez.gumb["bg"] == "green":
            sez.gumb.config(bg="blue", text=chr(9873) if sys.version_info[0] == 3 and TkVersion >= 8.6 else ':)')
            self.st_poklikanih -= 1
            if sez.mina == 1:
                self.mines -= 1

        elif sez.gumb["bg"] == "blue":
            if sez.gumb == 1:
                self.mines += 1
            self.st_poklikanih += 1
            sez.gumb.config(bg="green", text="")

        if self.st_poklikanih == 0 and self.mines == 0:
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
        ## Če dam tole v callback, potem začne prehitevat ura
        ## Če pustim tukaj in če zaprem "nastavitve" potem ura crkne
        self.top = Toplevel()
        self.top.title("Nastavi")
        self.top.attributes("-topmost", True)

        frame = Frame(self.top)

        frame.pack()

        Label(frame, text="Število vrstic").grid(row=0, column=0, sticky=W)
        Label(frame, text="Število stolpcev").grid(row=1, column=0, sticky=W)
        Label(frame, text="Število min").grid(row=2, column=0, sticky=W)
##        Button(frame, text="+").grid(row=0, column=2)
##        Button(frame, text="-").grid(row=1, column=2)
        self.e1 = Entry(frame)
        self.e2 = Entry(frame)
        self.e3 = Entry(frame)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)

        self.var = IntVar()
        c = Checkbutton(self.top, text="Skrij številke", variable=self.var)
        c.pack()

        b = Button(self.top, text="OK", command=self.callback)
        self.top.bind("<Return>", self.callback)
        b.pack()

    def callback(self,event=None):
        '''Dobi podatke iz okna če obstajajo, sicer ohrani stare vrednosti'''
                
        self.e1.get1 = self.e1.get() or self.minesweeper.st_vrstic1234
        self.e2.get2 = self.e2.get() or self.minesweeper.st_stolpcev1234
        self.e3.get3 = self.e3.get() or self.minesweeper.mines1234
        
        self.minesweeper.st_vrstic1234 = max(int(self.e1.get1),1)
        self.minesweeper.st_stolpcev1234 = max(int(self.e2.get2),1)
        self.minesweeper.mines1234 = max(min(int(self.e3.get3),self.minesweeper.st_stolpcev1234*self.minesweeper.st_vrstic1234),0) #Število min ne sme biti večje od velikosti igralnega polja
        self.minesweeper.vidne_st = self.var.get()

        self.top.destroy()
        
        self.minesweeper.zbrisi_polje()
        self.minesweeper.nova_igra()

##Timer

class Timer:
    def __init__(self,minesweeper):
        self.sec = 0
        self.minesweeper = minesweeper
        self.timer = Toplevel()
        self.timer.title("Čas")
        self.timer.attributes("-topmost", True)
        self.time = Label(self.timer, fg='green')
        self.time.pack()
        Button(self.timer, fg='blue', text='Start', command=self.tick).pack()



    def tick(self):
        self.sec += 1
        self.time['text'] = self.sec
        # Take advantage of the after method of the Label
        self.time.after(1000, self.tick)

root = Tk()
root.title('Minolovec')
minesweeper = Minesweeper(root,VRSTICE,STOLPCI,MINE, POKAZI_ST, POKAZI)
root.mainloop()
