from WickContractions.wick.contract import contract

class Correlator:
    def __init__(self, cop, aop):
        self.cop=cop
        self.aop=aop
        self.diagrams=[]

    
    def contract(self):
        self.diagrams=contract(self.aop,self.cop).diagrams