def sort_data(data, field, reverse=False):

    if not data:
        return []

    # Fonction de clé qui gère les différents types
    def get_sort_key(item):
        value = item.get(field)

        # Pour les listes, on trie par taille
        if isinstance(value, list):
            return len(value)

        # Pour None, on met à la fin
        if value is None:
            return float('inf') if not reverse else float('-inf')

        return value

    try:
        return sorted(data, key=get_sort_key, reverse=reverse)
    except Exception as e:
        print(f"Erreur lors du tri sur le champ '{field}': {e}")
        return data


def sort_data_multi(data, fields, reverse_list=None):

    if not data:
        return []

    if reverse_list is None:
        reverse_list = [False] * len(fields)

    # On trie en cascade (du dernier au premier critère)
    result = data.copy()

    for i in range(len(fields) - 1, -1, -1):
        field = fields[i]
        reverse = reverse_list[i] if i < len(reverse_list) else False

        def get_sort_key(item):
            value = item.get(field)

            if isinstance(value, list):
                return len(value)

            if value is None:
                return float('inf') if not reverse else float('-inf')

            return value

        try:
            result = sorted(result, key=get_sort_key, reverse=reverse)
        except:
            print(f"Erreur lors du tri sur '{field}'")

    return result


def sort_by_expression(data, key_func, reverse=False):

    try:
        return sorted(data, key=key_func, reverse=reverse)
    except Exception as e:
        print(f"Erreur lors du tri avec expression personnalisée: {e}")
        return data


def sort_by_list_stats(data, field, stat="mean", reverse=False):

    if not data:
        return []

    def get_sort_key(item):
        value = item.get(field)

        if not isinstance(value, list):
            return 0

        if not value:
            return 0

        try:
            if stat == "min":
                return min(value)
            elif stat == "max":
                return max(value)
            elif stat == "mean":
                return sum(value) / len(value)
            elif stat == "sum":
                return sum(value)
            elif stat == "size":
                return len(value)
            else:
                return 0
        except:
            return 0

    try:
        return sorted(data, key=get_sort_key, reverse=reverse)
    except Exception as e:
        print(f"Erreur lors du tri: {e}")
        return data