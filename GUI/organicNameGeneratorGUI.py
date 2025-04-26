# ------------------------------------
# Copyright (c) 2025 Mateusz Celiński
# Licensed under the MIT license
# See LICENSE.txt for details
# ------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox

# Returns the prefix of the hydrocarbon name based on the number of carbon atoms
def generatePrefix(carbonCount):
    specificNames = {
        1: "met", 2: "et", 3: "prop", 4: "but", 5: "pent", 6: "heks", 7: "hept", 8: "okt", 9: "non", 10: "dek",
        11: "undek", 12: "dodek", 13: "tridek", 14: "tetradek", 15: "pentadek", 16: "heksadek", 17: "heptadek", 18: "oktadek", 19: "nonadek", 20: "ikoz"
    }
    return specificNames.get(carbonCount, "")

# Calculates the number of hydrogen atoms for a given compound (alkane, alkene, or alkyne)
def calculateHydrogens(carbonCount, doubleBond, tripleBond):
    baseHydrogens = 2 * carbonCount + 2
    if doubleBond:
        baseHydrogens -= 2
    if tripleBond:
        baseHydrogens -= 4
    return baseHydrogens

# Creates a string representing substituents and their positions in the name
def generateSubstituentString(substituents):
    substituentCounts = {}
    for position, type_ in substituents:
        if type_ not in substituentCounts:
            substituentCounts[type_] = []
        substituentCounts[type_].append(position)

    substituentOrder = {
        "CH3": "metylo",
        "C2H5": "etylo",
        "Cl": "chloro",
        "Br": "bromo",
        "F": "fluoro",
        "NO2": "nitro",
    }

    substituentStrings = []
    for type_, positions in sorted(substituentCounts.items(), key=lambda x: substituentOrder.get(x[0], x[0])):
        count = len(positions)
        positionsStr = ",".join(map(str, sorted(positions)))
        prefix = substituentOrder.get(type_, type_)
        multiplicativePrefix = {
            1: "", 2: "di", 3: "tri", 4: "tetra", 5: "penta", 6: "heksa", 7: "hepta", 8: "okta", 9: "nona", 10: "deka"
        }.get(count, f"{count}-")
        substituentStrings.append(f"{positionsStr}-{multiplicativePrefix}{prefix}")

    return "-".join(substituentStrings)

# Generates the full IUPAC name based on the number of carbon atoms, compound type, bonds, and substituents
def generateIUPACName(carbonCount, compoundType, doubleBond, tripleBond, substituents):
    baseName = generatePrefix(carbonCount)

    substituentString = generateSubstituentString(substituents)
    if substituentString:
        baseName = f"{substituentString}{baseName}"

    if compoundType == "alken" and doubleBond:
        baseName += f"{doubleBond}-en"
    elif compoundType == "alkin" and tripleBond:
        baseName += f"{tripleBond}-yn"
    else:
        baseName += "an"

    return baseName

# Calculates the molecular formula of the compound, considering the substituents
def calculateMolecularFormula(carbonCount, substituents):
    hydrogenCount = 2 * carbonCount + 2
    elementCounts = {"C": carbonCount, "H": hydrogenCount}

    for position, substituent in substituents:
        if substituent == "CH3":
            elementCounts["C"] += 1
            elementCounts["H"] += 3
            elementCounts["H"] -= 1  # substituent replaces 1 H atom
        elif substituent == "C2H5":
            elementCounts["C"] += 2
            elementCounts["H"] += 5
            elementCounts["H"] -= 1
        elif substituent in ["Cl", "Br", "F", "NO2"]:
            elementCounts["H"] -= 1
            elementCounts[substituent] = elementCounts.get(substituent, 0) + 1

    formulaParts = []
    for element, count in elementCounts.items():
        if count > 1:
            formulaParts.append(f"{element}{count}")
        elif count == 1:
            formulaParts.append(f"{element}")

    return "".join(formulaParts)

# Updates visible bond position entry fields depending on the compound type
def updateBondEntries(event):
    compoundType = compoundTypeVar.get()
    if compoundType == "alken":
        doubleBondFrame.grid(row=3, column=0, columnspan=2, sticky="we")
        tripleBondFrame.grid_remove()
    elif compoundType == "alkin":
        tripleBondFrame.grid(row=3, column=0, columnspan=2, sticky="we")
        doubleBondFrame.grid_remove()
    else:
        doubleBondFrame.grid_remove()
        tripleBondFrame.grid_remove()

# Generates the name and formula based on user input
def generate():
    try:
        carbonCount = int(carbonEntry.get())
        if carbonCount < 1 or carbonCount > 20:
            raise ValueError("The number of carbon atoms must be between 1 and 20.")

        compoundType = compoundTypeVar.get()
        doubleBond = int(doubleBondEntry.get()) if compoundType == "alken" else None
        tripleBond = int(tripleBondEntry.get()) if compoundType == "alkin" else None

        substituents = []
        for pos, sub in substituentData:
            substituents.append((int(pos), sub))

        name = generateIUPACName(carbonCount, compoundType, doubleBond, tripleBond, substituents)
        formula = calculateMolecularFormula(carbonCount, substituents)

        resultName.set(name)
        resultFormula.set(formula)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Adds a substituent to the list and refreshes the display
