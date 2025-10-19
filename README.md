# Fribbble
🎨 Fribbble — yksinkertainen Dribbble-klooni (oppimisprojekti)

Fribbble on Flask-sovellus, jonka avulla käyttäjät voivat jakaa kuviaan, selata muiden julkaisuja sekä hallita omia sisältöjään. Projekti on osa harjoitustyötä, ja sen avulla harjoitellaan mm. autentikointia, CRUD-toiminnallisuuksia sekä relaatiotietokannan käyttöä.

---

## ✨ Ominaisuudet

- 🔐 **Autentikointi** — Käyttäjä voi luoda tunnuksen ja kirjautua sisään.
- 📤 **Sisällön hallinta** — Käyttäjä voi lisätä uusia kuvia, muokata niitä ja poistaa omiaan.
- 👀 **Sisällön selaus** — Kaikki käyttäjien lisäämät kuvat näkyvät etusivulla.
- 🔍 **Haku** — Käyttäjä voi hakea kuvia nimen perusteella.

---

## 🚀 Käynnistysohjeet

1. **Asenna riippuvuudet**

   pip install flask 

2. **Luo tietokanta**

    sqlite3 database.db < schema.sql
    sqlite3 database.db < init.sql

3. **Luo config.py**

    secret_key = "valitse-tähän-jokin-satunnainen-merkkijono"

4. **Käynnistä sovellus**

    flask run

5. **Avaa selaimessa**

    http://127.0.0.1:5000/

## 🧪 Testausohjeet

    Luo tunnus kohdasta Luo tunnus.

    Kirjaudu sisään.

    Lisää uusi kuva valitsemalla New picture.

    Muokkaa tai poista kuva omalta sivultaan.

    Hae kuvia etusivun hakulaatikolla.

## Arvosana tavoite on 3 tämän projektin kautta osana oppimistani ja kehitystäni.