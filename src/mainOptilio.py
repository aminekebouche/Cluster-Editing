import sys
import signal
import numpy as np
import time

sys.setrecursionlimit(1500)

class Killer:
  exit_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit)
    signal.signal(signal.SIGTERM, self.exit)

  def exit(self,signum, frame):
    self.exit_now = True 

killer = Killer()




def Tolist_adjacence():
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
    list_adjacence =  [ [] for _ in range(nombre_sommet) ]
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
            list_adjacence[cle1-1].append(cle2)
            list_adjacence[cle2-1].append(cle1)
            l=[cle1,cle2]
            l.sort()
            list_arete.append(l)
    for list_voisins in list_adjacence:
        list_voisins.sort()
    list_arete.sort()
    return nombre_sommet,list_adjacence, list_arete,MonGraph

def cost(sommet,list_clic,G,k):
    degre_sommet = len(G[sommet])
    list_cost_clic = [] # stocker es cost pour chaque clic 
    for clic in list_clic :
        if (k.exit_now):
            return None, None
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

def clusters(G,k):
    list_sommets = [*G]
    np.random.shuffle(list_sommets)
    sommet1= list_sommets.pop(0)
    list_clic =[{sommet1}]
    for sommet in list_sommets:
        if (k.exit_now):
            return
        nouvelle_clic, valeur = cost(sommet,list_clic,G,k)
        if nouvelle_clic == None:
            return
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

def recherche_dichotomique(list_aretes_triee, fin_list, debut_list, arete):
    if fin_list >= debut_list:
        mediane = (fin_list + debut_list) // 2
        if list_aretes_triee[mediane] == arete:
            return True
        elif list_aretes_triee[mediane] > arete:
            return recherche_dichotomique(list_aretes_triee, mediane - 1,debut_list, arete)
        else:
            return recherche_dichotomique(list_aretes_triee,  fin_list,mediane + 1, arete)

def ameliorer(a,lie,visite,cpt_visit,Graph):
    if (visite[a]== cpt_visit): #a-1
        return False
    visite[a] = cpt_visit # a-1
    for voisin in Graph[a]:
        if (voisin == lie[a]):
            continue
        if (not lie[voisin-1] and visite[voisin-1] != cpt_visit):
            lie[voisin-1]=a+1
            lie[a] = voisin
            return True
        if (lie[voisin-1] > 0):
            visite[voisin-1] = cpt_visit
            result = ameliorer(lie[voisin-1]-1, lie, visite, cpt_visit,Graph)
            if (result) :
                lie[a] = voisin
                lie[voisin-1] = a+1
                return True
            
    return False

def imprimer_arete_modifiee(list_clic,list_arete):
    list_arete_modi=[]
    rights = len(list_arete)-1
    for c in list_clic:
        for a in c:
            for b in c:
                if a<b:
                    t = [a,b]
                    list_arete_modi.append(t)
    for arete1 in list_arete_modi:
        if not (recherche_dichotomique(list_arete,rights,0,arete1)):
            print(arete1[0],arete1[1])
    rights1 = len(list_arete_modi)-1
    list_arete_modi.sort()
    for arete2 in list_arete:
        if not (recherche_dichotomique(list_arete_modi,rights1,0,arete2)):
            print(arete2[0],arete2[1])

def test_aretes(list_clic, ordre_clic, Graph, num_iterations):
    n = len(Graph)
    order = np.arange(n)
    np.random.shuffle(order)
    compar_arete = np.full((n), 0).tolist()
    for num in range(0,num_iterations):
        for i in order:
            for a in Graph[i]:
                compar_arete[ordre_clic[a-1]] = len(list_clic[ordre_clic[a-1]]) + len(Graph[i])
            compar_arete[ordre_clic[i]] = len(list_clic[ordre_clic[i]]) + len(Graph[i])

            best = [compar_arete[ordre_clic[i]], ordre_clic[i]]
            for a in Graph[i]:
                compar_arete[ordre_clic[a-1]] -= 2
                best = min(best, [compar_arete[ordre_clic[a-1]], ordre_clic[a-1] ])
            if (ordre_clic[i] != best[1]):
                if i in  list_clic[ordre_clic[i]]:
                    it = list_clic[ordre_clic[i]].index(i)
                    #assert(it != list_clic[ordre_clic[i]][-1])
                    if (it != list_clic[ordre_clic[i]][-1]):
                        list_clic[ordre_clic[i]].pop(it)
                        ordre_clic[i] = best[1]
                        list_clic[ordre_clic[i]].append(i)
    return list_clic
    

                
