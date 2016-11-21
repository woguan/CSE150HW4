#!/usr/bin/env python

from BayesianNetwork import *
#
#   * Creates and tests the alarm network as given in the book.
#
class SalmonNetwork(object):
    """ generated source for class SalmonNetwork """
    @classmethod
    def main(cls, args):
        """ generated source for method main """
        salmon_run = BayesianNetwork()
        #  Add variables to network
        asia = RandomVariable("asia")
        smoker = RandomVariable("smoker")
        tb = RandomVariable("tb")
        lung_cancer = RandomVariable("lung_cancer")
        tb_or_cancer = RandomVariable("tb_or_cancer")
        bronchitis = RandomVariable("bronchitis")
        xray = RandomVariable("xray")
        dispnea = RandomVariable("dispnea")

        salmon_run.addVariable(tb)
        salmon_run.addVariable(asia)
        salmon_run.addVariable(smoker)
        salmon_run.addVariable(lung_cancer)
        salmon_run.addVariable(tb_or_cancer)
        salmon_run.addVariable(bronchitis)
        salmon_run.addVariable(xray)
        salmon_run.addVariable(dispnea)
        #  Add edges to network
        salmon_run.addEdge(asia, tb)
        salmon_run.addEdge(smoker, lung_cancer)
        salmon_run.addEdge(smoker, bronchitis)
        salmon_run.addEdge(tb, tb_or_cancer)
        salmon_run.addEdge(lung_cancer, tb_or_cancer)
        salmon_run.addEdge(tb_or_cancer, dispnea)
        salmon_run.addEdge(bronchitis, dispnea)
        salmon_run.addEdge(tb_or_cancer, xray)
        #  Initialize probability tables
        asiaProbs = [.01]
        smokerProbs = [.5]
        tbProbs = [.05, .01]
        lungProbs = [.1, .01]
        bronchitisProbs = [.6,.3]
        tb_or_cancerProbs = [1, 1, 1, 0]
        xrayProbs = [.98, .05]
        dispneaProbs = [.9, .7, .8, .1]

        salmon_run.setProbabilities(asia, asiaProbs)
        salmon_run.setProbabilities(smoker, smokerProbs)
        salmon_run.setProbabilities(tb, tbProbs)
        salmon_run.setProbabilities(lung_cancer, lungProbs)
        salmon_run.setProbabilities(bronchitis, bronchitisProbs)
        salmon_run.setProbabilities(tb_or_cancer, tb_or_cancerProbs)
        salmon_run.setProbabilities(xray, xrayProbs)
        salmon_run.setProbabilities(dispnea, dispneaProbs)

        #  Perform sampling tests
        #  ----------------------
        print("Test 1")
        given1 = {}
        given1[asia]= True
        given1[smoker]=False
        given1[xray]=True
        given1[dispnea]=False

        print("rejection sampling: " +str(salmon_run.performRejectionSampling(tb, given1, 199999)))
        print("weighted sampling: " + str(salmon_run.performWeightedSampling(tb, given1, 199999)))
        print("gibbs sampling: " + str(salmon_run.performGibbsSampling(tb, given1, 199999)))



if __name__ == '__main__':
    import sys
    SalmonNetwork.main(sys.argv)
import sys
#SalmonNetwork.main(sys.argv)
