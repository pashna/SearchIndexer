# coding: utf-8
from Engine.Optimizer import Optimizer
from Engine.Simple9 import Simple9
from Engine.Searcher import Searcher

class QueryExecutor():

    STR_ELEMENTS = ["!", "&", "|", "(", ")"]

    def __init__(self, searcher):
        self.searcher = searcher

        self.OPERATORS = {
            '*': (1, lambda w1, w2: self.searcher.and_not(w1, w2)), # И-НЕ
            '^': (1, lambda w1, w2: self.searcher.not_and(w1, w2)), # НЕ-И
            '&': (1, lambda w1, w2: self.searcher.and_(w1, w2)),
            '|': (2, lambda w1, w2: self.searcher.or_(w1, w2)),
             }
    """
    def f(a, b, sign):
        #print (a + " " + sign + " " + b)
        return "res("+a + " " + sign + " " + b +")"


OPERATORS = {
            '*': (2, lambda x, y: f(x, y, "AND NOT")), # И-НЕ
            '^': (2, lambda x, y: f(x, y, "NOT AND")), # ИЛИ-НЕ
            '&': (1, lambda x, y: f(x, y, "&")),
            '|': (2, lambda x, y: f(x, y, "|")),
             }
     """

#STR_ELEMENTS = ["!", "&", "|"]

    def parse(self, formula_string):
        term = ''
        for s in formula_string:
            if s not in QueryExecutor.STR_ELEMENTS:
                term += s
            elif term: # если символ не цифра, то выдаём собранное число и начинаем собирать заново
                yield term
                term = ''
            if s in QueryExecutor.STR_ELEMENTS or s in "()": # если символ - оператор или скобка, то выдаём как есть
                yield s
        if term:  # если в конце строки есть число, выдаём его
            yield term


    def shunting_yard(self, parsed_formula):
        stack = []  # в качестве стэка используем список
        for token in parsed_formula:
            # если элемент - оператор, то отправляем дальше все операторы из стека,
            # чей приоритет больше или равен пришедшему,
            # до открывающей скобки или опустошения стека.
            # здесь мы пользуемся тем, что все операторы право-ассоциативны
            if token in self.OPERATORS:
                while stack and stack[-1] != "(" and self.OPERATORS[token][0] <= self.OPERATORS[stack[-1]][0]:
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                # если элемент - закрывающая скобка, выдаём все элементы из стека, до открывающей скобки,
                # а открывающую скобку выкидываем из стека.
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                # если элемент - открывающая скобка, просто положим её в стек
                stack.append(token)
            else:
                # если элемент - число, отправим его сразу на выход
                yield token
        while stack:
            yield stack.pop()


    def calc(self, polish):
        stack = []
        for token in polish:
            if token in self.OPERATORS:  # если приходящий элемент - оператор,
                y, x = stack.pop(), stack.pop()  # забираем 2 числа из стека
                stack.append(self.OPERATORS[token][1](x, y)) # вычисляем оператор, возвращаем в стек
            else:
                stack.append(token)
        return stack[0] # результат вычисления - единственный элемент в стеке


    def query(self, text):
        result = self.calc(self.shunting_yard(self.preprocess(text)))
        if isinstance(result, list):
            return result
        else:
            return self.searcher.find_word(result)

    def preprocess(self, q):
        q = q.replace(' ', '')
        q = list(self.parse(q))

        for i in range(len(q)):
            if q[i]== '!':
                if q[i-1] == '&':
                    q[i] = ''
                    q[i - 1] = '*'
                elif q[i+2] == "&":
                    q[i] = ''
                    q[i + 2] = '^'

        q = filter(lambda a: a != '', q)

        return q

"""
for i in shunting_yard(parse(u"власти&(бельгии|парижа)*теракт")):
    print i
"""

"""
optimizer = Optimizer(Simple9())
r_index = \
    {
        "a": {
            "docs": [0, 5, 7,],
        }
        ,
        "b": {
            "docs": [0,3,4,5,],
        }
    }

r_index = optimizer.create_jump_table(r_index, jump_step=3)
optimizer.encode_it(r_index)
searcher = Searcher(r_index, Simple9())

q = QueryExecutor(searcher)
for i in q.shunting_yard(q.parse("путин&(россия|крым)")):
    print i
"""
#print q.query(u"b & !a")
#print calc(shunting_yard(preprocess(u"!теракт&власти&(бельгии|парижа)&!путин")))

"""
for i in preprocess(u"!теракт&власти&(бельгии|парижа)&!путин"):
    print i
"""
#a = list(parse(u"!теракт&власти&(бельгии|парижа)&!теракт"))

#    print i
"""
for i in range(len(a)):
    if a[i]=='!':
        if a[i-1] == '&':
            a[i] = ''
            a[i-1] = '*'
        elif a[i+2] == "&":
            a[i] = ''
            a[i+2] = '^'

a.remove('')
for i in a:
    print i
"""