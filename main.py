from load import load_file, save_file
from stats import calcule_stats, get_field_stats
from filters import (filter_data, filter_combined, filter_by_expression,
                     filter_list_advanced, filter_by_stats, filter_multi_conditions)
from sort import sort_data, sort_data_multi, sort_by_expression, sort_by_list_stats
from utils import (add_field, remove_field, rename_field,
                   transform_field, show_data_table, get_user_value)

# Variables globales
data = None


def menu_principal():
    """Affiche le menu principal."""
    print("\n" + "=" * 70)
    print(" " * 20 + "DATA FILTER - MENU PRINCIPAL")
    print("=" * 70)
    print("  1. Charger un fichier (CSV, JSON, XML, YAML)")
    print("  2. Afficher les données")
    print("  3. Afficher les statistiques")
    print("  4. Filtrer les données")
    print("  5. Trier les données")
    print("  6. Gérer les champs (ajouter/supprimer)")
    print("  7. Sauvegarder les données")
    print("  8. Quitter")
    print("=" * 70)


def menu_filtrage():
    global data

    if data is None or not data:
        print("✗ Aucune donnée chargée.")
        return

    print("\n" + "=" * 70)
    print("MENU FILTRAGE")
    print("=" * 70)
    print("  1. Filtrage simple (champ, opérateur, valeur)")
    print("  2. Filtrage avancé sur listes (all, any, min, max, mean)")
    print("  3. Comparaison entre deux champs")
    print("  4. Filtrage par rapport aux stats (moyenne, médiane, etc.)")
    print("  5. Filtrage par expression personnalisée")
    print("  6. Filtrage multi-conditions (ET logique)")
    print("  0. Retour")
    print("=" * 70)

    choix = input("Votre choix : ").strip()

    if choix == "1":
        # Filtrage simple
        print("\nChamps disponibles :", list(data[0].keys()))
        field = input("Champ : ").strip()

        if field not in data[0]:
            print(f"✗ Le champ '{field}' n'existe pas.")
            return

        print("\nOpérateurs : ==, !=, <, >, <=, >=, contains, startswith, endswith")
        operator = input("Opérateur : ").strip()
        value = get_user_value("Valeur : ")

        data = filter_data(data, field, operator, value)
        print(f"Filtrage appliqué : {len(data)} entrées restantes")

    elif choix == "2":
        # Filtrage avancé sur listes
        print("\nChamps disponibles :", list(data[0].keys()))
        field = input("Champ (doit être une liste) : ").strip()

        print("\nOpérateurs : all_gt, all_lt, any_gt, any_lt, min_gt, max_lt, mean_gt, mean_lt")
        operator = input("Opérateur : ").strip()
        value = get_user_value("Valeur : ", "float")

        data = filter_list_advanced(data, field, operator, value)
        print(f"Filtrage appliqué : {len(data)} entrées restantes")

    elif choix == "3":
        # Comparaison entre deux champs
        print("\nChamps disponibles :", list(data[0].keys()))
        field1 = input("Premier champ : ").strip()
        field2 = input("Deuxième champ : ").strip()

        print("\nOpérateurs : ==, !=, <, >, <=, >=")
        operator = input("Opérateur : ").strip()

        data = filter_combined(data, field1, field2, operator)
        print(f"Filtrage appliqué : {len(data)} entrées restantes")

    elif choix == "4":
        # Filtrage par stats
        print("\nChamps disponibles :", list(data[0].keys()))
        field = input("Champ (numérique) : ").strip()

        print("\nTypes de stats : mean, median, percentile_25, percentile_75")
        stat_type = input("Type de statistique : ").strip()

        print("\nOpérateurs : <, >, <=, >=")
        operator = input("Opérateur : ").strip()

        data = filter_by_stats(data, field, operator, stat_type)
        print(f"Filtrage appliqué : {len(data)} entrées restantes")

    elif choix == "5":
        # Expression personnalisée
        print("\nExemple : price * quantity > 1000")
        print("Variables disponibles : les noms des champs de vos données")
        expression = input("Expression Python : ").strip()

        try:
            func = eval(f"lambda item: {expression}")
            data = filter_by_expression(data, func)
            print(f"Filtrage appliqué : {len(data)} entrées restantes")
        except Exception as e:
            print(f"Erreur dans l'expression : {e}")

    elif choix == "6":
        # Multi-conditions
        conditions = []
        print("\nEntrez les conditions (vide pour terminer)")

        while True:
            print(f"\nCondition #{len(conditions) + 1}")
            field = input("  Champ (ou ENTER pour terminer) : ").strip()

            if not field:
                break

            operator = input("  Opérateur : ").strip()
            value = get_user_value("  Valeur : ")

            conditions.append((field, operator, value))

        if conditions:
            data = filter_multi_conditions(data, conditions)
            print(f"Filtrage appliqué : {len(data)} entrées restantes")


