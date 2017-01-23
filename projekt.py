import orodja2
import re
import orodja3
import csv

def zajemi_plesnipari():
    osnovni_naslov = 'https://www.worlddancesport.org/Couple/List'
    parametri = 'divisionFilter=General&divisionFilter=Professional&statusFilter=Active&countryFilter=-1&ageGroupFilter=180&ageGroupFilter=179&ageGroupFilter=177&ageGroupFilter=178&ageGroupFilter=181&ageGroupFilter=182&ageGroupFilter=183&ageGroupFilter=196&ageGroupFilter=205&ageGroupFilter=206&ageGroupFilter=175&ageGroupFilter=176&formAction=&Column=JoinDate&Direction=Ascending&pageSize=100'
    for stran in range(1, 159):
        naslov = '{}?{}&page={}'.format(osnovni_naslov, parametri, stran)
        ime_datoteke = 'plesnipari/{:02}.html'.format(stran)
        orodja2.shrani(naslov, ime_datoteke)   

def pocisti_plesnipari(plesnipar):
    podatki = plesnipar.groupdict()
    podatki['plesalec'] = podatki['plesalec'].strip()
    podatki['plesalka'] = podatki['plesalka'].strip()
    podatki['drzava'] = podatki['drzava'].strip()
    podatki['kategorija'] = podatki['kategorija'].strip()
    podatki['idplesalca'] = podatki['idplesalca'].strip()
    return podatki

def pripravi_plesnipari():
    regex_plesnipar = re.compile(
        r'<td><a href="/Athlete/Detail/(?P<idplesalca>(\D*?-\w{8}-\w{4}-\w{4}-\w{4}-\w{12}))">(?P<plesalec>(\D*?))</a></td><td><a href="/Athlete/Detail/\D*?-\w{8}-\w{4}-\w{4}-\w{4}-\w{12}">(?P<plesalka>(\D*?))</a></td><td data-division="General" data-country="(?P<drzava>(\D*?))">(\D{3})</td><td>(?P<kategorija>(\D*?))</td>',
        flags=re.DOTALL
    )

    plesnipari = []
    for html_plesnipari in orodja2.datoteke('plesnipari/'):
        for plesnipar in re.finditer(regex_plesnipar, orodja2.vsebina_datoteke(html_plesnipari)):
            plesnipari.append(pocisti_plesnipari(plesnipar))

    orodja3.zapisi_tabelo(plesnipari, ['plesalec', 'plesalka', 'drzava', 'kategorija', 'idplesalca'], 'plesnipari.csv')       

with open('plesnipari.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    seznam = []
    for row in readCSV:
            seznam += [row[4]]
            seznam1 = seznam[1:]
    
def zajemi_nastope():
    osnovni_naslov = 'https://www.worlddancesport.org/Athlete/Detail/'
    for ime in seznam1:
        naslov = '{}{}'.format(osnovni_naslov, ime)
        ime_datoteke = 'tekmovanja/{}.html'.format(ime)
        orodja2.shrani(naslov, ime_datoteke)
        
def pocisti_tekmovanja(tekmovanje):
    podatki = tekmovanje.groupdict()
    podatki['uvrstitev'] = podatki['uvrstitev']
    podatki['datum'] = podatki['datum']
    podatki['kategorija2'] = podatki['kategorija2']
    podatki['disciplina'] = podatki['disciplina']
    podatki['dogodek'] = podatki['dogodek']
    podatki['kraj'] = podatki['kraj']
    podatki['drzava2'] = podatki['drzava2']
    return podatki

def pripravi_tekmovanja():
    regex_tekmovanje = re.compile(
        r'<td>(?P<uvrstitev>(\d*?.))</td><td class="dateColumn">'
        r'(?P<datum>(\d{2})(\D*?)(\d{4}))</td><td><a href="/Event/Competition/(\D*?)-(\d{5})/'
        r'(?P<kategorija2>(\D*?))-(?P<disciplina>(\D*?))-(\d{5})/Ranking">'
        r'(?P<dogodek>(\D*?))</a></td><td>(\D*?)</td><td>(\D*?)</td><td>'
        r'(?P<kraj>(\D*?))-(?P<drzava2>(\D*?))</td><td class="(\D*?)"></td>((</tr><tr class="(\D*?)">)|(</tr></tbody></table>))',
        flags=re.DOTALL
    )


    
    tekmovanja = []
    for html_tekmovanja in orodja2.datoteke('tekmovanja/'):
        print(html_tekmovanja)
        for tekmovanje in re.finditer(regex_tekmovanje, orodja2.vsebina_datoteke(html_tekmovanja)):
            s = pocisti_tekmovanja(tekmovanje)
            s["ime"] = html_tekmovanja.split("/")[1].split(".")[0]
            tekmovanja.append(s)

    orodja3.zapisi_tabelo(tekmovanja, ['ime', 'uvrstitev', 'datum', 'kategorija2', 'disciplina', 'dogodek', 'kraj', 'drzava2'], 'tekmovanja.csv')       

   
zajemi_plesnipari()   
pripravi_plesnipari()  
zajemi_nastope()   
pripravi_tekmovanja()
