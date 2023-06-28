"""
    General utilities
"""

import copy

def diagram_as_graph(d, allBaryonTensors):
    """
        Converts a diagram to a graph.
        B[0]_{123} B_[2]_{321} -> {0,2: [[0,2],[1,1],[2,0]]}
    """
    tst=copy.deepcopy(d)

    graph = {}

    for b in reversed(tst.commuting):
        tst.commuting.remove(b)
        bIdx=allBaryonTensors[b.id()]
    
        for idx in reversed(b.indices):
            for e in tst.commuting:
                if idx in e.indices:
                    fIdx=allBaryonTensors[e.id()]
                    contraction=str(bIdx)+","+str(fIdx)
                    if contraction in graph:
                        graph[contraction].append([b.indices.index(idx),e.indices.index(idx)])
                    else:
                        graph[contraction]=[[b.indices.index(idx),e.indices.index(idx)]]
                    
                    break

    return graph