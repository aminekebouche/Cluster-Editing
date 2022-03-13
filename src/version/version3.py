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
    #list_arretes=[]
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
            #list_arretes.append({cle1,cle2})
            if (not(cle1 in MonGraph)):
                MonGraph[cle1] ={cle2}
            else :
                MonGraph[cle1].add(cle2)
            if (not (cle2 in MonGraph)):
                MonGraph[cle2] ={cle1}
            else :
                MonGraph[cle2].add(cle1)
    return MonGraph #, list_arretes



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
    sommet1= list_sommets[0]
    list_clic =[{sommet1}]
    for sommet in G:
        if sommet != sommet1:
            nouvelle_clic, valeur = cost(sommet,list_clic,G)
            if nouvelle_clic :
                list_clic.append(valeur)
            else:
                list_clic[valeur].add(sommet)
    return list_clic

def list_clic_ToDict (list_clic,G):
    d = dict()
    
    for clic in list_clic:
        for sommet in clic :
            s = clic-{sommet}
            d[sommet]= s-G[sommet] | G[sommet] - s

    return d

def afficher(d) :
    list_aret_vu=[]
    for sommet in d:
        for voisin in d[sommet]:
            if {voisin,sommet} not in list_aret_vu:
                print (sommet,voisin)
                list_aret_vu.append({voisin,sommet})
       


   
G={1:{2,3},2:{1,3,4,5},3:{1,2,4,6},4:{2,3},5:{2,6,7},6:{3,5,7},7:{5,6}}
F= {1: {2, 6, 7}, 2: {8, 1, 6}, 6: {1, 2, 7}, 7: {1, 6}, 8: {2, 3, 5}, 3: {8, 4}, 4: {3}, 5: {8}}

#G = ToGraph()
#afficher(list_clic_ToDict(clusters(G),G))
start = time.time()
print(clusters(G))
d=list_clic_ToDict(clusters(G),G)
print(clusters(d))
c= list_clic_ToDict(clusters(d),d)
print(clusters(c))
l= list_clic_ToDict(clusters(c),c)
print(clusters(l))


end = time.time()
print ("le temps",end-start)

