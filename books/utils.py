def unit_by_field(sql_response_rows, field, filtered=[], duplicate=False):
    result = {}
    headers = []

    for row in sql_response_rows:
        if field not in row:
            raise Exception('field not exist')

        item = result.get(row[field], {})
        for key, value in row.items():
            if key == field or key in filtered:
                continue

            headers.append(key)

            tmp = item.get(key, [])

            if value in tmp and not duplicate:
                continue

            item[key] = tmp + [value]

        result[row[field]] = item

    return result, [field] + headers


def nested_dict_to_list(d):
    result = []

    for key, nested in d.items():
        item = [key]
        for nested_key, value in nested.items():
            item += [', '.join(map(str, value))]

        result.append(item)

    return result
