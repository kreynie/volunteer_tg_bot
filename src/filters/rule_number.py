def is_valid_rule_number(rule_number: str) -> bool:
    numbers = rule_number.split(".")
    for number in numbers:
        return False if not number.isdigit() else True
    return True
