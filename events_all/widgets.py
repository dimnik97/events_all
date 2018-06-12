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
            <input %(attrs)s id="%(id)s" is_datetimepicker type="text" value=""/>
            <input %(attrs)s is_datetimepicker name="%(name)s" type="text" value=""/>
            
            
            <script type="text/javascript">
            $(document).ready(function() {
                
                
                $('#%(id)s').datetimepicker({
                    value:"%(value)s",
                    format:'Y-m-d H:i',
                });
                $('#%(id)s').on('change', function(){
                    $('[name ="%(name)s"]').val(SetTimeToServer($('#%(id)s').val()));
                });
                $('#%(id)s').change();
                
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