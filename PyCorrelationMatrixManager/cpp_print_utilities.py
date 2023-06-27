import os
from PyCorrelationMatrixManager.utilities import diagram_as_graph


def create_input_file(ndiags, gammas):
    print("TODO: Need to handle momenta and baryon flavor!")
    s="cfg=__CFG__\n"
    s+="PerambulatorFileBase=/p/gpfs1/culver5/su4_spectroscopy/4flavor___FERMION__/__VOL__/__BETA__/evecs_perams_dbl/cfg___CFG__/perambulators___KAPPA___LapH___MAX_NVEC__vecs_tsource\n"
    s+="peram_sources=ALL\n"
    s+="EvecFileBase=/p/gpfs1/culver5/su4_spectroscopy/4flavor___FERMION__/__VOL__/__BETA__/evecs_perams/cfg___CFG__/LapH_128vecs_\n"
    s+="NDIAGS="+ndiags+"\n"
    s+="mom=0 0 0\n"
    s+="gammas="
    for i,g in enumerate(gammas):
        s+="GAMMAS/baryon_uuuu_{}_{}.txt".format(g[0],g[1])
        if i<len(gammas)-1:
            s+=","
    s+="\n"
    s+="dts=ALL\n"
    s+="ts=ALL\n"

    fileName = "run_base.in"
    file=open(fileName,"w")
    file.write(s)
    file.close()


def create_diagram_names_file(laphDiagrams):
    s=""
    for d in laphDiagrams:
        s+=d.name()
        s+="\n"
    
    fileName="diagram_names.txt"
    file=open(fileName,"w")
    file.write(s)
    file.close()



def cppArrayPrint(lst):
    return str(lst).replace('[','{').replace(']','}')


def create_diagram_gpu_file(laphDiagrams, allBaryonTensors, allBaryonSinks, allBaryonProps):
    allBaryonTensorsBack={v: k for k,v in allBaryonTensors.items()}

    s=cpp_file_header()

    for d in laphDiagrams:
        for blocks,contraction in diagram_as_graph(d,allBaryonTensors).items():
            blocks=blocks.split(',')


            block0=allBaryonTensorsBack[int(blocks[0])]
            block1=allBaryonTensorsBack[int(blocks[1])]
            
            if block0[0:3]=="B^*":
                b0type='bprops'
                b0Idx=allBaryonProps[block0]
            else: 
                b0type='bsinks'
                b0Idx=allBaryonSinks[block0]
            
            if block1[0:3]=="B^*":
                b1type='bprops'
                b1Idx=allBaryonProps[block1]
            else:
                b1type='bsinks'
                b1Idx=allBaryonSinks[block1]

            s+="  diagrams.push_back(Diagram({}[{}],{}[{}],std::vector<std::vector<int>>{}));\n".format(b0type,b0Idx,b1type,b1Idx,cppArrayPrint(contraction))

    s+=cpp_file_footer()

    fileName = "define_diagrams_gpu.cpp"
    file=open(fileName,"w")
    file.write(s)
    file.close()


def cpp_file_header():
    s = ""
    s += "#include \"define_diagrams.h\"\n"
    s += "#include \"diagram_utils.h\"\n"
    s += "#include <complex>\n"
    s += "#include <iostream>\n\n"

    s += "using namespace std;\n"
    s += "using Tensor4 = Eigen::Tensor<std::complex<double>,4>;\n"
    s += "using cd = std::complex<double>;  \n\n"

    s += "struct Diagram { \n"
    s += "  const Tensor4 &bLeft, &bRight; \n"
    s += "  std::vector<std::vector<int>> contractions; \n"
    s += "  Diagram(const Tensor4 &left, const Tensor4 &right, std::vector<std::vector<int>> contracts):bLeft(left),bRight(right),contractions(contracts){}\n"
    s += "};\n\n"


    s += "void compute_diagrams(vector<cd> &res, const vector<Tensor4> &bprops, const vector<Tensor4> &bsinks) \n"
    s += "{\n"
    s += "  std::vector<Diagram> diagrams;\n"

    return s


def cpp_file_footer():
    s = ""

    s += "  for(size_t i=0; i<diagrams.size(); ++i)\n"
    s += "  {\n"
    s += "    const Diagram d = diagrams[i]; \n"
    s += "    res[i]=cuTensor_contract(d.bLeft,d.bRight,d.contractions);\n"
    s += "  }\n"

    s += "}  \n"

    return s