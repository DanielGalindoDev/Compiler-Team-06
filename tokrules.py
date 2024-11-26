import ply.lex as lex


# ---------- Classess ----------- #

class Token_Info:
    def __init__(self,string, t = None, v = None):
        self.string = string
        self.type = t
        self.value = v
    

    def __str__(self):
        return self.string

class LexicalError(Exception): 
    pass

# -------------------------------- # 


reserved = {
    'if' : 'IF',
    'main' : 'MAIN',
    'int' : 'TYPE',
    'char' : 'TYPE',
    'float': 'TYPE', 
}

tokens = (
    'TYPE','ID','MATH1','MATH2','CONSTANT','SEMICOLON',
    'EQUAL','LP','RP','LB','RB','IF','MAIN',
    'RELATION','AND','OR'
)


def t_AND(t):
    r'&&'
    t.value = Token_Info(t.value)
    return t

def t_OR(t):
    r'\|\|'
    t.value = Token_Info(t.value)
    return t

def t_FLOAT(t): 
    r'[0-9]+\.[0-9]* | \.[0-9]+'
    t.type = 'CONSTANT'
    t.value = Token_Info(t.value,'float',float(t.value))
    return t

def t_INTEGER(t): 
    r'\d+'
    t.type = 'CONSTANT'
    t.value = Token_Info(t.value,'int', int(t.value))
    return t


def t_CHAR(t): 
    r'\'[a-zA-Z]\''
    t.type = 'CONSTANT'
    t.value = Token_Info(t.value,'char',t.value[1:-1])
    return t

def t_MATH1(t):
    r'\+|-'
    t.value = Token_Info(t.value)
    return t

def t_MATH2(t):
    r'\*|/'
    t.value = Token_Info(t.value)
    return t

def t_LP(t):
    r'\('
    t.value = Token_Info(t.value)
    return t

def t_RP(t):
    r'\)'
    t.value = Token_Info(t.value)
    return t

def t_LB(t):
    r'{'
    t.value = Token_Info(t.value)
    return t

def t_RB(t):
    r'}'
    t.value = Token_Info(t.value)
    return t

def t_SEMICOLON(t):
    r';'
    t.value = Token_Info(t.value)
    return t

def t_RELATION(t):
    r'< | > | =='
    t.value = Token_Info(t.value)
    return t

def t_EQUAL(t): 
    r'='
    t.value = Token_Info(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')

    if t.value == 'int':
        t.value = Token_Info(t.value,'int')
    elif t.value == 'char':
        t.value = Token_Info(t.value,'char')
    elif t.value == 'float': 
        t.value = Token_Info(t.value,'float')
    else: 
        t.value = Token_Info(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == '__main__':
    
    # Test it out
    data = '''
    &&
    45&%
    ||
    '''

    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()

        if not tok:
            break      # No more input
        print(tok.value.string)
