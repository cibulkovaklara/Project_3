import sys
import csv
import requests
from bs4 import BeautifulSoup

ZAKLADNI_URL = "https://volby.cz/pls/ps2017nss/"


def nacti_html(stranka):
    """Stáhne a vrátí HTML parser BeautifulSoup ze zadané adresy."""
    try:
        print(f"📡 Načítám stránku: {stranka}")
        odpoved = requests.get(stranka)
        odpoved.raise_for_status()
        return BeautifulSoup(odpoved.text, "html.parser")
    except requests.exceptions.RequestException as chyba:
        print(f"💥 Chyba při načítání stránky: {chyba}")
        sys.exit(1)


def najdi_obce(parsed_html):
    """Získá názvy obcí, jejich kódy a odkazy na detaily."""
    jmena = [td.text.strip() for td in parsed_html.select("td.overflow_name")]
    cisla = [td.text.strip() for td in parsed_html.select("td.cislo")]
    odkazy = [ZAKLADNI_URL + a["href"] for a in parsed_html.select("td.cislo a")]
    return jmena, cisla, odkazy


def ziskej_strany(odkaz):
    """Vrátí seznam politických stran z detailu první obce."""
    soup = nacti_html(odkaz)
    return [td.text.strip() for td in soup.select("td.overflow_name")]


def zpracuj_jednu_obec(odkaz):
    """Získá volební výsledky pro konkrétní obec."""
    soup = nacti_html(odkaz)

    try:
        registrovani = soup.select_one("td[headers='sa2']").text.strip().replace('\xa0', ' ')
        obalky = soup.select_one("td[headers='sa3']").text.strip().replace('\xa0', ' ')
        platne_hlasy = soup.select_one("td[headers='sa6']").text.strip().replace('\xa0', ' ')
    except AttributeError:
        return None  # chybějící data

    vysledky = []
    for td in soup.select("td.cislo"):
        hlavicka = td.get("headers", "")
        if "t1sb4" in hlavicka or "t2sb4" in hlavicka:
            hlas = td.text.strip().replace('\xa0', ' ') or "0"
            vysledky.append(hlas)

    return [registrovani, obalky, platne_hlasy] + vysledky


def exportuj_csv(jmeno_souboru, hlavicka, obsah):
    """Uloží data do CSV souboru."""
    try:
        with open(jmeno_souboru, "w", encoding="utf-8", newline="") as f:
            zapisovac = csv.writer(f)
            zapisovac.writerow(hlavicka)
            zapisovac.writerows(obsah)
        print(f"💾 Data uložena do souboru: {jmeno_souboru}")
    except IOError as chyba:
        print(f"🚫 Chyba při ukládání souboru: {chyba}")


def hlavni_spusteni(url, vystup_soubor, test=False):
    html = nacti_html(url)
    obce, kody, odkazy = najdi_obce(html)

    print(f"🔍 Nalezeno {len(obce)} obcí")

    strany = ziskej_strany(odkazy[0])
    hlavicka = [
        "Kód obce",
        "Název obce",
        "Registrovaní voliči",
        "Vydané obálky",
        "Platné hlasy",
    ] + strany

    tabulka = []
    for idx, (kod, obec, link) in enumerate(zip(kody, obce, odkazy), 1):
        print(f"🔁 {idx}/{len(obce)} – {obec}")
        radek = zpracuj_jednu_obec(link)
        if radek:
            tabulka.append([kod, obec] + radek)

    if test:
        print("\n🧪 Testovací režim – náhled dat:\n")
        print(hlavicka)
        for radek in tabulka[:3]:
            print(radek)
    else:
        exportuj_csv(vystup_soubor, hlavicka, tabulka)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("\nPoužití:\n  python main.py <URL> <výstupní_soubor.csv> [--test]")
        print("\nPříklad:")
        print(
            '  python main.py '
            '"https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3101" '
            '"vysledky.csv"\n'
        )
        sys.exit(1)

    adresa = sys.argv[1]
    vystup = sys.argv[2]
    test_rezim = "--test" in sys.argv

    hlavni_spusteni(adresa, vystup, test_rezim)
