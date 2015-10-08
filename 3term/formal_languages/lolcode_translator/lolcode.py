#!/usr/bin/env python

from lolcode_lex import *

import ply.yacc as yacc

import sys

import re


class LabelFactory:
    def __init__(self):
        self.first_unused = 0
        
    def new_label(self):
        self.first_unused += 1
        return "_label" + str(self.first_unused - 1)
        
    def postprocess(self, text):
        for i in range(self.first_unused):
            label = "_label" + str(i)
            j = text.index(label + ': ')
            lineno = text[:j].count('\n') + 1
            text = text.replace(label + ': ', '')
            text = re.sub(r'\b' + label + r'\b', str(lineno), text)
        return text


class TempVarFactory:
    def __init__(self):
        self.first_unused = 0
        
    def new_var(self):
        self.first_unused += 1
        return "_temp" + str(self.first_unused - 1)


temp_vars = TempVarFactory()
labels = LabelFactory()

def p_file(p):
    '''file : HAI program KTHXBYE'''
    p[0] = p[2]

def p_program_middle(p):
    '''program : program statement'''
    p[0] = p[1] + p[2]
    
def p_program_end(p):
    '''program : statement'''
    p[0] = p[1]
    

def p_statement_simple_declaration(p):
    '''statement : I HAS A IDENTIFIER'''
    p[0] = ''

def p_statement_declaration_with_assignment(p):
    '''statement : I HAS A IDENTIFIER ITZ expression'''
    p[0] = p[6][1] + 'mov {0} {1}\n'.format(p[6][0], p[4])
    
def p_statement_assignment_number(p):
    '''statement : IDENTIFIER R expression'''
    p[0] = p[3][1] + 'mov {0} {1}\n'.format(p[3][0], p[1])

def p_statement_print(p):
    '''statement : VISIBLE expression'''
    p[0] = p[2][1] + 'out {0}\n'.format(p[2][0])
    
def p_statement_expression(p):
    '''statement : expression'''
    p[0] = p[1][1]
    p[0] += 'mov {0} {1}\n'.format(p[1][0], 'IT')
    
def p_statement_if_then(p):
    '''statement : O RLY WHAT YA RLY program OIC'''
    tmp_zero = temp_vars.new_var()
    p[0] = 'let {0} 0\n'.format(tmp_zero)
    label1 = labels.new_label()
    label2 = labels.new_label()
    p[0] += 'cmp IT {0} {1} {2} {1}\n'.format(tmp_zero, label1, label2)
    p[0] += '{0}: '.format(label1)
    p[0] += p[6]
    p[0] += '{0}: '.format(label2)
    
def p_statement_if_then_else(p):
    '''statement : O RLY WHAT YA RLY program NO WAI program OIC'''
    tmp_zero = temp_vars.new_var()
    p[0] = 'let {0} 0\n'.format(tmp_zero)
    label1 = labels.new_label()
    label2 = labels.new_label()
    label3 = labels.new_label()
    p[0] += 'cmp IT {0} {1} {2} {1}\n'.format(tmp_zero, label1, label2)
    p[0] += '{0}: '.format(label1)
    p[0] += p[6]
    p[0] += 'jmp {0}\n'.format(label3)
    p[0] += '{0}: '.format(label2)
    p[0] += p[9]
    p[0] += '{0}: '.format(label3)
    

def p_statement_loop(p):
    '''statement : IM IN YR IDENTIFIER UPPIN YR IDENTIFIER TIL expression program IM OUTTA YR IDENTIFIER 
                 | IM IN YR IDENTIFIER NERFIN YR IDENTIFIER TIL expression program IM OUTTA YR IDENTIFIER
                 | IM IN YR IDENTIFIER UPPIN YR IDENTIFIER WILE expression program IM OUTTA YR IDENTIFIER 
                 | IM IN YR IDENTIFIER NERFIN YR IDENTIFIER WILE expression program IM OUTTA YR IDENTIFIER'''
    
    label1 = labels.new_label()
    label2 = labels.new_label()
    label3 = labels.new_label()
    
    p[0] = '{0}: '.format(label3)
    
    p[0] += p[9][1]
    tmp_zero = temp_vars.new_var()
    p[0] += 'let {0} 0\n'.format(tmp_zero)
    p[0] += 'cmp {0} {1} {2} {3} {2}\n'.format(p[9][0], tmp_zero, label1, label2)
    if p[8] == 'TIL':
        p[0] += '{0}: '.format(label2)
    else:
        p[0] += '{0}: '.format(label1)
    p[0] += p[10]
    
    tmp_one = temp_vars.new_var()
    p[0] += 'let {0} 1\n'.format(tmp_one)
    
    if p[5] == 'UPPIN':
        p[0] += 'add {0} {1} {2}\n'.format(p[7], tmp_one, p[7])
    else:  
        p[0] += 'sub {0} {1} {2}\n'.format(p[7], tmp_one, p[7])
        
    p[0] += 'jmp {0}\n'.format(label3)
    
    if p[8] == 'TIL':
        p[0] += '{0}: '.format(label1)
    else:
        p[0] += '{0}: '.format(label2)

