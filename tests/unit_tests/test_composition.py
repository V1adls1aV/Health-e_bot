from tests.unit_tests.setup import UserMock, user
from data_structures import Composition


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
    comp = Composition('МолОко, сахАр, =!,+,,  e132, Е123,  ,. курица,молокосодержащий продукт')
    comp.set_user(user)
    assert set(comp.additives) == {'сахар', 'молоко'}
    assert set(comp.ecodes) == {'е132', 'е123'}
