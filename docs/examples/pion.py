from PyCorrelationMatrixManager.correlation_matrix import CorrelationMatrix
from make_ops import *

create=[create_pion_op()]
annihilate=[annihilate_pion_op()]

gammas=[]

print(create[0])
print(annihilate[0])


cmat = CorrelationMatrix(create, annihilate, gammas, [0], [0], 0)
cmat.run()