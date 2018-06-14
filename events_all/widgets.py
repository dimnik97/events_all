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
        else:
            if type(value) is not str:
                value = value.strftime("%Y-%m-%d %H:%M")

        date = str(value[0:10])
        hours = str(value[11:13])
        min = str(value[14:16])
        html = '''
<<<<<<< HEAD
            <input %(attrs)s detect_id="%(id)s" is_date is_datetimepicker type="text" value=""/>
            <input %(attrs)s detect_id="%(id)s" is_hours is_datetimepicker type="text" value=""/>
            <input %(attrs)s detect_id="%(id)s" is_min is_datetimepicker type="text" value=""/>
=======
            <input %(attrs)s id="%(id)s" is_datetimepicker type="text" value=""/>
>>>>>>> 379b4e859ea8d112d86595008c487620600bdbc7
            <input %(attrs)s is_datetimepicker name="%(name)s" type="text" value=""/>
            
            
            <script type="text/javascript">
            $(document).ready(function() {
                $input_elements = $('[detect_id="%(id)s"]');
                
                
                var user_date = SetTimeToUser_js_str("%(value)s");
                
                
                var date_in = user_date.substring(0,10),
                hours_in = user_date.substring(11,13),
                mins_in = user_date.substring(14,16);
                
                
                var date = $input_elements.filter($('[is_date]'));
                var hours = $input_elements.filter($('[is_hours]'));
                var mins = $input_elements.filter($('[is_min]'));
                
                debugger;
                date.datetimepicker({
                    value:date_in,
                    timepicker:false,
                    format:'Y-m-d',
                });
                hours.val(hours_in);
                mins.val(mins_in);
                
<<<<<<< HEAD
                
                $input_elements.on('change', function(){
                    
                    str_val = date.val() + ' ' + hours.val()+':'+mins.val();
                
                
                    $('[name ="%(name)s"]').val(SetTimeToServer(str_val));
=======
                $('#%(id)s').datetimepicker({
                    value:"%(value)s",
                    format:'Y-m-d H:i',
>>>>>>> 379b4e859ea8d112d86595008c487620600bdbc7
                });
                $('#%(id)s').on('change', function(){
                    $('[name ="%(name)s"]').val(SetTimeToServer($('#%(id)s').val()));
                });
                $('#%(id)s').change();
                
                $input_elements.change();
                
            });
            </script>
        ''' % {
            'attrs': flat_attrs,
            'id': attrs['id'],
            'value': value,
            'date': date,
            'hours': hours,
            'min': min,
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