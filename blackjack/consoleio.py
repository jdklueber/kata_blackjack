def get_int_from_user(prompt: str, min_val: int = None, max_val: int = None):
    message = prompt
    if min_val:
        message += f" min:{min_val}"
    if max_val:
        message += f" max:{max_val}"
    message += "> "
    valid = False

    while not valid:
        value = input(message)
        result = validate_int(value, min_val, max_val)
        if result is not False:
            return result

        print(
            f"Invalid input.  Please enter an integer between {min_val} and {max_val}"
        )


def get_menu_choice(menu: dict[int, str]):
    min_choice = min(menu.keys())
    max_choice = max(menu.keys())

    for key in menu:
        print(f"{key}: {menu[key]}")

    return get_int_from_user("", min_val=min_choice, max_val=max_choice)


def validate_int(value: str, min_val: int = None, max_val: int = None):
    try:
        result = int(value)
        if min_val is not None:
            if result < min_val:
                return False
        if max_val is not None:
            if result > max_val:
                return False

        return result
    except ValueError:
        return False


def print_title(title):
    print("=" * len(title))
    print(title)
    print("=" * len(title))
