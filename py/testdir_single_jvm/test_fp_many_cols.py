import unittest
import random, sys, time, os
sys.path.extend(['.','..','py'])

import h2o, h2o_cmd, h2o_hosts, h2o_browse as h2b, h2o_import as h2i, h2o_exec as h2e

print "Stress the # of cols with fp reals here." 
print "Can pick fp format but will start with just the first (e0)"
def write_syn_dataset(csvPathname, rowCount, colCount, SEEDPERFILE, sel):
    # we can do all sorts of methods off the r object
    r = random.Random(SEEDPERFILE)

    def e0(val): return "%e" % val
    def e1(val): return "%20e" % val
    def e2(val): return "%-20e" % val
    def e3(val): return "%020e" % val
    def e4(val): return "%+e" % val
    def e5(val): return "%+20e" % val
    def e6(val): return "%+-20e" % val
    def e7(val): return "%+020e" % val
    def e8(val): return "%.4e" % val
    def e9(val): return "%20.4e" % val
    def e10(val): return "%-20.4e" % val
    def e11(val): return "%020.4e" % val
    def e12(val): return "%+.4e" % val
    def e13(val): return "%+20.4e" % val
    def e14(val): return "%+-20.4e" % val
    def e15(val): return "%+020.4e" % val

    def f0(val): return "%f" % val
    def f1(val): return "%20f" % val
    def f2(val): return "%-20f" % val
    def f3(val): return "%020f" % val
    def f4(val): return "%+f" % val
    def f5(val): return "%+20f" % val
    def f6(val): return "%+-20f" % val
    def f7(val): return "%+020f" % val
    def f8(val): return "%.4f" % val
    def f9(val): return "%20.4f" % val
    def f10(val): return "%-20.4f" % val
    def f11(val): return "%020.4f" % val
    def f12(val): return "%+.4f" % val
    def f13(val): return "%+20.4f" % val
    def f14(val): return "%+-20.4f" % val
    def f15(val): return "%+020.4f" % val

    def g0(val): return "%g" % val
    def g1(val): return "%20g" % val
    def g2(val): return "%-20g" % val
    def g3(val): return "%020g" % val
    def g4(val): return "%+g" % val
    def g5(val): return "%+20g" % val
    def g6(val): return "%+-20g" % val
    def g7(val): return "%+020g" % val
    def g8(val): return "%.4g" % val
    def g9(val): return "%20.4g" % val
    def g10(val): return "%-20.4g" % val
    def g11(val): return "%020.4g" % val
    def g12(val): return "%+.4g" % val
    def g13(val): return "%+20.4g" % val
    def g14(val): return "%+-20.4g" % val
    def g15(val): return "%+020.4g" % val

    # try a neat way to use a dictionary to case select functions
    # didn't want to use python advanced string format with variable as format
    # because they do left/right align outside of that??
    caseList=[
        e0, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15,
        f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15,
        g0, g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14, g15,
        ]

    if sel<0 or sel>=len(caseList):
        raise Exception("sel out of range in write_syn_dataset:", sel)
    f = caseList[sel]

    ## MIN = -1e20
    ## MAX = 1e20
    # okay to use the same value across the whole dataset?
    ## val = r.uniform(MIN,MAX)
    val = r.triangular(-1e9,1e9,0)

    dsf = open(csvPathname, "w+")
    for i in range(rowCount):
        rowData = []
        for j in range(colCount):
            rowData.append(f(val)) # f should always return string
        rowDataCsv = ",".join(rowData)
        dsf.write(rowDataCsv + "\n")
    dsf.close()

class Basic(unittest.TestCase):
    def tearDown(self):
        h2o.check_sandbox_for_errors()

    @classmethod
    def setUpClass(cls):
        localhost = h2o.decide_if_localhost()
        if (localhost):
            h2o.build_cloud(1,java_heap_GB=14)
        else:
            h2o_hosts.build_cloud_with_hosts()

    @classmethod
    def tearDownClass(cls):
        h2o.tear_down_cloud()

    def test_many_cols_and_values_with_syn(self):
        SEED = random.randint(0, sys.maxint)
        SEED = 1967029306372214551
        print "\nUsing random seed:", SEED
        random.seed(SEED)
        SYNDATASETS_DIR = h2o.make_syn_dir()
        tryList = [
            (100, 10000, 'cA', 30, 120),
            (100, 30000, 'cB', 30, 120),
            (100, 50000, 'cC', 30, 120),
            (100, 70000, 'cD', 30, 120),
            (100, 90000, 'cE', 30, 120),
            (100, 100000, 'cF', 30, 120),
            (100, 200000, 'cG', 30, 120),
            (100, 300000, 'cH', 30, 120),
            (100, 400000, 'cI', 30, 120),
            (100, 500000, 'cJ', 30, 120),
            (100, 600000, 'cK', 30, 120),
            (100, 700000, 'cL', 30, 120),
            (100, 800000, 'cM', 30, 120),
            (100, 900000, 'cN', 30, 120),
            (100, 1000000, 'cO', 30, 120),
            ]
        
        for (rowCount, colCount, key2, timeoutSecs, timeoutSecs2) in tryList:
            SEEDPERFILE = random.randint(0, sys.maxint)
            sel = 0
            csvFilename = "syn_%s_%s_%s_%s.csv" % (SEEDPERFILE, sel, rowCount, colCount)
            csvPathname = SYNDATASETS_DIR + '/' + csvFilename

            print "Creating random", csvPathname
            write_syn_dataset(csvPathname, rowCount, colCount, SEEDPERFILE, sel)

            start = time.time()
            parseKey = h2o_cmd.parseFile(None, csvPathname, key2=key2, timeoutSecs=timeoutSecs, doSummary=True)
            h2o.check_sandbox_for_errors()
            print csvFilename, 'parse time:', parseKey['response']['time']
            print "Parse and summary:", parseKey['destination_key'], "took", time.time() - start, "seconds"

            # We should be able to see the parse result?
            start = time.time()
            inspect = h2o_cmd.runInspect(None, parseKey['destination_key'], timeoutSecs=timeoutSecs2)
            print "Inspect:", parseKey['destination_key'], "took", time.time() - start, "seconds"
            h2o_cmd.infoFromInspect(inspect, csvPathname)
            print "\n" + csvPathname, \
                "    num_rows:", "{:,}".format(inspect['num_rows']), \
                "    num_cols:", "{:,}".format(inspect['num_cols'])

            # should match # of cols in header or ??
            self.assertEqual(inspect['num_cols'], colCount,
                "parse created result with the wrong number of cols %s %s" % (inspect['num_cols'], colCount))
            self.assertEqual(inspect['num_rows'], rowCount,
                "parse created result with the wrong number of rows (header shouldn't count) %s %s" % \
                (inspect['num_rows'], rowCount))

            # if not h2o.browse_disable:
            #     h2b.browseJsonHistoryAsUrlLastMatch("Inspect")
            #     time.sleep(3)

if __name__ == '__main__':
    h2o.unit_main()
