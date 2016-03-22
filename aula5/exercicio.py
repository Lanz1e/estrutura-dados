def num(s):
    try:
        s=int(s)
        return True
    except ValueError:
        return False

from aula5.fila import Fila
from aula4.pilha import Pilha

class ErroLexico(Exception):
    pass

class ErroSintatico(Exception):
    pass

def analise_lexica(expressao):

    def caracteres(param1):
        return param1 in "(){.}[]+-*/"

    fila=Fila()
    count=0
    pilha=Pilha()
    while count!=len(expressao):
        if not(caracteres(expressao[count]) or num(expressao[count])):
            raise ErroLexico
        else:
            if caracteres(expressao[count]):
                if not pilha.vazia():
                    fila.enfileirar(pilha.desempilhar())
                fila.enfileirar(expressao[count])
            if num(expressao[count]):
                if pilha.vazia():
                    pilha.empilhar(expressao[count])
                else:
                    final=pilha.desempilhar()
                    pilha.empilhar(final+expressao[count])
        count+=1
    if not pilha.vazia():
        fila.enfileirar(pilha.desempilhar())
    return fila

def analise_sintatica(fila):

    novafila=Fila()
    if fila.vazia():
        raise ErroSintatico;
    save=''
    while not fila.vazia():
        item=fila.desenfileirar()
        if num(item):
            save=int(item)
            if fila.vazia():
                novafila.enfileirar(save)
                return novafila
            if fila.primeiro()!='.':
                novafila.enfileirar(save)
        elif item=='.':
            item=fila.desenfileirar()
            save=float(save)
            save+=(float(item))/(10**(len(item)))
            novafila.enfileirar(save)
        else:
            novafila.enfileirar(item)
    return novafila

def avaliar(expressao):

    fila=analise_sintatica(analise_lexica(expressao))
    if fila.vazia():
        #erro vazio
        raise ErroSintatico
    item=fila.desenfileirar()
    if num(item):
        valor=item
    if fila.vazia():
        return item
    while not fila.vazia():
        item=fila.desenfileirar()
        #codição de exclusão parenteses
        if num(item) or item in ('+-*/'):
            if not num(item):
                #verifica a operação
                if item in '*':
                    valor*=fila.desenfileirar()
                if item in '/':
                    valor/=fila.desenfileirar()
                if item in '+':
                    valor+=fila.desenfileirar()
                if item in '-':
                    valor-=fila.desenfileirar()
            else:
                valor=item
    return valor #retorno do resultado

import unittest

