# Adding own modules path
import sys
sys.path.append('./modules/')

# Importing own modules
from myTopo import *

def tampilanMenu():
    pass

def pilih1():
    print(1)
    
def pilih2():
    print(2)

if __name__=="__main__":
    initializeTopo()
    menu = True
    while menu:
        tampilanMenu()
        pilihan = int(input('Masukkan pilihan (-1 untuk exit): '))
        
        if pilihan == 1:
            pilih1()
        elif pilihan == 2:
            pilih2()
        elif pilihan == -1:
            exit()