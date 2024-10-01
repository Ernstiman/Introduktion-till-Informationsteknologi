#Programmet kör det populära selat minesweeper där man med hjälp av en matris kan skapa ett rutnät där minor placeras. Dessa minor har blivit definerade som objekt av klassen Mina.
#DD100N
#25/11
#Viktor Forslund

import random as rand
from time import *
from tkinter import * 
import os
from tkinter.font import Font
from tkinter import messagebox


class Person():
  def __init__(self, namn, poäng):
    """
    Konstruktor till klassen
    Inparametrar: namn(str), poäng(float)
    """
    self.namn = namn
    self.poäng = poäng
  
  def __lt__(self, other):
    """
    Metoden gör så att objekt av klassen Person ska sorteras från minst poäng till högst
    Returvärden: True(bool), False(bool)
    """
    return self.poäng < other.poäng
  
  def __str__(self):
    """
    Metoden hanterar vad som ska skrivas i konsollen när vi vill skriva ut klassen
    Returvärde: str
    """
    return f"{self.namn}: {self.poäng}\n"
  
class Mina():
  
  def __init__(self):
    """
    Konstruktor till klassen
    """

    self.tecken = "  "
    pass
  
  def  __str__(self):
    """
    Metoden skriver ut minan på konsolen
    Returvärde: self.tecken(str)
    """
    return self.tecken
    pass 

