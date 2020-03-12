from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib
import mysql.connector as mysql

conex=mysql.connect(host='localhost',user='root',passwd='',db='Direcciones')
Ope=conex.cursor()
try:
    Ope.execute("drop table webp;")
except Exception:
    pass
try:
    Ope.execute("create table webp(pagina VARCHAR(255),estatus int)")
except Exception:
    pass
pag_ini=input('Ingrese dirección:  ')
try:
    Ope.execute("insert into webp values('"+pag_ini+"',0);")
except mysql.errors.IntegrityError:
    sys.exit()
except mysql.errors.DataError:
    sys.exit()
conex.commit()
conex.close()

while(1):
    e=""
    i=0
    conex=mysql.connect(host='localhost',user='root',passwd='',db='Direcciones')
    Ope=conex.cursor()
    Ope.execute("SELECT * FROM webp;")
    for pagina,estatus in Ope.fetchall():
        print(pagina+" "+str(estatus))
        if(estatus==0):
            try:
                url=urlopen(pagina)
            except urllib.error.HTTPError:
                continue
            except UnicodeEncodeError:
                continue
            bs=BeautifulSoup(url.read(),'html.parser',from_encoding="iso-8859-1")
            for enlaces in bs.find_all("a"):
                s=enlaces.get("href")
                try:
                    if(s[0:4]=="http"):
                        try:
                            Ope.execute("insert into webp values('"+s+"',0);")
                            print(s)
                        except mysql.errors.IntegrityError:
                            pass
                        except mysql.errors.DataError:
                            pass
                    else:
                        try:
                            Ope.execute("insert into webp values('"+pagina+s+"',0);")
                            print(pagina+s)
                        except mysql.errors.IntegrityError:
                            pass
                        except mysql.errors.DataError:
                            pass
                except TypeError:
                    pass
            i=1
            Ope.execute("update webp set estatus=1 where pagina='"+pagina+"';")
            conex.commit()    
    conex.close()
    if(i==0):
        sys.exit()