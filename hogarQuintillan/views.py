from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render


from datetime import date, datetime
from calendar import HTMLCalendar, LocaleHTMLCalendar
import locale, re, time
# Create your views here.


def index(request):
    return render(request, "index.html")

def calendario(request, year=date.today().year, month=date.today().month):
    year = int(year)
    month = int(month)
  
    if year < 1900 or year > 2099: year = date.today().year
    try:
        #with TimeEncoding('es_ES.UTF-8'):
        #month_name = calendar.month_name[month]
        #locale.setlocale(locale.LC_ALL, 'es_ES')
        #month_name = time.strftime('%B').capitalize()
        locale.setlocale(locale.LC_TIME, 'es_ES')
        month_name = datetime.strptime(str(month), "%m").strftime("%B").capitalize()
        title = "Nuestro Calendario - %s %s" % (month_name, year)
        calendarios = []
        for i in range(month,13):
            cal = HTMLCalendar().formatmonth(year, i)
            #cal = cal.replace('<table border="0" cellpadding="0" cellspacing="0" class="month">', '<table class="table table-bordered">')
            cal = cal.replace('<table border="0" cellpadding="0" cellspacing="0" class="month">', '<table class="table table-hover table-dark tablaCalendario">')
                
            matchs = re.finditer(r'>(\d{1,2})<', cal)
            for match in matchs:
                aux = '><a href=# class="enlaceDia">%s</a><' % match.group(1)
                cal = cal.replace(match.group(0), aux)

            calendarios.append((datetime.strptime(str(i), "%m").strftime("%B").capitalize(), cal))


        context = {
            "topEnlaces": "",
            "pageTitle": title,
            "calendarios": calendarios,
            "numeroMes": 1,
            "nombreMes": month_name,
        }
        return render(request, "calendario.html", context)
    except Exception as e:
        print(e)
        raise Http404("Error inesperado en la pagina")