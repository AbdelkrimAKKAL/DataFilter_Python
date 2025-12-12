def sort_data(data, field, reverse=False):

    if not data:
        return []

    # get key
    def get_sort_key(item):
        value = item.get(field)

        # Pour les listes on trie par taille
        if isinstance(value, list):
            return len(value)

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

    # On trie en cascade (du dernier au premier critere)
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

