from blockstream import *
import scipy as sp
import time

TET = 0
UID = 1
TF = 20
NC = 4
TEMP = sp.array(
    [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    for i in xrange(NC)], dtype=sp.float32
).T
FILT = -TEMP
BLOCK = BS3SortDataBlock([(TET, UID, 2, 3, 4, 5), (TET, UID, 2, 3, 4, 5)])
BLOCK_BYTES = BLOCK.payload()
BLOCK_LEN = len(BLOCK_BYTES)

if __name__ == '__main__':
    LIB = load_blockstream('test')
    print 'got lib:', LIB, 'APPNAME:', get_appname()
    WID = LIB.startWriter('pyTestSortWriter', 'SORT')
    print "returned: WID = LIB.startWriter('pyTestSortWriter', 'SORT')"
    PREAMBLE = BS3SortSetupBlock([
        [TET, NC, TF, 0, sp.eye(TF * NC, dtype=sp.float32),
            [(1, FILT, TEMP, 1.0, 1, 0, 0)]]
    ])
    LIB.setPreamble(WID, PREAMBLE.BLOCK_CODE, PREAMBLE.payload(),
                    len(PREAMBLE))
    try:
    #        for i in xrange(100000):
        while True:
            LIB.sendBlock(WID, BLOCK.BLOCK_CODE, BLOCK_BYTES, BLOCK_LEN)
            print '.',
            time.sleep(0.5)
    except Exception, ex:
        print ex
    finally:
        LIB.finalizeAll()
        print 'exit!'
