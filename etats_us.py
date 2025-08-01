

import threading
import time
import sys
from IPython.display import display, clear_output


def etats_us_p(tps= None):
  liste = liste_etats()
  l = liste.copy()
  t = time.time()

  def afficher_actuels():
    
    a_display = ''
    for nom in l:
      if nom not in liste:
        a_display+=' 🌳'+nom +' '
      else : 
        a_display+=' ###### '
    clear_output(wait=True) 
    display(a_display)

    if tps is not None:
      deb = time.time()

  def chrono(stop_event):
    debut = time.time()
    while not stop_event.is_set():
        ecoule = int(time.time() - debut)
        sys.stdout.write(f"\r⏱️  Temps écoulé : {ecoule} s")
        sys.stdout.flush()
        time.sleep(1)

  stop_event = threading.Event()
  thread = threading.Thread(target=chrono, args=(stop_event,))
  thread.start()

  while liste:
    nom_test = input('entrez un nom')
    if tps is not None and time.time() - t > tps:
      raise Exception('Perdu !')
    if nom_test in liste:
      liste.remove(nom_test)
      afficher_actuels()
    

  stop_event.set()
  thread.join()

  print('C \' est une victoire')

def liste_etats():
  liste = []
  with open('noms_etats.txt', 'r', encoding='latin1') as file:
      for line in file:
          i = 0
          cpt = 0
          nom = ''
          cpt2 = 0
          flag = True
          f2 = False
          while i < len(line):       
              if cpt == 1:
                  cpt2 += 1
                  if cpt2 >=2 and line[i] != ' ':
                    nom += line[i]
                  if cpt2 >=2 and line[i] == ' ' and nom == 'New' and flag:
                    nom += line[i]
                    flag = False
                    f2 = True 
              if line[i] == ' ' and (nom != 'New' or flag == False) and not f2 :
                cpt += 1
              i += 1
              f2 = False
          liste.append(nom)

  liste[36]='Caroline du Nord' 
  liste[37]='Dakota du Nord' 
  liste[44]= 'Caroline du Sud'
  liste[45]= 'Dakota du Sud'
  liste.pop(-1)
  liste.pop(-1)
  return(liste)
