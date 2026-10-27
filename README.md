# Scripting-Python
Third small assignment for Python 2026/2027 mimuw's course.

## Osoba 2: sciezki i JSON

Program tworzy strukture `root/Miesiac/Dzien/Pora/Dane.json`.
Miesiace sa parowane z przedzialami dni. Przedzialy sa domkniete.
Bez `-m` wybierane sa wszystkie miesiace; bez `-d` caly tydzien dla
kazdego miesiaca. Jesli podano obie listy, musza miec rowne dlugosci.
Pory dnia sa przypisywane kolejno do rozwinietej listy dni, a dla
pozostalych dni przyjmowane jest `Morning` (zgodnie z dotychczasowym kodem).
Powtorzone sciezki sa przetwarzane tylko raz.

Przyklad zapisu, a potem odczytu:

```sh
python file_manager.py -t -j -r data -m May June -d Monday-Wednesday Friday -p Evening
python file_manager.py -o -j -r data -m May June -d Monday-Wednesday Friday -p Evening
```

Zapis tworzy brakujace katalogi i nadpisuje `Dane.json` losowym rekordem:
`{"Model": "A", "Wynik": 17, "Czas": 465}`. Model to A/B/C, a Wynik i Czas
sa liczbami calkowitymi 0-1000; Czas jest wyrazony w sekundach.
Odczyt sumuje Czas tylko dla modelu A. Brakujace lub niepoprawne pliki
sa zglaszane i pomijane. Odczyt nie tworzy katalogow.

Funkcje `write_json(directory)` i `read_json(directory)` otrzymuja katalog,
nie pelna sciezke pliku. `generate_paths(...)` jedynie wyznacza sciezki.
Obsluga CSV pozostaje do implementacji przez osobe 1/3; proba jej uzycia
zglasza brak implementacji.

Testy (biblioteka standardowa, bez dodatkowych zaleznosci):

```sh
python -m unittest -v
```
