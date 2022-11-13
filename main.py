# Naudojami moduliai
from tkinter import *
from tkinter import ttk, messagebox
import datetime
from mydb import *

# DB objektas
duomenys = DuomenuBaze(db='DB.db')

# Globalūs kintamieji
count = 0
selected_rowid = 0


# funkcijos
def valyti_laukus():
    pavadinimas.delete(0, 'end')
    kaina.delete(0, 'end')
    data.delete(0, 'end')


def saugot_irasa():
    global duomenys
    duomenys.irasyti_duomenis_db(pavadinimas=pavadinimas.get(), kaina=kaina.get(), data=data.get())
    valyti_laukus()


def nustatyti_data():
    data = datetime.datetime.now()
    datos_kint.set(f'{data:%Y %m %d}')


def pasiimti_irasa():
    f = duomenys.pasiimti_duomenis_db('select rowid, * from islaidos')
    global count
    for irasas in f:
        tv.insert(parent='', index='0', iid=count, values=(irasas[0], irasas[1], irasas[2], irasas[3]))
        count += 1
    tv.after(1000, atnaujinti_duomenis)


def pasirinkti_irasa_pele(event):
    global selected_rowid
    pasirinktas_irasas = tv.focus()
    paimti_reiksmes = tv.item(pasirinktas_irasas, 'values')

    try:
        selected_rowid = paimti_reiksmes[0]
        d = paimti_reiksmes[3]
        pavadinimo_kint.set(paimti_reiksmes[1])
        kainos_kint.set(paimti_reiksmes[2])
        datos_kint.set(str(d))
    except Exception:
        pass


def atnaujinti_irasa():
    global selected_rowid

    pasirinktas_irasas = tv.focus()
    # atnaujinam įrašą
    try:
        duomenys.atnaujinti_duomenis_db(pavadinimo_kint.get(), kainos_kint.get(), datos_kint.get(), selected_rowid)
        tv.item(pasirinktas_irasas, text='', values=(pavadinimo_kint.get(), kainos_kint.get(), datos_kint.get()))
    except Exception as ep:
        messagebox.showerror('Klaida', ep)

    valyti_laukus()
    tv.after(400, atnaujinti_duomenis)


# parodo balansą, kai pirminis balansas buvo 5000
def mano_balansas():
    f = duomenys.pasiimti_duomenis_db(query='Select sum(kaina) from islaidos')
    for i in f:
        for j in i:
            messagebox.showinfo('Mano išlaidos: ', f'Išviso išleista: {j} \nLikutis: {5000 - j}')


# darame refrešą, kad po duomenų ivedimo/pakeitimo nereikėtų uždaryti ir atidaryti programos
def atnaujinti_duomenis():
    for item in tv.get_children():
        tv.delete(item)
    pasiimti_irasa()


def trinti_irasa():
    global selected_rowid
    duomenys.trinti_duomenis_db(selected_rowid)
    atnaujinti_duomenis()
    valyti_laukus()


# sukuriam tkinter objektą
ws = Tk()
ws.title('Mano išlaidų suvestinė')

# kintamieji
pavadinimo_kint = StringVar()
kainos_kint = IntVar()
datos_kint = StringVar()
sriftas = ('Helvetica', 10)

# pakeičiam tkinter ikoną
p1 = PhotoImage(file='templates/ikona.png')
ws.iconphoto(False, p1)

# Frame valdiklis(widget)
virsus = Frame(ws)
virsus.pack()

apacia = Frame(ws, padx=30, pady=30)
apacia.pack(expand=True, fill=BOTH)

# Frame valdiklio laukų pavadinimai apačioje
Label(apacia, text='Pavadinimas', font=sriftas).grid(row=0, column=0, sticky=W)
Label(apacia, text='Kaina', font=sriftas).grid(row=1, column=0, sticky=W)
Label(apacia, text='Data', font=sriftas).grid(row=2, column=0, sticky=W)

# Frame valdiklio laukų įvestis apačioje
pavadinimas = Entry(apacia, font=sriftas, textvariable=pavadinimo_kint)
kaina = Entry(apacia, font=sriftas, textvariable=kainos_kint)
data = Entry(apacia, font=sriftas, textvariable=datos_kint)

# išdėstymas
pavadinimas.grid(row=0, column=1, sticky=EW, padx=(10, 0))
kaina.grid(row=1, column=1, sticky=EW, padx=(10, 0))
data.grid(row=2, column=1, sticky=EW, padx=(10, 0))

# Mygtukai
siandien_data_btn = Button(
    apacia,
    text='Šiandienos data',
    font=sriftas,
    bg='darkgrey',
    fg='black',
    command=nustatyti_data,
    width=15,
    cursor='hand2'
)

irasyti_btn = Button(
    apacia,
    text='Įrašyti',
    font=sriftas,
    command=saugot_irasa,
    bg='lightgrey',
    fg='black',
    cursor='hand2'
)

isvalyti_btn = Button(
    apacia,
    text='Išvalyti',
    font=sriftas,
    command=valyti_laukus,
    bg='grey',
    fg='black',
    cursor='hand2'
)

balansas_btn = Button(
    apacia,
    text='Mano balansas',
    font=sriftas,
    bg='lightgrey',
    fg='black',
    command=mano_balansas,
    cursor='hand2'
)

atnaujinti_btn = Button(
    apacia,
    text='Atnaujinti įrašą',
    bg='grey',
    fg='black',
    command=atnaujinti_irasa,
    font=sriftas,
    cursor='hand2'
)

trinti_btn = Button(
    apacia,
    text='Trinti įrašą',
    bg='darkgrey',
    fg='black',
    command=trinti_irasa,
    font=sriftas,
    cursor='hand2'
)

iseiti_btn = Button(
    apacia,
    text='Uždaryti programą',
    font=sriftas,
    command=lambda: ws.destroy(),
    bg='black',
    fg='white',
    cursor='hand2'
)

# išdėsymas
irasyti_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
isvalyti_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
siandien_data_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
balansas_btn.grid(row=0, column=3, sticky=EW, padx=(10, 0))
atnaujinti_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0))
trinti_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))
iseiti_btn.grid(row=2, column=4, sticky=EW, padx=(10, 0))


# Treeview valdiklis(widget)
tv = ttk.Treeview(virsus, columns=(1, 2, 3, 4), show='headings', height=8)
tv.pack(side='left')

# Treeview antraštės
tv.column(1, anchor=CENTER, width=45)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text='Eil. Nr.')
tv.heading(2, text='Pavadinimas', )
tv.heading(3, text='Kaina')
tv.heading(4, text='Data')

# Scrollbar'as, vertikalus
scrollbar = Scrollbar(virsus, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side='right', fill='y')
tv.config(yscrollcommand=scrollbar.set)

# įrašo parinkimas pele
tv.bind('<ButtonRelease-1>', pasirinkti_irasa_pele)

# pakeičiam treeview stilių/temą
stilius = ttk.Style()
stilius.theme_use('clam')
stilius.map('Treeview')

# calling function
pasiimti_irasa()

# infinite loop
ws.mainloop()
