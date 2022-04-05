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


def gen_testing():
    i = 0
    while True:
        i += 1
        yield i


def run_command(cmd):
    ['go', 'east', 'rm', 'stuff']
    allowed = ['northwest', 'east', 'north']
    match cmd.split():
        case ['exit']:
            print('quit terminal')
        case ['rm', *files]:
            for file in files:
                print(f'Removing {file}')
        case ['go', ('north', 'south', 'east', 'west') as direction]:
            print(f'Going {direction}')
        case ['go', direction] if direction in allowed:
            print(f'Going {direction}')



if __name__ == '__main__':
    a = gen_testing()
    for i in a:
        i = a.__next__()
        print(i)
