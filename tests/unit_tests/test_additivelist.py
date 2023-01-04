from data_structures.additive_list import AdditiveList


def test_1():
    al = AdditiveList('Молоко, сахар, мука')
    assert al == ['молоко', 'сахар', 'мука']

def test_2():
    al = AdditiveList('Молоко, сахар, E132, е123')
    assert al == ['молоко', 'сахар', 'e132', 'е123']

def test_3():
    al = AdditiveList('Молоко, сахар, =!,+  E132, е123,  ,. ')
    assert al == ['молоко', 'сахар', 'e132', 'е123']

def test_4():
    al = AdditiveList('Молоко,+  E132,, сахар , =! е123, ,. ')
    assert al == ['молоко', 'e132', 'сахар', 'е123']

def test_5():
    al = AdditiveList('МолОко, сахАр, =!,+,,  e132, Е123,  ,. ')
    assert al == ['молоко', 'сахар', 'e132', 'е123']
