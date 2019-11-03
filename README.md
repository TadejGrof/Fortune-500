# Fortune-500

## Vzpostavitev programskega okolja:

Analiziral bom prvih 500 svetovnih gospodarskih družb glede na letni prihodek. Podateke bon zajel na strani
[fortune 500](https://fortune.com/global500/2019/search/)

Za vsako koorporacijo bom zajel:

* Ime ter sedež firme,
* Direktorja,
* Sektor in industrijo
* Število let na lestvici
* Spremembo na lestvici
* Za vsako leto:
    - Število zaposlenih
    - Letni prihodek in zaslužek,
    - Sredstva
    
Delovne hipoteze:

- Vzroki za večje skoke na lestvici
- Letne spremembe v odvisnosti od sektorja in indrustrije
- Večje število delavcev vodi do večjega prihodka vendar ne nujno zaslužka,

## Priprava podatkov:

Podatke sem zajel s skripto, ki se nahaja v datoteki zajemi_in_obdelaj.py.
Vse obdelane podatke sem shranil v datoteko firme.json, in jih nato locil tako, da sem osnovne podatke vsake firme ter letosnje rezultate shranil v datoteko firme.json, rezultate prejsnjih 4 let pa sem shranil v datoteke: vec_letna_sredstva.csv, vec_letni_prihodki.csv, vec_letni_dobicki.csv, vec_letni_zaposleni.csv.
   


