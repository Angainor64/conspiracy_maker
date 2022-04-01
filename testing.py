from words import read_file


def foo():
    ex = '\\xe2\\x80\\x9cRow, Row, Row Your Boat\\xe2\\x80\\x9d'
    loc = {'out': None}
    exec(f'out = b"{ex}".decode("utf-8")', globals(), loc)
    print(loc['out'])


def bar():
    i = 0
    with open('words.dat', 'rb') as f:
        while True:
            line = f.readline()
            if i != 418:
                i += 1
                continue
            break
        print(line)
        print(line.decode('utf-8'))


if __name__ == '__main__':
    foo()
