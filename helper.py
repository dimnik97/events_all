from hashlib import md5
from os import path as op, os
from time import time


# Изменение (filename, URL) вставкой '.mini' и изменение расширения на jpg
def _add_mini(s):
    parts = s.split(".")
    parts.insert(-1, "mini")
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return ".".join(parts)

# Удаление миниатюры с физического носителя.
def _del_mini(p):
    mini_path = _add_mini(p)
    if os.path.exists(mini_path):
        os.remove(mini_path)

def upload_to(instance, filename, prefix=None, unique=False):
    ext = op.splitext(filename)[1]
    name = str(instance.pk or '') + filename + (str(time()) if unique else '')

    filename = md5(name.encode('utf8')).hexdigest() + ext
    basedir = op.join(instance._meta.app_label, instance._meta.module_name)
    if prefix:
        basedir = op.join(basedir, prefix)
    return op.join(basedir, filename[:2], filename[2:4], filename)


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
