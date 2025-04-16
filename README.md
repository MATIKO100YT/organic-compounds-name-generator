# Generator nazw związków organicznych
###### <i>Note: for Polish speakers only (for now)<i>

Jest to prosty generator nazw związków organicznych zgodny z zasadami IUPAC (Międzynarodowej Unii Chemii Czystej i Stosowanej).

## Obsługiwane typy związków (na ten moment) to:
- alkany
- alkeny
- alkiny

## Jak zbudować?
Jeśli nie chcesz korzystać z gotowego pliku .exe, możesz sam zbudować cały projekt.
### Krok po kroku jak to zrobić
- sklonuj całe repo
```bash
git clone https://github.com/MATIKO100YT/organic-compound-name-generator.git
```
- przejdź do repo
```bash
cd organic-compound-name-generator
'''
- zainstaluj [Pyinstallera]() z repo lub przez ```bash pip install pyinstaller ```
- wywołaj ```bash pyinstaller --name "Generator nazw związków organicznych" --noconsole --onefile organicNameGeneratorGUI.py ```
- wygenerowany ```bash .exe ``` znajdziesz w ```bash dist/ ```

## Dodatkowe zasoby
- dokumentacja [Pyinstallera](https://pyinstaller.org/en/stable/)