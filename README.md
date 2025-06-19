# ENGETO PYTHON AKADEMIE – PROJEKT 3
---
Třetí projekt Python Akademie

## POPIS PROJEKTU
---
Tento projekt slouží k extrakci výsledků z parlamentních voleb v roce 2017.  
Vstupem je URL adresa s výsledky pro daný okres.  
Výstupem je `.csv` soubor s výsledky jednotlivých obcí a politických stran.

Oficiální zdroj: [volby.cz](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)

---

## INSTALACE KNIHOVEN
---
Doporučeno je použít **virtuální prostředí**.

### 1. VYTVOŘENÍ VIRTUÁLNÍHO PROSTŘEDÍ

```bash
python3 -m venv .venv
```
### 2. AKTIVACE VIRTUÁLNÍHO PROSTŘEDÍ


Pro Linux/macOS:
```bash
source .venv/bin/activate
```
Pro Windows:
```bash
.venv\Scripts\activate
```
### 3. INSTALACE KNIHOVEN
```bash
pip3 install -r requirements.txt
```

Použité knihovny:

- requests – pro stahování dat z webu
- beautifulsoup4 – pro parsování HTML

## SPUŠTĚNÍ PROJEKTU
---
Program se spouští s těmito argumenty:
```bash
python main.py <url_okresu> <vystupni_soubor.csv>
```
## PŘÍKLAD:
---
```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3101" "vysledky_ceske_budejovice.csv"
```

## STRUČNÝ PRŮBĚH PROGRAMU
---
📡 Načítám stránku: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3101  
🔍 Nalezeno 109 obcí
📡 Načítám stránku: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=3&xobec=535826&xvyber=3101  
🔁 1/109 – Adamov
📡 Načítám stránku: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=3&xobec=535826&xvyber=3101  
🔁 2/109 – Bečice
📡 Načítám stránku: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=3&xobec=536156&xvyber=3101  
🔁 3/109 – Borek
📡 Načítám stránku: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=3&xobec=544272&xvyber=3101  
🔁 4/109 – Borovany
📡 Načítám stránku: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=3&xobec=544281&xvyber=3101  
🔁 5/109 – Borovnice
📡 Načítám stránku: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=3&xobec=535681&xvyber=3101  
🔁 6/109 – Boršov nad Vltavou
📡 Načítám stránku: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=3&xobec=544299&xvyber=3101  
...  
💾 Data uložena do souboru: vysledky_ceske_budejovice.csv  

## STRUKTURA CSV SOUBORU
---

Každý řádek reprezentuje jednu obec. Sloupce zahrnují:

- Kód obce  
- Název obce  
- Počet voličů, obálek, platných hlasů  
- Výsledky jednotlivých politických stran (v %)

**Ukázka:**

```
Kód obce,Název obce,Registrovaní,Obálky,Platné,Občanská demokratická strana...
535826,Adamov,682,474,472,"19,27 %","0,00 %","0,42 %",...
536156,Bečice,82,63,63,"4,76 %","0,00 %","0,00 %",...
544272,Borek,1 215,923,914,"13,45 %","0,10 %",...
```

