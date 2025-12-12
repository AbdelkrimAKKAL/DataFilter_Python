def calcule_stats(data):

    if not data:
        print("Aucune donnée")
        return

    champs = data[0].keys()

    print("\n" + "=" * 60)
    print("STATISTIQUES")
    print("=" * 60)

    for champ in champs:
        valeurs = [item[champ] for item in data if champ in item]

        if not valeurs:
            continue

        print(f"\n Champ : {champ}")
        print("-" * 40)

        # Nombre entier ou float
        if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in valeurs):
            print(f"  Type        : Numérique")
            print(f"  Minimum     : {min(valeurs)}")
            print(f"  Maximum     : {max(valeurs)}")
            print(f"  Moyenne     : {sum(valeurs) / len(valeurs):.2f}")
            print(f"  Médiane     : {sorted(valeurs)[len(valeurs) // 2]:.2f}")

        # Booléen
        elif all(isinstance(v, bool) for v in valeurs):
            true_count = sum(valeurs)
            false_count = len(valeurs) - true_count
            print(f"  Type        : Booléen")
            print(f"  Vrai        : {true_count} ({true_count / len(valeurs) * 100:.1f}%)")
            print(f"  Faux        : {false_count} ({false_count / len(valeurs) * 100:.1f}%)")

        # Liste
        elif all(isinstance(v, list) for v in valeurs):
            tailles = [len(v) for v in valeurs]
            print(f"  Type        : Liste")
            print(f"  Taille min  : {min(tailles)}")
            print(f"  Taille max  : {max(tailles)}")
            print(f"  Taille moy. : {sum(tailles) / len(tailles):.2f}")

            # Stats sur les éléments des listes (si numériques)
            tous_elements = [elem for liste in valeurs for elem in liste]
            if tous_elements and all(isinstance(e, (int, float)) for e in tous_elements):
                print(f"  --- Éléments des listes ---")
                print(f"  Min éléments: {min(tous_elements)}")
                print(f"  Max éléments: {max(tous_elements)}")
                print(f"  Moy éléments: {sum(tous_elements) / len(tous_elements):.2f}")

        # Chaîne de caractères
        elif all(isinstance(v, str) for v in valeurs):
            longueurs = [len(v) for v in valeurs]
            print(f"  Type        : Texte")
            print(f"  Longueur min: {min(longueurs)}")
            print(f"  Longueur max: {max(longueurs)}")
            print(f"  Longueur moy: {sum(longueurs) / len(longueurs):.2f}")
            print(f"  Valeurs uniq: {len(set(valeurs))}")

        else:
            print(f"  Type        : Mixte ou non géré")

    print("\n" + "=" * 60)


def get_field_stats(data, field):

    if not data:
        return None

    valeurs = [item[field] for item in data if field in item]

    if not valeurs:
        return None

    stats = {"field": field}

    # si colonne est entier ou float
    if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in valeurs):
        stats["type"] = "numeric"
        stats["min"] = min(valeurs)

        stats["max"] = max(valeurs)
        stats["mean"] = sum(valeurs) / len(valeurs)
        sorted_vals = sorted(valeurs)
        stats["median"] = sorted_vals[len(sorted_vals) // 2]
        stats["percentile_25"] = sorted_vals[len(sorted_vals) // 4]
        stats["percentile_75"] = sorted_vals[3 * len(sorted_vals) // 4]

    # si bool
    elif all(isinstance(v, bool) for v in valeurs):
        stats["type"] = "boolean"
        stats["true_count"] = sum(valeurs)
        stats["false_count"] = len(valeurs) - sum(valeurs)
        stats["true_percent"] = sum(valeurs) / len(valeurs)

    # si listes
    elif all(isinstance(v, list) for v in valeurs):
        tailles = [len(v) for v in valeurs]
        stats["type"] = "list"
        stats["min_size"] = min(tailles)
        stats["max_size"] = max(tailles)
        stats["mean_size"] = sum(tailles) / len(tailles)

    return stats