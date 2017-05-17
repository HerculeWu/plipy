from ply import yacc
from exp1bytecode_lex import tokens, lexer

# define the structures of our abstract machine
addr_ix = 0
program = []
symbol_table = dict()
label_table = dict()

def p_prog(_):
    '''
    prog : instr_list
    '''
    pass

def p_instr_list(_):
    '''
    instr_list : labeled_instr instr_list
              | empty
    '''
    pass

def p_labeled_instr(p):
    '''
    labeled_instr : label_def instr
    '''
    global label_table
    global program
    global addr_ix
    # if label exists record it in the label table
    if p[1]:
        label_table[p[1]] = addr_ix
    # append instr to program
    program.append(p[2])
    addr_ix += 1

def p_label_def(p):
    '''
    label_def : NAME ':' 
              | empty
    '''
    p[0] = p[1]

def p_instr(p):
    '''
    instr : PRINT exp ';'
         | STORE NAME exp ';'
         | JUMPT exp label ';'
         | JUMPF exp label ';'
         | JUMP label ';'
         | STOP ';'
         | NOOP ';'
    '''
    # for each instr assemble the appropriate tuple
    if p[1] == 'print':
        p[0] = ('print', p[2])
    elif p[1] == 'store':
        p[0] = ('store', p[2], p[3])
    elif p[1] == 'jumpT':
        p[0] = ('jumpT', p[2], p[3])
    elif p[1] == 'jumpF':
        p[0] = ('jumpF', p[2], p[3])
    elif p[1] == 'jump':
        p[0] = ('jump', p[2])
    elif p[1] == 'stop':
        p[0] = ('stop',)
    elif p[1] == 'noop':
        p[0] = ('noop',)
    else:
        raise ValueError("Unexpected instr value: %s" % p[1])

def p_label(p):
    '''
        label : NAME
        '''
    p[0] = p[1]

def p_bin_exp(p):
    '''
    exp : '+' exp exp
        | '-' exp exp
        | '*' exp exp
        | '/' exp exp
        | EQ exp exp
        | LE exp exp
    '''
    p[0] = (p[1], p[2], p[3])
    
def p_uminus_exp(p):
    '''
    exp : '-' exp
    '''
    p[0] = ('UMINUS', p[2])
    
def p_paren_exp(p):
    '''
    exp : '(' exp ')'
    '''
    # parens are not necessary in trees
    p[0] = p[2]
    
def p_var_exp(p):
    '''
    exp : NAME
    '''
    p[0] = ('NAME', p[1])

def p_number_exp(p):
    '''
    exp : NUMBER
    '''
    p[0] = ('NUMBER', int(p[1]))

def p_empty(p):
    '''
    empty :
    '''
    p[0] = ''

def p_error(t):
    print("Syntax error at '%s'" % t.value)

parser = yacc.yacc()
