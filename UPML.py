

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
