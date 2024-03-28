def plural_form(number: int, one: str, two: str, five: str) -> str:
    """
    Returns the correct Russian plural form of a word depending on the number.

    :param number: The number to determine the plural form.
    :param one: The word form for the singular or when the number ends with 1 (excluding numbers ending with 11).
    :param two: The word form for numbers ending with 2, 3, or 4 (excluding numbers ending with 12, 13, or 14).
    :param five: The word form for all other cases, including numbers ending with 0, or those ending with 5, 6, 7, 8, or 9.
    :return: The appropriate word form depending on the number.
    """
    if number % 10 == 1 and number % 100 != 11:
        return one
    elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return two
    else:
        return five
