from tests.unit.setup import UserMock, user
from data_structures.composition import Composition


def test_1(user: UserMock):
    comp = Composition('Молоко, сахар, мука')
    comp.set_user(user)
    assert set(comp.additives) == {'сахар', 'молоко'}

def test_2(user: UserMock):
    comp = Composition('Молоко, сахар, E132, е123')
    comp.set_user(user)
    assert set(comp.additives) == {'сахар', 'молоко'}
    assert set(comp.ecodes) == {'е132', 'е123'}

def test_3(user: UserMock):
    comp = Composition('Молоко, сахар, =!,+  E132, е123,  ,. ')
    comp.set_user(user)
    assert set(comp.additives) == {'сахар', 'молоко'}
    assert set(comp.ecodes) == {'е132', 'е123'}

def test_4(user: UserMock):
    comp = Composition('Молоко,орехи кедровые ,+  E132,, сахар , =! е123, ,.картофель ,,')
    comp.set_user(user)
    assert set(comp.additives) == {'сахар', 'молоко'}
    assert set(comp.ecodes) == {'е132', 'е123'}

def test_5(user: UserMock):
    comp = Composition('МолОко, сахАр, =!,+,,  e132    Е123,  ,. курица,молокосодержащий продукт')
    comp.set_user(user)
    assert set(comp.additives) == {'сахар', 'молоко'}
    assert set(comp.ecodes) == {'е132', 'е123'}

def test_6(user: UserMock):
    comp = Composition(', сахароза,  e-123')
    comp.set_user(user)
    assert set(comp.additives) == {'сахар'}
    assert set(comp.ecodes) == {'е123'}

def test_7(user: UserMock):
    comp = Composition(' следы молочных продуктов,  сахар ,  e123')
    comp.set_user(user)
    assert set(comp.additives) == {'сахар', 'молоко'}
    assert set(comp.ecodes) == {'е123'}

def test_8(user: UserMock):
    comp = Composition('яблочная кислота,  сахар,  e123')
    comp.set_user(user)
    assert set(comp.additives) == {'сахар'}
    assert set(comp.ecodes) == {'е123', 'е296'}

def test_9(user: UserMock):
    comp = Composition('Молочная кислота, .,  сахар ,  e123')
    comp.set_user(user)
    assert set(comp.additives) == {'сахар', 'молоко'}
    assert set(comp.ecodes) == {'е123', 'е270'}

def test_10(user: UserMock):
    comp = Composition('мука крупного помола')
    comp.set_user(user)
    assert set(comp.additives) == set()
    assert set(comp.ecodes) == set()
