from pathlib import Path

from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "reports" / "figures"
OUTPUT = ROOT / "reports" / "informe_ejecutivo_covid19.pdf"

PW, PH = A4
LM = 19 * mm
RM = 18 * mm
TM = 16 * mm
BM = 15 * mm
CW = PW - LM - RM

INK = HexColor("#20252B")
MUTED = HexColor("#626B73")
BLUE = HexColor("#376AA3")
SKY = HexColor("#77A6CF")
RED = HexColor("#B64A4A")
GOLD = HexColor("#B88932")
GREEN = HexColor("#387C6D")
LIGHT = HexColor("#E5E8EB")


def register_fonts():
    options = {
        "Report": ["arial.ttf", "calibri.ttf"],
        "Report-Bold": ["arialbd.ttf", "calibrib.ttf"],
        "Report-Italic": ["ariali.ttf", "calibrii.ttf"],
    }
    fonts = Path("C:/Windows/Fonts")
    for name, candidates in options.items():
        for candidate in candidates:
            path = fonts / candidate
            if path.exists():
                pdfmetrics.registerFont(TTFont(name, str(path)))
                break


register_fonts()
REG = "Report"
BOLD = "Report-Bold"
ITALIC = "Report-Italic"


def paragraph(c, text, x, y_top, width, size=9.2, color=INK, bold=False,
              italic=False, leading=None, align=TA_LEFT):
    font = ITALIC if italic else BOLD if bold else REG
    style = ParagraphStyle(
        "p",
        fontName=font,
        fontSize=size,
        leading=leading or size * 1.32,
        textColor=color,
        alignment=align,
        splitLongWords=False,
    )
    p = Paragraph(text, style)
    _, height = p.wrap(width, PH)
    p.drawOn(c, x, y_top - height)
    return height


def page_header(c, section):
    c.setFont(REG, 7)
    c.setFillColor(MUTED)
    c.drawString(LM, PH - 9 * mm, "INFORME EJECUTIVO · COVID-19 EN ESTADOS UNIDOS")
    c.drawRightString(PW - RM, PH - 9 * mm, section.upper())


def page_footer(c, number):
    c.setStrokeColor(LIGHT)
    c.setLineWidth(0.5)
    c.line(LM, 11 * mm, PW - RM, 11 * mm)
    c.setFont(REG, 6.5)
    c.setFillColor(MUTED)
    c.drawString(LM, 7.5 * mm, "Fuente: The COVID Tracking Project · Datos hasta el 7 de marzo de 2021")
    c.drawRightString(PW - RM, 7.5 * mm, str(number))


def title(c, text, subtitle=None, y=None):
    y = y or PH - 24 * mm
    h = paragraph(c, text, LM, y, CW, 17, INK, True, leading=20)
    y -= h + 2.5 * mm
    if subtitle:
        h2 = paragraph(c, subtitle, LM, y, CW, 8.5, MUTED, leading=11)
        y -= h2 + 4 * mm
    c.setStrokeColor(LIGHT)
    c.line(LM, y, PW - RM, y)
    return y - 5 * mm


def small_heading(c, text, y):
    c.setFont(BOLD, 9)
    c.setFillColor(INK)
    c.drawString(LM, y, text)
    return y - 5 * mm


def note(c, text, y, color=BLUE):
    c.setStrokeColor(color)
    c.setLineWidth(2)
    c.line(LM, y, LM, y - 15 * mm)
    h = paragraph(c, text, LM + 4 * mm, y, CW - 4 * mm, 9.1, INK, leading=12)
    return min(y - h - 4 * mm, y - 17 * mm)


def bullet(c, lead, detail, y, size=8.7):
    c.setFillColor(BLUE)
    c.circle(LM + 1.5 * mm, y - 2.1 * mm, 0.8 * mm, fill=1, stroke=0)
    h = paragraph(
        c,
        f"<b>{lead}</b> {detail}",
        LM + 5 * mm,
        y,
        CW - 5 * mm,
        size,
        INK,
        leading=size * 1.35,
    )
    return y - h - 3 * mm


