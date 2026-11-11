from src.cart import checkout


def test_ten_percent_discount_then_ten_percent_tax():
    items = [{"unit_price": 10.0, "quantity": 2}]

    assert checkout(
        items,
        discount_percent=10,
        tax_rate=0.10
    ) == 19.80


def test_zero_discount_then_ten_percent_tax():
    items = [{"unit_price": 10.0, "quantity": 2}]

    assert checkout(
        items,
        discount_percent=0,
        tax_rate=0.10
    ) == 22.00
