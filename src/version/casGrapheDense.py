from ast import While
import sys
import signal
import time
import numpy as np


#https://www.optil.io/optilion/help/signals#python3
class Killer:
  exit_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit)
    signal.signal(signal.SIGTERM, self.exit)

  def exit(self,signum, frame):
    self.exit_now = True 

killer = Killer()


def ToGraph():
    MonGraph = dict()
    for line in sys.stdin:
        if (line[0]!="p" and line[0]!="c"):
            num=[]
            for value in line.split(' '):
                try:
                    v = int(value)
                    num.append(v)
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
    return MonGraph

def ToMatrice():
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
            print(nombre_sommet)
            break
    Matrice = []
    for i in range (0,nombre_sommet):
        column = []
        for j in range (0,nombre_sommet):
            column.append(0)
        Matrice.append(column)

    for line in sys.stdin:
        if (line[0]!="p" and line[0]!="c"):
            num=[]
            for value in line.split(' '):
                try:
                    v = int(value)
                    num.append(v)
                except ValueError:
                    pass
            cle1 = int(num[0])
            cle2 = int(num[1])
            Matrice[cle1][cle2]= 1
            Matrice[cle2][cle1]= 1
        return Matrice



def cost(sommet,list_clic,G):
    degre_sommet = len(G[sommet])
    list_cost_clic = [] # stocker es cost pour chaque clic 
    for clic in list_clic :
        taille_clic = len (clic)
        nombre_arete_clic =len (G[sommet].intersection(clic))
        valeur_cost = (taille_clic - nombre_arete_clic) + (degre_sommet - nombre_arete_clic)
        list_cost_clic.append(valeur_cost)

    min_cost = min(list_cost_clic)
    indice_min_cost = list_cost_clic.index(min_cost)
    if min_cost < degre_sommet :
        return False,indice_min_cost
    else :
        return True,{sommet}





def clusters(G):
    list_sommets = [*G]
    sommet1= list_sommets.pop(0)
    np.random.shuffle(list_sommets)
    list_clic =[{sommet1}]
    for sommet in list_sommets:
        np.random.shuffle(list_clic)
        nouvelle_clic, valeur = cost(sommet,list_clic,G)
        if nouvelle_clic :
            list_clic.append(valeur)
        else:
            list_clic[valeur].add(sommet)
    return list_clic
               
def arete_ajout_supp(graph,cluster):
    list_arret_modif = set()
    for sommet in graph:
        s = graph[sommet]
        s.add(sommet)
        for r in cluster:
            if sommet in r :
                for voisin in (s-r):
                    arete_supp = tuple(sorted((sommet,voisin)))
                    list_arret_modif.add(arete_supp)
                for voisin_nouv in (r-s):
                    arete_ajout = tuple(sorted((sommet,voisin_nouv)))
                    list_arret_modif.add(arete_ajout)
                
    return list_arret_modif

def ecrire_fichier(list_arete):
    for arete in list_arete:
        u,v = arete
        print(u,v)
        


#G={1:{2,3},2:{1,3,4,5},3:{1,2,4,6},4:{2,3},5:{2,6,7},6:{3,5,7},7:{5,6}}
#F= {1: {2, 6, 7}, 2: {8, 1, 6}, 6: {1, 2, 7}, 7: {1, 6}, 8: {2, 3, 5}, 3: {8, 4}, 4: {3}, 5: {8}}

MonGraphInput= ToGraph()
listModi = arete_ajout_supp(MonGraphInput,clusters(MonGraphInput))
score1 = len(listModi)


i=0
while (i<=10):
    listModi2 = arete_ajout_supp(MonGraphInput,clusters(MonGraphInput))
    if score1 > len(listModi2):
        listModi = listModi2
        score1 = len(listModi2)
    i+=1


ecrire_fichier(listModi)

##li = arete_ajout_supp(MonGraphInput,clusters(MonGraphInput))
##print (len(li))



