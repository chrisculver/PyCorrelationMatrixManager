from WickContractions.wick.contract import contract
from WickContractions.laph.diagram import LDiagram

class Correlator:
    def __init__(self, cop, aop):
        self.cop=cop
        self.aop=aop
        self.diagrams=[]

    
    def contract(self):
        self.diagrams=contract(self.aop,self.cop).diagrams

    def laphify(self):
        for i,d in enumerate(self.diagrams):
            self.diagrams[i]=LDiagram(d)

        for d in self.diagrams:
            d.create_baryon_blocks()
            d.combine_indices()

        # the below has no guarantee to be NC agnostic nor work for any multi meson&baryon operator
        for d in self.diagrams:
            d.create_baryon_source()

    def compute_value(self, diagram_values, dt, t):
        res = 0.0
        for d in self.diagrams:
            res+=d.coef*diagram_values[self.diagrams.name()][dt][t]
        return res
    
    def load_diagram_values(self, data):
        self.value = 0
        for d in self.diagrams:
            self.value += d.coef*data[d.name()][0][0]