from load import load_json, load_csv, save_json, save_csv
from stats import calcule_stats

data = None

print("Data Filter")

while True:
    print("1. Charger un fichier")
    print("2. Afficher les stats")
    print("3. Filtrer les données")
    print("4. Trier les données")
    print("5. Sauvegarder les données")
    print("6. Quitter")

    choice = input("Choix : ")

    if choice == "1":
        filepath = input("Entrez le chemin du fichier : ")

        # On choisit selon l’extension
        if filepath.endswith(".json"):
            data = load_json(filepath)
            print("Fichier JSON chargé avec succès.")
            print(data)

        elif filepath.endswith(".csv"):
            data = load_csv(filepath)
            print("Fichier CSV chargé avec succès.")
            print(data)

        else:
            print("Format non supporté.")

    elif choice == "2":
        if data is None:
            print("Aucune donnée chargée.")
        else:
            calcule_stats(data)

    elif choice == "3":
        print("Filtrage non encore implémenté.")

    elif choice == "4":
        print("Tri non encore implémenté.")

    elif choice == "5":
        if data is None:
            print("Aucune donnée à sauvegarder.")
        else:
            filepath = input("Où sauvegarder ? (.json ou .csv) : ")

            if filepath.endswith(".json"):
                save_json(filepath, data)
                print("Données sauvegardées en JSON.")
            elif filepath.endswith(".csv"):
                save_csv(filepath, data)
                print("Données sauvegardées en CSV.")
            else:
                print("Format non supporté.")

    elif choice == "6":
        print("Au revoir !")
        break

    else:
        print("Choix invalide.")
