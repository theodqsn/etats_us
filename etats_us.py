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
    all_states = liste_etats()
    remaining = set(all_states)
    found = []

    output = widgets.Output()
    input_box = widgets.Text(placeholder='Entrez un État')
    bouton = widgets.Button(description="Valider")
    chrono_label = widgets.Label(value="⏱️ Temps écoulé : 0 s")
    message = widgets.Label(value="")

    display(chrono_label, input_box, bouton, output, message)

    # Chronomètre en thread
    stop_event = threading.Event()
    debut = time.time()

    def chrono():
        while not stop_event.is_set():
            ecoule = int(time.time() - debut)
            chrono_label.value = f"⏱️ Temps écoulé : {ecoule} s"
            if tps is not None and ecoule >= tps:
                message.value = "⛔ Temps écoulé ! Partie perdue."
                bouton.disabled = True
                input_box.disabled = True
                stop_event.set()
            time.sleep(1)

    thread = threading.Thread(target=chrono)
    thread.start()

    # Affichage des états trouvés
    def update_display():
        with output:
            clear_output(wait=True)
            print("🌿 États trouvés :")
            print(", ".join(sorted(found)))
            print("\n🔍 États restants :")
            print(f"{len(remaining)} restants.")

    # Callback bouton
    def on_valider(_):
        nom = input_box.value.strip()
        if nom in remaining:
            found.append(nom)
            remaining.remove(nom)
            message.value = f"✅ Bien joué : {nom}"
        else:
            message.value = f"❌ Mauvais ou déjà trouvé : {nom}"
        input_box.value = ""
        update_display()
        if not remaining:
            message.value = "🏆 Victoire ! Tous les états trouvés."
            bouton.disabled = True
            input_box.disabled = True
            stop_event.set()

    bouton.on_click(on_valider)
    input_box.on_submit(on_valider)

    update_display()
