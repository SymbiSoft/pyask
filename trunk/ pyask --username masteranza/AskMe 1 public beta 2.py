# pyAsk simple app asking from predefinied words
# author: ranza, website: http://masteranza.wordpress.com

import appuifw, e32, audio, re, random, os, time
appuifw.app.title = u"pyAsk"

strona=0
strona2=1

def case(n):
    return os.path.normcase(n)
path='E:\\dicts\\sports.txt'


def slownik():
    try:
        os.listdir('E:\\dicts\\')
    except:
        os.mkdir('E:\\dicts\\')
        
    lista2=[]
    for k in os.listdir(u'E:\\dicts\\'):
        lista2.append(unicode(k))
    if lista2 == []:
        a=appuifw.note(u"No dicts found. You must create one.")
        stworz()
        for k in os.listdir(u'E:\\dicts\\'):
            lista2.append(unicode(k))
        
    index3 = appuifw.popup_menu(lista2, u"Choose:")
    if index3 == None:
        appuifw.note(u"Nothing chosen!") 
    else:
        global path
        path = os.path.join('E:\\dicts\\', lista2[index3])
        appuifw.note(u"Dict loaded succesfully " + lista2[index3])
    menu()
    
def stworz():
    f=appuifw.query(u"Enter a name for a dict","text")
    global secret
    if f:
        k=open('E:\\dicts\\' + f + '.txt','w')
        k.close()    
        global path
        path = os.path.join('E:\\dicts\\' + f + '.txt')
        appuifw.note(u"Dict loaded succesfully " + f)
        
    else:
        appuifw.note(u"No name added!")
    menu()

def usunslownik():
    lista2=[]
    for k in os.listdir(u'E:\\dicts\\'):
        lista2.append(unicode(k))
    if lista2 == []:
        appuifw.note(u"No dicts found")
    else:
        index2 = appuifw.multi_selection_list(lista2, style='checkbox', search_field=1)
    
        if index2 == ():
            appuifw.note(u"Nothing chosen")
        else:
            wybrano = ''
            for i in index2:
                wybrano = wybrano + lista2[i] + ' '
            czynapewno = appuifw.query("Are you sure you want to delete " + wybrano + '?', "query")
            if czynapewno:
                for i in index2:
                    os.remove('E:\\dicts\\' + lista2[i])
                appuifw.note(u"Deleted.")
             
            else:
                pass
    menu()

    

def slowa():
    regex = "(.*?)\s*,\s*(.*)[\s]?"
    try:
        f = file(path)
        slowa = f.read()
        slowa = re.findall(regex, slowa)
        f.close()
        return slowa
    except:
        slownik()
    


def zwrocliste():
    k=[]
    for i in slowa():
        k.append(unicode(str(i[0]+'-'+i[1].strip())))
    return k
    
def Direction(x):
    if x==0:
        return u'Turn right to left'    
    elif x==1:
        return u'Turn left to right'


def usun():
    if zwrocliste() == []:
        appuifw.note(u"No words found.")
    else:
        index2 = appuifw.multi_selection_list(zwrocliste(), style='checkbox', search_field=1)
    
        if index2 == ():
            appuifw.note(u"Nothing chosen")
        else:
            wybrano = ''
            for i in index2:
                wybrano = wybrano + zwrocliste()[i] + ' '
            czynapewno = appuifw.query("Are you sure you want to delete " + wybrano + '?', "query")
            if czynapewno:
                noweslowa = slowa()
                poczatek = index2[0]
                koniec = index2[-1]
                noweslowa = noweslowa[:poczatek] + noweslowa[koniec+1:]
                f=open(path, 'w')
                f.close()
                f=open(path, 'a')
                for i in noweslowa:
                    f.write(i[0] + ' , ' + i[1] + '\n')
                f.close()
             
            else:
                pass
    menu()

def menu():
    choices = [u"Ask", u"Choose dict", u"Add a word", u"Remove word",u"New dict",u"Remove dict", Direction(strona)]
    index = appuifw.popup_menu(choices, u"Menu:") 
    
    if index == 1:
        slownik()
    elif index == 0:
        zle=[]
        wszystkie=0
        w=slowa()
        
        random.shuffle(w)
        k=0
        global strona, strona2
        for k in w:
    #     audio.say(unicode(k[0]))
            pytaj = appuifw.query(unicode('#' + str(wszystkie) + '/' + str(len(w)) + ' ' + k[strona]),"text")
            
            if case(unicode(pytaj)) == case(k[strona2].strip()):
                appuifw.note(u"That's correct!")
                wszystkie+=1
            elif case(unicode(pytaj)) == case((k[strona2].strip())[:-1]):
                
                appuifw.note(u"Almost! It was " + case(k[strona2].strip()))
                zle.append(k)
                wszystkie+=1
                w.append(k)
            else:
                dalej = appuifw.query(u'Wrong. ' + case(k[strona2].strip()) + ' Continue?',"query")
                wszystkie+=1
                zle.append(k)
                w.append(k)
                if dalej:
                    pass
                else:
                    break
        appuifw.note(u"You did " + str(len(zle)) + " mistakes in "+ str(wszystkie))
        menu()
#dodawanie slow
    elif index == 2: 
        names = appuifw.multi_query(u"Word", u"Meaning")
        if names:
            first, last = names
            czynapewno = appuifw.query("Are you sure you want to add " + first + " - " + last, "query")
            if czynapewno:
                appuifw.note(u"Added: " + first + " - " + last)
                f=open(path, 'a')
                f.write('\n' + case(first) + ' , ' + case(last))
                f.close()
                menu()
            else:
                pass
        else:
            appuifw.note(u"Adding canceled")
            menu()

    elif index == 3:
        usun()
    elif index == 4:
        stworz()
    elif index == 5:
        usunslownik()
    elif index == 6:
        global strona
        if strona==0:
            strona = 1
            strona2=0
            menu()
        elif strona == 1:
            strona = 0
            strona2=1
            menu()
slownik()

