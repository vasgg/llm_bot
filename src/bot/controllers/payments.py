from yookassa import Payment


async def get_subscription_payment(value: int) -> PaymentResponse:
    payment = Payment.create({
        "amount": {
            "value": f"{value}.00",
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.example.com/return_url"
        },
        "capture": True,
        "description": f"Подписка на {days} дней",
        "save_payment_method": True
    })
    return payment

def create_payment(amount: float, description: str = "Оплата подписки", return_url: str = None) -> Payment:

    payment = Payment.create({
        "amount": {
            "value": str(amount),
            "currency": "RUB",
        },
        "confirmation": {
            "type": "redirect",
            "return_url": return_url or "https://example.com/return",
        },
        "capture": True,
        "description": description,
    })
    return payment


res = Payment.create(
    {
        "amount": {
            "value": 1000,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://merchant-site.ru/return_url"
        },
        "capture": True,
        "description": "Заказ №72",
        "metadata": {
            'orderNumber': '72'
        },
        "receipt": {
            "customer": {
                "full_name": "Ivanov Ivan Ivanovich",
                "email": "email@email.ru",
                "phone": "79211234567",
                "inn": "6321341814"
            },
            "items": [
                {
                    "description": "Переносное зарядное устройство Хувей",
                    "quantity": "1.00",
                    "amount": {
                        "value": 1000,
                        "currency": "RUB"
                    },
                    "vat_code": "2",
                    "payment_mode": "full_payment",
                    "payment_subject": "commodity",
                    "country_of_origin_code": "CN",
                    "product_code": "44 4D 01 00 21 FA 41 00 23 05 41 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 AB 00",
                    "customs_declaration_number": "10714040/140917/0090376",
                    "excise": "20.00",
                    "supplier": {
                        "name": "string",
                        "phone": "string",
                        "inn": "string"
                    }
                },
            ]
        }
    }
)

var_dump.var_dump(res)
