
# Принимает ключ, возвращает строку с ошибкой
def validate_error(key, field_name):
    status = {
        'empty': 'Поле ' + field_name + ' не заполнено',
        'format': 'Неверный формат ' + field_name,
        'exist': field_name + ' уже существует в базе',
        'True': field_name + ' уже существует в базе',
        'False': ''
    }
    return status[key]