class Game():

  def __init__(self, rot):
    """
    Konstruktorn till klassen
    Inparameter: rot(Tk)
    """
    self.rot = rot
    self.antal_minor = IntVar()
    self.storlek = IntVar()
    self.drag = IntVar()
    self.namn = StringVar()
    self.spelplan = Frame(rot,name = "spelplan")
    self.titel = Label(self.rot,text="MINESWEEPER",font = ("Stencil", 50),name = "titel", bg = "white")
    self.minfält = Frame(self.spelplan, border=60,)
    self.starta_om_knapp = Button(self.spelplan,text="Starta om",name = 'startaOm',command = lambda: self.skapa_spelruta(self.spelplan,self.namn.get()))

    self.matris = None
    self.redan_klickat = []
    self.knapp_lista = []
    self.knapp_storlek = 5
    self.starttid = None
    self.antal_minor.set(8)
    self.storlek.set(10)

    self.titel.pack()

    self.ruta_bredd = 60
    self.avstånd = 20
    self.border_width = 3
    self.font = ("Times", 20)
    self.neutral_ruta = "  "

  def meny(self,ruta = None):
    """
    Metoden skapar en menyruta till spelet
    Inparametrar: ruta(Frame)
    """
    if ruta != None:
      ruta.destroy()

    meny_ruta_ram = Frame(self.rot, bg = "black",bd = self.border_width)
    meny_ruta_ram.pack()
    meny_ruta = Frame(meny_ruta_ram, pady=self.ruta_bredd, padx=self.ruta_bredd)
    meny_ruta.pack(anchor=N)
    spela_knapp = Button(meny_ruta, text="Normalt", command = lambda: self.ange_namn(meny_ruta_ram)) 
    sluta_knapp = Button(meny_ruta, text= "Avsluta", command = lambda: self.rot.destroy())
    top_tio_knapp = Button(meny_ruta, text = "top-lista",command=lambda:self.top_10(meny_ruta_ram))
    sandlåda_knapp = Button(meny_ruta, text = "Sandlåda", command = lambda:self.spel_inställningar(meny_ruta_ram))
    info_knapp = Button(meny_ruta, text = "?", command = lambda:messagebox.showinfo("Information","""Normal: Vanligt minesweeper med en 10 x 10 spelplan. Ditt spelresutlat kommer läggas in i top-listan.
                                                                                    \nSandlåda: Minsesweeper med valfri spelstorlek mellan 5x5 - 15x15, valfri mängd minor, resultatet kommer inte läggas in i top-listan.
                                                                                    \nRegler: Vid klick av en ruta så kommer antingen en siffra komma fram, detta indikerar den mängd omgivande minor rutan har. Rutan går ur spel, detta innebär att rutan har noll omgivande minor. Eller så har rutan en mina på sig, då tar spelet slut. För att vinna så krävs det att spelaren röjer alla rutor som inte har en mina på sig. 
                                                                                    \nKontroller: Högerklick: röja, Vänsterklick: Flagga (Vänsterklick på en redan flaggad ruta gör rutan oflaggad)"""))
    self.pack_alla(spela_knapp, sandlåda_knapp, top_tio_knapp, sluta_knapp, info_knapp)
    self.konfiguera(meny_ruta,Button,"width", self.avstånd, "bg", "white")
    self.konfiguera(meny_ruta, (Button, Label, Scale), "font", self.font)
    self.bind(meny_ruta,Button,"Enter","bg", "#E0E0E0")
    self.bind(meny_ruta, Button, "Leave", "bg", "white")

  def konfiguera(self, ruta,klass, parameter, värde, andra_parameter = None, andra_värde = None):
    """
    Metoden gör det möjligt att konfiguera flera widgets och ändra max två parametrar på dessa widgets.
    Inparametrar: ruta(Frame), klass(Button/Frame(Label), parameter(str), värde(str), andra_parameter(str), andra_värde(str))
    """
    for widget in ruta.winfo_children():
      if isinstance(widget, klass):
        try:
          widget[parameter] = värde
          widget[andra_parameter] = andra_värde
        except:
          widget[parameter] = värde

  def bind(self, ruta, klass, bind, parameter, arg):
    """
    Metoden gör det möjligt att binda flera widgets med valfrit event som påverkar valfri parameter. 
    Inparametrar: ruta(Frame), klass(Button/Frame/Label), bind(str), parameter(str), arg(str)
    """
    for widget in ruta.winfo_children():
      if isinstance(widget, klass):
        widget.bind("<" + bind + ">", lambda event, x = parameter, y = arg, z = widget:self.bind_funktion(event,x,y,z) )

  def bind_funktion(self,event, parameter, arg, widget):
    """
    Metoden ändrar en widgets parameter till ett valfritt argument
    """
    widget[parameter] = arg

    
  def spel_inställningar(self,ruta): 
    """
    Metoden skapar en ruta där man kan ändra olika inställningar i spelet som storlek på planen och antalet minor.
    Inparametrar: ruta(Frame)
    """
    ruta.destroy()
    scale_längd = 300
    scale_bredd = 40
    knapp_bredd = self.avstånd

    spel_inställningar_ruta_ram = Frame(self.rot, bg = "black", bd = self.border_width)
    spel_inställningar_ruta = Frame(spel_inställningar_ruta_ram, pady=self.ruta_bredd , padx=self.ruta_bredd)
    storlek_text_var = StringVar(spel_inställningar_ruta)
    antal_minor_text_var = StringVar(spel_inställningar_ruta)
    tillbaka_knapp = Button(spel_inställningar_ruta,text = "Tillbaka till menyn" ,width = knapp_bredd,command = lambda:self.meny(spel_inställningar_ruta_ram))
    storlek_text = Label(spel_inställningar_ruta,textvariable=storlek_text_var)
    höger_knapp = Button(spel_inställningar_ruta,text = ">", command = lambda:self.ändra_storlek(storlek_text_var,True,ange_minor))
    vänster_knapp = Button(spel_inställningar_ruta,text="<", command = lambda:self.ändra_storlek(storlek_text_var,False, ange_minor))
    ange_minor = Scale(spel_inställningar_ruta, from_=1,activebackground="black", bg= "black",to=(self.storlek.get()**2 - 1),length=scale_längd,width = scale_bredd, command = lambda antal, var = antal_minor_text_var:self.ändra_antal_minor(antal,var) ,orient="horizontal", showvalue=False)
    antal_minor_text = Label(spel_inställningar_ruta, textvariable=antal_minor_text_var)
    spela_knapp = Button(spel_inställningar_ruta, text="spela",width = knapp_bredd, command = lambda:self.skapa_spelruta(spel_inställningar_ruta_ram,True))

    self.placera_spelinställningar_widgets(vänster_knapp, storlek_text, höger_knapp, antal_minor_text, ange_minor, tillbaka_knapp,spela_knapp)
    storlek_text_var.set(f"{self.storlek.get()}x{self.storlek.get()}")
    antal_minor_text_var.set(f"Antal minor: {self.antal_minor.get()}")

    spel_inställningar_ruta_ram.pack()
    spel_inställningar_ruta.pack()

    self.konfiguera(spel_inställningar_ruta, (Button, Label, Scale), "font", self.font)
    self.konfiguera(spel_inställningar_ruta, Button, "bg", "white")
    self.bind(spel_inställningar_ruta,Button,"Enter","bg", "#E0E0E0")
    self.bind(spel_inställningar_ruta, (Button), "Leave", "bg", "white")

  def placera_spelinställningar_widgets(self, vänster_knapp,                                     
    storlek_text, 
    höger_knapp, 
    antal_minor_text, 
    ange_minor, 
    tillbaka_knapp, 
    spela_knapp):
    """
    Metoden placerar samtliga widgets som ska in på rutan spel_inställningar_ruta
    Inparametrar: vänster_knapp(Button), storlek_text(Label), höger_knapp(Button), antal_minor(Label), ange_minor(Scale), tillbaka_knapp(Button),spela_knapp(Button)
    """
    vänster_knapp.grid(row=0, column=0, pady=self.avstånd)
    storlek_text.grid(row=0, column=1, pady = self.avstånd)
    höger_knapp.grid(row=0, column=2, pady = self.avstånd)
    antal_minor_text.grid(row=1, column= 1) 
    ange_minor.grid(row=2, column = 1)
    tillbaka_knapp.grid(row=self.border_width, column= 1,pady=self.avstånd)
    spela_knapp.grid(row = 4, column= 1,pady=self.avstånd)



  def pack_alla(self,*arg):
    """
    Metoden gör det möjligt att packetera flera widgets på samma gång
    Inparameter: *arg(tuple)
    """
    for widget in arg:
      widget.pack(pady = self.avstånd)
      


  def ändra_antal_minor(self,antal,var):
    """
    Metoden ändrar variablerna för antalet minor och textvaribeln som skriver ut antalet_minor
    Inparametrar: antal(int), var(strVar)
    """
    self.antal_minor.set(antal)
    var.set(f"Antal minor: {self.antal_minor.get()}")



  def ändra_storlek(self,storlek, add, skala):
    """
    Metoden ändrar storleken på planen
    Inparametrar: storlek(strVar), add(Bool), skala(skala)
    """
    max = 15
    min = 5
    if (self.storlek.get() == max and add) or (self.storlek.get() == min and not add):
      pass
    else:
      if add:
        self.storlek.set(self.storlek.get() + 1)
      else:
        self.storlek.set(self.storlek.get() - 1)
      storlek.set(f"{self.storlek.get()}x{self.storlek.get()}")
      skala["to"] = self.storlek.get()**2 - 1

  
  def top_10(self, ruta):
    """
    Metoden inplementerar en grafisk top 10 lista
    Inparametrar: ruta(Frame)
    """
    ruta.destroy()
    top_lista_ruta_ram = Frame(self.rot,bd = self.border_width, bg = "black")
    top_list_ruta = Frame(top_lista_ruta_ram,bg = "white")
    namn_label = Label(top_list_ruta,font = "Courier",width=self.ruta_bredd,text=f"Topp-10\n{'Plats':<20s}{'Namn':<20s}{'Tid(sek)':<20s}")
    listb = Listbox(top_list_ruta,width=self.ruta_bredd, font="Courier")
    tillbaka_knapp = Button(top_list_ruta, text="Tillbaka till menyn", bg = "white", command = lambda:self.meny(top_lista_ruta_ram))
    self.bind(top_list_ruta,Button,"Enter","bg", "#E0E0E0")
    self.bind(top_list_ruta, (Button), "Leave", "bg", "white")
    top_lista = läs_in_fil()
    top_lista_ruta_ram.pack()
    top_list_ruta.pack()
    top = 10
    
    for index,person in enumerate(top_lista, 1):                                      
      if index>top:  
        break
      person = f"{str(index) + '.':<20s}{person.namn:<20s}{person.poäng:<20n}"
      listb.insert(index,person)

    namn_label.pack()
    listb.pack() 
    tillbaka_knapp.pack()
  
  def skapa_spelruta(self, ruta, sandlåda = None):
    """
    Metoden skapar spelrutan för programmet samt definerar alla widgets som behövs
    Inparametrar:ruta(Frame), sandlåda(Bool)
    """
    ruta.destroy()

    if sandlåda:
      self.namn.set("")
    else:
      self.antal_minor.set(8)
      self.storlek.set(8)

    spelplan_ram = Frame(self.rot, bg = "black", bd = self.border_width)
    self.spelplan = Frame(spelplan_ram,name = "spelplan", padx = self.ruta_bredd, pady=self.ruta_bredd)
    self.minfält = Frame(self.spelplan, border=10, bg = "#404040")
    self.starta_om_knapp = Button(self.spelplan,text="Starta om",name = 'startaOm',command = lambda: self.skapa_spelruta(spelplan_ram, sandlåda))
    self.matris,_,_ = generera_matris(self.storlek, self.neutral_ruta)
    self.redan_klickat = []
    self.knapp_lista = []
    self.starttid = time()
    self.drag.set(0)
    spelplan_ram.pack()
    self.spelplan.pack()
    self.pack_alla(self.minfält, self.starta_om_knapp)
    self.placera_knappar(spelplan_ram)
    self.konfiguera(self.spelplan, Button, "width", self.avstånd, "font", ("Helvetica",self.avstånd))
    self.konfiguera(self.spelplan,Button,"bg","white")
    self.bind(self.spelplan, (Button), "Enter", "bg", "#E0E0E0")
    self.bind(self.spelplan, Button, "Leave","bg","white"  )

  def placera_knappar(self, spelplan_ram):
    """
    Metoden placerar ut knapparna som bygger upp själva spelplanen
    Inparametrar: spelplan_ram(Frame)
    """

    for y,rad in enumerate(self.matris):
      knapp_lista_x = []
      for x, kolumn in enumerate(rad): 
        knapp = Button(self.minfält,text = self.neutral_ruta,activebackground="#c0c0c0",bg = "#c0c0c0",pady=self.knapp_storlek,padx = self.knapp_storlek + 10)
        knapp.grid(column=x, row=y)
        knapp.bind('<Button-1>', lambda event,kords = (y,x): self.klick(event, kords,spelplan_ram))
        knapp.bind('<Button-3>',lambda event, kords = (y,x): self.placera_flagga(event, kords))
        knapp_lista_x.append(knapp)
        x = x * self.knapp_storlek
      self.knapp_lista.append(knapp_lista_x)
      y = y * self.knapp_storlek

  def klick(self,event, kords, spelplan_ram):
    """
    Metoden definerar logiken som sker när spelaren klickar på en ruta som man vill röja
    Inparametrar: event(event), kords(Tuple), spelplan_ram(Frame)
    """
    rad, kolumn = kords
    if self.knapp_lista[rad][kolumn]["state"]!="disabled":
      self.drag.set(self.drag.get()+1)
      if self.drag.get() == 1: 
        genererarMinor(self.matris, rad, kolumn,self.antal_minor)
      hantera_rutor(self.matris, rad, kolumn, self.redan_klickat)
      self.få_data()
      print(self.drag.get())
      if kollision(self.matris, rad, kolumn):
        self.förlorat(spelplan_ram)
      if kolla_vinst(self.matris, self.neutral_ruta):
        sluttid = time()
        tid = sluttid - self.starttid
        if self.namn.get() != "":
          skriv(tid, self.namn.get(), self.antal_minor)
        spelplan_ram.destroy()
        self.vinst_ruta(tid)
        pass

  def ange_namn(self,ruta = None):
    """
    Metoden skapar rutan där spelaren kan ange sitt namn samt dess widgets
    Inparametrar: ruta(Frame)
    """
    if ruta != None:
      ruta.destroy()
    klickat_enter = BooleanVar()
    klickat_enter.set(False)
    popup_ruta_ram = Frame(self.rot, bg = "black", bd = self.border_width)
    popup_ruta = Frame(popup_ruta_ram, padx = self.ruta_bredd, pady = self.ruta_bredd)
    namn = Entry(popup_ruta)
    instruktioner = Label(popup_ruta,text="Ange ditt namn.")
    inte_angivit_namn_text = Label(popup_ruta, text = "Du måste angiva ett namn", fg = "red")
    tillbaka_knapp = Button(popup_ruta, text = "Tillbaka till menyn",bg = "white", command = lambda: self.meny(popup_ruta_ram))

    popup_ruta_ram.pack()
    popup_ruta.pack()
    self.pack_alla(instruktioner, namn, tillbaka_knapp)
    namn.bind('<Return>', lambda event,:self.kolla_namn(event, namn, popup_ruta_ram, klickat_enter, inte_angivit_namn_text))
    self.konfiguera(popup_ruta, (Label, Entry, Button), "font", ("Helvetica",self.avstånd))
    self.bind(popup_ruta, (Button), "Enter", "bg", "#E0E0E0")
    self.bind(popup_ruta, Button, "Leave","bg","white")

  def kolla_namn(self,event, namn, popup_ruta_ram,klickat_enter, instruktioner):
    """
    Metoden kollar ifall namnet som spelaren angivit är användbart
    Inparametrar: event(event), namn(strVar), popup_ruta_ram(Frame), klickat_enter(Bool), instruktioner(Label)
    """
  
    if len(namn.get()) > 0 and not är_samma_namn(namn.get()):
      self.namn.set(namn.get())
      self.skapa_spelruta(popup_ruta_ram)
    else:
        instruktioner["text"] = "Detta namn finns redan" if är_samma_namn(namn.get()) else  "Du måste ange ett namn"
        if not klickat_enter.get():
          instruktioner.pack()
          klickat_enter.set(True)
  

  def vinst_ruta(self, tid):
    """
    Metoden skapar en ruta som dyker upp när man vinner spelet samt dess widgets
    Inparametrar: tid(Float)
    """
    vinst_ruta_ram = Frame(self.rot, bd = self.border_width, bg = "black")
    vinst_ruta = Frame(vinst_ruta_ram, padx = self.ruta_bredd, pady=self.ruta_bredd)
    vinst_text = Label(vinst_ruta,text="Grattis du vann!")
    spela_igen = Button(vinst_ruta, text= "Spela igen", command = lambda:self.nytt_spel(vinst_ruta_ram))
    avsluta = Button(vinst_ruta, text="Avsluta", command = lambda:self.meny(vinst_ruta_ram))
    spel_resultat = Label(vinst_ruta, text = f"Din tid är {round(tid)} sekunder")
    vinst_ruta_ram.pack()
    vinst_ruta.pack()
    self.pack_alla(vinst_text, spel_resultat, spel_resultat, spela_igen, avsluta)
    self.konfiguera(vinst_ruta, (Button, Label), "width", self.avstånd, "font", ("Helvetica",self.avstånd))
    self.konfiguera(vinst_ruta,Button,"bg","white")
    self.bind(vinst_ruta, (Button), "Enter", "bg", "#E0E0E0")
    self.bind(vinst_ruta, Button, "Leave","bg","white"  )

  def förlorat(self,spelplan_ram):
    """
    Metoden skapar en popup som dyker upp när spelaren förlorat samt dess widgets
    Inparametrar: spelplan_ram(Frame)
    """
    if kollaKeyError(self.spelplan):
      self.spelplan.nametowidget("startaOm").destroy()

    for rad in self.knapp_lista:
      for knapp in rad:
        knapp["state"] = "disabled"
    slut_text = Label(self.spelplan, text = "GAME OVER!", fg="red")
    spela_igen = Button(self.spelplan, text= "Spela igen", command = lambda:self.nytt_spel(spelplan_ram))
    avsluta = Button(self.spelplan, text="Avsluta", command=lambda:self.meny(spelplan_ram))
    self.pack_alla(slut_text, spela_igen, avsluta)
    self.konfiguera(self.spelplan, (Button, Label), "width", self.avstånd, "font", ("Helvetica",self.avstånd))
    self.konfiguera(self.spelplan,Button,"bg","white")
    self.bind(self.spelplan, (Button), "Enter", "bg", "#E0E0E0")
    self.bind(self.spelplan, Button, "Leave","bg","white"  )
    pass

  def nytt_spel(self,ruta):
    """
    Metoden skapar logif för att ta bort den tidigare rutan och gå tillbaka till där man anger sitt namn
    Inparametrar: ruta(Frame)
    """

    if self.namn.get() == "":
      self.skapa_spelruta(ruta, True)
    else:
      self.ange_namn(ruta)

  def få_data(self):
    """
    Metoden för över all information från matrisen till det grafiska minfältet, samt ändrar färg på siffrorna 
    """
    for y,rad in enumerate(self.matris):
      for x,kolumn in enumerate(rad):
        self.knapp_lista[y][x]["text"] = self.matris[y][x] 
    for rad in self.knapp_lista:
      for knapp in rad:
        if knapp["text"] == "0":
          knapp.config(text = self.neutral_ruta,state = "disabled", relief = "sunken")
        if knapp["text"] == "1":
          knapp.config(fg = "green",activeforeground="green")
        if knapp["text"] == "2":
          knapp.config(fg = "yellow", activeforeground="yellow")
        if knapp["text"] == "3":
          knapp.config(fg = "red", activeforeground="red")
        if knapp["text"] == "4":
          knapp.config(fg = "purple", activeforeground="purple")

    pass

  def placera_flagga(self,event, kords):
    """
    Metoden placerar ut flaggan på spelplanen
    Inparametrar: event(event), kords(tuple)
    """
    rad, kolumn = kords
    flagga(self.matris, rad, kolumn, self.neutral_ruta)
    tecken = self.knapp_lista[rad][kolumn]["text"]
    if tecken == "F":
      self.knapp_lista[rad][kolumn]["text"] = self.neutral_ruta
    elif tecken == self.neutral_ruta and self.knapp_lista[rad][kolumn]["state"] != "disabled": 
      self.knapp_lista[rad][kolumn]["text"] = "F"
  


