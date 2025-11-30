import json
import csv
import ast

def convert_value(value):
    """
    Convertit une valeur CSV en son type correct :
    - int
    - float
    - bool
    - list
    - sinon string
    """

    # Essayer int
    try:
        return int(value)
    except:
        pass

    # Essayer float
    try:
        return float(value)
    except:
        pass

    # Booléen
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False

    # Listes style "[12, 15, 17]"
    try:
        if value.startswith("[") and value.endswith("]"):
            return ast.literal_eval(value)
    except:
        pass

    # Sinon string
    return value


def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_csv(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        res = []

        for row in reader:
            converted_row = {key: convert_value(value) for key, value in row.items()}
            res.append(converted_row)

        return res

def save_csv(filepath, data):
    if not data:
        return
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
