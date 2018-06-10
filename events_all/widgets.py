from datetime import timedelta

from django import forms
from django.forms.utils import flatatt
from django.utils.datetime_safe import datetime
from django.utils.safestring import mark_safe


class CustomDateTimePicker(forms.PasswordInput):
    # принимает параметр prams, который нужен для настройки виджета
    def __init__(self, prams=None):
        if prams is not None:
            prams = prams.copy()
        super().__init__(prams)

    def render(self, name, value, attrs=None):
        super().render(name, value, attrs)
        flat_attrs = flatatt(attrs)

        # default_time - параметр для возвращения текущей даты и времени
        if value is None:
            try:
                if self.attrs['default_time'] == '1':
                    value = datetime.now().strftime("%Y-%m-%d %H:%M")
            except:
                pass
            # default_time_plus_delta - параметр для возвращения текущей даты и времени + 1 час
            try:
                if self.attrs['default_time_plus_delta'] == '1':
                    value = datetime.now() + timedelta(hours=1)
                    value = value.strftime("%Y-%m-%d %H:%M")
            except:
                pass

        html = '''
            <input %(attrs)s is_datetimepicker type="text" value=""/>
            <input class="custom_hidden_field  %(id)s"  name="%(name)s" type="text" value=""/>
            
            
            <script type="text/javascript">
            $(document).ready(function() {
                // одно из полей скрыто, оно отправляется на сервер
                // берем дату, которая пришла и учитываем часовой пояс пользователя
                
                var d = new Date();
                var timezone = d.getTimezoneOffset();
                var text = "%(value)s";
                var date = new Date(text.replace(/(\d+)-(\d+)-(\d+)/, '$2/$3/$1'));
                // var date_with_timezone = new Date(+date - timezone * 6e4);
                // debugger;
                // по изменению видимого поля просталвляем дату в гмт+0 в скрытое поле для отправки на сервер
                
                $('#%(id)s').on('change', function(){
                    var date_val = $('#%(id)s').val().replace(/(\d+)-(\d+)-(\d+)/, '$2/$3/$1');
                    var date_with_timezone_for_hidden = new Date(+date_val + timezone * 6e4);
                    var str_date = date_with_timezone_for_hidden.getFullYear()+'-'+
                                   date_with_timezone_for_hidden.getMonth() +'-'+
                                   date_with_timezone_for_hidden.getDay() +' '+
                                   date_with_timezone_for_hidden.getHours() +':'+
                                   date_with_timezone_for_hidden.getMinutes();
                    $('.custom_hidden_field.%(id)s').val(str_date);
                });
                
                
                
                $('#%(id)s').datetimepicker({
                    value:date,
                    format:'Y-m-d H:i',
                    minDate:0,
                    minTime:0,
                });
                
                $('#%(id)s').change(); // триггерим событие на элементе вручну, чтобы сразу заполнить скрытое поле
            });
            </script>
        ''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
            'name': name,
        }
        return mark_safe(html)


class CustomDatePicker(forms.PasswordInput):
    def render(self, name, value, attrs=None, params=None):
        super().render(name, value, attrs)
        flat_attrs = flatatt(attrs)
        html = '''
            <input %(attrs)s is_datepicker name="%(name)s" type="text" value="%(value)s"/>
            
            <script type="text/javascript">
            $(document).ready(function() {
                $('[is_datepicker]').datetimepicker({
                    timepicker:false,
                    format:'Y-m-d'
                });
            });
            </script>
        ''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
            'name': name,
        }
        return mark_safe(html)