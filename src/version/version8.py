import sys
import signal
import numpy as np


class Killer:
  exit_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit)
    signal.signal(signal.SIGTERM, self.exit)

  def exit(self,signum, frame):
    self.exit_now = True 

killer = Killer()




def ToMatrice():
    nombre_sommet = 0
    nombre_arret =0
    MonGraph = dict()
    for line in sys.stdin:
        if ("cep" in line):
            num=[]
            for value in line.split(' '):
                try:
                    v = int(value)
                    num.append(v)
                except ValueError:
                    pass
            nombre_sommet, nombre_arret = (num[0],num[1])
            break
    
    Matrice =  [ [] for _ in range(nombre_sommet) ]
    list_arete =[]
    for line in sys.stdin:
        if (line[0]!="p" and line[0]!="c"):
            num=[] 
            for value in line.split(' '):
                try:
                    num.append(value)
                except ValueError:
                    pass
            cle1 = int(num[0])
            cle2 = int(num[1])
            if (not(cle1 in MonGraph)):
                MonGraph[cle1] ={cle2}
            else :
                MonGraph[cle1].add(cle2)
            if (not (cle2 in MonGraph)):
                MonGraph[cle2] ={cle1}
            else :
                MonGraph[cle2].add(cle1)
            Matrice[cle1-1].append(cle2)
            Matrice[cle2-1].append(cle1)
            l=[cle1,cle2]
            l.sort()
            list_arete.append(l)
    for list_voisins in Matrice:
        list_voisins.sort()
    list_arete.sort()
    return nombre_sommet,Matrice, list_arete,MonGraph

def recherche_dichotomique(list_aretes_triee, fin_list, debut_list, arete):
    if fin_list >= debut_list:
        mediane = (fin_list + debut_list) // 2
        if list_aretes_triee[mediane] == arete:
            return True
        elif list_aretes_triee[mediane] > arete:
            return recherche_dichotomique(list_aretes_triee, mediane - 1,debut_list, arete)
        else:
            return recherche_dichotomique(list_aretes_triee,  fin_list,mediane + 1, arete)
