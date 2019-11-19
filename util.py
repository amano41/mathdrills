import bisect
import itertools
import random

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def swap_random(equations):
    """
    項をランダムに入れ替える
    """

    eq = list()

    for t1, t2, ans in equations:
        if random.random() >= 0.5:
            t1, t2 = t2, t1
        eq.append((t1, t2, ans))

    return eq


def sample(population, weights, k=1):

    result = list()

    f = k // len(population) + 1
    p = population[:] * f
    w = weights[:] * f

    for i in range(k):
        n = len(p)
        r = choice(range(n), w)
        v = p[r]
        result.append(v)
        del p[r]
        del w[r]

    return result


def choice(sequence, weights):

    w = list(itertools.accumulate(weights))
    i = bisect.bisect(w, random.random() * w[-1])
    return sequence[i]


def save(filename, equations, operator):

    pdf = canvas.Canvas(filename, pagesize=landscape(A4), bottomup=False)

    fontname = 'UD Digi Kyokasho N-B'
    fontfile = '/mnt/c/Windows/Fonts/UDDigiKyokashoN-B.ttc'
    fontsize = 24
    pdfmetrics.registerFont(TTFont(fontname, fontfile))
    pdf.setFont(fontname, fontsize)

    xmargin = 20
    ymargin = 17.5

    for i, eq in enumerate(equations):
        x1 = xmargin + 128.5 * ((i // 10) % 2)
        x2 = x1 + 20
        y = ymargin + 20 * (i % 10)
        pdf.drawString(x1 * mm, y * mm, '({})'.format(i + 1))
        pdf.drawString(x2 * mm, y * mm,
                       '{0[0]:^3} {1} {0[1]:^3} ='.format(eq, operator))

    pdf.showPage()
    pdf.save()