def cas_graphe_sparse(Graph,list_arete):
    taille_graphe = len(Graph)
    graphe_nouv = np.full((taille_graphe,0), 0).tolist()
    lie = np.full((taille_graphe), 0).tolist()
    taille =0
    list_clic = []
    #print(list_arete)
    for arete in list_arete :
        if(not lie[arete[0]-1] and not lie[arete[1]-1]):
            for voisin in Graph[arete[0]-1]:
                if (not lie[voisin-1] and voisin != arete[1]):
                    t = [min(arete[1],voisin),max(arete[1],voisin)]
                    rights = len(list_arete)-1
                    #print(t)
                    if (recherche_dichotomique(list_arete,rights,0,t)):
                        #print('azul')
                        lie[voisin-1] = lie[arete[0]-1]= lie[arete[1]-1] = -1
                        list_clic.append([voisin,arete[0],arete[1]])
                        taille +=3
                        break
    cpt_visit=0
    num =0
    nb_triangles = 1e9
    visite = np.full((taille_graphe), 0).tolist()
    while(not killer.exit_now):
        trouve = False
        cpt_visit+=1
        for  i in range(0,taille_graphe): #voir la valeur de i
            if (lie[i]):
                continue
            res = ameliorer(i,lie,visite,cpt_visit,Graph)
            if (res):
                num+=1
                trouve = True
        if (not trouve) :
            break   

    for i in range(0,taille_graphe):
        if (lie[i]> i+1):
            list_clic.append([i+1,lie[i]])
        elif (not lie[i]):
            list_clic.append([i+1])

    nb_triangle = len(list_arete) - taille - num

    ordre_clic = np.full((taille_graphe), 0).tolist()
    for i in range(0,len(list_clic)):
        for a in list_clic[i]:
            ordre_clic[a-1] = i

    l=test_aretes(list_clic, ordre_clic, Graph, 5)
    taille_solution = len(l)
    start = time.time()
    end=0
    while(end-start<300):
        l1 =test_aretes(list_clic, ordre_clic, Graph, 5)
        if taille_solution > len(l1):
            l=l1
            taille_solution = len(l1)
        end = time.time()
    imprimer_arete_modifiee(l,list_arete)

def cas_graphe_dense(MonGraphInput,killer):
    cluster = clusters(MonGraphInput,killer) or []
    listModi = arete_ajout_supp(MonGraphInput,cluster)
    score1 = len(listModi)
    start = time.time()
    end=0
    while ( end - start < 400 and  (not killer.exit_now )):
        cluster2 = clusters(MonGraphInput,killer) 
        if cluster2 == None:
            break
        listModi2 = arete_ajout_supp(MonGraphInput,cluster2)
        if score1 > len(listModi2):
            listModi = listModi2
            score1 = len(listModi2)
        end = time.time()
    ecrire_fichier(listModi)

#Graph= [[2, 3, 4, 5, 6, 7, 8, 9], [1, 3, 4, 5, 6, 9], [1, 2, 4, 5, 6, 9, 10], [1, 2, 3, 5, 6, 7, 10], [1, 2, 3, 4, 6, 10], [1, 2, 3, 4, 5, 10], [1, 4, 8, 9, 10], [1, 7, 9, 10], [1, 2, 3, 7, 8, 10], [3, 4, 5, 6, 7, 8, 9]]
#list_arete=[[1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9], [2, 3], [2, 4], [2, 5], [2, 6], [2, 9], [3, 4], [3, 5], [3, 6], [3, 9], [3, 10], [4, 5], [4, 6], [4, 7], [4, 10], [5, 6], [5, 10], [6, 10], [7, 8], [7, 9], [7, 10], [8, 9], [8, 10], [9, 10]]
#Graph = [[2, 6, 7], [1, 6, 8], [4, 8], [3], [8], [1, 2, 7], [1, 6], [2, 3, 5]]
#list_arete = [[1, 2], [1, 6], [1, 7], [2, 6], [2, 8], [3, 4], [3, 8], [5, 8], [6, 7]]
#Graph, list_arete = Tolist_adjacence()

program1, list_adjacence ,list_arete, MonGraph = Tolist_adjacence()

if program1 > 30000 :
    cas_graphe_sparse(list_adjacence,list_arete)
else:
    cas_graphe_dense(MonGraph,killer)

