import sys

from util import sample, save


def main():

    f = dict()
    f[1] = _make_1d_1d

    if len(sys.argv) == 1:
        lv = 1
    else:
        lv = int(sys.argv[1])

    eq = f[lv]()

    save('mathdrill.pdf', eq, '-')


def _make_1d_1d(num=20, zero=False):
    """
    1 桁 - 1 桁の引き算
    """

    eq = list()
    wt = list()

    if zero:
        s = 0
    else:
        s = 1

    for ans in range(s, 10):
        w = 1 / (11 - ans)
        for t1 in range(ans, 11):
            t2 = t1 - ans
            eq.append((t1, t2, ans))
            wt.append(w)

    return sample(eq, wt, num)


if __name__ == '__main__':
    main()
