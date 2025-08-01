import threading
import time
import sys
from IPython.display import display, clear_output
import ipywidgets as widgets


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
                    if cpt2 >= 2 and line[i] != ' ':
                        nom += line[i]
                    if cpt2 >= 2 and line[i] == ' ' and nom == 'New' and flag:
                        nom += line[i]
                        flag = False
                        f2 = True 
                if line[i] == ' ' and (nom != 'New' or not flag) and not f2:
                    cpt += 1
                i += 1
                f2 = False
            liste.append(nom)
    liste[36] = 'Caroline du Nord' 
    liste[37] = 'Dakota du Nord' 
    liste[44] = 'Caroline du Sud'
    liste[45] = 'Dakota du Sud'
    liste.pop(-1)
    liste.pop(-1)
    return liste

def etats_us_p(tps=None):
    # Chargement de la liste
    liste_complete = liste_etats()
    restants = liste_complete.copy()
    trouvés = []

    # Widgets
    input_box = widgets.Text(placeholder='Entrez un État')
    bouton = widgets.Button(description="Valider")
    chrono_label = widgets.Label(value="⏱️ Temps écoulé : 0 s")
    message = widgets.Label(value="")
    output = widgets.Output()

    # Affichage initial
    display(chrono_label, input_box, bouton, output, message)

    # Chrono
    debut = time.time()

    def lancer_chrono():
        ecoule = int(time.time() - debut)
        chrono_label.value = f"⏱️ Temps écoulé : {ecoule} s"
        if tps is not None and ecoule >= tps:
            message.value = "⛔ Temps écoulé ! Partie perdue."
            bouton.disabled = True
            input_box.disabled = True
        else:
            threading.Timer(1, lancer_chrono).start()

    lancer_chrono()

    def afficher_actuels():
        with output:
            clear_output(wait=True)
            print("🌍 À deviner :\n")
            a_print = ''
            i = 0
            for nom in liste_complete:
                if nom in trouvés:
                    a_print+=" 🌳"+ nom + ' '
                else:
                    i+=1
                    a_print += " ###### "
                    if i== 5 :
                        a_print += '\n'
                        i= 0
            print(a_print)
            print(f"\n🔎 États restants : {len(restants)}")

    # Fonction appelée à chaque validation
    def valider(_):
        nom = input_box.value.strip()
        if bouton.disabled:
            return
        if nom in restants:
            restants.remove(nom)
            trouvés.append(nom)
            message.value = f"✅ Bien joué : {nom}"
        else:
            message.value = f"❌ Mauvais ou déjà trouvé : {nom}"
        input_box.value = ""
        afficher_actuels()
        if not restants:
            message.value = "🏆 Victoire ! Tous les états trouvés."
            bouton.disabled = True
            input_box.disabled = True

    bouton.on_click(valider)
    input_box.on_submit(valider)

    afficher_actuels()

