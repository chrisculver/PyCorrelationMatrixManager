"""
    General utilities
"""

import copy

def diagram_as_graph(d, allBaryonTensors):
    """ Converts a diagram object to a compact graph representation

        .. math:: B\\left[0\\right]_{123} B\\left[2\\right]_{321} \\rightarrow \\{\\text{"}0,2\\text{"}: \\left[\\left[0,2\\right],\\left[1,1\\right],\\left[2,0\\right]\\right]\\}
    
        Args:
            d (WickContractions.laph.LDiagram): Diagram
            allBaryonTensors (Dictionary): Mapping from tensor name to index

        Returns:
            Dictionary of tensors being contracted, and which indices are being contracted
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