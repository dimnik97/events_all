import os
from hashlib import md5
from time import time
from os import path as op


# Изменение (filename, URL) вставкой '.mini' и изменение расширения на jpg
def _add_mini(s):
    parts = s.split(".")
    parts.insert(-1, "mini")
    if parts[-1].lower() not in ['jpeg', 'jpg', 'png']:
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

    basedir = 'media'
    if prefix:
        basedir = op.join(basedir, prefix)
    filename = md5(name.encode('utf8')).hexdigest() + ext

    return op.join(basedir, prefix, filename[:2], filename[2:4], filename)


def parse_from_error_to_json(request, form):
    data = []
    for k, v in form._errors.items():
        text = {
            'desc': ', '.join(v),
        }
        if k == '__all__':
            text['key'] = '#%s' % request.POST.get('form')
        else:
            text['key'] = '#id_%s' % k
        data.append(text)
    return data
