from WickContractions.wick.contract import *
from PyCorrelationMatrixManager.correlator import Correlator
from PyCorrelationMatrixManager.diagram_data import *
from PyCorrelationMatrixManager.cpp_print_utilities import *

class CorrelationMatrix:
    def __init__(self, cops, aops, gammas, dts, t0s, cfg, dfiles=[]):
        self.cops=cops
        self.aops=aops
        self.correlators=[]
        self.dts=dts
        self.t0s=t0s
        self.dfiles=dfiles
        self.gammas=gammas
        self.cfg=cfg

    def run(self):
        try:
            self.contract()
        except:
            raise RuntimeError("Failed to contract all operators.  Check all quarks are paired with anti-quarks")

        try:
            self.laphify()
        except:
            raise RuntimeError("Failed to LapHify diagrams...")

        try: 
            data = DiagramData(self.dfiles, self.cfg)
        except:
            raise RuntimeError("Failed to load diagram files")

        try:
            self.load_diagram_values(data.diagram_data)
            self.compute_correlators()
        except:
            print("TODO: This can be massively improved")
            print("      For now just tells you the full calculation")

            allBaryonTensors, allBaryonSinks, allBaryonProps = self.get_baryon_tensor_dictionaries()
            create_diagram_gpu_file(self.get_all_diagrams(), allBaryonTensors, allBaryonSinks, allBaryonProps)    
            create_input_file(str(len(self.get_all_diagrams())),self.gammas)
            create_diagram_names_file(self.get_all_diagrams())

            raise RuntimeError("Failed to load all diagram values")

        try:
            self.save_corrs_to_files()
        except:
            raise RuntimeError("Couldn't save results to file")

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

    def compute_correlators(self):
        for c in self.correlators:
            c.compute_correlator(self.dts, self.t0s)

    def save_corrs_to_files(self):
        for i in range(0,len(self.aops)):
            for j in range(0,len(self.cops)):
                corr = self.correlators[i*len(self.aops)+j].values

                with open("corr_aop{}_cop{}_{}.txt".format(i,j,self.cfg),'w') as file:
                    for value in corr[:-1]:
                        file.write("{} {}\n".format(value.real, value.imag))
                    file.write("{} {}".format(corr[-1].real, corr[-1].imag))
                    
