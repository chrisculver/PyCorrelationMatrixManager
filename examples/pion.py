from PyCorrelationMatrixManager.correlation_matrix import CorrelationMatrix
from make_ops import *

create=create_pion_op()
annihilate=annihilate_pion_op


cmat = CorrelationMatrix(create, annihilate)