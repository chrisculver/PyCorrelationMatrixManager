from WickContractions.wick.contract import *
from PyCorrelationMatrixManager.correlator import Correlator

class CorrelationMatrix:
    def __init__(self, cops, aops):
        self.cops=cops
        self.aops=aops
        self.correlators=[]
    
    def contract_all(self):
        for c in self.cops:
            for a in self.aops:
                corr=Correlator(a,c)
                corr.contract()
                self.correlators.append(corr)

    
    def get_all_diagrams(self):
        all_diagrams=[]
        for c in self.correlators:
            for d in c.diagrams:
                all_diagrams.append(d)

        return all_diagrams