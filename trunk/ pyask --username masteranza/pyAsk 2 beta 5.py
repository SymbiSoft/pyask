# pyAsk simple app asking from predefinied words
# author: ranza, website: http://code.google.com/p/pyask/ or http://masteranza.wordpress.com

import appuifw, e32, audio, re, random, os, time
appuifw.app.title = u"pyAsk2"

strona=0
strona2=1
losowosc=0

def case(n):
    return os.path.normcase(n)
path='E:\\dicts\\temp.txt'


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
    try:
        f = file(path)
        slowa = f.read()
        print slowa
        slowa=slowa.split('\r\n')
        print slowa
        slowa2=[]
        for i in slowa:
            slowa2.extend(i.split('\n'))
        slowa=slowa2
        if ('' in slowa):
            slowa.remove('')
        
        slowa2=[]
        slowa3=[]
        for i in slowa:
            slowa2.append(i.split('-'))
        for k in slowa2:
            slowa3.append([k[0].split(','),k[1].split(',')])
        slowa=slowa3
        f.close()
        return slowa
    except:
        slownik()
    


def zwrocliste():
    k=[]
    for i in slowa():
        k.append(unicode(str(i[0])[1:-1].replace("'","").replace('[','').replace(']','').replace("\"","").replace('\\','')+'-'+str(i[1])[1:-1].replace("'","").replace('[','').replace(']','').replace("\"","").replace('\\','')))
    
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
                noweslowa = zwrocliste()
                poczatek = index2[0]
                koniec = index2[-1]
                print noweslowa
                noweslowa = noweslowa[:poczatek] + noweslowa[koniec+1:]
                print noweslowa
                f=open(path, 'w')
                f.close()
                f=open(path, 'a')
                for i in noweslowa:
                    f.write(str(i) + '\r\n')
                f.close()
             
            else:
                pass
    menu()

def menu():
    choices = [u"Ask", u"Choose dict", u"Add a word", u"Remove word",u"New dict",u"Remove dict", Direction(strona), u"About"]
    index = appuifw.popup_menu(choices, u"Menu:") 
    
    if index == 1:
        slownik()
    elif index == 7:
        appuifw.note(u"pyAsk 2 beta 4 coded by Ranza. Updates available at http://code.google.com/p/pyask/", "info")
        menu()
        
    elif index == 0:
        zle=[]
        wszystkie=0
        w=slowa()
        
        random.shuffle(w)
        k=0
        global strona, strona2, losowosc
        for k in w:
            if (losowosc):
                strona=random.randint(0,1)

           
            pytaj = appuifw.query(unicode('#' + str(wszystkie+1) + '/' + str(len(w)) + ' ' + str(k[strona])[1:-1]) + ' (' + str(len(k[strona2])) + ')',"text")
            
            odpowiedz=[]
            for i in k[strona2]:
                odpowiedz.append(case(i).strip())
           
            if case(unicode(pytaj).strip()) in odpowiedz:
                appuifw.note(u"That's correct! " + str(odpowiedz)[1:-1])
                wszystkie+=1
            else:
                dalej = appuifw.query(u'Wrong. ' + str(odpowiedz)[1:-1] + ' Continue?',"query")
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
                f.write('\r\n' + case(first.strip(',')) + '-' + case(last.strip(',')))
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
        global losowosc
        losowosc = appuifw.query(u"Maybe you would like to use random side asking?", "query")
        if (losowosc):
            menu()
        else:
            if strona==0:
                strona = 1
                strona2=0
                menu()
            elif strona == 1:
                strona = 0
                strona2=1
                menu()
slownik()

