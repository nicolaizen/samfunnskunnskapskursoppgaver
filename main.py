#!/usr/bin/env python

import tkinter as tk
import json
from random import randrange, shuffle
from types import SimpleNamespace

root = tk.Tk()
root.title("samfunnskunnskapsprøven øve til prøve")

canvas = tk.Canvas(root, width=1000, height=800)
canvas.pack()

total = 0
rette = 0
feil = 0
svar_avgitt = False
har_svart_tidligere = False


def korrektSvar():
    global svar_avgitt
    global rette
    global total
    global har_svart_tidligere
    label = tk.Label(root, text='              Korrekt!              ', fg='green', font=('helvetica', 16, 'bold'))
    canvas.create_window(500, 550, window=label)
    if not svar_avgitt:
        rette = rette + 1
        total = total + 1
    svar_avgitt = True
    har_svart_tidligere = True
    score()
    neste_knapp()


def feilSvar():
    global svar_avgitt
    global feil
    global total
    global har_svart_tidligere

    label = tk.Label(root, text='              OY! Prøv igjen              ', fg='red', font=('helvetica', 12, 'bold'))
    canvas.create_window(500, 550, window=label)
    if not svar_avgitt:
        feil = feil + 1
        total = total + 1
    svar_avgitt = True
    har_svart_tidligere = True
    score()
    neste_knapp()


def create_oppgave_tekst(oppgave_tekst):
    label = tk.Label(root, text=oppgave_tekst, fg='black', font=('helvetica', 16, 'bold'))
    canvas.create_window(500, 200, window=label)


def alternativ_boks(svar_tekst, y_posisjon, korrekt_svar):
    if svar_tekst == ":)":
        return
    if korrekt_svar:
        button = tk.Button(text=svar_tekst, command=korrektSvar, bg='white', fg='black', font=('helvetica', 16, 'bold'))
    else:
        button = tk.Button(text=svar_tekst, command=feilSvar, bg='white', fg='black', font=('helvetica', 16, 'bold'))
    canvas.create_window(500, y_posisjon, window=button)


def neste_knapp():
    button = tk.Button(text="Neste", command=sett_opp_oppgave, bg='white', fg='black', font=('helvetica', 16, 'bold'))
    canvas.create_window(500, 590, window=button)


def score():
    global svar_avgitt
    global rette
    global feil
    global total

    if total == 0:
        label = tk.Label(root, text='rette: ' + str(rette), fg='green', font=('helvetica', 16, 'bold'))
        canvas.create_window(800, 10, window=label)
        label = tk.Label(root, text='feil: ' + str(feil), fg='red', font=('helvetica', 16, 'bold'))
        canvas.create_window(800, 40, window=label)
        label = tk.Label(root, text='total: ' + str(total), fg='black', font=('helvetica', 16, 'bold'))
        canvas.create_window(800, 70, window=label)
    if total > 0:
        retteprosent = "{:.2f}".format((rette / total) * 100)
        rett_tekst = '          rette: ' + str(rette) + ' (' + retteprosent + '%)          '
        label = tk.Label(root, text=rett_tekst, fg='green', font=('helvetica', 16, 'bold'), justify="left")
        canvas.create_window(800, 10, window=label)
        label = tk.Label(root, text='feil: ' + str(feil), fg='red', font=('helvetica', 16, 'bold'))
        canvas.create_window(800, 40, window=label)
        label = tk.Label(root, text='total: ' + str(total), fg='black', font=('helvetica', 16, 'bold'))
        canvas.create_window(800, 70, window=label)


def sett_opp_oppgave():
    global oppgaver

    oppgave = oppgaver[total % len(oppgaver)]
    # oppgave = oppgaver[randrange(len(oppgaver))]

    canvas.delete("all")
    create_oppgave_tekst(oppgave.Tekst)

    if not oppgave.C == ":)":
        svar_alternativ = [(oppgave.A, oppgave.Fasit == "A"),
                           (oppgave.B, oppgave.Fasit == "B"),
                           (oppgave.C, oppgave.Fasit == "C")]
        shuffle(svar_alternativ)
        alternativ_boks(svar_alternativ[0][0], 295, svar_alternativ[0][1])
        alternativ_boks(svar_alternativ[1][0], 385, svar_alternativ[1][1])
        alternativ_boks(svar_alternativ[2][0], 475, svar_alternativ[2][1])
    else:
        svar_alternativ = [(oppgave.A, oppgave.Fasit == "A"),
                           (oppgave.B, oppgave.Fasit == "B")]
        shuffle(svar_alternativ)
        alternativ_boks(svar_alternativ[0][0], 350, svar_alternativ[0][1])
        alternativ_boks(svar_alternativ[1][0], 450, svar_alternativ[1][1])

    global svar_avgitt
    svar_avgitt = False

    score()


def finn_oppgaver():
    global oppgaver
    with open("samfunnkunskapsprøve.json", encoding='utf-8') as jsonFile:
        oppgaver = (json.loads(jsonFile.read(), object_hook=lambda d: SimpleNamespace(**d))).Oppgaver
        jsonFile.close()
        return oppgaver


oppgaver = finn_oppgaver()


def main():
    global svar_avgitt
    svar_avgitt = False
    global oppgaver
    shuffle(oppgaver)
    sett_opp_oppgave()
    root.mainloop()


if __name__ == "__main__":
    main()
