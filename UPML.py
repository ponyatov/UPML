
import os,sys
import graphviz

class Frame:

    def __init__(self,V):
        self.type = self.__class__.__name__.lower()
        self.val  = V
        self.slot = {}
        self.nest = []

    def __repr__(self): return self.dump()

    # full tree dump
    def dump(self,depth=0,prefix=''):
        # head
        tree = self._pad(depth) + self.head(prefix)
        # infinite recursion block
        if not depth: Frame._dump = []
        if self in Frame._dump: return tree + ' _/'
        else: Frame._dump.append(self)
        # slot{}s
        for i in self.slot:
            tree += self.slot[i].dump(depth+1,'%s = '%i)
        # nest[]ed
        idx = 0
        for j in self.nest:
            tree += j.dump(depth+1,'%i: '%idx) ; idx += 1
        # subtree dump
        return tree

    def plot(self,dot=None,parent=None):
        if not dot:
            dot = graphviz.Digraph() ; dot.attr(rankdir='LR')
            Frame._plot = []
        # node
        dot.node(self.head())
        if parent: dot.edge(self.head(),parent.head())
        # infinite recursion block
        if self in Frame._plot: return dot
        else: Frame._plot.append(self)
        # sub slot{}s
        for i in self.slot:
            dot = self.slot[i].plot(dot,parent=self)
        # subplot
        return dot

    # <T:V> header only dump
    def head(self,prefix=''):
        return '%s<%s:%s> id:%x' % (prefix,self.type,self._val(),id(self))
    def _pad(self,depth):
        return '\n' + ' '*4 * depth
    def _val(self):
        return '%s' % self.val

    def __getitem__(self,key):
        return self.slot[key]
    def __setitem__(self,key,that):
        if callable(that): self[key] = Cmd(that) ; return self
        self.slot[key] = that ; return self
    def __lshift__(self,that):
        self[that.type] = that ; return self
    def __floordiv__(self,that):
        if isinstance(that,str): return self // String(that)
        self.nest.append(that) ; return self

    def pop(self): return self.nest.pop(-1)
    def top(self): return self.nest[-1]

class Primitive(Frame): pass
class Symbol(Primitive): pass
class String(Primitive): pass

class Active(Frame): pass
class VM(Active): pass
class Cmd(Active):
    def __init__(self, F):
        Active.__init__(self,F.__name__)
        self.fn = F
    def eval(self,ctx):
        self.fn(ctx)

vm = VM('UPML') ; vm << vm

import ply.lex  as lex

tokens = ['symbol']

t_ignore         = ' \t\r\n'
t_ignore_comment = r'[\#\\].*'

def t_symbol(t):
    r'[`]|[^ \t\r\n\#\\]+'
    return Symbol(t.value)

def t_error(t): raise SyntaxError(t)

def WORD(ctx):
    token = ctx.lexer.token()
    if token: ctx // token
    return token
vm['`'] = WORD

def FIND(ctx):
    token = ctx.pop()
    try:             ctx // ctx[token.val] ; return True
    except KeyError: ctx // token          ; return False

def EVAL(ctx): ctx.pop().eval(ctx)

def INTERP(ctx):
    ctx.lexer = lex.lex() ; ctx.lexer.input(ctx.pop().val)
    while True:
        if not WORD(ctx): break
        if isinstance(ctx.top(),Symbol):
            if not FIND(ctx): raise SyntaxError(ctx.top())
        EVAL(ctx)
        print(ctx.plot().view())

if __name__ == '__main__':
    for i in sys.argv[1:]:
        with open(i) as src:
            vm // src.read() ; INTERP(vm)
