import csv
import re
import os
import codecs

from tkinter import Tk

from string import Template
from html.parser import HTMLParser


# Function parses selected database input, takes optional parameter flags and generates html file.
# Polish grammar word endings are taken into consideration while generating html file content.

def generateTemplate(dataIn,promoFlag,promoText,tytulInput,userOn,files,dd):

    branza = dataIn[1]
    stronawww = dataIn[2]
    if re.search('http://',stronawww) or re.search('https://',stronawww):
        stronawww = stronawww.replace("http://","")
        stronawww = stronawww.replace("https://","")
        stronawww = stronawww.split('/', 1)[0]
    pozycja = dataIn[3]
    checi = dataIn[4]
    imie = dataIn[7]
    miasto = dataIn[8]
    
    
    try:

	
	#if imie = '-'
        if (imie != 'Państwo') and (imie != '-'):
            tytul = tytulInput
        elif (imie == 'Państwo') and (not (tytulInput == '')):
            return 'Brak imienia w bazie danych.\nPole \'witam\' musi byc puste!'
        else:
            tytul = 'Państwa'
            imie = 'Państwo'
            
        if int(pozycja) < 11:
            dotarcie = '94%'
            potencjal = '6%'
        elif int(pozycja) < 21:
            dotarcie = '6%'
            potencjal = '94%'
        elif int(pozycja) < 31:
            dotarcie = '1,1%'
            potencjal = '98,9%'
        elif int(pozycja) < 51:
            dotarcie = '0,2%'
            potencjal = '99,8%'
        elif int(pozycja) < 101:
            dotarcie = '0,1%'
            potencjal = '99,9%'
        else:
            dotarcie = '0,01%'
            potencjal = '99,99%'
    except:
        return "err 0x01"

    try:   
        dict_miasta = {}
        dict_branze = {}

        with open('miasta.txt', 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                dict_miasta[row[0]] = row[1]

        with open('branze.txt', 'r') as csv_filee:
            csv_readerr = csv.reader(csv_filee, delimiter=',')
            for roww in csv_readerr:
                dict_branze[roww[0]] = roww[1]
    except:
        return "err 0x02"
        
    try:
        #will be replaces with 'gender' field
        if imie.endswith('a'):
            szanown = 'Szanowna'
            zwrot = 'Pani'
            zwrot_kto = 'Pani'
            zwrot_komu = 'Pani'
            zwrot_kogo = 'Pani'
            zwrot_z_kim = 'Panią'
            
            koncowka = 'e'
            zwrot_panstwa = 'Panią'
        elif imie == "Państwo":
            szanown = 'Szanowni'
            zwrot = 'Państwo'
            zwrot_kto = 'Państwo'
            zwrot_komu = 'Państwu'
            zwrot_kogo = 'Państwa'
            zwrot_z_kim = 'Państwem'
            koncowka = 'ą'
            zwrot_panstwa = 'Państwa'
        else:
            szanown = 'Szanowny'
            zwrot = 'Panie'
            zwrot_kto = 'Pan'
            zwrot_komu = 'Panu'
            zwrot_kogo = 'Pana'
            zwrot_z_kim = 'Panem'
            koncowka = 'e'
            zwrot_panstwa = 'Pana'
    except:
        return "err 0x03"
    
    user = ['John Doe', 'Jane Doe', 'Agnes Doe']
    telephone = ['666 999 333', '789 456 123', '321 987 456']
    
    dict_users = dict(zip(user,telephone))

    who = userOn
    tel = dict_users[who]


    try:
        nazwapliku = stronawww + '.html'
    except:
        return "err 0x04"


    txt = codecs.open('szablony/' + files[1],'r','utf-8-sig')

	## create html file

    pathname = os.path.abspath("maile/%s.html" % nazwapliku)
        
    edit = codecs.open(pathname,'w','utf-8-sig')


    try:
        text = txt.read()
    except:
        return "err 0x12"

	#replace empty spots in html template with keywords from database input
    try:
        d = dict(var_zwroty=dd['keywords'],var_strony_konkurencja=dd['konkur'],var_wyszukania=dd['wyszuk'],var_cena=dd['cena'],var_zwrot_panstwa=zwrot_panstwa,var_zwrot_z_kim=zwrot_z_kim,var_who=who,var_tel=tel,var_tytul=tytul,var_zwrot_kto=zwrot_kto,var_zwrot_kogo=zwrot_kogo,var_branza_odm=dict_branze[branza].lower(),var_koncowka=koncowka,var_zwrot_komu=zwrot_komu,var_miasto_odm=dict_miasta[miasto],var_szanown=szanown,var_strona=stronawww,var_zwrot=zwrot,var_miasto=miasto,var_pozycja=pozycja,var_branza=branza,var_dotarcie=dotarcie,var_potencjal=potencjal)
    except:
        return "err 0x13"

    try:
        tabl_file = codecs.open('tabele/' + files[0],'r','utf-8-sig')
    except:
        tabl_file = codecs.open("tableTemplate" + '.html','r','utf-8-sig')

    try:
        tabl = tabl_file.read()

    except:
        return "No table file found"
    


	## substitute site rebuild offer
    try:
        stronainter_file = codecs.open('stronaintern.html','r','utf-8-sig')
        stronaintern = stronainter_file.read()
        przebudowa = '<br><span style="margin-left:40px">- Przebudowa strony: <b><span style="color:#e94e27">wskazana</span></b><br>'
    except:
        return "err no strintern file"

    try:
        if not (checi == 'Nie' or checi == 'nie'):
            s = Template(text).safe_substitute(dict(var_strona_checi=stronaintern))
            s = Template(s).safe_substitute(dict(var_przebudowa=przebudowa))
        else:
            s = Template(text).safe_substitute(dict(var_strona_checi=''))
            s = Template(s).safe_substitute(dict(var_przebudowa=''))
    except:
        return "No checi"        

	#substitute table
    try:
        s = Template(s).safe_substitute(dict(var_table=tabl))
    except:
        return "table substitute error"


	#insert promo text
    if promoFlag == True:
        promoText = promoText.replace('\n','<br>')
        
        htmlPromo = """<p style="padding: 15px; margin-bottom:
                              -10px; text-align: justify; font-size:
                              16px; color: #221f20; font-family: open
                              sans,sans-serif; line-height:
                              130%;background-color: #ffffff;"><b><span
                                  style="color:#e94e27">ZNIŻKA ZA
                                  SEKTOR: </span></b> """
        promoOut = htmlPromo + promoText + '</p>'

        
        s = Template(s).safe_substitute(dict(var_promo=promoOut))
        
    else:
        s = Template(s).safe_substitute(dict(var_promo=''))
        
    
	#substitute dictionary with keywords
    try:
        s = Template(s).safe_substitute(d)
    except:
        return "err 0x14"

    
    try:
        edit.write(s)
    except:
        return "err 0x15"    

    #close clipboard    
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(s)
    r.destroy()
        
        
        
    return "Wygenerowano!\n" + stronawww