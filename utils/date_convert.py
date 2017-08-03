from datetime import datetime, date, time
from .calverter import calverter
def jalali_to_gregorian(dat_str):
    '''
    Gets date in (char(8)) (or / delimited) (or char(10) / delimited)
    returns Date
    returns None on error
    '''
    cal = calverter()
    try:
        year = None
        month = None
        day = None
        if len(dat_str) == 8:
            year = dat_str[0:4]
            month = dat_str[4:6]
            day = dat_str[6:8]
        elif len(dat_str) == 10:
            year = dat_str[0:4]
            month = dat_str[5:7]
            day = dat_str[8:10]
        else:
            splited = dat_str.split('/')
            year = splited[0]
            month = splited[1]
            day = splited[2]
        if not year.isdigit(): return None
        if not month.isdigit(): return None
        if not day.isdigit(): return None
        jd = cal.jalali_to_jd(int(year),int(month),int(day))
        dat_tuple = cal.jd_to_gregorian(jd)
        return date(dat_tuple[0],dat_tuple[1],dat_tuple[2])
    except (Exception,msg):
        # print msg
        return None

def gregorian_to_jalali(date,sep='/'):
    '''
    Gets georgian date
    returns persian date in char(10) (/ separated)
    '''
    if date == '' or date == None: return ''
    cal = calverter()
    date_str = str(date)
    year = date_str[0:4]
    month = date_str[5:7]
    day = date_str[8:10]
    jd = cal.gregorian_to_jd(int(year),int(month),int(day))
    dat_tuple = cal.jd_to_jalali(jd)
    format = "%s"+sep+"%s"+sep+"%s"
    return format %(str(dat_tuple[0]).rjust(4,'0'),str(dat_tuple[1]).rjust(2,'0'),str(dat_tuple[2]).rjust(2,'0'))


def jalali_today():
    date = datetime.now().date()
    return gregorian_to_jalali(date)

def jalali_weekday(date):
    day = date.weekday()
    if day == 0: return 'دوشنبه'
    if day == 1: return 'سه شنبه'
    if day == 2: return 'چهارشنبه'
    if day == 3: return 'پنج شنبه'
    if day == 4: return 'جمعه'
    if day == 5: return 'شنبه'
    if day == 6: return 'یکشنبه'
