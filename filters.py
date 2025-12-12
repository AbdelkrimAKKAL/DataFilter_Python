from stats import get_field_stats


def filter_data(data, field, operator, value):
    if not data:
        return []

    result = []
    for item in data:
        if field not in item:
            continue

        field_value = item[field]

        # Gestion selon type
        if operator == "==":
            if field_value == value:
                result.append(item)
        elif operator == "!=":
            if field_value != value:
                result.append(item)
        elif operator == "<":
            if isinstance(field_value, list):
                if len(field_value) < value:
                    result.append(item)
            else:
                try:
                    if field_value < value:
                        result.append(item)
                except:
                    pass

        elif operator == ">":
            if isinstance(field_value, list):
                if len(field_value) > value:
                    result.append(item)
            else:
                try:
                    if field_value > value:
                        result.append(item)
                except:
                    pass

        elif operator == "<=":
            if isinstance(field_value, list):
                if len(field_value) <= value:
                    result.append(item)
            else:
                try:
                    if field_value <= value:
                        result.append(item)
                except:
                    pass

        elif operator == ">=":
            if isinstance(field_value, list):
                if len(field_value) >= value:
                    result.append(item)
            else:
                try:
                    if field_value >= value:
                        result.append(item)
                except:
                    pass

        # Operateur pour chaines de caracteres ici
        elif operator == "contains":
            if isinstance(field_value, str) and value in field_value:
                result.append(item)
        elif operator == "startswith":
            if isinstance(field_value, str) and field_value.startswith(value):
                result.append(item)

        elif operator == "endswith":
            if isinstance(field_value, str) and field_value.endswith(value):
                result.append(item)

    return result


def filter_combined(data, field1, field2, operator):
    if not data:
        return []

    result = []

    for item in data:
        if field1 not in item or field2 not in item:
            continue

        val1 = item[field1]
        val2 = item[field2]

        try:
            if operator == ">" and val1 > val2:
                result.append(item)
            elif operator == "<" and val1 < val2:
                result.append(item)
            elif operator == "==" and val1 == val2:
                result.append(item)
            elif operator == ">=" and val1 >= val2:
                result.append(item)
            elif operator == "<=" and val1 <= val2:
                result.append(item)
            elif operator == "!=":
                if val1 != val2:
                    result.append(item)
        except:
            continue

    return result


def filter_by_stats(data, field, operator, stat_type="mean"):

    if not data:
        return []

    stats = get_field_stats(data, field)
    if not stats or stats["type"] != "numeric":
        print(f"Impossible de calculer les stats pour '{field}'")
        return data

    threshold = stats.get(stat_type)

    if threshold is None:
        print(f"Statistique '{stat_type}' non disponible")
        return data

    print(f"Seuil calculé ({stat_type}) : {threshold:.2f}")

    return filter_data(data, field, operator, threshold)


def filter_multi_conditions(data, conditions):

    result = data

    for field, operator, value in conditions:
        result = filter_data(result, field, operator, value)

    return result