def generera_matris(sida,tecken):
  """
  Funktionen genererar matrisen som kommer hålla all information om spelplanen.
  Inparametrar: sida(strVar), tecken(str)
  """
  x_axel = tecken
  y_axel = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
  matris_1 = []
  for höjd in range(sida.get()):
    matris_2 = []
    for bredd in range(sida.get()):
      matris_2.append(tecken)
    matris_1.append(matris_2)
  for num in range(len(matris_1[0])):
    if num == 0:
      x_axel += tecken
      x_axel += str(num + 1)
    elif num < 10:
      x_axel += "   "
      x_axel += str(num + 1)
    else:
      x_axel += tecken
      x_axel += str(num + 1)

  return matris_1, x_axel, y_axel  



def genererarMinor(karta, rad, kolumn, antal_minor):
  """
  Funktionen kommer generera minorna på spelplanen
  Inparameter: karta(matris), rad(int), kolumn(int), antal_minor(int)
  """
  kord_list = []
  
  tur = 0
  while tur < antal_minor.get():
    x = rand.randint(0, len(karta[0]) - 1)
    y = rand.randint(0, len(karta) - 1)
    if (x,y) in kord_list or (x,y) == (kolumn, rad):
      continue
    kord_list.append((x,y))
    tur += 1
  for kord in kord_list:
    karta[kord[1]][kord[0]] = Mina()
  pass
  

