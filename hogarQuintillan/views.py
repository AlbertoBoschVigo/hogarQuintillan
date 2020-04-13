from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import FormRegistro
from django.contrib.auth import login, authenticate

from django.views.decorators.cache import cache_page

from datetime import date, datetime
from calendar import HTMLCalendar, LocaleHTMLCalendar
import locale, re, time, os
import logging

logger = logging.getLogger(__name__)
# Create your views here.

@cache_page(60 * 15)
def index(request):
    return render(request, "index.html")

def registro(request):
    if request.method == 'POST':
        form = FormRegistro(request.POST)
        clavePrefijada = os.getenv('CLAVE_PREFIJADA')
        if form.is_valid() and clavePrefijada == form.cleaned_data.get('claveMaestra'):
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        form = FormRegistro()
    return render(request, 'registration/registro.html', {'form': form})


@cache_page(60 * 15)
def calendario(request, year=date.today().year, month=date.today().month):
    year = int(year)
    month = int(month)
  
    if year < 1900 or year > 2099: year = date.today().year
    try:
        locale.setlocale(locale.LC_TIME, 'es')
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
        logger.error(f'Failed calendar: {e}')
        raise Http404('Failed calendar')