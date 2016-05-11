from collections import Counter

def soma_quadrados(n):
    lruCache={0:[0]}
    if n==0 or n==1:
        return [n]
    else:
        listQuad=[]
        max=1
        while max**2<=n:
            listQuad.append(max**2)
            max+=1
        while len(listQuad)>0:
            num=n
            quad=listQuad[:]
            a=quad.pop()
            res=[]
            while num>0:
                if num in lruCache.keys() and num!=n:
                    res+=lruCache[num]
                    num=0
                else:
                    if len(quad)>0:
                        if num-a<0:
                           a=quad.pop()
                        else:
                            num-=a
                            res.append(a)
                            if num<quad[-1]:
                                a=quad.pop()
                    else:
                        num-=a
                        res.append(a)
            if n not in lruCache.keys() or len(res)<len(lruCache[n]) :
                lruCache[n]=res[:]
            listQuad.pop()

    return lruCache[n]

import unittest


class SomaQuadradosPerfeitosTestes(unittest.TestCase):
    def teste_0(self):
        self.assert_possui_mesmo_elementos([0], soma_quadrados(0))

    def teste_1(self):
        self.assert_possui_mesmo_elementos([1], soma_quadrados(1))

    def teste_2(self):
        self.assert_possui_mesmo_elementos([1, 1], soma_quadrados(2))

    def teste_3(self):
        self.assert_possui_mesmo_elementos([1, 1, 1], soma_quadrados(3))

    def teste_4(self):
        self.assert_possui_mesmo_elementos([4], soma_quadrados(4))

    def teste_5(self):
        self.assert_possui_mesmo_elementos([4, 1], soma_quadrados(5))

    def teste_11(self):
        self.assert_possui_mesmo_elementos([9, 1, 1], soma_quadrados(11))

    def teste_12(self):
        self.assert_possui_mesmo_elementos([4, 4, 4], soma_quadrados(12))

    def assert_possui_mesmo_elementos(self, esperado, resultado):
        self.assertEqual(Counter(esperado), Counter(resultado))