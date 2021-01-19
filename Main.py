from grammarParser.SLR import SLR

def read_file(filename : str):
    with open(filename, 'r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    while '' in lines:
        lines.remove('')
    return lines

def test1():
    slr1 = SLR('productions1.txt')
    s1 = read_file('test1.txt')
    for s in s1:
        if slr1.analyze(s, False) != False:
            print(s + '符合语法。')
        else:
            print(s + '不符合语法。')
    return

def test2():
    slr2 = SLR('productions2.txt')
    s2 = read_file('test2.txt')
    for s in s2:
        if slr2.analyze(s, True) != False:
            print(s + '符合语法。')
        else:
            print(s + '不符合语法。')
    return

if __name__ == '__main__':
    """
    txt文件中的每一项都需要用空格隔开。
    """
    # test1()
    test2()

    pass
