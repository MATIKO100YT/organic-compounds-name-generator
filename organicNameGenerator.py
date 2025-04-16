# ------------------------------------
# Copyright (c) 2025 Mateusz Celiński
# Licenced under the MIT license
# See LICENCE.txt for details
# ------------------------------------

# Funkcja generująca prefiks nazwy związku organicznego
# Argumentem jest ilość atomów węgla w związku
# Zwraca prefiks dla konkretnej liczby atomów
def generatePrefix(carbonCount):
	# słownik z prefiksami
    specificNames = {
    	1: "met", 2: "et", 3: "prop", 4: "but", 5: "pent", 6: "heks", 7: "hept", 8: "okt", 9: "non", 10: "dek", 11: "undek", 12: "dodek", 13: "tridek", 14: "tetradek", 15: "pentadek", 16: "heksadek", 17: "heptadek", 18: "oktadek", 19: "nonadek", 20: "ikoz"
    	}
    if carbonCount in specificNames:
        return specificNames[carbonCount]
    else:
        raise ValueError("Liczba atomów węgla musi być w przedziale 1-20.")

# Funkcja zliczająca ilość atomów wodoru
# Argumentami są ilość atomów węgla i pozycja wiązania podwójnego/potrójnego (znaczenie ma sam fakt obecności wiązania (jeśli nie ma = None) a nie pozycja)
# Zwraca ilość atomów wodoru
def calculateHydrogens(carbonCount, doubleBond, tripleBond):
    baseHydrogens = 2 * carbonCount + 2
    if doubleBond:
        baseHydrogens -= 2
    if tripleBond:
        baseHydrogens -= 4
    return baseHydrogens

# Funkcja generująca prefiks dla podstawników
# Argumentem jest lista podstawników
# Zwraca wygenerowany prefiks
def generateSubstituentString(substituents):
    substituentCounts = {}
    # Pętla sorawdzająca pozycję każdego podstawnika
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
    # Pętla generująca odpowiednie prefiksy dla podstawników z uwzględnieniem ich pozycji i ilości
    for type_, positions in sorted(substituentCounts.items(), key=lambda x: substituentOrder.get(x[0], x[0])):
        count = len(positions)
        positionsStr = ",".join(map(str, sorted(positions)))
        prefix = substituentOrder.get(type_, type_)
        multiplicativePrefix = {
            1: "", 2: "di", 3: "tri", 4: "tetra", 5: "penta", 6: "heksa", 7: "hepta", 8: "okta", 9: "nona", 10: "deka"
        }.get(count, f"{count}-")
        substituentStrings.append(f"{positionsStr}-{multiplicativePrefix}{prefix}")

    return "-".join(substituentStrings)

# Funkcja generująca pełną nazwę związku organicznego według zasad IUPAC
# Argumentami są: ilość węgli, typ związku, pozycja wiązania podwójnego/potrójnego oraz lista podstawników
# Zwraca wygenerowaną mazwę
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

# Funkcja generująca wzór sumaryczny związku
# Argumentami są ilość węgli i lista podstawników
# Zwraca wzór sumaryczny
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
	# Lista dostępnych podstawników
    substituentsList = ["CH3", "C2H5", "Cl", "Br", "F", "NO2"]

    print("=== Generator nazw związków organicznych ===")

    while True:
        try:
            print("\nMenu:")
            print("1 - Wygeneruj nazwę związku")
            print("2 - Wyjście")
            menuChoice = input("Wybierz opcję: ")

            if menuChoice == "2":
                print("Zakończono działanie programu.")
                break

            if menuChoice != "1":
                print("Nieprawidłowy wybór.")
                continue

            carbonCount = int(input("Podaj liczbę atomów węgla (1-20): "))
            if carbonCount < 1 or carbonCount > 20:
                raise ValueError("Liczba atomów węgla musi być w przedziale 1-20.")

            print("Typ związku:")
            print("1 - Alkan")
            print("2 - Alken")
            print("3 - Alkin")
            compoundType = input("Wybierz typ związku: ")

            doubleBond = None
            tripleBond = None
            if compoundType == "2":
                compoundType = "alken"
                doubleBond = int(input("Podaj pozycję wiązania podwójnego: "))
            elif compoundType == "3":
                compoundType = "alkin"
                tripleBond = int(input("Podaj pozycję wiązania potrójnego: "))
            else:
                compoundType = "alkan"

            substituents = []
            print(f"Dostępne podstawniki: {', '.join(substituentsList)}")
            print("Dodawanie podstawników (wpisz 'stop', aby zakończyć):")
            while True:
                position = input("Podaj pozycję podstawnika: ")
                if position.lower() == "stop":
                    break
                substituent = input("Podaj typ podstawnika: ")
                if substituent in substituentsList:
                    substituents.append((int(position), substituent))
                else:
                    print("Nieprawidłowy typ podstawnika.")

            iupacName = generateIUPACName(carbonCount, compoundType, doubleBond, tripleBond, substituents)
            molecularFormula = calculateMolecularFormula(carbonCount, substituents)

            print(f"Nazwa: {iupacName}")
            print(f"Wzór sumaryczny: {molecularFormula}")

        except Exception as e:
            print(f"Błąd: {e}")

if __name__ == "__main__":
    main()

