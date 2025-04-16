------------------------------------

Copyright (c) 2025 Mateusz Celiński

Licensed under the MIT license

See LICENSE.txt for details

------------------------------------

import tkinter as tk from tkinter import ttk, messagebox

Funkcja generująca prefiks nazwy związku organicznego

def generatePrefix(carbonCount): # słownik z prefiksami dla danej liczby atomów węgla specificNames = { 1: "met", 2: "et", 3: "prop", 4: "but", 5: "pent", 6: "heks", 7: "hept", 8: "okt", 9: "non", 10: "dek", 11: "undek", 12: "dodek", 13: "tridek", 14: "tetradek", 15: "pentadek", 16: "heksadek", 17: "heptadek", 18: "oktadek", 19: "nonadek", 20: "ikoz" } return specificNames.get(carbonCount, "")

Funkcja zliczająca ilość atomów wodoru na podstawie obecności w. podwójnych i potrójnych

def calculateHydrogens(carbonCount, doubleBond, tripleBond): baseHydrogens = 2 * carbonCount + 2 if doubleBond: baseHydrogens -= 2 if tripleBond: baseHydrogens -= 4 return baseHydrogens

Funkcja generująca prefiks dla podstawników

def generateSubstituentString(substituents): substituentCounts = {} for position, type_ in substituents: if type_ not in substituentCounts: substituentCounts[type_] = [] substituentCounts[type_].append(position)

substituentOrder = { "CH3": "metylo", "C2H5": "etylo", "Cl": "chloro", "Br": "bromo", "F": "fluoro", "NO2": "nitro", } substituentStrings = [] for type_, positions in sorted(substituentCounts.items(), key=lambda x: substituentOrder.get(x[0], x[0])): count = len(positions) positionsStr = ",".join(map(str, sorted(positions))) prefix = substituentOrder.get(type_, type_) multiplicativePrefix = { 1: "", 2: "di", 3: "tri", 4: "tetra", 5: "penta", 6: "heksa", 7: "hepta", 8: "okta", 9: "nona", 10: "deka" }.get(count, f"{count}-") substituentStrings.append(f"{positionsStr}-{multiplicativePrefix}{prefix}") return "-".join(substituentStrings) 

Funkcja generująca nazwę związku według IUPAC

def generateIUPACName(carbonCount, compoundType, doubleBond, tripleBond, substituents): baseName = generatePrefix(carbonCount) substituentString = generateSubstituentString(substituents) if substituentString: baseName = f"{substituentString}{baseName}"

if compoundType == "alken" and doubleBond: baseName += f"{doubleBond}-en" elif compoundType == "alkin" and tripleBond: baseName += f"{tripleBond}-yn" else: baseName += "an" return baseName 

Funkcja generująca wzór sumaryczny związku

def calculateMolecularFormula(carbonCount, substituents): hydrogenCount = 2 * carbonCount + 2 elementCounts = {"C": carbonCount, "H": hydrogenCount}

for position, substituent in substituents: if substituent == "CH3": elementCounts["C"] += 1 elementCounts["H"] += 3 elementCounts["H"] -= 1 elif substituent == "C2H5": elementCounts["C"] += 2 elementCounts["H"] += 5 elementCounts["H"] -= 1 elif substituent in ["Cl", "Br", "F", "NO2"]: elementCounts["H"] -= 1 elementCounts[substituent] = elementCounts.get(substituent, 0) + 1 formulaParts = [] for element, count in elementCounts.items(): if count > 1: formulaParts.append(f"{element}{count}") elif count == 1: formulaParts.append(f"{element}") return "".join(formulaParts) 

Aktualizacja interfejsu w zależności od wybranego typu związku

def updateBondEntries(event): compoundType = compoundTypeVar.get() if compoundType == "alken": doubleBondFrame.grid(row=3, column=0, columnspan=2, sticky="we") tripleBondFrame.grid_remove() elif compoundType == "alkin": tripleBondFrame.grid(row=3, column=0, columnspan=2, sticky="we") doubleBondFrame.grid_remove() else: doubleBondFrame.grid_remove() tripleBondFrame.grid_remove()

Funkcja generująca nazwę i wzór po kliknięciu "Generuj"

def generate(): try: carbonCount = int(carbonEntry.get()) if carbonCount < 1 or carbonCount > 20: raise ValueError("Liczba atomów węgla musi być w przedziale 1-20.")

compoundType = compoundTypeVar.get() doubleBond = int(doubleBondEntry.get()) if compoundType == "alken" else None tripleBond = int(tripleBondEntry.get()) if compoundType == "alkin" else None substituents = [] for pos, sub in substituentData: substituents.append((int(pos), sub)) name = generateIUPACName(carbonCount, compoundType, doubleBond, tripleBond, substituents) formula = calculateMolecularFormula(carbonCount, substituents) resultName.set(name) resultFormula.set(formula) except Exception as e: messagebox.showerror("Błąd", str(e)) 

Dodanie podstawnika do listy po kliknięciu "Dodaj +"

