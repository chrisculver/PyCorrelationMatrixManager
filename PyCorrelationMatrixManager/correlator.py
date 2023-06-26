from WickContractions.wick.contract import contract
from WickContractions.laph.diagram import LDiagram

class Correlator:
    def __init__(self, cop, aop):
        self.cop=cop
        self.aop=aop
        self.diagrams=[]
        self.values=[]

    
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
        for d in self.diagrams:
            d.value = data[d.name()]

    def compute_correlator(self, dts, t0s):
        self.values = [0 for dt in dts]
        for dt in dts:
            value=0
            for t0 in t0s:
                for d in self.diagrams:
                    value+=d.coef*d.value[dt][t0]
            self.values[dt]=value/len(t0s)