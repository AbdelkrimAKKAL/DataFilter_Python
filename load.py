import json
import csv
import ast
import xml.etree.ElementTree as ET

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


def convert_value(value):
    if isinstance(value, (int, float, bool, list)):
        return value

    if not isinstance(value, str):
        return value

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

    return value


# JSON
def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# CSV
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


# XML
def load_xml(filepath):

    tree = ET.parse(filepath)
    root = tree.getroot()

    result = []
    for item_elem in root:
        item = {}
        for field in item_elem:
            value = field.text
            item[field.tag] = convert_value(value) if value else None
        result.append(item)

    return result


def save_xml(filepath, data, root_name="data", item_name="item"):

    if not data:
        return

    root = ET.Element(root_name)

    for item in data:
        item_elem = ET.SubElement(root, item_name)
        for key, value in item.items():
            field_elem = ET.SubElement(item_elem, key)
            field_elem.text = str(value)

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(filepath, encoding="utf-8", xml_declaration=True)


# YAML
def load_yaml(filepath):

    if not YAML_AVAILABLE:
        raise ImportError("PyYAML n'est pas installé.")

    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(filepath, data):

    if not YAML_AVAILABLE:
        raise ImportError("PyYAML n'est pas installé.")

    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


# Fonction générique
def load_file(filename):
    filepath = "fichiers/"+ filename
    if filepath.endswith(".json"):
        return load_json(filepath)
    elif filepath.endswith(".csv"):
        return load_csv(filepath)
    elif filepath.endswith(".xml"):
        return load_xml(filepath)
    elif filepath.endswith((".yaml", ".yml")):
        return load_yaml(filepath)
    else:
        raise ValueError(f"Format non supporté : {filepath}")


def save_file(filename, data):
    filepath = "save/" + filename
    if filepath.endswith(".json"):
        save_json(filepath, data)
    elif filepath.endswith(".csv"):
        save_csv(filepath, data)
    elif filepath.endswith(".xml"):
        save_xml(filepath, data)
    elif filepath.endswith((".yaml", ".yml")):
        save_yaml(filepath, data)
    else:
        raise ValueError(f"Format non supporté : {filepath}")