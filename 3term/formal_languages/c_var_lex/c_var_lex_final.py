import ply.lex as lex
from ply.lex import TOKEN
import re
import sys

nesting_level = 0
variables = [set()]

reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'for' : 'FOR',
   'return' : 'RETURN',
   'break' : 'BREAK',
   'switch' : 'SWITCH',
   'case' : 'CASE',
   'const' : 'CONST',
   'continue' : 'CONTINUE',
   'default' : 'DEFAULT',
   'do' : 'DO',
   'goto' : 'GOTO'
}


tokens = [
    'FUNC_DECL',
    'FUNC_PROTO',
    'INIT',
    'FUNC_CALL',
    'CAST',
    
    'IDENTIFIER',
    
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',  
    'COMMA',
    
    'LBRA',
    'RBRA',
    
    'SEP',
    'COLON',
    'DOT',
    'HASH',
    'OPERATORS',
    'AMPERSAND',
    'ASSIGN',
    
    'COMMENT',
    'INCLUDE',
    
    'NUMBER',
    'STRING'
    
] + list(reserved.values())


t_OPERATORS = r'\+|-|\*|/|%|==|!=|<>|<=|>=|=|<|>|&&|\|\|'

t_ASSIGN   = r'='

t_LPAREN   = r'\('
t_RPAREN   = r'\)'

t_LBRA     = r'\['
t_RBRA     = r'\]'

t_COMMA    = r','
t_SEP      = r';'
t_COLON    = r':'
t_DOT      = r'\.'
t_HASH     = r'\#' 

t_NUMBER   = r'\b[0-9]+\b'

t_AMPERSAND = r'&'

t_ignore   = ' \t'


def t_INCLUDE(t):
    r'\#include\s*<.*>'
    return t

type_re = r'((((unsigned)|(signed))( (short)|(long))?( int)?)|((short)|(long))( int)?|(int)|(float)|(double)|(bool)|(char))(\s*\*)*' # e. g. insigned long* ** 
identifier = r'[A-Z_a-z][A-Z_a-z0-9]*' # variable and function name
number = r'\b[0-9]+\b'
id_decl = r'(\s*\*)*' + identifier + '(\s*\[\s*' + number + '\s*\])*'
id_init = id_decl + '(\s*=\s*' + number + ')?'
    
    
@TOKEN('(' + type_re + '\s+|void(\s*\*)*\s+)?' + identifier + '\s*\(' + '((' + type_re + '|void(\s*\*)+)' + '(\s+' + id_decl + ')?\s*(,\s*' + '(' + type_re + '|void(\s*\*)+)' + '(\s+' + id_decl + ')?\s*)*)?' + '\);')
def t_FUNC_PROTO(t):
    return t
 
@TOKEN('(' + type_re + '\s+|void(\s*\*)*\s+)?' + identifier + '\s*\(' + '((' + type_re + '|void(\s*\*)+)' + '\s+' + id_decl + '\s*(,\s*' + '(' + type_re + '|void(\s*\*)+)' + '\s+' + id_decl + '\s*)*)?' + '\)')
def t_FUNC_DECL(t):
    global nesting_level
    m = re.findall(identifier, t.value)
    if len(variables) <= nesting_level + 1:
        variables.append(set())       
    for item in m:
        if not re.match(type_re + '$', item):
            variables[nesting_level + 1].add(item)   
    return t




@TOKEN('(' + type_re + '|void(\s*\*)+)' + '\s+' + id_init + '\s*(,\s*' + id_init + '\s*)*;')
def t_INIT(t):
    global nesting_level
    m = re.findall(identifier, t.value)
    for item in m:
        if not re.match(type_re + '$', item):
            variables[nesting_level].add(item)
    return t

@TOKEN(identifier + '\s*\(')
def t_FUNC_CALL(t):
    return t

@TOKEN('\(\s*' + type_re + '\s*\)')
def t_CAST(t):
    return t

@TOKEN(identifier)
def t_IDENTIFIER(t):
    t.type = reserved.get(t.value, 'IDENTIFIER') # check for reserved words
    if t.type == 'IDENTIFIER':
        is_here = False
        for i in range(nesting_level + 1):
            if t.value in variables[i]:
                is_here = True
                break
        if is_here == False:
            print(t.value, "is not declared")
    return t

    
def t_STRING(t):
    r'(\"|\')([^\\\n]|(\\.))*(\"|\')'
    return t

def t_LBRACE(t):
    r'\{'
    global nesting_level
    nesting_level += 1
    if len(variables) <= nesting_level:
        variables.append(set())
    return t
    
def t_RBRACE(t):
    r'\}'
    global nesting_level
    variables[nesting_level] = set()
    nesting_level -= 1
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
   
def t_ignore_COMMENT(t):
    r'(/\*(.|\n)*\*/)|(//.*)'
    
def t_error(t):
    #print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    

if __name__ == '__main__': 
    
    f = open(sys.argv[1])
    
    lexer = lex.lex(debug = False)
    
    data = f.read()
    
    lexer.input(data)
    
    while True:
        tok = lexer.token()
        if not tok: 
            break
        #print(tok)
