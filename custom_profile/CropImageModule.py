import json
import os

from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render_to_response

from custom_profile.forms import ImageUploadForm
from custom_profile.models import ProfileAvatar
from events_all import helper, settings


class CropImageModule:
    # Берем с пользователя картинку и записываем во временную папку
    # return Урл на картинку, размеры, коэффициент соотношения сторон
    @login_required(login_url='/accounts/login/')
    def load_image(request):
        if 'image' in request.FILES:
            image = request.FILES['image']
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
            if 'image' in request.FILES:
                image = request.FILES['image']
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