def kollision(karta, rad, kolumn):
  """
  Funktionen kommer kolla om det är en kollision mellan de angivna kordinaterna och en mina, då kommer den returnera true, annars false.
  Inparametrar: karta(matris), rad(int), kolumn(int)
  Returvärde: True(bool), False(bool)
  """
  if type(karta[rad][kolumn]) == Mina:
    return True
  return False
  
  pass

def kollisionRunt(karta, rad, kolumn):
  """
  Funktionen kommer kolla om de är några minor runt om spelarens angivna kordinater då kommer den returnera en siffra på antalet minor runt.
  Inparametrar: karta(matris), rad(int), kolumn(int)
  Returvärden: antal_minor(str)
  """
  antal_minor = 0
  top_start, top_slut, sida_start, sida_slut = rutorRunt(karta, rad, kolumn)
  for y in range(top_start, top_slut):
    for x in range(sida_start, sida_slut):
      if (y, x) != (rad, kolumn):
        if type(karta[y][x]) == Mina:
          antal_minor += 1
  return str(antal_minor) 
  pass

def kolla_vinst(karta,tecken):
  """
  Funktionen kollar om samtliga minor har blicit flaggade, i så fall returneras true
  Inparametrar: karta(matris), tecken(str)
  Returvärde: True(bool), False(bool)
  """

  for rad in karta:
    for kolumn in rad:
      if kolumn == tecken or kolumn == "F" and type(kolumn) != Mina:
        return False
  return True

  pass

