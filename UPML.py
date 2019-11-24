
import os,sys

class Frame:

    def __init__(self,V):
        self.type = self.__class__.__name__.lower()
        self.val  = V
        self.slot = {}
        self.nest = []

    def __repr__(self): return self.dump()
    def dump(self,depth=0,prefix=''):
        tree = self._pad(depth) + self.head(prefix)
        return tree
    def head(self,prefix=''):
        return '%s<%s:%s> id:%x' % (prefix,self.type,self._val(),id(self))
    def _pad(self,depth):
        return '\n' + '\t'*4 * depth
    def _val(self):
        return '%s' % self.val

    def __getitem__(self,key):
        return self.slot[key]
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

vm = VM('UPML')

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

def FIND(ctx):
    token = ctx.pop()
    try:             ctx // ctx[token.val] ; return True
    except KeyError: ctx // token          ; return False

def INTERP(ctx):
    ctx.lexer = lex.lex() ; ctx.lexer.input(ctx.pop().val)
    while True:
        if not WORD(ctx): break
        if isinstance(ctx.top(),Symbol):
            if not FIND(ctx): raise SyntaxError(ctx.top())
        EVAL(ctx)

if __name__ == '__main__':
    for i in sys.argv[1:]:
        with open(i) as src:
            vm // src.read() ; INTERP(vm)
