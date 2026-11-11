from .discounts import apply_discount


def subtotal(items):
    return sum(item["unit_price"] * item["quantity"] for item in items)


def checkout(items, discount_percent=0, tax_rate=0.0):
    amount = subtotal(items)
    discounted_amount = apply_discount(amount, discount_percent)
    total = discounted_amount * (1 + tax_rate)
    return round(total, 2)
