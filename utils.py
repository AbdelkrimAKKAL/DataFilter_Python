

def add_field(data, field_name, default_value=None):

    if not data:
        return data

    for item in data:
        if callable(default_value):
            item[field_name] = default_value(item)
        else:
            item[field_name] = default_value

    return data


def remove_field(data, field_name):

    if not data:
        return data

    for item in data:
        if field_name in item:
            del item[field_name]

    return data


def rename_field(data, old_name, new_name):

    if not data:
        return data

    for item in data:
        if old_name in item:
            item[new_name] = item.pop(old_name)

    return data


def transform_field(data, field_name, transform_func):

    if not data:
        return data

    for item in data:
        if field_name in item:
            try:
                item[field_name] = transform_func(item[field_name])
            except:
                pass

    return data


def show_data_table(data, limit=None):

    if not data:
        print("Aucune donnée à afficher.")
        return

    # Limiter si nécessaire
    display_data = data[:limit] if limit else data

    # Récupérer les champs
    fields = list(data[0].keys())

    # Calculer les largeurs de colonnes
    col_widths = {}
    for field in fields:
        col_widths[field] = max(
            len(str(field)),
            max(len(str(item.get(field, ""))) for item in display_data)
        )
        col_widths[field] = min(col_widths[field], 30)  # Max 30 caractères

    # En-tête
    header = " | ".join(f"{field:<{col_widths[field]}}" for field in fields)
    separator = "-+-".join("-" * col_widths[field] for field in fields)

    print("\n" + header)
    print(separator)

    # Données
    for item in display_data:
        row = " | ".join(
            f"{str(item.get(field, '')):<{col_widths[field]}}"[:col_widths[field]]
            for field in fields
        )
        print(row)

    # Information sur les données non affichées
    if limit and len(data) > limit:
        print(f"\n... et {len(data) - limit} autres entrées")

    print(f"\nTotal : {len(data)} entrées")


def get_user_value(prompt, value_type=None):

    value_str = input(prompt).strip()

    if value_type == "int":
        return int(value_str)
    elif value_type == "float":
        return float(value_str)
    elif value_type == "bool":
        return value_str.lower() in ["true", "1", "yes", "oui"]
    elif value_type == "str":
        return value_str
    else:
        # Auto-détection
        try:
            if value_str.isdigit() or (value_str.startswith('-') and value_str[1:].isdigit()):
                return int(value_str)
        except:
            pass

        try:
            if '.' in value_str:
                return float(value_str)
        except:
            pass

        if value_str.lower() == "true":
            return True
        elif value_str.lower() == "false":
            return False

        return value_str