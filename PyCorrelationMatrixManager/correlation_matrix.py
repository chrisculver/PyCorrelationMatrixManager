from WickContractions.wick.contract import *
from PyCorrelationMatrixManager.correlator import Correlator

class CorrelationMatrix:
    def __init__(self, cops, aops):
        self.cops=cops
        self.aops=aops
        self.correlators=[]
    
    def contract(self):
        for c in self.cops:
            for a in self.aops:
                corr=Correlator(a,c)
                corr.contract()
                self.correlators.append(corr)

    def laphify(self):
        for c in self.correlators:
            c.laphify()

    
    def get_all_diagrams(self):
        all_diagrams=[]
        for c in self.correlators:
            for d in c.diagrams:
                all_diagrams.append(d)

        return all_diagrams
    
    def get_baryon_tensor_dictionaries(self):
        sinkIdx=0
        allBaryonSinks={}
        propIdx=0
        allBaryonProps={}
        bIdx=0
        allBaryonTensors={}

        for c in self.correlators:
            d = c.diagrams[0]
            for block in d.commuting:
                if block.id() not in allBaryonTensors:
                    allBaryonTensors[block.id()]=bIdx
                    bIdx+=1
                if block.name=="B" and block.id() not in allBaryonSinks:
                    allBaryonSinks[block.id()]=sinkIdx
                    sinkIdx+=1
                elif block.name=="B^*" and block.id() not in allBaryonProps:
                    allBaryonProps[block.id()]=propIdx 
                    propIdx+=1
                    
                #print(block, block.name, block.arguments)
        return allBaryonTensors, allBaryonSinks, allBaryonProps

    def load_diagram_values(self, data):
        for c in self.correlators:
            c.load_diagram_values(data)