from django import template

register = template.Library()


@register.filter(name='format_phone')
def format_phone(value):
    """Преобразует строку с номером телефона в формат +7 (XXX) XXX-XXXX."""
    if value:
        # Оставляем только цифры в строке
        digits = filter(str.isdigit, value)
        phone_number = ''.join(digits)

        # Форматируем номер телефона
        return f'+7 ({phone_number[1:4]}) {phone_number[4:7]}-{phone_number[7:]}'

    return value


