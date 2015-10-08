#!/usr/bin/env python

import ply.lex as lex
import re

reserved = {
   'HAI',
   'KTHXBYE',
   
   #'BTW',
   #'OBTW',
   #'TLDR',
   
   'I', 'HAS', 'A',
   'ITZ',
   'R',
   
   'AN', # can be omitted
   'MKAY', # if EOL can be omitted
   
   'OF',
   
   'SUM',
   'DIFF',
   'PRODUKT',
   'QUOSHUNT',
   'MOD',
   'BIGGR',
   'SMALLR',
   
   'BOTH',
   'EITHER',
   'WON',
   'NOT',
   'ALL',
   'ANY',
   
   #'BOTH',
   'SAEM',
   'DIFFRINT',
   
   #'IT',
   
   'VISIBLE',
   
   'O', #'RLY?',
   'YA', 'RLY',
   'MEBBE',
   'NO', 'WAI',
   'OIC',
   
   'IM', 'IN', 'YR',
   'TIL', 'WILE',
   'UPPIN', 'NERFIN',
   'OUTTA',
   'GTFO'
}

tokens = [
   'IDENTIFIER', 
   'NUMBER',
   'WHAT',
   'COMMENT'
] + list(reserved)

def t_ignore_COMMENT(t):
    r'((BTW.*)|(OBTW(.|\n)*?TLDR))' #spaces?

t_WHAT = r'\?'

def t_NUMBER(t):
   r'\b[0-9]+\b'
   return t 

t_ignore = ' \t,'

def t_IDENTIFIER(t):
    r'[A-Z_a-z][A-Z_a-z0-9]*'
    t.type = (t.value in reserved) and t.value or 'IDENTIFIER'    # Check for reserved words
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
   

if __name__ == '__main__': 
    
    f = open('example.lolcode')
    
    lexer = lex.lex(debug = True)
    
    data = f.read()
    
    lexer.input(data)
    
    while True:
        tok = lexer.token()
        if not tok: 
            break
        print(tok)