

def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def print_django(message):
    print(f"[Django] {message}")


def remove_substrings_from_string(string_a: str, substrings: list) -> str:
    for substring in substrings:
        string_a = string_a.replace(substring, '')
    return string_a
