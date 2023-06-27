import copy

def diagram_as_graph(d, allBaryonTensors):
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