def flagga(karta, rad, kolumn,tecken):
  """
  Funktionen flaggar den angivna rutan spelaren skrivit.
  Inparametrar: karta(matris), rad(int), kolumn(int), tecken(str)
  """
  if type(karta[rad][kolumn]) == Mina:
    if karta[rad][kolumn].tecken == "F":
      karta[rad][kolumn].tecken = tecken
    else: 
      karta[rad][kolumn].tecken = "F"
  elif karta[rad][kolumn] == "F":
    karta[rad][kolumn] = tecken
  elif karta[rad][kolumn] == tecken: 
    karta[rad][kolumn] = "F" 


def rutorRunt(karta, rad, kolumn):
  """
  Funktionen kollar hur många rutor den angivna rutan har runtomkring sig
  Inparametrar: karta(matris), rad(int), kolumn(int)
  Returvärden: top_start(int), top_slut(int), sida_start(int), sida_slut(int)
  """
  top_start = rad - 1
  top_slut = rad +2
  sida_start = kolumn - 1
  sida_slut = kolumn + 2
  if top_start < 0:
    top_start = 0
  if top_slut > len(karta):
    top_slut = len(karta)
  if sida_start < 0:
    sida_start = 0
  if sida_slut > len(karta[0]):
    sida_slut = len(karta[0]) 
  return top_start, top_slut, sida_start, sida_slut




