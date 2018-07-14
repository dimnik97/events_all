import json
import os

from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from events_all import helper, settings


class PhotoEditor:
    # Берем с пользователя картинку и записываем во временную папку
    # return Урл на картинку, размеры, коэффициент соотношения сторон
    @login_required(login_url='/accounts/login/')
    def load_image(request):
        if 'load_image' in request.FILES:
            image = request.FILES['load_image']
            status = 200

            if int(image.size) > 26214400:
                status = 'size_error'

            image_types = [
                'image/png', 'image/jpg',
                'image/jpeg', 'image/pjpeg', 'image/gif'
            ]
            if image.content_type not in image_types:
                data = json.dumps({
                    'status': 405,
                    'error': _('Bad image format.')
                })
                return HttpResponse(
                    data, content_type="application/json", status=405)

            path = helper.temporary_path(image.name)
            path = default_storage.save(path, ContentFile(image.read()))
            img_url = os.path.join(settings.MEDIA_URL, path)

            pil_im = Image.open(image)

            width = pil_im.width
            height = pil_im.height
            coefficient = width / height

            image_info = {
                'width': width,
                'height': height,
                'coefficient': coefficient
            }
            data = json.dumps({
                'status': status,
                'link': img_url,
                'name': image.name,
                'image_info': image_info
            })
            return HttpResponse(data, content_type='application/json')
        return HttpResponse(_('Invalid request!'))

    # Снова берем с пользователя картинку, проверяем, так как на клиенте могли поменять
    # return сохранение в переданную модель
    def save_image(request, model):
        if request.method == 'POST' and request.is_ajax():
            if 'load_image' in request.FILES:
                image = request.FILES['load_image']
                status = 200

                if int(image.size) > 26214400:
                    status = 'size_error'

                image_types = [
                    'image/png', 'image/jpg',
                    'image/jpeg', 'image/pjpeg', 'image/gif'
                ]
                if image.content_type not in image_types:
                    data = json.dumps({
                        'status': 405,
                        'error': _('Bad image format.')
                    })
                    return HttpResponse(
                        data, content_type="application/json", status=405)

                if "image_type" in request.POST:
                    image_type = request.POST['image_type']
                else:
                    image_type = 'avatar'

                model.image = image
                model.save(admin_panel=False, request=request, image_type=image_type)

                data = json.dumps({
                    'status': status,
                })
                return HttpResponse(data, content_type='application/json')
            elif "image_type" in request.POST:
                image_type = request.POST['image_type']
                model.save(admin_panel=False, request=request, image_type=image_type)
                data = json.dumps({
                    'status': 200,
                })
                return HttpResponse(data, content_type='application/json')
            return HttpResponse(_('Invalid request!'))

        return HttpResponse(_('Invalid request type!'))

    # Добавляем:
    # - создание миниатюры
    # - удаление миниатюры и основного изображения (дефолтная не удаляется)
    #   при попытке записи поверх существующей записи
    #   Кроп + перевороты
    def save_photo(self_cls, cls, admin_panel=True, image_type='avatar', force_insert=False, force_update=False,
                   using=None, request=None):
        try:
            obj = cls.objects.get(id=self_cls.user.profileavatar.id)
            if obj.image.path != self_cls.image.path:
                helper._del_mini(obj.image.path, postfix='mini')
                helper._del_mini(obj.image.path, postfix='reduced')
                if str(obj.image).find('default') == -1:
                    obj.image.delete()
        except:
            pass
        super(cls, self_cls).save()

        if admin_panel:
            mini = Image.open(self_cls.image.path)
            reduced = Image.open(self_cls.image.path)
            mini = helper.create_mini_image(mini)
            reduced = helper.create_medium_image(reduced)

            quality_val = 85
            mini.save(self_cls.mini_path, quality=quality_val, optimize=True, progressive=True)
            reduced.save(self_cls.reduced_path, quality=quality_val, optimize=True, progressive=True)
        else:
            # Редактирование с клиента
            if image_type == 'avatar':
                # Редактирование аватарки(учитывая поворот и кроп) и создание миниатюры по умолчанию
                reduced = Image.open(self_cls.image.path)

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
                reduced.save(self_cls.reduced_path, quality=quality_val, optimize=True, progressive=True)

                mini = helper.create_mini_image(new_response)
                mini.save(self_cls.mini_path, optimize=True, progressive=True)
            elif image_type == 'mini':
                # Редактирование миниатюры
                reduced = Image.open(self_cls.reduced_path)
                mini = reduced.crop((float(request.POST['crop_x1']),
                                     float(request.POST['crop_y1']),
                                     float(request.POST['crop_x2']),
                                     float(request.POST['crop_y2'])))
                mini.save(self_cls.mini_path, optimize=True, progressive=True)

    # Получение размеров картинки для миниатюры
    def get_image_size(path):
        reduced = Image.open(path)
        coefficient = reduced.width / reduced.height
        max = 500
        if coefficient < 1:
            width = 'auto'
            height = str(max) + 'px'
            width_crop_coef = reduced.height / max
            margin_left = str((max - reduced.width / width_crop_coef) / 2) + 'px'
            margin_top = 0

        elif coefficient == 1:
            width = str(max) + 'px'
            height = str(max) + 'px'
            margin_top = 0
            margin_left = 0
        elif coefficient > 1:
            width = str(max) + 'px'
            height = 'auto'
            height_crop_coef = reduced.width / max
            margin_left = 0
            margin_top = str((max - reduced.height / height_crop_coef) / 2) + 'px'

        image_attr = {
            'margin_top': margin_top,
            'margin_left': margin_left,
            'width': width,
            'height': height,
            'orig_height': reduced.height,
            'orig_width': reduced.width
        }
        return image_attr

    # Делаем свою delete с учетом миниатюры
    def delete_photo(self_cls, cls, using=None):
        try:
            obj = cls.objects.get(id=self_cls.id)
            path = obj.image.path
            helper._del_mini(path, postfix='mini')
            helper._del_mini(path, postfix='reduced')
            if 'default' not in path:
                obj.image.delete()
        except (cls.DoesNotExist, ValueError):
            pass
        super(cls, self_cls).delete()