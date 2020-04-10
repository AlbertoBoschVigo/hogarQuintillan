from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render


from datetime import date, datetime
from calendar import HTMLCalendar, LocaleHTMLCalendar
import locale, re, time
# Create your views here.


def index(request):
    return HttpResponse('Activo')

def tareas(request):
    cpt= 'COMPLETADA'
    pdt = ""
    lc = "LENGUA CASTELLANA"
    lg = "LINGUA GALEGA"
    mt = "MATEMATICAS"
    cn = "CIENCIAS NATURAIS"
    cs = "CIENCIAS SOCIAIS"
    pl = "PLÁSTICA"
    ing = "INGLÉS"
    context = {
        "asignaturas":{
            lc:{
                "RIMAS": [["LC_RIMAS.pdf",cpt]],
                "LIBRO": [["2_CLASES DE SÍLABAS_SONIDO J.pdf",cpt]],
                "PRESENTAR A ALGUIEN": [["1_LC_presentar_a_alguien.pdf",cpt]],
                "EL SUSTANTIVO": [["EL_SUSTANTIVO.pdf",cpt]],
                "COMPETENCIA LECTORA": [("COMPETENCIA_LECTORA.pdf",cpt)],
                "ACTIVIDAD DE ESCRITURA": [["mejoro_mi_escritura.pdf",cpt]],
                "ACTIVIDADES DE REPASO":[["Actividades de repaso.pdf",cpt]],
                "Algo de ortografía":[["sinonima_antonima.pdf", cpt], ["sonido_r_fuerte.pdf", cpt]],
                "Escribir una receta":[["ESCRIBIR_UNA_RECETA.pdf", cpt]]
            },
            lg:{
                "REALIZA UN FOLLETO INFORMATIVO": [["LG_ELABORA_UN_FOLLETO_INFORMATIVO.pdf", cpt]],
                "LIBRO" : [["Rapida a tartaruga.pdf", cpt]],
                "LIBRO :SUBSTANTIVOS" : [["3_LG_SUBSTANTIVOS.pdf", cpt]],
                "DIA DA POESÍA" : [["3_LG_DIA DA POESÍA.pdf", cpt]],
                "HORA DE LECTURA" : [["HORA DE LECTURA.pdf", cpt]],
                "COMPRENSIÓN LECTORA" : [["comprendo_un_poema.pdf", cpt]],
                "ACTIVIDADES DE REPASO" : [["Actividades de repaso_lg.pdf", cpt]],
                "Repaso ortografía" : [["aprendo_mais.pdf", cpt], ["signos_interrogacion_admiracion.pdf", cpt]],
                "Repaso de gramática e ortografía" : [["SILABAS_LG.pdf", pdt], ["SUBSTANTIVOS_LG.pdf", pdt], ["substantivos_interrogacion_admircion.pdf", pdt]],
                "HAMBURGUESA, BOCADILLOS E ROSQUILLAS":[["HAMBURGUESA_BOCADILLOS_ROSQUILLAS.pdf", pdt]],
            },
            mt:{
                "REPASO":[["mat_ep3_REPASO.pdf", cpt]],
                "Calculo mental":[["Cálculo mental.pdf", cpt]],
                "JUEGOS Y RETOS DE CÁLCULO Y PROBLEMAS":[["MAT_2.pdf", cpt]],
                "DIVISIÓN":[["3_MATEMATICAS_REPASO_DIVISION.pdf", cpt], ["4_MATE_REPASO DIVISION.pdf", cpt]],
                "CÁLCULO MULTIPLICACIÓNS":[["CALCULO_MULTIPLICACIONES.pdf", cpt]],
                "PROBLEMAS":[["problemas.pdf", cpt]],
                "MITAD, TERCIO Y CUARTO":[["mitad_tercio_cuarto.pdf", pdt]],
                "Repaso":[["repaso_numeros.pdf", pdt]],
                "Repaso division":[["reparto_division_exacta.pdf", pdt]],
                "JUEGOS Y ACERTIJOS" : [["ACERTIJOS.pdf", pdt], ["juegos_1.pdf", pdt]],
                "NÚMEROS Y OPERACIONES" : [["numeros_operaciones.pdf", pdt]],
                "MULTIPLICACIÓN Y DIVISIÓN" : [["multiplicacion_division.pdf", pdt]],
            },
            cn:{
                "Tema3_SOMO DISTINTOS DOUTROS ANIMAIS" : [["t3_cn.pdf", cpt]],
                "QUEDA NA CASA" : [["3_CN_QUEDANACASA.pdf", cpt]],
                "O NOSO LABORATORIO" : [["O noso laboratorio.pdf", cpt]],
                "ES VIERNES!!" : [["ES VIERNES.pdf", cpt]],        
                "O NOSO CORPO" : [["O_NOSO_CORPO.pdf", cpt], ["cn_ep3_48_49_etiquetar.pdf", cpt], ["cn_ep3_50_51_etiquetar.pdf", cpt]],    
            },
            cs:{
                "Construir unha andavía" : [["cs_construir_unhaandavía.pdf", cpt]],
                "CONSTRÚE UN FÓSIL NA CASA" : [["FÓSILES.pdf", cpt]],
                "O NOSO LABORATORIO" : [["3_Experimentos con auga.pdf", cpt]],
                "CICLO DA AUGA" : [["ciclo_d_auga.pdf", cpt]],
                "A auga" : [["BOYAN SLAT. MISIÓN SALVAR O OCÉANO.pdf", cpt], ["ciclo_auga_paisaxes.pdf", cpt]],
                "LLUVIAS EXTRAÑAS":[["LLUVIAS_EXTRAÑAS.pdf", cpt]],
            },
            pl:{
                "Colores fríos y cálidos" : [["Los colores fríos y cálidos.pdf", cpt]],
                "CAMPO DE FLORES" : [["CAMPO DE FLORES.pdf", cpt]],
                "FAI O TEU RETRATO" : [["Fai o teu propio retrato.doc", cpt]],
                "LEOPOLDO NÓVOA" : [["Orixinal_ou_copia_LEOPOLDO_NOVOA.pdf", cpt], ["Pinta-con-LEOPOLDO_NOVOA.pdf", cpt]],
                "COLLAGE CON MATISSE": [["A_CAIDA_DE_ICARO_MATISSE.pdf", pdt]]
            },
            ing:{
                "Proposta de traballo para a semana do 30 de marzo ao 3 de abril" : [["Traballos 3º semana do 30 m ao 3 a.docx", cpt], ["Extension worksheet 2- Unit 6.pdf", cpt]],
                "Vídeos, xogos e máis." : [["ACTIVIDAD", cpt]],
                "STORY TIME: THE GRUFFALO" : [["ACTIVIDADES THE GRUFFALO", cpt]],
                "WHAT IS JESSIE DOING?" : [["ACTIVIDAD", cpt]],
                "STORY TIME: MR CROCODILE'S TOOTHBRUSH" : [["ACTIVIDADES MR CROCODILE", cpt]],
                "Inspector Clouseau sketch":  [["ACTIVIDAD", cpt]],
                "STORY TIME: PEACE AT LAST" : [["ACTIVIDADES PEACE AT LAST", cpt]],
            }          
        }
    }
    return render(request, "veraPage/tareasVera.html", context)

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
        title = "Vera's Calendar - %s %s" % (month_name, year)
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
            'usuario':str(request.user),
            "columnaEstrecha": False,
            "calendarios": calendarios,
            "numeroMes": 1,
            "nombreMes": month_name,
        }
        return render(request, "veraPage/calendario.html", context)
    except Exception as e:
        print(e)
        raise Http404("Error inesperado en la pagina")