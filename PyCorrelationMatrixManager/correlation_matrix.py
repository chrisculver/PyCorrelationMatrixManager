from WickContractions.wick.contract import *

class CorrelationMatrix:
    def __init__(self, cops, aops):
        self.cops=cops
        self.aops=aops
    
    def contract_all():
        for c in self.cops:
            for a in self.aops:
                contract(a,c)