def addSubstituent(): position = substituentPositionEntry.get() substituent = substituentTypeVar.get() if position.isdigit() and substituent: substituentData.append((position, substituent)) refreshSubstituentDisplay() else: messagebox.showerror("Błąd", "Podaj poprawną pozycję i typ podstawnika.")

Usunięcie podstawnika z listy

def removeSubstituent(index): if 0 <= index < len(substituentData): del substituentData[index] refreshSubstituentDisplay()

Odświeżenie widoku dodanych podstawników

def refreshSubstituentDisplay(): for widget in substituentDisplayFrame.winfo_children(): widget.destroy()

for i, (pos, sub) in enumerate(substituentData): tk.Label(substituentDisplayFrame, text=f"{pos}: {sub}", bg="#f0f8ff", anchor="w").grid(row=i, column=0, sticky="w") tk.Button(substituentDisplayFrame, text="-", command=lambda idx=i: removeSubstituent(idx), bg="#ffb6b9", relief="flat", width=2).grid(row=i, column=1, sticky="e") 

--- UI: Tworzenie i rozmieszczanie elementów interfejsu graficznego ---

root = tk.Tk() root.title("Generator nazw związków organicznych") root.configure(bg="#f7f9fc") root.geometry("550x600")

substituentData = []

Pole do wpisania liczby atomów węgla

tk.Label(root, text="Liczba atomów węgla (1-20):", bg="#f7f9fc", anchor="w").grid(row=0, column=0, sticky="w") carbonEntry = tk.Entry(root, bg="#f0f8ff", relief="flat") carbonEntry.grid(row=0, column=1, sticky="we")

Menu wyboru typu związku

compoundTypeVar = tk.StringVar(value="alkan") tk.Label(root, text="Typ związku:", bg="#f7f9fc", anchor="w").grid(row=1, column=0, sticky="w") compoundTypeMenu = ttk.Combobox(root, textvariable=compoundTypeVar, values=["alkan", "alken", "alkin"], state="readonly") compoundTypeMenu.grid(row=1, column=1, sticky="we") compoundTypeMenu.bind("<>", updateBondEntries)

Sekcja: pozycja wiązania podwójnego

doubleBondFrame = tk.Frame(root, bg="#f7f9fc") tk.Label(doubleBondFrame, text="Pozycja wiązania podwójnego:", bg="#f7f9fc", anchor="w").grid(row=0, column=0, sticky="w") doubleBondEntry = tk.Entry(doubleBondFrame, bg="#f0f8ff", relief="flat") doubleBondEntry.grid(row=0, column=1, sticky="we")

Sekcja: pozycja wiązania potrójnego

tripleBondFrame = tk.Frame(root, bg="#f7f9fc") tk.Label(tripleBondFrame, text="Pozycja wiązania potrójnego:", bg="#f7f9fc", anchor="w").grid(row=0, column=0, sticky="w") tripleBondEntry = tk.Entry(tripleBondFrame, bg="#f0f8ff", relief="flat") tripleBondEntry.grid(row=0, column=1, sticky="we")

Sekcja dodawania podstawników

tk.Label(root, text="Dodaj podstawniki (pozycja i typ):", bg="#f7f9fc", anchor="w").grid(row=4, column=0, columnspan=2, sticky="w") substituentPositionEntry = tk.Entry(root, bg="#f0f8ff", relief="flat") substituentPositionEntry.grid(row=5, column=0, sticky="we")

substituentTypeVar = tk.StringVar() substituentTypeMenu = ttk.Combobox(root, textvariable=substituentTypeVar, values=["CH3", "C2H5", "Cl", "Br", "F", "NO2"], state="readonly") substituentTypeMenu.grid(row=5, column=1, sticky="we")

Przycisk dodający podstawniki

tk.Button(root, text="Dodaj +", command=addSubstituent, bg="#c6f1d6", relief="flat").grid(row=5, column=2, sticky="w")

Ramka z listą dodanych podstawników

substituentDisplayFrame = tk.Frame(root, bg="#f7f9fc") substituentDisplayFrame.grid(row=6, column=0, columnspan=3, sticky="we")

Etykiety z wynikami

resultName = tk.StringVar() resultFormula = tk.StringVar()

tk.Label(root, text="Nazwa:", bg="#f7f9fc", anchor="w").grid(row=7, column=0, sticky="w") resultNameLabel = tk.Label(root, textvariable=resultName, bg="#ffffff", relief="flat", anchor="w") resultNameLabel.grid(row=7, column=1, columnspan=2, sticky="we")

tk.Label(root, text="Wzór sumaryczny:", bg="#f7f9fc", anchor="w").grid(row=8, column=0, sticky="w") resultFormulaLabel = tk.Label(root, textvariable=resultFormula, bg="#ffffff", relief="flat", anchor="w") resultFormulaLabel.grid(row=8, column=1, columnspan=2, sticky="we")

Przyciski: Generuj i Zamknij

tk.Button(root, text="Generuj", command=generate, bg="#b5e3f3", relief="flat").grid(row=9, column=0, sticky="we") tk.Button(root, text="Zamknij", command=root.quit, bg="#f7d1cd", relief="flat").grid(row=9, column=2, sticky="we")

Uruchomienie głównej pętli aplikacji

root.mainloop()