def menu_tri():

    global data

    if data is None or not data:
        print("Aucune donnée chargée.")
        return

    print("\n" + "=" * 70)
    print("MENU TRI")
    print("=" * 70)
    print("  1. Tri simple (un champ)")
    print("  2. Tri multi-critères (plusieurs champs)")
    print("  3. Tri sur statistique de liste (min, max, mean, sum)")
    print("  4. Tri par expression personnalisée")
    print("  0. Retour")
    print("=" * 70)

    choix = input("Votre choix : ").strip()

    if choix == "1":
        # Tri simple
        print("\nChamps disponibles :", list(data[0].keys()))
        field = input("Champ de tri : ").strip()

        if field not in data[0]:
            print(f"✗ Le champ '{field}' n'existe pas.")
            return

        order = input("Ordre croissant (c) ou décroissant (d) ? [c] : ").strip().lower()
        reverse = (order == "d")

        data = sort_data(data, field, reverse)
        print(f"Données triées par '{field}'")

    elif choix == "2":
        # Tri multi-critères
        print("\nChamps disponibles :", list(data[0].keys()))
        fields_str = input("Champs (séparés par des virgules) : ").strip()
        fields = [f.strip() for f in fields_str.split(",")]

        reverse_list = []
        for field in fields:
            order = input(f"  '{field}' - croissant (c) ou décroissant (d) ? [c] : ").strip().lower()
            reverse_list.append(order == "d")

        data = sort_data_multi(data, fields, reverse_list)
        print(f"Données triées par {len(fields)} critères")

    elif choix == "3":
        # Tri sur stats de liste
        print("\nChamps disponibles :", list(data[0].keys()))
        field = input("Champ (doit être une liste) : ").strip()

        print("\nStatistiques : min, max, mean, sum, size")
        stat = input("Statistique : ").strip()

        order = input("Ordre croissant (c) ou décroissant (d) ? [c] : ").strip().lower()
        reverse = (order == "d")

        data = sort_by_list_stats(data, field, stat, reverse)
        print(f"Données triées par '{stat}' de '{field}'")

    elif choix == "4":
        # Tri par expression
        print("\nExemple : item['price'] * item['quantity']")
        expression = input("Expression Python : ").strip()

        try:
            func = eval(f"lambda item: {expression}")
            order = input("Ordre croissant (c) ou décroissant (d) ? [c] : ").strip().lower()
            reverse = (order == "d")

            data = sort_by_expression(data, func, reverse)
            print(f"Tri appliqué")
        except Exception as e:
            print(f"Erreur dans l'expression : {e}")


def menu_gestion_champs():

    global data

    if data is None or not data:
        print("Aucune donnée chargée.")
        return

    print("\n" + "=" * 70)
    print("GESTION DES CHAMPS")
    print("=" * 70)
    print("  1. Ajouter un champ")
    print("  2. Supprimer un champ")
    print("  3. Renommer un champ")
    print("  4. Transformer un champ")
    print("  0. Retour")
    print("=" * 70)

    choix = input("Votre choix : ").strip()

    if choix == "1":
        # Ajouter un champ
        field_name = input("Nom du nouveau champ : ").strip()
        default_value = get_user_value("Valeur par défaut : ")

        data = add_field(data, field_name, default_value)
        print(f"Champ '{field_name}' ajouté")

    elif choix == "2":
        # Supprimer un champ
        print("\nChamps disponibles :", list(data[0].keys()))
        field_name = input("Champ à supprimer : ").strip()

        confirm = input(f"Confirmer la suppression de '{field_name}' ? (o/n) : ").strip().lower()
        if confirm == "o":
            data = remove_field(data, field_name)
            print(f"Champ '{field_name}' supprimé")

    elif choix == "3":
        # Renommer un champ
        print("\nChamps disponibles :", list(data[0].keys()))
        old_name = input("Ancien nom : ").strip()
        new_name = input("Nouveau nom : ").strip()

        data = rename_field(data, old_name, new_name)
        print(f"Champ renommé : '{old_name}' -> '{new_name}'")

    elif choix == "4":
        # Transformer un champ
        print("\nChamps disponibles :", list(data[0].keys()))
        field_name = input("Champ à transformer : ").strip()

        print("\nExemple : x * 1.2 (pour augmenter de 20%)")
        expression = input("Expression (variable = x) : ").strip()

        try:
            func = eval(f"lambda x: {expression}")
            data = transform_field(data, field_name, func)
            print(f"Transformation appliquée")
        except Exception as e:
            print(f"✗ Erreur : {e}")


def main():

    global data

    print("\n" + "=" * 70)
    print(" " * 15 + "DATA FILTER")
    print("=" * 70)
    print("  Programme de chargement, filtrage, tri et analyse de données")
    print("  Formats supportés : CSV, JSON, XML, YAML")
    print("=" * 70)

    while True:
        menu_principal()
        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            # Charger un fichier
            filepath = input("\nChemin du fichier : ").strip()

            try:
                data = load_file(filepath)
                print(f"Fichier chargé : {len(data)} entrées")
                print(f"  Champs : {list(data[0].keys())}")
            except Exception as e:
                print(f"Erreur lors du chargement : {e}")

        elif choix == "2":
            # Afficher les données
            if data is None:
                print("Aucune donnée chargée.")
            else:
                limit_str = input("Nombre d'entrées à afficher (vide = toutes) : ").strip()
                limit = int(limit_str) if limit_str else None
                show_data_table(data, limit)

        elif choix == "3":
            # Statistiques
            if data is None:
                print("Aucune donnée chargée.")
            else:
                calcule_stats(data)

        elif choix == "4":
            # Filtrage
            menu_filtrage()

        elif choix == "5":
            # Tri
            menu_tri()

        elif choix == "6":
            # Gestion des champs
            menu_gestion_champs()

        elif choix == "7":
            # Sauvegarder
            if data is None:
                print("Aucune donnée à sauvegarder.")
            else:
                filepath = input("\nChemin de sauvegarde (.json, .csv, .xml, .yaml) : ").strip()

                try:
                    save_file(filepath, data)
                    print(f"Données sauvegardées : {filepath}")
                except Exception as e:
                    print(f"Erreur lors de la sauvegarde : {e}")

        elif choix == "8":
            # Quitter
            print("\n" + "=" * 70)
            print(" " * 20 + "Merci d'avoir utilisé DATA FILTER")
            print(" " * 25 + "Au revoir !")
            print("=" * 70 + "\n")
            break

        else:
            print("Choix invalide. Veuillez entrer un nombre entre 1 et 8.")


if __name__ == "__main__":
    main()