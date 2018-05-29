from django import forms
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe


class CustomDateTimePicker(forms.PasswordInput):
    def render(self, name, value, attrs=None, params=None):
        super().render(name, value, attrs)
        flat_attrs = flatatt(attrs)

        html = '''
            <input %(attrs)s is_datetimepicker name="%(name)s" type="text" value="%(value)s"/>
            
            <script type="text/javascript">
            $(document).ready(function() {
            
                var val = "%(value)s";
                if(val == "None"){
                    var currentdate = new Date(); 
                    var datetime =  currentdate.getFullYear() + "-"
                                + (currentdate.getMonth()+1)  + "-" 
                                + currentdate.getDate() + " "  
                                + currentdate.getHours() + ":"  
                                + currentdate.getMinutes()
                    $('[is_datetimepicker]').attr('value', datetime);           
                }
            
                $('[is_datetimepicker]').datetimepicker({
                    format:'Y-m-d H:i',
                    minDate:0,
                    minTime:0,
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