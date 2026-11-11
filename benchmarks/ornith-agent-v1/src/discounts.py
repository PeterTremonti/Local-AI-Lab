def apply_discount(amount, percent):
    if percent <= 0:
        return amount

    return amount - amount * (percent / 100)
