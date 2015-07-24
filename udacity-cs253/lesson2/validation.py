import string

months = ['January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December']
              
month_abbvs = dict((m[:3].lower(), m) for m in months)

def valid_month(month):
    if month:
        short_month =  month[:3].lower()
        return month_abbvs.get(short_month)
            
def valid_day(day):
    if day and day.isdigit():
        if int(day) > 0 and int(day) <= 31:
            return int(day)
                    
def valid_year(year):
    if year and year.isdigit():
        if int(year) >= 1900 and int(year) <= 2020:
            return int(year)
