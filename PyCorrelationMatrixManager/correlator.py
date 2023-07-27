from WickContractions.wick.contract import contract
from WickContractions.laph.diagram import LDiagram

class Correlator:
    """ Class to hold all the correlator ops, contraction result, and values
    """
    def __init__(self, cop, aop):
        #:WickContractions.ops.operator: Creation operator
        self.cop=cop 
        #:WickContractions.ops.operator: Annihilation operator
        self.aop=aop
        #:Resulting list from WickContractions.contract.  Is either a list of WickContractions.corrs.diagram or WickContractions.laph.diagram
        self.diagrams=[]
        #:list(complex) values for different operator separation
        self.values=[]

    
    def contract(self):
        """ See WickContractions.contract 
        """
        self.diagrams=contract(self.aop,self.cop).diagrams

    def laphify(self):
        """ Converts the diagram in spatial coordinates to Laph coordinates

            1. Convert :math:`D^{-1}\\rightarrow\\tau` and adds appropriate :math:`V` matrices.
            2. Combine appropriate objects into T tensors
            3. Combine appropriate objects into B tensors

            The diagram now looks like a contraction of meson & baryon blocks.
        """
        for i,d in enumerate(self.diagrams):
            self.diagrams[i]=LDiagram(d)

        for d in self.diagrams:
            d.create_m_blocks()
            d.create_b_blocks()
            d.create_hadron_blocks()
            d.combine_indices()
            d.create_hadron_source()    

    def load_diagram_values(self, data):
        """ loads from DiagramData into the diagram"""
        for d in self.diagrams:
            d.value = data[d.name()]

    def compute_correlator(self, dts, t0s):
        """ Computes the correlator averaging over t0s for each dt."""
        self.values = [0 for dt in dts]
        for dt in dts:
            value=0
            for t0 in t0s:
                for d in self.diagrams:
                    value+=d.coef*d.value[dt][t0]
            self.values[dt]=value/len(t0s)