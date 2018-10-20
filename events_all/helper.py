import os
from hashlib import md5
from time import time
from os import path as op
from PIL import Image


# Возвращает массив в 2СС из 10СС
def convert_base(num):
    if num == 0:
        return [0]
    res = [int(x) for x in list('{0:b}'.format(num))]
    return res


class ImageHelper:
    @staticmethod
    def add_mini(s, postfix=''):
        parts = s.split(".")
        parts.insert(-1, postfix)
        if parts[-1].lower() not in ['jpeg', 'jpg', 'png']:
            parts[-1] = 'jpg'
        return ".".join(parts)

    # Удаление миниатюры с физического носителя.
    @classmethod
    def del_mini(cls, p, postfix=''):
        mini_path = cls.add_mini(p, postfix)
        if 'default' not in mini_path:
            if os.path.exists(mini_path):
                os.remove(mini_path)

    @staticmethod
    def upload_to(instance, filename, prefix=None, unique=False):
        ext = op.splitext(filename)[1]
        name = str(instance.pk or '') + filename + (str(time()) if unique else '')
        filename = md5(name.encode('utf8')).hexdigest() + ext

        return op.join(prefix, filename[:2], filename[2:4], filename)

    @staticmethod
    def temporary_path(filename):
        ext = op.splitext(filename)[1]
        name = filename + str(time())
        filename = md5(name.encode('utf8')).hexdigest() + ext

        return op.join('temporary', filename[:2], filename[2:4], filename)


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


# Создание миниатюры (на основе ориг.)
def create_mini_image(img):
    img.thumbnail(
        (128, 128),
        Image.ANTIALIAS
    )
    return img


# Создание форматированного изображения (на основе ориг.)
def create_medium_image(img):
    height = img.height
    width = img.width

    max_width = 1440
    max_height = 1440
    if width >= max_width or height >= max_height:
        correlation = width / height
        height = width / correlation
        width = max_width

        img.thumbnail(
            (width, height),
            Image.ANTIALIAS
        )
    return img


# Приведение курсора в dict для RAW Запросов
@staticmethod
def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]



# from django.db import connection
# cursor = connection.cursor()
#
# cursor.execute("""Select * from events__eventmembership ms
#             left join events__event ev on ms.event_id = ev.id
#             where (select id from profiles_profile where user_id = 34) = ms.person_id""")
#
# row = Event.dictfetchall(cursor)
