import sys
import signal
import time

#https://www.optil.io/optilion/help/signals#python3
class Killer:
  exit_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit)
    signal.signal(signal.SIGTERM, self.exit)

  def exit(self,signum, frame):
    self.exit_now = True 

killer = Killer()

def is_int(element):
    try:
        int(element)
        return True
    except ValueError:  
        return False



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



def cost(sommet,list_clic,G):
    degre_sommet = len(G[sommet])
    list_cost_clic = [] # stocker es cost pour chaque clic 
    for clic in list_clic :
        taille_clic = len (clic)
        nombre_arete_clic =len (G[sommet].intersection(set(clic)))
        valeur_cost = (taille_clic - nombre_arete_clic) + (degre_sommet - nombre_arete_clic)
        list_cost_clic.append(valeur_cost)

    min_cost = min(list_cost_clic)
    indice_min_cost = list_cost_clic.index(min_cost)
    if min_cost < degre_sommet :
        return False,indice_min_cost
    else :
        return True,[sommet]

def clusters(G):
    list_sommets = [*G]
    sommet1= list_sommets[0]
    list_clic =[[sommet1]]
    arret_ajout=[]
    arret_supp=[]
    for sommet in G:
        if sommet != sommet1:
            nouvelle_clic, valeur = cost(sommet,list_clic,G)
            if nouvelle_clic :
                for voisin in clic:
                    if (voisin in G[sommet]) and ({voisin,sommet} not in arret_supp):
                        print (voisin,sommet)
                        arret_supp.append({voisin,sommet})
                list_clic.append(valeur)
            else:
                for voisin in list_clic[valeur]:
                    if (voisin not in G[sommet]) and ({voisin,sommet} not in arret_ajout):
                        print (voisin,sommet)
                        arret_ajout.append({voisin,sommet})
                for clic in list_clic:
                    if clic != list_clic[valeur]:
                        for voisin in clic:
                            if (voisin in G[sommet]) and ({voisin,sommet} not in arret_supp):
                                print (voisin,sommet)
                                arret_supp.append({voisin,sommet})
                list_clic[valeur].append(sommet)
    return list_clic


#G={1:{2,3},2:{1,3,4,5},3:{1,2,4,6},4:{2,3},5:{2,6,7},6:{3,5,7},7:{5,6}}
#F= {1: {2, 6, 7}, 2: {8, 1, 6}, 6: {1, 2, 7}, 7: {1, 6}, 8: {2, 3, 5}, 3: {8, 4}, 4: {3}, 5: {8}}
start = time.time()
F = ToGraph()
clusters(F)
end = time.time()
print("le temps d'execution", end-start)