def p_expression_binop(p):
    '''expression : SUM OF expression AN expression
                  | SUM OF expression expression
                  | DIFF OF expression AN expression
                  | DIFF OF expression expression
                  | PRODUKT OF expression AN expression
                  | PRODUKT OF expression expression
                  | QUOSHUNT OF expression AN expression
                  | QUOSHUNT OF expression expression
                  | MOD OF expression AN expression
                  | MOD OF expression expression
                  | BIGGR OF expression AN expression
                  | BIGGR OF expression expression
                  | SMALLR OF expression AN expression
                  | SMALLR OF expression expression'''
                  
    tmp = temp_vars.new_var()
    
    expr1 = p[3]
    if len(p) == 6:
        expr2 = p[5]
    else:
        expr2 = p[4]
        
    code = expr1[1] + expr2[1]
    
    if p[1] == 'SUM':
        code += 'add {0} {1} {2}\n'.format(expr1[0], expr2[0], tmp)
    elif p[1] == 'DIFF':
        code += 'sub {0} {1} {2}\n'.format(expr1[0], expr2[0], tmp)
    elif p[1] == 'PRODUKT':
        code += 'mul {0} {1} {2}\n'.format(expr1[0], expr2[0], tmp)
    elif p[1] == 'QUOSHUNT':
        code += 'div {0} {1} {2}\n'.format(expr1[0], expr2[0], tmp)
    elif p[1] == 'MOD':
        tmp1 = temp_vars.new_var()
        code += 'div {0} {1} {2}\n'.format(expr1[0], expr2[0], tmp1)
        tmp2 = temp_vars.new_var()
        code += 'mul {0} {1} {2}\n'.format(expr2[0], tmp1, tmp2)
        code += 'sub {0} {1} {2}\n'.format(expr1[0], tmp2, tmp)
    elif p[1] == 'BIGGR':
        label1 = labels.new_label()
        label2 = labels.new_label()
        label3 = labels.new_label()
        code += 'cmp {0} {1} {2} {3} {3}\n'.format(expr1[0], expr2[0], label1, label2)
        code += '{0}: mov {1} {2}\n'.format(label1, expr2[0], tmp)
        code += 'jmp {0}\n'.format(label3)
        code += '{0}: mov {1} {2}\n'.format(label2, expr1[0], tmp)
        code += '{0}: '.format(label3)
    elif p[1] == 'SMALLR':
        label1 = labels.new_label()
        label2 = labels.new_label()
        label3 = labels.new_label()
        code += 'cmp {0} {1} {2} {3} {3}\n'.format(expr1[0], expr2[0], label1, label2)
        code += '{0}: mov {1} {2}\n'.format(label1, expr1[0], tmp)
        code += 'jmp {0}\n'.format(label3)
        code += '{0}: mov {1} {2}\n'.format(label2, expr2[0], tmp)
        code += '{0}: '.format(label3)
    p[0] = (tmp, code)

