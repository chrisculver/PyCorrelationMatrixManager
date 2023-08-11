from WickContractions.wick.contract import *
from PyCorrelationMatrixManager.correlator import Correlator
from PyCorrelationMatrixManager.diagram_data import *
from PyCorrelationMatrixManager.cpp_print_utilities import *

class CorrelationMatrix:
    """ The main class to interface with, just requires initialization and then calling run(). 
    """

    def __init__(self, cops, aops, dts, t0s, cfg, dfiles=[]):
        #:list(WickContractions.ops.operator): Array of creation operators built via WickContractions.ops objects
        self.cops=cops
        #:list(WickContractions.ops.operator): Array of annihilation operators built via WickContractions.ops objects
        self.aops=aops
        #:list(Correlators): A list of all correlators
        self.correlators=[]
        #:list(int): Array of creation annihilation operator separations to compute correlators at
        self.dts=dts
        #:list(int): Array of source times to average over
        self.t0s=t0s
        #:list(str): List of diagram file base names formated as diagram_cfg.txt, leave out cfg.txt   
        self.dfiles=dfiles
        #get all gamma matrix names
        self.gammas=[]
        for o in cops:
            for g in o.get_gammas():
                self.gammas.append(g)
        for o in aops:
            for g in o.get_gammas():
                self.gammas.append(g)
        #:int: Cfg to load dfiles for and compute correlators on
        self.cfg=cfg

    def run(self):
        """ Takes all of the operators and performs the following

        1. Contract all quarks
        2. Laphify the diagrams
        3. Load diagram file data
        4. Compute correlator value
        5. Save correlators to file

        """
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
        """ Contract all correlation matrix elements using Wick's theorem.

            See WickContractions.contract.
        """
        for c in self.cops:
            for a in self.aops:
                corr=Correlator(a,c)
                corr.contract()
                self.correlators.append(corr)

    def laphify(self):
        """ Convert diagram of point propagators into LapH space

                Specifically 
                
                1. Convert :math:`D^{-1}\\rightarrow\\tau` and adds appropriate :math:`V` matrices.
                2. Combine appropriate objects into T tensors
                3.

        """
        for c in self.correlators:
            c.laphify()

    
    def get_all_diagrams(self):
        """ Gets all diagrams that occur in the correlation matrix.

            This is used to generate the cpp files for numerically evaluating the diagrams.
        
            Return:
                List(LDiagram)
        """
        all_diagrams=[]
        for c in self.correlators:
            for d in c.diagrams:
                all_diagrams.append(d)

        return all_diagrams
    
    def get_baryon_tensor_dictionaries(self):
        """ Gets dictionaries mapping tensor names to indices.

            Return values of tuple are 

            # All baryon tensors
            # baryon sinks
            # baryon props
        
            Return:
                Tuple(Dictionary(LDiagram,int), Dictionary(LDiagram,int), Dictionary(LDiagram,int))
        """
        sinkIdx=0
        allBaryonSinks={}
        propIdx=0
        allBaryonProps={}
        bIdx=0
        allBaryonTensors={}

        # iterate through all correlators and diagrams
        # if the tensor is NOT in the appropriate list 
        # add it and increase the index.
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
        """ Transfer data from the diagram files into the Diagram class

            Args:
                data (Dictionary(str, complex)): Maps diagram name to series of complex valules for different dt,t0
        """
        for c in self.correlators:
            c.load_diagram_values(data)

    def compute_correlators(self):
        """ Compute all correlators averaging over source times
        """
        for c in self.correlators:
            c.compute_correlator(self.dts, self.t0s)

    def save_corrs_to_files(self):
        """ Save correlation functions to files.

            Files for annihilation operator i and creation operator j are named as 
            "corr_aopi_copj_cfg.txt".  The content is two columns, with the 
            real part in the first column and imaginary part in the second column.  Each
            line is a different dt.
        """
        for i in range(0,len(self.aops)):
            for j in range(0,len(self.cops)):
                corr = self.correlators[i*len(self.aops)+j].values

                with open("corr_aop{}_cop{}_{}.txt".format(i,j,self.cfg),'w') as file:
                    for value in corr[:-1]: # avoid newline on last line of file.
                        file.write("{} {}\n".format(value.real, value.imag))
                    file.write("{} {}".format(corr[-1].real, corr[-1].imag))
                    