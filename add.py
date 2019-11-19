import random
import sys

from util import sample, save, swap_random


def main():

    f = dict()
    f[1] = _make_1d_1d
    f[2] = _make_1d_1d_carrying
    f[3] = _make_2d_1d
    f[4] = _make_2d_2d
    f[5] = _make_2d_1d_carrying
    f[6] = _make_2d_2d_both
    f[7] = _make_2d_2d_carrying

    if len(sys.argv) == 1:
        lv = 1
    else:
        lv = int(sys.argv[1])

    eq = f[lv]()

    save('mathdrill.pdf', eq, '+')


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

    eq = sample(eq, wt, num)
    eq = swap_random(eq)

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

    eq = sample(eq, wt, num)
    eq = swap_random(eq)

    return eq


def _make_2d_1d(num=20, zero=True):
    """
    2 桁 + 1 桁の足し算
    """

    eq = list()

    # 一の位の足し算を作成
    ones = _make_1d_1d(num, zero)

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
    eq = swap_random(eq)

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


def _make_2d_2d_carrying(num=20):
    """
    2 桁 + 2 桁の繰り上がりのある足し算
    """

    eq = list()

    # 十の位（和が 20 ～ 80 になるペア）
    tens = list()
    wt = list()

    for ans in range(2, 9):
        e = ans // 2 + 1
        w = 1 / (e - 1)
        for t1 in range(1, e):
            t2 = ans - t1
            tens.append((t1, t2, ans))
            wt.append(w)

    tens = sample(tens, wt, num)
    tens = swap_random(tens)

    # 一の位
    ones = _make_1d_1d_carrying(num)

    # 合成
    for a, b in zip(tens, ones):
        t1 = a[0] * 10 + b[0]
        t2 = a[1] * 10 + b[1]
        ans = t1 + t2
        eq.append((t1, t2, ans))

    return eq


if __name__ == '__main__':
    main()
