def apply_discount(amount, percent):
    if percent <= 0:
        return amount

    return amount * (1 - percent / 100)
