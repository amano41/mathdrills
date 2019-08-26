import bisect
import itertools
import random
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm


def main():

    eq = _make()
    _save('mathdrill.pdf', eq)


def _make(num=20):

    eq = list()
    wt = list()

    for ans in range(1, 11):
        w = 10 / (ans + 1)
        for t1 in range(0, ans + 1):
            t2 = ans - t1
            eq.append((ans, t1, t2))
            wt.append(w)

    result = list()

    for i in range(num):
        n = len(eq)
        r = _sample(range(n), wt)
        v = eq[r]
        result.append(v)
        del eq[r]
        del wt[r]

    return result


def _sample(sequence, weights):

    w = list(itertools.accumulate(weights))
    i = bisect.bisect(w, random.random() * w[-1])
    return sequence[i]


def _save(filename, equations):

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
        pdf.drawString(x1*mm, y*mm, '({})'.format(i+1))
        pdf.drawString(x2*mm, y*mm, '{0[1]:^3} + {0[2]:^3} ='.format(eq))

    pdf.showPage()
    pdf.save()


if __name__ == '__main__':
    main()
