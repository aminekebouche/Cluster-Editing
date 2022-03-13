import sys
import signal
import time
import numpy as np



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
            break
    Matrice = np.zeros((nombre_sommet, nombre_sommet),dtype='uint8')
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
            Matrice[cle1-1][cle2-1]= 1
            Matrice[cle2-1][cle1-1]= 1
    return Matrice
#F= {1: {2, 6, 7}, 2: {8, 1, 6}, 6: {1, 2, 7}, 7: {1, 6}, 8: {2, 3, 5}, 3: {8, 4}, 4: {3}, 5: {8}}
start = time.time()
ma=ToMatrice()
end =time.time()
print(ma[2][2])

print("Temps d'execution ", end-start)