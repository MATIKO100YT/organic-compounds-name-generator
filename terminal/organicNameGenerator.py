# ------------------------------------
# Copyright (c) 2025 Mateusz Celiński
# Licensed under the MIT license
# See LICENSE.txt for details
# ------------------------------------

# Function that generates the prefix of the organic compound name
# Argument: number of carbon atoms in the compound
# Returns the prefix for a specific number of carbon atoms
def generatePrefix(carbonCount):
    # dictionary with prefixes
    specificNames = {
        1: "met", 2: "et", 3: "prop", 4: "but", 5: "pent", 6: "heks", 7: "hept", 8: "okt", 9: "non", 10: "dek", 11: "undek", 12: "dodek", 13: "tridek", 14: "tetradek", 15: "pentadek", 16: "heksadek", 17: "heptadek", 18: "oktadek", 19: "nonadek", 20: "ikoz"
    }
    if carbonCount in specificNames:
        return specificNames[carbonCount]
    else:
        raise ValueError("Number of carbon atoms must be between 1 and 20.")

# Function that calculates the number of hydrogen atoms
# Arguments: number of carbon atoms and the position of a double/triple bond 
# (only the presence of the bond matters — if none, pass None)
# Returns the number of hydrogen atoms
def calculateHydrogens(carbonCount, doubleBond, tripleBond):
    baseHydrogens = 2 * carbonCount + 2
    if doubleBond:
        baseHydrogens -= 2
    if tripleBond:
        baseHydrogens -= 4
    return baseHydrogens

# Function that generates the prefix for substituents
# Argument: list of substituents
# Returns the generated prefix
def generateSubstituentString(substituents):
    substituentCounts = {}
    # Loop checking the position of each substituent
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
    # Loop generating appropriate prefixes for substituents considering their position and quantity
    for type_, positions in sorted(substituentCounts.items(), key=lambda x: substituentOrder.get(x[0], x[0])):
        count = len(positions)
        positionsStr = ",".join(map(str, sorted(positions)))
        prefix = substituentOrder.get(type_, type_)
        multiplicativePrefix = {
            1: "", 2: "di", 3: "tri", 4: "tetra", 5: "penta", 6: "heksa", 7: "hepta", 8: "okta", 9: "nona", 10: "deka"
        }.get(count, f"{count}-")
        substituentStrings.append(f"{positionsStr}-{multiplicativePrefix}{prefix}")

    return "-".join(substituentStrings)

# Function that generates the full name of an organic compound according to IUPAC rules
# Arguments: number of carbon atoms, type of compound, position of double/triple bond, and list of substituents
# Returns the generated name
def generateIUPACName(carbonCount, compoundType, doubleBond, tripleBond, substituents):
    baseName = generatePrefix(carbonCount)

    substituentString = generateSubstituentString(substituents)
    if substituentString:
        baseName = f"{substituentString}{baseName}"

    if compoundType == "alken" and doubleBond:
        baseName += f"-{doubleBond}-en"
    elif compoundType == "alkin" and tripleBond:
        baseName += f"-{tripleBond}-yn"
    else:
        baseName += "an"

    return baseName

# Function that calculates the molecular formula of the compound
# Arguments: number of carbon atoms and list of substituents
# Returns the molecular formula
def calculateMolecularFormula(carbonCount, substituents):
    hydrogenCount = 2 * carbonCount + 2
    elementCounts = {"C": carbonCount, "H": hydrogenCount}

    for position, substituent in substituents:
        if substituent == "CH3":
            elementCounts["C"] += 1
            elementCounts["H"] += 3
            elementCounts["H"] -= 1
        elif substituent == "C2H5":
            elementCounts["C"] += 2
            elementCounts["H"] += 5
            elementCounts["H"] -= 1
        elif substituent == "Cl" or substituent == "Br" or substituent == "F" or substituent == "NO2":
            elementCounts["H"] -= 1
            elementCounts[substituent] = elementCounts.get(substituent, 0) + 1

    formulaParts = []
    for element, count in elementCounts.items():
        if count > 1:
            formulaParts.append(f"{element}{count}")
        elif count == 1:
            formulaParts.append(f"{element}")

    return "".join(formulaParts)

def main():
    # List of available substituents
    substituentsList = ["CH3", "C2H5", "Cl", "Br", "F", "NO2"]

    print("=== Organic Compounds Name Generator ===")

    while True:
        try:
            print("\nMenu:")
            print("1 - Generate compound name")
            print("2 - Exit")
            menuChoice = input("Choose an option: ")

            if menuChoice == "2":
                print("Program terminated.")
                break

            if menuChoice != "1":
                print("Invalid choice.")
                continue

            carbonCount = int(input("Enter the number of carbon atoms (1-20): "))
            if carbonCount < 1 or carbonCount > 20:
                raise ValueError("Number of carbon atoms must be between 1 and 20.")

            print("Type of compound:")
            print("1 - Alkane")
            print("2 - Alkene")
            print("3 - Alkyne")
            compoundType = input("Choose the type of compound: ")

            doubleBond = None
            tripleBond = None
            if compoundType == "2":
                compoundType = "alken"
                doubleBond = int(input("Enter the position of the double bond: "))
            elif compoundType == "3":
                compoundType = "alkin"
                tripleBond = int(input("Enter the position of the triple bond: "))
            else:
                compoundType = "alkan"

            substituents = []
            print(f"Available substituents: {', '.join(substituentsList)}")
            print("Adding substituents (type 'stop' to finish):")
            while True:
                position = input("Enter the position of the substituent: ")
                if position.lower() == "stop":
                    break
                substituent = input("Enter the type of substituent: ")
                if substituent in substituentsList:
                    substituents.append((int(position), substituent))
                else:
                    print("Invalid substituent type.")

            iupacName = generateIUPACName(carbonCount, compoundType, doubleBond, tripleBond, substituents)
            molecularFormula = calculateMolecularFormula(carbonCount, substituents)

            print(f"Name: {iupacName}")
            print(f"Molecular formula: {molecularFormula}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()