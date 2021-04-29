def getlibs(extdir, makeFlags):
    flags = ''
    pythonLibPaths = [
        p for p in makeFlags['PYTHONLIBS'].split() if p.startswith('-L')
    ]
    for p in pythonLibPaths:
        flags += ' -Wl,-rpath,' + p.replace('-L', '') + ' '
    flags += '-L' + extdir + ' -lkorali -Wl,-rpath,' + extdir + ' '
    flags += '-L' + makeFlags['GSLPREFIX'] + '/lib -Wl,-rpath,' + makeFlags['GSLPREFIX'] + '/lib '
    flags += ' ' + makeFlags['ONEDNNLIBS']
    flags += ' ' + makeFlags['CUDNNLIBS']
    flags += ' ' + makeFlags['LIBGPLIBS']
    flags += ' ' + makeFlags['RTNORMLIBS']
    flags += ' ' + makeFlags['LIBCOLIBS']
    print(flags + ' ' + makeFlags['GSLLIBS'] + ' ' + makeFlags['PYTHONLIBS'])

