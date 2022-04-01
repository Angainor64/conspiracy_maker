def foo():
    ex = '\\xe2\\x80\\x9cRow, Row, Row Your Boat\\xe2\\x80\\x9d'
    loc = {'out': None}
    exec(f'out = b"{ex}".decode("utf-8")', globals(), loc)
    print(loc['out'])


foo()