def draw_image(c, filename, x, y_top, width, height):
    c.drawImage(
        str(FIG / filename),
        x,
        y_top - height,
        width=width,
        height=height,
        preserveAspectRatio=True,
        anchor="c",
        mask="auto",
    )


def caption(c, text, y):
    return y - paragraph(c, text, LM, y, CW, 6.7, MUTED, italic=True,
                         align=TA_CENTER, leading=8.5) - 3 * mm


def cover(c):
    c.setFillColor(white)
    c.rect(0, 0, PW, PH, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(0, PH - 5 * mm, PW, 5 * mm, fill=1, stroke=0)
    c.setFont(BOLD, 8)
    c.setFillColor(BLUE)
    c.drawString(LM, PH - 30 * mm, "INFORME EJECUTIVO")
    paragraph(
        c,
        "La pandemia en datos:<br/>una historia de presión, desigualdad y aprendizaje",
        LM,
        PH - 48 * mm,
        CW,
        25,
        INK,
        True,
        leading=29,
    )
    paragraph(
        c,
        "Análisis exploratorio del COVID-19 en Estados Unidos",
        LM,
        PH - 83 * mm,
        CW,
        13,
        BLUE,
        leading=16,
    )
    c.setStrokeColor(BLUE)
    c.setLineWidth(1)
    c.line(LM, PH - 101 * mm, LM + 34 * mm, PH - 101 * mm)
    paragraph(
        c,
        "El invierno de 2020-2021 reunió los máximos nacionales de casos, "
        "hospitalización y mortalidad. Sin embargo, los totales nacionales "
        "ocultan diferencias profundas entre estados y limitaciones importantes "
        "en la calidad del reporte.",
        LM,
        PH - 111 * mm,
        125 * mm,
        11.5,
        INK,
        leading=16,
    )
    c.setFont(REG, 8)
    c.setFillColor(MUTED)
    c.drawString(LM, 37 * mm, "Periodo analizado")
    c.setFont(BOLD, 10)
    c.setFillColor(INK)
    c.drawString(LM, 31 * mm, "13 de enero de 2020 — 7 de marzo de 2021")
    c.setFont(REG, 8)
    c.setFillColor(MUTED)
    c.drawString(LM, 24 * mm, "20.780 registros · 56 jurisdicciones · 41 variables")
    c.drawRightString(PW - RM, 24 * mm, "Miguel Redondo · Junio 2026")


def page_context(c):
    page_header(c, "Contexto")
    y = title(c, "Antes de interpretar, entender qué estamos midiendo")
    h = paragraph(
        c,
        "The COVID Tracking Project reunió diariamente información publicada por "
        "estados y territorios estadounidenses hasta marzo de 2021. El análisis "
        "trabaja con 20.780 observaciones y combina indicadores acumulados, "
        "incrementos diarios y variables de presión hospitalaria.",
        LM, y, CW, 10, INK, leading=14,
    )
    y -= h + 7 * mm
    y = small_heading(c, "Preguntas que guían el análisis", y)
    for lead, detail in [
        ("Evolución", "¿Cuándo se alcanzaron los momentos de máxima presión?"),
        ("Relaciones", "¿Cómo se vinculan casos, pruebas, hospitalizaciones y fallecimientos?"),
        ("Territorio", "¿Cambian las conclusiones al ajustar los datos por población?"),
        ("Calidad", "¿Qué variables permiten comparaciones fiables y cuáles exigen cautela?"),
    ]:
        y = bullet(c, lead, detail, y)
    y -= 3 * mm
    y = small_heading(c, "Una decisión metodológica clave", y)
    y = note(
        c,
        "<b>Ausencia no significa cero.</b> Cuando ninguna jurisdicción reportó "
        "hospitalizaciones, el dato se mantuvo como ausente. Además, las correcciones "
        "negativas se conservaron para garantizar trazabilidad.",
        y,
        GREEN,
    )
    y -= 3 * mm
    paragraph(
        c,
        "Se emplearon medias móviles de siete días para reducir el efecto de retrasos "
        "semanales y se calculó correlación de Spearman, más robusta ante distribuciones "
        "asimétricas y valores extremos.",
        LM, y, CW, 9, MUTED, italic=True, leading=12,
    )
    page_footer(c, 2)


def page_quality(c):
    page_header(c, "Calidad de datos")
    y = title(
        c,
        "La cobertura es suficiente para la historia principal, pero no para todas las variables",
    )
    draw_image(c, "cobertura_variables.png", LM, y, CW, 104 * mm)
    y -= 106 * mm
    y = caption(
        c,
        "Cobertura de las veinte variables con más información disponible.",
        y,
    )
    y = note(
        c,
        "<b>Casos, fallecimientos y pruebas superan el 95 % de cobertura.</b> "
        "Hospitalizaciones actuales alcanzan el 83,4 %, mientras que UCI y "
        "ventilación quedan por debajo del nivel necesario para comparaciones generales.",
        y,
        GOLD,
    )
    paragraph(
        c,
        "La selección de indicadores no responde únicamente a su interés, sino a su "
        "capacidad para sostener conclusiones comparables entre jurisdicciones.",
        LM, y, CW, 8.7, MUTED, italic=True, leading=11,
    )
    page_footer(c, 3)


def page_reporting(c):
    page_header(c, "Calidad de datos")
    y = title(c, "El sistema de reporte maduró durante la pandemia")
    draw_image(c, "cobertura_hospitalizaciones_tiempo.png", LM, y, CW, 83 * mm)
    y -= 86 * mm
    y = caption(
        c,
        "Número diario de jurisdicciones con información de hospitalización disponible.",
        y,
    )
    y = small_heading(c, "Las correcciones forman parte de la historia del dato", y)
    h = paragraph(
        c,
        "Se detectaron <b>141 registros</b> con algún incremento negativo en casos, "
        "fallecimientos o pruebas. Son revisiones retrospectivas: eliminación de "
        "duplicados, reclasificaciones o cambios de criterio.",
        LM, y, CW, 9.5, INK, leading=13,
    )
    y -= h + 5 * mm
    draw_image(c, "boxplots_incrementos_diarios.png", LM, y, CW, 58 * mm)
    y -= 61 * mm
    paragraph(
        c,
        "Los valores extremos no se eliminaron automáticamente. Algunos representan "
        "picos epidemiológicos reales y otros evidencian ajustes administrativos.",
        LM, y, CW, 8.6, MUTED, italic=True, leading=11,
    )
    page_footer(c, 4)


def page_waves(c):
    page_header(c, "Evolución nacional")
    y = title(c, "Tres olas y un invierno que desbordó la escala")
    draw_image(c, "evolucion_mensual.png", LM, y, CW, 126 * mm)
    y -= 130 * mm
    y = note(
        c,
        "La agregación mensual distingue una primera ola en primavera, un repunte "
        "estival y una ola invernal muy superior. <b>Enero de 2021 concentra el mayor "
        "impacto conjunto.</b>",
        y,
        BLUE,
    )
    paragraph(
        c,
        "El análisis mensual reduce el ruido del calendario de notificación y permite "
        "comparar la magnitud relativa de cada etapa.",
        LM, y, CW, 8.6, MUTED, italic=True, leading=11,
    )
    page_footer(c, 5)


def page_peaks(c):
    page_header(c, "Evolución nacional")
    y = title(c, "La presión máxima se concentró en apenas ocho días")
    half = (CW - 6 * mm) / 2
    draw_image(c, "evolucion_casos_usa.png", LM, y, half, 75 * mm)
    draw_image(c, "evolucion_fallecimientos_usa.png", LM + half + 6 * mm, y, half, 75 * mm)
    y -= 79 * mm
    y = caption(
        c,
        "Casos y fallecimientos diarios con media móvil de siete días.",
        y,
    )
    draw_image(c, "evolucion_hospitalizaciones_usa.png", LM, y, CW, 76 * mm)
    y -= 79 * mm
    y = note(
        c,
        "<b>6 de enero:</b> 132.474 hospitalizados. &nbsp;&nbsp; "
        "<b>11 de enero:</b> 247.111 casos diarios. &nbsp;&nbsp; "
        "<b>13 de enero:</b> 3.335 fallecimientos diarios.",
        y,
        RED,
    )
    page_footer(c, 6)


def page_distributions(c):
    page_header(c, "Distribuciones")
    y = title(c, "Los días normales fueron muy distintos de los días críticos")
    draw_image(c, "distribucion_casos_fallecimientos.png", LM, y, CW, 93 * mm)
    y -= 97 * mm
    y = caption(c, "Distribución de incrementos nacionales diarios no negativos.", y)
    h = paragraph(
        c,
        "Las distribuciones están sesgadas hacia la derecha: la mayoría de los días "
        "se concentra en niveles moderados, mientras un grupo reducido de jornadas "
        "alcanza cifras excepcionalmente altas.",
        LM, y, CW, 9.5, INK, leading=13,
    )
    y -= h + 5 * mm
    y = small_heading(c, "Por qué importa", y)
    y = bullet(
        c,
        "Media frente a mediana.",
        "La media queda arrastrada por las grandes olas y no representa un día típico.",
        y,
    )
    y = bullet(
        c,
        "Outliers con significado.",
        "Los extremos pueden ser episodios epidemiológicos reales, no errores descartables.",
        y,
    )
    bullet(
        c,
        "Lectura ejecutiva.",
        "Los promedios del periodo completo ocultan la intensidad de las fases críticas.",
        y,
    )
    page_footer(c, 7)


def page_testing(c):
    page_header(c, "Pruebas y detección")
    y = title(c, "Más pruebas explican parte del crecimiento, pero no toda la historia")
    draw_image(c, "pruebas_positividad.png", LM, y, CW, 124 * mm)
    y -= 128 * mm
    y = note(
        c,
        "La capacidad diagnóstica aumentó de forma sostenida, pero la positividad "
        "también volvió a elevarse durante las grandes olas. El crecimiento de casos "
        "no puede atribuirse únicamente a que se realizaron más pruebas.",
        y,
        GOLD,
    )
    paragraph(
        c,
        "La tasa es aproximada: los estados no utilizaron siempre la misma unidad "
        "de reporte para pruebas, resultados y personas examinadas.",
        LM, y, CW, 8.5, MUTED, italic=True, leading=11,
    )
    page_footer(c, 8)


def page_relationships(c):
    page_header(c, "Relaciones estadísticas")
    y = title(c, "Los indicadores se mueven juntos, aunque no al mismo tiempo")
    half = (CW - 6 * mm) / 2
    draw_image(c, "matriz_correlacion.png", LM, y, half, 86 * mm)
    draw_image(c, "relaciones_bivariantes.png", LM + half + 6 * mm, y, half, 86 * mm)
    y -= 90 * mm
    y = caption(
        c,
        "Correlaciones de Spearman y relaciones entre casos, hospitalización y pruebas.",
        y,
    )
    h = paragraph(
        c,
        "Casos, hospitalizaciones y fallecimientos presentan asociaciones positivas. "
        "Las pruebas también se relacionan con los casos detectados, pero la "
        "positividad demuestra que la transmisión tuvo un papel propio.",
        LM, y, CW, 9.3, INK, leading=13,
    )
    y -= h + 5 * mm
    draw_image(c, "correlacion_desfase_casos_muertes.png", LM, y, CW, 58 * mm)
    y -= 61 * mm
    paragraph(
        c,
        "La asociación más alta aparece al desplazar los fallecimientos "
        "<b>16 días</b> respecto a los casos, con una correlación de <b>0,798</b>. "
        "Es una relación agregada, no un plazo clínico individual.",
        LM, y, CW, 8.8, MUTED, italic=True, leading=11.5,
    )
    page_footer(c, 9)


def page_states(c):
    page_header(c, "Territorio")
    y = title(c, "La cifra nacional oculta epidemias estatales diferentes")
    draw_image(c, "evolucion_top_5_estados.png", LM, y, CW, 117 * mm)
    y -= 121 * mm
    y = note(
        c,
        "California, Texas, Florida, Nueva York e Illinois no alcanzaron sus repuntes "
        "previos con la misma sincronía ni intensidad. La ola invernal terminó "
        "alineando las curvas, pero la trayectoria anterior fue heterogénea.",
        y,
        GREEN,
    )
    y = small_heading(c, "Implicación para dirección", y)
    paragraph(
        c,
        "Las decisiones territoriales no deberían basarse únicamente en el agregado "
        "nacional. La misma política puede llegar tarde a un estado y demasiado "
        "pronto a otro.",
        LM, y, CW, 9, INK, leading=12,
    )
    page_footer(c, 10)


def page_rankings(c):
    page_header(c, "Territorio")
    y = title(c, "El ranking cambia cuando dejamos de contar personas y medimos tasas")
    half = (CW - 6 * mm) / 2
    draw_image(c, "top_10_estados_casos.png", LM, y, half, 75 * mm)
    draw_image(c, "top_10_estados_fallecimientos.png", LM + half + 6 * mm, y, half, 75 * mm)
    y -= 78 * mm
    y = caption(c, "Rankings absolutos al final del periodo.", y)
    draw_image(c, "ranking_estados_por_100k.png", LM, y, CW, 96 * mm)
    y -= 99 * mm
    y = note(
        c,
        "<b>Volumen absoluto:</b> California y Texas lideran. "
        "<b>Casos por 100.000 habitantes:</b> Dakota del Norte y Dakota del Sur. "
        "<b>Mortalidad por 100.000:</b> Nueva Jersey y Massachusetts.",
        y,
        RED,
    )
    page_footer(c, 11)


def page_conclusions(c):
    page_header(c, "Conclusiones")
    y = title(c, "Lo que la historia de los datos deja para la toma de decisiones")
    conclusions = [
        ("1", "La ola invernal fue el punto de máxima presión.",
         "Hospitalizaciones, casos y fallecimientos alcanzaron máximos nacionales en ocho días."),
        ("2", "El dato requiere contexto antes de convertirse en mensaje.",
         "Ausencias, cambios de definición y 141 correcciones negativas condicionan la lectura diaria."),
        ("3", "Casos y mortalidad están relacionados en el tiempo.",
         "El máximo de asociación aparece con un desfase aproximado de 16 días."),
        ("4", "Más diagnóstico no explica por sí solo las grandes olas.",
         "La positividad aumentó al mismo tiempo que los casos durante los periodos críticos."),
        ("5", "El tamaño del estado cambia el ranking.",
         "Los totales favorecen a los territorios más poblados; las tasas revelan otra geografía del impacto."),
        ("6", "La respuesta debe combinar escalas.",
         "La tendencia nacional es útil para dirección, pero la acción necesita seguimiento estatal."),
    ]
    for number, lead, detail in conclusions:
        c.setFont(BOLD, 14)
        c.setFillColor(BLUE)
        c.drawString(LM, y - 1 * mm, number)
        h = paragraph(
            c,
            f"<b>{lead}</b><br/>{detail}",
            LM + 10 * mm,
            y,
            CW - 10 * mm,
            9.5,
            INK,
            leading=13,
        )
        y -= max(h + 6 * mm, 22 * mm)
    c.setStrokeColor(LIGHT)
    c.line(LM, y, PW - RM, y)
    y -= 7 * mm
    paragraph(
        c,
        "<b>Siguiente paso recomendado:</b> convertir este análisis en un cuadro "
        "ejecutivo reproducible con tasas por población, alertas de cobertura y "
        "anotaciones de revisiones administrativas.",
        LM, y, CW, 10, INK, leading=14,
    )
    page_footer(c, 12)


def build():
    canvas = Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    canvas.setTitle("Informe ejecutivo COVID-19 en Estados Unidos")
    canvas.setAuthor("Miguel Redondo")
    pages = [
        cover,
        page_context,
        page_quality,
        page_reporting,
        page_waves,
        page_peaks,
        page_distributions,
        page_testing,
        page_relationships,
        page_states,
        page_rankings,
        page_conclusions,
    ]
    for index, page in enumerate(pages):
        page(canvas)
        if index < len(pages) - 1:
            canvas.showPage()
    canvas.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