def hantera_rutor(karta, rad, kolumn, redan_klickat):
  """
  Funktionen analyserar den angivna rutan och kollar ifall den är omgiven av noll minor så ska den även kolla närliggande rutor och ifall dess närliggande rutor har noll minor osv..
  Inparametrar: karta(matris), rad(int), kolumn(int), redan_klickat(list)
  Returvärden: Karta(Matris)
  """
  if (rad,kolumn) in redan_klickat:
    return
  if type(karta[rad][kolumn]) == Mina:
    return
  redan_klickat.append((rad,kolumn))
  if kollisionRunt(karta, rad, kolumn) == "0" or len(redan_klickat) == 1:
    top_start, top_slut, sida_start,sida_slut = rutorRunt(karta, rad, kolumn) 
    for y in range(top_start, top_slut):
      for x in range(sida_start, sida_slut):
        hantera_rutor(karta, y, x, redan_klickat)
        karta[rad][kolumn] = kollisionRunt(karta, rad, kolumn)
  
  else:
    karta[rad][kolumn] = kollisionRunt(karta, rad, kolumn)
  return karta

def skriv(tid, namn, antal_minor):
  """
  Funktionen skriver in till textfilen användarnamnet samt dess poäng
  Inparametrar: starttid(float), namn(str), antal_minor(int)
  """
  poäng = round(tid)
  str = f"{namn}, {poäng}"
  with open("top-10.txt", "a") as file:
    file.write(str + "\n")

def läs_in_fil():
  """
  Funktionen läser in från textfilen och skriver ut värderna i en topp-lista
  """
  top_lista = []
  top = 10
  with open("top-10.txt", "r") as fil:
    for rad in fil:
      rad = rad.split(", ")
      top_lista.append(Person(rad[0], int(rad[1].strip("\n"))))
  top_lista.sort()
  return top_lista

def är_samma_namn(namn):
  """
  Funktionen kollar ifall det angivna namnet redan finns i topplistan, i så fall returneras True, annars False
  Inparametrar: namn(str)
  Returvärden: True(Bool), False(Bool)
  """
  with open("top-10.txt", "r") as fil:
    for person in fil:
      person = person.split(", ")
      if person[0] == namn:
        return True
  return False


def kollaKeyError(rot):
  """
  Funktionen kollar ifall widgeten med namnet "startaOm" finns
  """
  try:
    rot.nametowidget('startaOm')
    return True
  except KeyError:
    return False

def main():
    """
    Huvudfunktionen som kör hela programmet
    """
    rot = Tk()
    rot.geometry("800x900")
    rot.config(bg="white")
    minesweeper = Game(rot)
    minesweeper.meny()
    rot.mainloop()
  
 
pass
if __name__ == "__main__":
  main()
















    