def addSubstituent():
    position = substituentPositionEntry.get()
    substituent = substituentTypeVar.get()
    if position.isdigit() and substituent:
        substituentData.append((position, substituent))
        refreshSubstituentDisplay()
    else:
        messagebox.showerror("Error", "Please provide a valid position and substituent type.")

# Removes a substituent from the list
def removeSubstituent(index):
    if 0 <= index < len(substituentData):
        del substituentData[index]
        refreshSubstituentDisplay()

# Refreshes the display of the substituents list in the GUI
def refreshSubstituentDisplay():
    for widget in substituentDisplayFrame.winfo_children():
        widget.destroy()

    for i, (pos, sub) in enumerate(substituentData):
        tk.Label(substituentDisplayFrame, text=f"{pos}: {sub}", bg="#f0f8ff", anchor="w").grid(row=i, column=0, sticky="w")
        tk.Button(substituentDisplayFrame, text="-", command=lambda idx=i: removeSubstituent(idx), bg="#ffb6b9", relief="flat", width=2).grid(row=i, column=1, sticky="e")

# Initialize the GUI
root = tk.Tk()
root.title("Organic Compound Name Generator")
root.configure(bg="#f7f9fc")
root.geometry("550x600")

substituentData = []  # Stores substituent data

# User Interface - labels, entries, buttons
tk.Label(root, text="Number of carbon atoms (1-20):", bg="#f7f9fc", anchor="w").grid(row=0, column=0, sticky="w")
carbonEntry = tk.Entry(root, bg="#f0f8ff", relief="flat")
carbonEntry.grid(row=0, column=1, sticky="we")

compoundTypeVar = tk.StringVar(value="alkan")
tk.Label(root, text="Compound type:", bg="#f7f9fc", anchor="w").grid(row=1, column=0, sticky="w")
compoundTypeMenu = ttk.Combobox(root, textvariable=compoundTypeVar, values=["alkan", "alken", "alkin"], state="readonly")
compoundTypeMenu.grid(row=1, column=1, sticky="we")
compoundTypeMenu.bind("<<ComboboxSelected>>", updateBondEntries)

# Bond position input fields
doubleBondFrame = tk.Frame(root, bg="#f7f9fc")
tk.Label(doubleBondFrame, text="Double bond position:", bg="#f7f9fc", anchor="w").grid(row=0, column=0, sticky="w")
doubleBondEntry = tk.Entry(doubleBondFrame, bg="#f0f8ff", relief="flat")
doubleBondEntry.grid(row=0, column=1, sticky="we")

tripleBondFrame = tk.Frame(root, bg="#f7f9fc")
tk.Label(tripleBondFrame, text="Triple bond position:", bg="#f7f9fc", anchor="w").grid(row=0, column=0, sticky="w")
tripleBondEntry = tk.Entry(tripleBondFrame, bg="#f0f8ff", relief="flat")
tripleBondEntry.grid(row=0, column=1, sticky="we")

# Section to add substituents
tk.Label(root, text="Add substituents (position and type):", bg="#f7f9fc", anchor="w").grid(row=4, column=0, columnspan=2, sticky="w")
substituentPositionEntry = tk.Entry(root, bg="#f0f8ff", relief="flat")
substituentPositionEntry.grid(row=5, column=0, sticky="we")

substituentTypeVar = tk.StringVar()
substituentTypeMenu = ttk.Combobox(root, textvariable=substituentTypeVar, values=["CH3", "C2H5", "Cl", "Br", "F", "NO2"], state="readonly")
substituentTypeMenu.grid(row=5, column=1, sticky="we")

tk.Button(root, text="Add +", command=addSubstituent, bg="#c6f1d6", relief="flat").grid(row=5, column=2, sticky="w")
substituentDisplayFrame = tk.Frame(root, bg="#f7f9fc")
substituentDisplayFrame.grid(row=6, column=0, columnspan=3, sticky="we")

# Result fields: name and molecular formula
resultName = tk.StringVar()
resultFormula = tk.StringVar()

tk.Label(root, text="Name:", bg="#f7f9fc", anchor="w").grid(row=7, column=0, sticky="w")
resultNameLabel = tk.Label(root, textvariable=resultName, bg="#ffffff", relief="flat", anchor="w")
resultNameLabel.grid(row=7, column=1, columnspan=2, sticky="we")

tk.Label(root, text="Molecular formula:", bg="#f7f9fc", anchor="w").grid(row=8, column=0, sticky="w")
resultFormulaLabel = tk.Label(root, textvariable=resultFormula, bg="#ffffff", relief="flat", anchor="w")
resultFormulaLabel.grid(row=8, column=1, columnspan=2, sticky="we")

# Buttons: generate and close the application
tk.Button(root, text="Generate", command=generate, bg="#b5e3f3", relief="flat").grid(row=9, column=0, sticky="we")
tk.Button(root, text="Close", command=root.quit, bg="#f7d1cd", relief="flat").grid(row=9, column=2, sticky="we")

root.mainloop()