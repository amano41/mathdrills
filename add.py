import bisect
import itertools
import random
import sys
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm


def main():

    f = dict()
    f[1] = _make_1d_1d
    f[2] = _make_1d_1d_carrying
    f[3] = _make_2d_1d

    if len(sys.argv) == 1:
        lv = 1
    else:
        lv = int(sys.argv[1])

    eq = f[lv]()

    _save('mathdrill.pdf', eq)


def _make_1d_1d(num=20):
    """
    1 桁 + 1 桁の足し算
    """

    eq = list()
    wt = list()

    for ans in range(1, 11):
        w = 11 / (ans + 1)
        for t1 in range(0, ans + 1):
            t2 = ans - t1
            eq.append((t1, t2, ans))
            wt.append(w)

    return _sample(eq, wt, num)


def _make_1d_1d_carrying(num=20):
    """
    1 桁 + 1 桁の繰り上がりのある足し算
    """

    eq = list()
    wt = list()

    for ans in range(11, 19):
        w = 8 / (19 - ans)
        for t1 in range(ans - 9, 10):
            t2 = ans - t1
            eq.append((t1, t2, ans))
            wt.append(w)

    return _sample(eq, wt, num)


def _make_2d_1d(num=20):
    """
    2 桁 + 1 桁の足し算
    """

    eq = list()
    wt = list()

    # 一の位の足し算を作成
    for ans in range(1, 10):
        w = 10 / (ans + 1)
        for t1 in range(0, ans + 1):
            t2 = ans - t1
            eq.append((t1, t2, ans))
            wt.append(w)
    ones =  _sample(eq, wt, num)

    eq.clear()

    # 十の位を追加
    tens = [x * 10 for x in range(1, 10)]
    for t1, t2, ans, in ones:
        t1 = t1 + random.choice(tens)
        ans = t1 + t2
        eq.append((t1, t2, ans))

    return eq


def _sample(population, weights, k=1):

    result = list()

    p = population[:]
    w = weights[:]

    for i in range(k):
        n = len(p)
        r = _choice(range(n), w)
        v = p[r]
        result.append(v)
        del p[r]
        del w[r]

    return result


def _choice(sequence, weights):

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
        pdf.drawString(x2*mm, y*mm, '{0[0]:^3} + {0[1]:^3} ='.format(eq))

    pdf.showPage()
    pdf.save()


if __name__ == '__main__':
    main()
