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
    f[4] = _make_2d_2d
    f[5] = _make_2d_1d_carrying
    f[6] = _make_2d_2d_both

    if len(sys.argv) == 1:
        lv = 1
    else:
        lv = int(sys.argv[1])

    eq = f[lv]()

    _save('mathdrill.pdf', eq)


def _make_1d_1d(num=20, zero=True):
    """
    1 桁 + 1 桁の足し算
    """

    eq = list()
    wt = list()

    if zero:
        s = 0
    else:
        s = 1

    for ans in range(s + 1, 10):
        e = ans // 2 + 1
        w = 1 / (e - s)
        for t1 in range(s, e):
            t2 = ans - t1
            eq.append((t1, t2, ans))
            wt.append(w)

    eq = _sample(eq, wt, num)
    eq = _swap_random(eq)

    return eq


def _make_1d_1d_carrying(num=20):
    """
    1 桁 + 1 桁の繰り上がりのある足し算
    """

    eq = list()
    wt = list()

    for ans in range(11, 19):
        s = ans - 9
        e = ans // 2 + 1
        w = 1 / (e - s)
        for t1 in range(s, e):
            t2 = ans - t1
            eq.append((t1, t2, ans))
            wt.append(w)

    eq = _sample(eq, wt, num)
    eq = _swap_random(eq)

    return eq


def _make_2d_1d(num=20, zero=True):
    """
    2 桁 + 1 桁の足し算
    """

    eq = list()
    wt = list()

    # 一の位の足し算を作成
    ones =  _make_1d_1d(num, zero)

    # 十の位を追加
    tens = [x * 10 for x in range(1, 10)]
    for t1, t2, ans in ones:
        t1 = t1 + random.choice(tens)
        ans = t1 + t2
        eq.append((t1, t2, ans))

    return eq


def _make_2d_2d(num=20):
    """
    2 桁 + 2 桁の足し算（十の位同士の足し算）
    """

    eq = list()

    # 十の位のペアを生成
    tens = _make_1d_1d(num, False)

    # 一の位を追加
    ones = [x for x in range(1, 10)]
    for t1, t2, ans in tens:
        t1 = t1 * 10 + random.choice(ones)
        t2 = t2 * 10
        ans = t1 + t2
        eq.append((t1, t2, ans))

    # 項をランダムに入れ替え
    eq = _swap_random(eq)

    return eq


def _make_2d_1d_carrying(num=20):
    """
    2 桁 + 1 桁の繰り上がりのある足し算
    """

    eq = list()

    # 一の位の繰り上がりのある足し算を作成
    ones = _make_1d_1d_carrying(num)

    # 十の位を追加
    # 一の位が繰り上がってくるので 8 まで
    tens = [x for x in range(1, 9)]
    for t1, t2, ans in ones:
        t1 = t1 + random.choice(tens) * 10
        ans = t1 + t2
        eq.append((t1, t2, ans))

    return eq


def _make_2d_2d_both(num=20):
    """
    2 桁 + 2 桁の足し算（一の位と十の位の両方で足し算）
    """

    eq = list()

    # 十の位
    tens = _make_1d_1d(num, False)

    # 一の位
    ones = _make_1d_1d(num, False)

    for ten, one in zip(tens, ones):
        t1 = ten[0] * 10 + one[0]
        t2 = ten[1] * 10 + one[1]
        ans = t1 + t2
        eq.append((t1, t2, ans))

    return eq


def _swap_random(equations):
    """
    項をランダムに入れ替える
    """

    eq = list()

    for t1, t2, ans in equations:
        if random.random() >= 0.5:
            t1, t2 = t2, t1
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


def _print(equations):

    for eq in equations:
        print("{} + {} = {}".format(*eq))


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
