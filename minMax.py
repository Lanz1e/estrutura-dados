import unittest

def min_max(seq):
    '''
    :param seq: uma sequencia
    :return: (min, max)
    Retorna tupla cujo primeiro valor mínimo (min) é o valor
    mínimo da sequencia seq.
    O segundo é o valor máximo (max) da sequencia
    '''
    return min(seq), max(seq)

def min(seq):
    if(seq==[]):
        return None
    elif (len(seq)==1):
        menor=seq[0]
    else:
        menor=min(seq[0:len(seq)-1])
        if menor<seq[len(seq)-1]:
            menor=menor
        else:
            menor=seq[len(seq)-1]
    return menor;

def max(seq):
    if(seq==[]):
        return None
    elif(len(seq)==1):
        maior=seq[0]
    else:
        maior=max(seq[0:len(seq)-1])
        if maior>seq[len(seq)-1]:
            maior=maior
        else:
            maior=seq[len(seq)-1]
    return maior

class MinMaxTestes(unittest.TestCase):
    def test_lista_vazia(self):
        self.assertTupleEqual((None, None), min_max([]))

    def test_lista_len_1(self):
        self.assertTupleEqual((1, 1), min_max([1]))

    def test_lista_consecutivos(self):
        self.assertTupleEqual((0, 500), min_max(list(range(501))))

if __name__ == '__main__':
    unittest.main()