def p_expression_bool_binop(p):
    '''expression : BOTH OF expression AN expression
                  | BOTH OF expression expression
                  | EITHER OF expression AN expression
                  | EITHER OF expression expression
                  | WON OF expression AN expression
                  | WON OF expression expression
                  | BOTH SAEM expression AN expression
                  | BOTH SAEM expression expression
                  | DIFFRINT expression AN expression
                  | DIFFRINT expression expression'''
    
    tmp = temp_vars.new_var()
    
    if p[1] == 'DIFFRINT':
        expr1 = p[2]
        if len(p) == 5:
            expr2 = p[4]
        else:
            expr2 = p[3]
    else:
        expr1 = p[3]
        if len(p) == 6:
            expr2 = p[5]
        else:
            expr2 = p[4]
        
    
    if p[1] == 'BOTH' and p[2] == 'SAEM':
        code = expr1[1] + expr2[1]
        label1 = labels.new_label()
        label2 = labels.new_label()
        label3 = labels.new_label()
        code += 'cmp {0} {1} {2} {3} {2}\n'.format(expr1[0], expr2[0], label1, label2)
        code += '{0}: let {1} 0\n'.format(label1, tmp)
        code += 'jmp {0}\n'.format(label3)
        code += '{0}: let {1} 1\n'.format(label2, tmp)
        code += '{0}: '.format(label3)

    elif p[1] == 'DIFFRINT':
        code = expr1[1] + expr2[1]
        label1 = labels.new_label()
        label2 = labels.new_label()
        label3 = labels.new_label()
        code += 'cmp {0} {1} {2} {3} {2}\n'.format(expr1[0], expr2[0], label1, label2)
        code += '{0}: let {1} 1\n'.format(label1, tmp)
        code += 'jmp {0}\n'.format(label3)
        code += '{0}: let {1} 0\n'.format(label2, tmp)
        code += '{0}: '.format(label3)
        
    elif p[1] == 'BOTH':
        code = expr1[1]
        tmp_zero = temp_vars.new_var()
        code += 'let {0} 0\n'.format(tmp_zero)
        label1 = labels.new_label()
        label2 = labels.new_label()
        label3 = labels.new_label()
        label4 = labels.new_label()
        code += 'cmp {0} {1} {2} {3} {2}\n'.format(expr1[0], tmp_zero, label1, label2)
        code += '{0}: '.format(label1)
        code += expr2[1]
        code += 'cmp {0} {1} {2} {3} {2}\n'.format(expr2[0], tmp_zero, label3, label2)
        code += '{0}: '.format(label3)
        code += 'let {0} 1\n'.format(tmp)
        code += 'jmp {0}\n'.format(label4)
        code += '{0}: '.format(label2)
        code += 'let {0} 0\n'.format(tmp)
        code += '{0}: '.format(label4)
    
    elif p[1] == 'EITHER':
        code = expr1[1]
        tmp_zero = temp_vars.new_var()
        code += 'let {0} 0\n'.format(tmp_zero)
        label1 = labels.new_label()
        label2 = labels.new_label()
        label3 = labels.new_label()
        label4 = labels.new_label()
        code += 'cmp {0} {1} {2} {3} {2}\n'.format(expr1[0], tmp_zero, label2, label1)
        code += '{0}: '.format(label1)
        code += expr2[1]
        code += 'cmp {0} {1} {2} {3} {2}\n'.format(expr2[0], tmp_zero, label2, label3)
        code += '{0}: '.format(label3)
        code += 'let {0} 0\n'.format(tmp)
        code += 'jmp {0}\n'.format(label4)
        code += '{0}: '.format(label2)
        code += 'let {0} 1\n'.format(tmp)
        code += '{0}: '.format(label4)
        
    elif p[1] == 'WON':
        code = expr1[1] + expr2[1]
        tmp_zero = temp_vars.new_var()
        code += 'let {0} 0\n'.format(tmp_zero)
        label1 = labels.new_label()
        label2 = labels.new_label()
        label3 = labels.new_label()
        label4 = labels.new_label()
        label5 = labels.new_label()
        code += 'cmp {0} {1} {2} {3} {2}\n'.format(expr1[0], tmp_zero, label1, label2)
        code += '{0}: '.format(label1)
        code += 'cmp {0} {1} {2} {3} {2}\n'.format(expr2[0], tmp_zero, label4, label3)
        code += '{0}: '.format(label2)
        code += 'cmp {0} {1} {2} {3} {2}\n'.format(expr2[0], tmp_zero, label3, label4)
        code += '{0}: '.format(label3)
        code += 'let {0} 1\n'.format(tmp)
        code += 'jmp {0}\n'.format(label5)
        code += '{0}: '.format(label4)
        code += 'let {0} 0\n'.format(tmp)
        code += '{0}: '.format(label5)
        
    p[0] = (tmp, code)
    
def p_expression_bool_unary(p):
    '''expression : NOT expression'''
    tmp = temp_vars.new_var()
    code = p[2][1]
    tmp_zero = temp_vars.new_var()
    code += 'let {0} 0\n'.format(tmp_zero)
    label1 = labels.new_label()
    label2 = labels.new_label()
    label3 = labels.new_label()
    code += 'cmp {0} {1} {2} {3} {2}\n'.format(p[2][0], tmp_zero, label1, label2)
    code += '{0}: '.format(label1)
    code += 'let {0} 0\n'.format(tmp)
    code += 'jmp {0}\n'.format(label3)
    code += '{0}: '.format(label2)
    code += 'let {0} 1\n'.format(tmp)
    code += '{0}: '.format(label3)
    
    p[0] = (tmp, code)

def p_expression_number(p):
    '''expression : NUMBER'''
    tmp = temp_vars.new_var()
    p[0] = (tmp, 'let {0} {1}\n'.format(tmp, p[1]))
  
def p_expression_variable(p):
    '''expression : IDENTIFIER'''
    tmp = temp_vars.new_var()
    p[0] = (tmp, 'mov {0} {1}\n'.format(p[1], tmp))

def p_error(p):
    print("Syntax error in input!")
    
    


if __name__ == '__main__': 

    lexer = lex.lex(debug = True)
    parser = yacc.yacc(start = "file", debug = 1)
    
    with open("example.lolcode") as f:
        text = f.read()
        result = parser.parse(text, tracking = True)
        
        result = labels.postprocess(result)
        
        output = open("output.code", 'w')
        output.write(result)
        output.close()