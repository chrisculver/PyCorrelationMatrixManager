from WickContractions.ops.quarks import Quark
from WickContractions.ops.commuting import SpinMatrix, IndexedObject
from WickContractions.ops.operator import Operator
from WickContractions.ops.elemental import ElementalOperator

def create_pion_op():
    q0=Quark(True,'u','s_0','c_0','x_0','t_i')
    q1=Quark(False,'d','s_1','c_1','x_0','t_i')
    g50=SpinMatrix('\\gamma^5',['s_0','s_1'])
    d0=IndexedObject('\\delta',['c_0','c_1'])

    return Operator([
                    ElementalOperator(1,[g50,d0],[q0,q1])
                    ])


def annihilate_pion_op():
    q2=Quark(True,'d','s_2','c_2','x_1','t_f')
    q3=Quark(False,'u','s_3','c_3','x_1','t_f')
    g51=SpinMatrix('\\gamma^5',['s_2','s_3'])
    d1=IndexedObject('\\delta',['c_2','c_3'])

    return Operator([
                    ElementalOperator(1,[g51,d1],[q2,q3])
                    ])