class AnaliseLexicaTestes(unittest.TestCase):
    def test_expressao_vazia(self):
        fila = analise_lexica('')
        self.assertTrue(fila.vazia())

    def test_caracter_estranho(self):
        self.assertRaises(ErroLexico, analise_lexica, 'a')
        self.assertRaises(ErroLexico, analise_lexica, 'ab')

    def test_inteiro_com_um_algarismo(self):
        fila = analise_lexica('1')
        self.assertEqual('1', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_inteiro_com_vários_algarismos(self):
        fila = analise_lexica('1234567890')
        self.assertEqual('1234567890', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_float(self):
        fila = analise_lexica('1234567890.34')
        self.assertEqual('1234567890', fila.desenfileirar())
        self.assertEqual('.', fila.desenfileirar())
        self.assertEqual('34', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_parenteses(self):
        fila = analise_lexica('(1)')
        self.assertEqual('(', fila.desenfileirar())
        self.assertEqual('1', fila.desenfileirar())
        self.assertEqual(')', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_chaves(self):
        fila = analise_lexica('{(1)}')
        self.assertEqual('{', fila.desenfileirar())
        self.assertEqual('(', fila.desenfileirar())
        self.assertEqual('1', fila.desenfileirar())
        self.assertEqual(')', fila.desenfileirar())
        self.assertEqual('}', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_colchetes(self):
        fila = analise_lexica('[{(1.0)}]')
        self.assertEqual('[', fila.desenfileirar())
        self.assertEqual('{', fila.desenfileirar())
        self.assertEqual('(', fila.desenfileirar())
        self.assertEqual('1', fila.desenfileirar())
        self.assertEqual('.', fila.desenfileirar())
        self.assertEqual('0', fila.desenfileirar())
        self.assertEqual(')', fila.desenfileirar())
        self.assertEqual('}', fila.desenfileirar())
        self.assertEqual(']', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_adicao(self):
        fila = analise_lexica('1+2.0')
        self.assertEqual('1', fila.desenfileirar())
        self.assertEqual('+', fila.desenfileirar())
        self.assertEqual('2', fila.desenfileirar())
        self.assertEqual('.', fila.desenfileirar())
        self.assertEqual('0', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_subtracao(self):
        fila = analise_lexica('1-2.0')
        self.assertEqual('1', fila.desenfileirar())
        self.assertEqual('-', fila.desenfileirar())
        self.assertEqual('2', fila.desenfileirar())
        self.assertEqual('.', fila.desenfileirar())
        self.assertEqual('0', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_multiplicacao(self):
        fila = analise_lexica('1*2.0')
        self.assertEqual('1', fila.desenfileirar())
        self.assertEqual('*', fila.desenfileirar())
        self.assertEqual('2', fila.desenfileirar())
        self.assertEqual('.', fila.desenfileirar())
        self.assertEqual('0', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_divisao(self):
        fila = analise_lexica('1/2.0')
        self.assertEqual('1', fila.desenfileirar())
        self.assertEqual('/', fila.desenfileirar())
        self.assertEqual('2', fila.desenfileirar())
        self.assertEqual('.', fila.desenfileirar())
        self.assertEqual('0', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_expresao_com_todos_simbolos(self):
        expressao = '1/{2.0+3*[7-(5-3)]}'
        fila = analise_lexica(expressao)
        self.assertListEqual(list(expressao), [e for e in fila])
        self.assertTrue(fila.vazia())


class AnaliseSintaticaTestes(unittest.TestCase):
    def test_fila_vazia(self):
        fila = Fila()
        self.assertRaises(ErroSintatico, analise_sintatica, fila)

    def test_int(self):
        fila = Fila()
        fila.enfileirar('1234567890')
        fila_sintatica = analise_sintatica(fila)
        self.assertEqual(1234567890, fila_sintatica.desenfileirar())
        self.assertTrue(fila_sintatica.vazia())

    def test_float(self):
        fila = Fila()
        fila.enfileirar('1234567890')
        fila.enfileirar('.')
        fila.enfileirar('4')
        fila_sintatica = analise_sintatica(fila)
        self.assertEqual(1234567890.4, fila_sintatica.desenfileirar())
        self.assertTrue(fila_sintatica.vazia())

    def test_expressao_com_todos_elementos(self):
        fila = analise_lexica('1000/{222.125+3*[7-(5-3)]}')
        fila_sintatica = analise_sintatica(fila)
        self.assertListEqual([1000, '/', '{', 222.125, '+', 3, '*', '[', 7, '-', '(', 5, '-', 3, ')', ']', '}'],
                             [e for e in fila_sintatica])


class AvaliacaoTestes(unittest.TestCase):
    def test_expressao_vazia(self):
        self.assertRaises(ErroSintatico, avaliar,(''))

    def test_inteiro(self):
        self.assert_avaliacao('1')

    def test_float(self):
        self.assert_avaliacao('2.1')

    def test_soma(self):
        self.assert_avaliacao('2+1')

    def test_subtracao_e_parenteses(self):
        self.assert_avaliacao('(2-1)')

    def test_expressao_com_todos_elementos(self):
        self.assertEqual(1.0, avaliar('2.0/[4*3+1-{15-(1+3)}]'))

    def assert_avaliacao(self, expressao):
        self.assertEqual(eval(expressao), avaliar(expressao))


if __name__ == '__main__':
    unittest.main()