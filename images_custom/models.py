from PIL import Image
from django.db import models

# Create your models here.
from events_all import helper


class PhotoEditor:
    # Создаем свою save
    # Добавляем:
    # - создание миниатюры
    # - удаление миниатюры и основного изображения
    #   при попытке записи поверх существующей записи
    def save(self, cls, admin_panel=True, image_type='avatar', force_insert=False, force_update=False, using=None,
             request=None, ):
        try:
            obj = cls.objects.get(id=self.user.profileavatar.id)
            if obj.image.path != self.image.path:
                helper._del_mini(obj.image.path, postfix='mini')
                helper._del_mini(obj.image.path, postfix='reduced')
                if 'default' not in obj.image:
                    obj.image.delete()
        except:
            pass
        super(cls, self).save()

        if admin_panel:
            mini = Image.open(self.image.path)
            reduced = Image.open(self.image.path)
            mini = helper.create_mini_image(mini)
            reduced = helper.create_medium_image(reduced)

            quality_val = 85
            mini.save(self.mini_path, quality=quality_val, optimize=True, progressive=True)
            reduced.save(self.reduced_path, quality=quality_val, optimize=True, progressive=True)
        else:
            # Редактирование с клиента
            if image_type == 'avatar':
                # Редактирование аватарки(учитывая поворот и кроп) и создание миниатюры по умолчанию
                reduced = Image.open(self.image.path)

                if request.POST['rotate'] == 'undefined':
                    angle = 0
                else:
                    angle = 360 - int(request.POST['rotate'])
                new_response = reduced.rotate(angle).crop((float(request.POST['crop_x1']),
                                                           float(request.POST['crop_y1']),
                                                           float(request.POST['crop_x2']),
                                                           float(request.POST['crop_y2'])))

                quality_val = 85
                reduced = helper.create_medium_image(new_response)
                reduced.save(self.reduced_path, quality=quality_val, optimize=True, progressive=True)

                mini = helper.create_mini_image(new_response)
                mini.save(self.mini_path, optimize=True, progressive=True)
            elif image_type == 'mini':
                # Редактирование миниатюры
                reduced = Image.open(self.reduced_path)
                mini = reduced.crop((float(request.POST['crop_x1']),
                                     float(request.POST['crop_y1']),
                                     float(request.POST['crop_x2']),
                                     float(request.POST['crop_y2'])))
                # mini = helper.create_mini_image(mini)
                mini.save(self.mini_path, optimize=True, progressive=True)

    # Делаем свою delete с учетом миниатюры
    def delete(self, cls, using=None):
        try:
            obj = cls.objects.get(id=self.id)
            path = obj.image.path
            helper._del_mini(path, postfix='mini')
            helper._del_mini(path, postfix='reduced')
            if 'default' not in path:
                obj.image.delete()
        except (cls.DoesNotExist, ValueError):
            pass
        super(cls, self).delete()

