import re
import orodja


vzorec = (
    r'<div class="rt-tr-group" role="rowgroup">'
    r'.*?'
    r'<span>(?P<mesto>\d+)</span>'
    r'.*?'
    r'href="(?P<link>https://fortune.com/global500/2019/(?P<poenostavljeno>.+?)/)">'
    r'.*?'
    r'<span><div>(?P<firma>.+?)</div></span>'
    r'.*?'
    r'<span>.+?</span>' # prihodki
    r'.*?'
    r'<span>.+?</span>' # sprememba prihodkov
    r'.*?'
    r'<span>.+?</span>' # dobicek
    r'.*?'
    r'<span>.+?</span>' # sredstva
    r'.*?'
    r'<span>.+?</span>' # sprememba dobicka
    r'.*?'
    r'<span>.+?</span>' # zaposleni
    r'.*?'
    r'<span>(?P<sprememba_na_lestvici>.+?)</span>'
    r'.*?'
    r'<span><div>(?P<drzava>.+?)</div></span>'
    r'.*?'
    r'</div></div></div>'
)

vzorec_na_strani = (
    r'"key":"revenues","value":"(?P<prihodki>.+?)"'
    r'.*?'
    r'"key":"revchange","value":"(?P<sprememba_prihodkov>.+?)"'
    r'.*?'
    r'"key":"profits","value":"(?P<dobicek>.+?)"'
    r'.*?'
    r'"key":"prftchange","value":"(?P<sprememba_dobicka>.+?)"'
    r'.*?'
    r'"key":"assets","value":"(?P<sredstva>.+?)"'
    r'.*?'
    r'"key":"employees","value":"(?P<zaposleni>.+?)"'
    r'.*?'
    r'"key":"ceo","value":"(?P<direktor>.+?)"'
    r'.*?'
    r'"key":"sector","value":"(?P<sektor>.+?)"'
    r'.*?'
    r'"key":"industry","value":"(?P<industrija>.+?)"'
    r'.*?'
    r'"key":"yearsonlist","value":"(?P<leta_na_lestvici>.+?)"'
)


def nalozi_firme():
    firme = []
    count = 0
    for n in range(1,6):
        vsebina = orodja.vsebina_datoteke('Spletne_strani/Global 500 _ Fortune' + str(n) + '.html')

        for zadetek in re.finditer(vzorec, vsebina):
            firme.append(zadetek.groupdict())
            count += 1
    return firme

def dodaj_letosnje_podatke(firma):
    ime_datoteke = 'Spletne_strani/Firme/' + firma['poenostavljeno'] + '/2019.html'
    orodja.shrani_spletno_stran(firma['link'], ime_datoteke)
    vsebina_strani = orodja.vsebina_datoteke(ime_datoteke)
    for zadetek in re.finditer(vzorec_na_strani, vsebina_strani):
        podatki_firme = zadetek.groupdict()
    firma.update(podatki_firme)

def dodaj_podatke_zadnjih_let(firma):
    dodaj_slovar_vecih_let(firma)
    leta = ['2018','2017','2016']
    for leto in leta:
        nalozi_podatke_starega_leta(firma,leto)

def dodaj_slovar_vecih_let(firma):
    slovar = {'vec_letna_sredstva':{'2019':firma['sredstva']},
                    'vec_letni_prihodki':{'2019':firma['prihodki']},
                    'vec_letni_dobicki':{'2019':firma['dobicek']},
                    'vec_letni_zaposleni':{'2019':firma['zaposleni']}
                    }
    firma.update(slovar)

def nalozi_podatke_starega_leta(firma,leto):
    ime_datoteke = 'Spletne_strani/Firme/' + firma['poenostavljeno'] + '/' + leto + '.html'
    orodja.shrani_spletno_stran(firma['link'].replace('2019',leto), ime_datoteke)
    vsebina_strani = orodja.vsebina_datoteke(ime_datoteke)
    zadetek = None
    for zadetek in re.finditer(vzorec_na_strani, vsebina_strani):
        zadetek = zadetek
        podatki_firme = zadetek.groupdict()
    if zadetek == None:
        podatki_firme = {'sredstva':'-','prihodki':'-','dobicek':'-','zaposleni':'-'}
    firma['vec_letna_sredstva'].update({leto:podatki_firme['sredstva']})
    firma['vec_letni_prihodki'].update({leto:podatki_firme['prihodki']})
    firma['vec_letni_dobicki'].update({leto:podatki_firme['dobicek']})
    firma['vec_letni_zaposleni'].update({leto:podatki_firme['zaposleni']})

