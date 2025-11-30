from dataclasses import fields


def calcule_stats(data):
    if not data:
        print("Aucune donneé")
        return

    champs = data[0].keys()

    for champ in champs:
        valeurs = [item[champ] for item in data]

        print(f"statistiques pour: {champ}")

        # nombre entier ou flottant
        if isinstance(valeurs[0], (int, float)):
            print(f"  Min : {min(valeurs)}")
            print(f"  Max : {max(valeurs)}")
            print(f"  Moyenne : {sum(valeurs) / len(valeurs):.2f}")

        # Booléen
        elif isinstance(valeurs[0], bool):
            true_count = sum(valeurs)
            false_count = len(valeurs) - true_count

            print(f"  % True : {true_count / len(valeurs) * 100:.1f}%")
            print(f"  % False : {false_count / len(valeurs) * 100:.1f}%")

        # Liste
        elif isinstance(valeurs[0], str):
            print("champ text")

        else:
            print(" Type non gere")
