from django import forms
from django.forms import utils
import django.utils.formats
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
import datetime,time
from utils import date_convert
from django.conf import settings

calbtn = u'''<img src="{STATIC_URL}jscalendar/images/cal.png" alt="calendar" id="%s_btn"
style="cursor: pointer; width: 18px; height:18px; vertical-align:middle; float: none;" title="Select date" />
<script type="text/javascript">
    function onJalaliDateSelected(calendar, date) {
        var e = document.getElementById("%s");
        var str = calendar.date.getFullYear() + "-" + (calendar.date.getMonth() + 1) + "-" + calendar.date.getDate();
        e.value = str;
    }
    Calendar.setup({
        inputField     :    "%s_display",
        button         :    "%s_btn",
        ifFormat       :    "%s",
        dateType       :    "jalali",
        weekNumbers    :     false,
        onUpdate       :     onJalaliDateSelected
    });
</script>'''
calbtn = calbtn.replace("{STATIC_URL}", settings.STATIC_URL)

class PersianDateTimeWidget(forms.widgets.TextInput):
    class Media:
        css = {
            'all': (settings.STATIC_URL + 'jscalendar/styles/skins/calendar-system.css',)
        }
        js = (
              settings.STATIC_URL + 'jscalendar/js/jalali.js',
              settings.STATIC_URL + 'jscalendar/js/calendar.js',
              settings.STATIC_URL + 'jscalendar/js/calendar-setup.js',
              settings.STATIC_URL + 'jscalendar/js/lang/calendar-fa.js',
        )

    dformat = '%Y-%m-%d'
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            try:
                final_attrs['value'] = \
                                   force_text(value.strftime(self.dformat))
            except:
                final_attrs['value'] = \
                                   force_text(value)
        if not 'id' in final_attrs:
            final_attrs['id'] = u'%s_id' % (name)
        id = final_attrs['id']

        jsdformat = self.dformat #.replace('%', '%%')
        cal = calbtn % (id, id, id, id, jsdformat)
        parsed_atts = utils.flatatt(final_attrs)
        dat_f = date_convert.gregorian_to_jalali(value,'-')
        a = u'<span><input type="text" id="%s_display" value="%s"/><input type="hidden" %s/> %s%s</span>' % (id,dat_f, parsed_atts, self.media, cal)
        return mark_safe(a)

    def value_from_datadict(self, data, files, name):
        dtf = "%Y-%m-%d" # django.utils.formats.get_format("SHORT_DATETIME_FORMAT") wrong format for my date
        #forms.fields.DateTimeField.DEFAULT_DATETIME_INPUT_FORMATS  deprecated
        empty_values = forms.fields.EMPTY_VALUES
        value = data.get(name, None)
        if value in empty_values:
            return None
        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, datetime.date):
            return datetime.datetime(value.year, value.month, value.day)

        dst = time.strptime(value, dtf)[:6]  # date string tuple
        return datetime.datetime(dst[0],dst[1],dst[2])
        # for format in dtf:
            # try:
                # dst = time.strptime(value, format)[:6]  # date string tuple
                # return datetime.datetime(dst[0],dst[1],dst[2])
            # except ValueError:
                # continue
#            # except Exception,e:
#                # return e.message
        # return None

    def _has_changed(self, initial, data):
        '''
        Return True if data differs from initial.
        Copy of parent's method, but modify value with strftime function before final comparsion
        '''
        if data is None:
            data_value = u''
        else:
            data_value = data

        if initial is None:
            initial_value = u''
        else:
            initial_value = initial

        try:
            if force_text(initial_value.strftime(self.dformat)) != force_text(data_value.strftime(self.dformat)):
                return True
        except:
            if force_text(initial_value) != force_text(data_value):
                return True
        return False