def uredi_podatke(firma):
    firma.pop('link')
    firma.pop('poenostavljeno')
    if firma['sprememba_na_lestvici'] == "-":
        firma['sprememba_na_lestvici'] = 0
    else:
        firma['sprememba_na_lestvici'] = int(firma['sprememba_na_lestvici'])
    floati = ['prihodki','sprememba_prihodkov','dobicek','sprememba_dobicka','sredstva']
    for key in floati:
        if firma[key] == '",':
            firma[key] = float(0)
        else:
            firma[key] = float(firma[key])
    integeri = ['mesto','leta_na_lestvici','zaposleni']
    for key in integeri:
        firma[key] = int(firma[key])
    vec_letni_slovarji = ['vec_letna_sredstva','vec_letni_prihodki','vec_letni_dobicki','vec_letni_zaposleni']
    for vec_letni_slovar in vec_letni_slovarji:
        slovar = firma[vec_letni_slovar]
        for key in slovar:
            if slovar[key] != '-':
                if vec_letni_slovar == "vec_letni_zaposleni":
                    slovar[key] = int(slovar[key])
                else:
                    slovar[key] = float(slovar[key])

def izloci_vec_letne_podatke(firme):
    sredstva, prihodki, dobicki, zaposleni = [], [], [], []
    for firma in firme:
        slovar = {'firma':firma['firma']}
        drugi_slovar = firma.pop('vec_letna_sredstva')
        slovar.update({key:drugi_slovar[key] for key in drugi_slovar})
        sredstva.append(slovar)
        slovar = {'firma':firma['firma']}
        drugi_slovar = firma.pop('vec_letni_prihodki')
        slovar.update({key:drugi_slovar[key] for key in drugi_slovar})
        prihodki.append(slovar)
        slovar = {'firma':firma['firma']}
        drugi_slovar = firma.pop('vec_letni_dobicki')
        slovar.update({key:drugi_slovar[key] for key in drugi_slovar})
        dobicki.append(slovar)
        slovar = {'firma':firma['firma']}
        drugi_slovar = firma.pop('vec_letni_zaposleni')
        slovar.update({key:drugi_slovar[key] for key in drugi_slovar})
        zaposleni.append(slovar)
    return sredstva, prihodki, dobicki, zaposleni

firme = nalozi_firme()
for firma in firme:
    dodaj_letosnje_podatke(firma)
    dodaj_slovar_vecih_let(firma)
    dodaj_podatke_zadnjih_let(firma)
    uredi_podatke(firma)
orodja.zapisi_json(firme, 'Zajeti_podatki/firme.json')
sredstva, prihodki, dobicki, zaposleni = izloci_vec_letne_podatke(firme)
orodja.zapisi_csv(firme,
    ['mesto','firma','sprememba_na_lestvici','direktor','drzava','sektor','industrija','leta_na_lestvici','prihodki','sprememba_prihodkov','dobicek','sprememba_dobicka','sredstva','zaposleni'],
    'Zajeti_podatki/firme.csv',)
orodja.zapisi_csv(sredstva,
    ['firma','2019','2018','2017','2016'],
    'Zajeti_podatki/vec_letna_sredstva.csv')
orodja.zapisi_csv(prihodki,
    ['firma','2019','2018','2017','2016'],
    'Zajeti_podatki/vec_letni_prihodki.csv')
orodja.zapisi_csv(dobicki,
    ['firma','2019','2018','2017','2016'],
    'Zajeti_podatki/vec_letni_dobicki.csv')
orodja.zapisi_csv(zaposleni,
    ['firma','2019','2018','2017','2016'],
    'Zajeti_podatki/vec_letni_zaposleni.csv')


