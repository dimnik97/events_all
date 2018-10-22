import json
import os
from os import path as op
from PIL import Image, ImageDraw, ImageEnhance
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from events_all import helper, settings


class PhotoEditor:
    # Берем с пользователя картинку и записываем во временную папку
    # return Урл на картинку, размеры, коэффициент соотношения сторон
    @login_required(login_url='/accounts/login/')
    def load_image(self):
        request = self
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
                    'error': 'Bad image format.'
                })
                return HttpResponse(
                    data, content_type="application/json", status=405)

            path = helper.ImageHelper.temporary_path(image.name)
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
        return HttpResponse('Invalid request!')

    # Снова берем с пользователя картинку, проверяем, так как на клиенте могли поменять
    # return сохранение в переданную модель
    @staticmethod
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
                        'error': 'Bad image format.'
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
            return HttpResponse('Invalid request!')

        return HttpResponse('Invalid request type!')

    # Добавляем:
    # - создание миниатюры
    # - удаление миниатюры и основного изображения (дефолтная не удаляется)
    #   при попытке записи поверх существующей записи
    #   Кроп + перевороты
    @staticmethod
    def save_photo(self_cls, cls, admin_panel=True, image_type='avatar', request=None):
        try:
            obj = cls.objects.get(id=self_cls.user.profileavatar.id)
            if obj.image.path != self_cls.image.path:
                helper.ImageHelper.del_mini(obj.image.path, postfix='mini')
                helper.ImageHelper.del_mini(obj.image.path, postfix='reduced')
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
    @staticmethod
    def get_image_size(path):
        reduced = Image.open(path)
        coefficient = reduced.width / reduced.height
        max_side_in_pixels = 500
        margin_top = 0
        margin_left = 0
        width = 0
        height = 0
        if coefficient < 1:
            width = 'auto'
            height = str(max_side_in_pixels) + 'px'
            width_crop_coef = reduced.height / max_side_in_pixels
            margin_left = str((max_side_in_pixels - reduced.width / width_crop_coef) / 2) + 'px'
            margin_top = 0

        elif coefficient == 1:
            width = str(max_side_in_pixels) + 'px'
            height = str(max_side_in_pixels) + 'px'
            margin_top = 0
            margin_left = 0
        elif coefficient > 1:
            width = str(max_side_in_pixels) + 'px'
            height = 'auto'
            height_crop_coef = reduced.width / max_side_in_pixels
            margin_left = 0
            margin_top = str((max_side_in_pixels - reduced.height / height_crop_coef) / 2) + 'px'

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
    @staticmethod
    def delete_photo(self_cls, cls, using=None):
        try:
            obj = cls.objects.get(id=self_cls.id)
            path = obj.image.path
            helper.ImageHelper.del_mini(path, postfix='mini')
            helper.ImageHelper.del_mini(path, postfix='reduced')
            if 'default' not in path:
                obj.image.delete()
        except (cls.DoesNotExist, ValueError):
            pass
        super(cls, self_cls).delete()

    @staticmethod
    def add_watermark(image, watermark, opacity=1, wm_interval=0):
        assert opacity >= 0 and opacity <= 1
        if opacity < 1:
            if watermark.mode != 'RGBA':
                watermark = watermark.convert('RGBA')
            else:
                watermark = watermark.copy()
            alpha = watermark.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            watermark.putalpha(alpha)
        layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
        for y in range(0, image.size[1], watermark.size[1] + wm_interval):
            for x in range(0, image.size[0], watermark.size[0] + wm_interval):
                layer.paste(watermark, (x, y))
        return Image.composite(layer, image, layer)

    @staticmethod
    def create_image_for_two_categories(categories, general_file_name, images_names):
        try:
            img_path_1 = op.join('media', 'avatar_event_default', categories[0], images_names[0] + '.png')
            img1 = Image.open(img_path_1)
            draw1 = ImageDraw.Draw(img1)
            h1 = img1.height
            w1 = img1.width
            draw1.polygon([(w1, h1), (0, h1), (w1, 0)], fill=(0, 0, 0, 0))
            img_path_2 = op.join('media', 'avatar_event_default', categories[1], images_names[1] + '.png')
            img2 = Image.open(img_path_2)
            draw2 = ImageDraw.Draw(img2)
            h2 = img2.height
            w2 = img2.width
            draw2.polygon([(0, 0), (0, h2), (w2, 0)], fill=(0, 0, 0, 0))
            img = PhotoEditor.add_watermark(img1, img2)

            img.save(op.join('media', 'avatar_event_default', 'general', general_file_name), 'PNG')

            result = {
                'image': op.join('general', general_file_name),
                'image_names': [images_names[0], images_names[1], 'default']
            }
            return result
        except IOError:
            return op.join('default.png')

    @staticmethod
    def create_image_for_three_categories(categories, general_file_name, images_names):
        try:
            img_path_1 = op.join('media', 'avatar_event_default', categories[0], images_names[0] + '.png')
            img1 = Image.open(img_path_1)
            draw1 = ImageDraw.Draw(img1)
            h1 = img1.height
            w1 = img1.width
            draw1.polygon([(w1/2, 0), (w1, 0), (w1, h1), (w1/2, h1)], fill=(0, 0, 0, 0))
            draw1.polygon([(w1, h1), (0, h1), (w1, 0)], fill=(0, 0, 0, 0))

            img_path_2 = op.join('media', 'avatar_event_default', categories[1], images_names[1] + '.png')
            img2 = Image.open(img_path_2)
            draw2 = ImageDraw.Draw(img2)
            h2 = img2.height
            w2 = img2.width
            draw2.polygon([(w2/2, 0), (0, 0), (0, h2), (w2/2, h2)], fill=(0, 0, 0, 0))
            draw2.polygon([(0, 0), (0, h2), (w2, h2)], fill=(0, 0, 0, 0))

            img_path_3 = op.join('media', 'avatar_event_default', categories[2], images_names[2] + '.png')
            img3 = Image.open(img_path_3)
            draw3 = ImageDraw.Draw(img3)
            h3 = img3.height
            w3 = img3.width
            draw3.polygon([(0, 0), (w3, 0), (w3, h3)], fill=(0, 0, 0, 0))
            draw3.polygon([(0, h3), (0, 0), (w3, 0)], fill=(0, 0, 0, 0))

            img = PhotoEditor.add_watermark(img1, img2)
            img = PhotoEditor.add_watermark(img, img3)
            img.save(op.join('media', 'avatar_event_default', 'general', general_file_name), 'PNG')
            result = {
                'image': op.join('general', general_file_name),
                'image_names': [images_names[0], images_names[1], images_names[2]]
            }
            return result
        except IOError:
            return op.join('default.png')