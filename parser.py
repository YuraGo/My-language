from ply import yacc

import abstract_tree as ast

from lexer import Lexer

function_dict = {}

class ParseError(Exception): pass


def parse_error(self, msg, coord):
    raise ParseError("%s: %s" % (coord, msg))

buffer = Lexer(parse_error)
buffer.run()
tokens = buffer.tokens


#ПРИОРИТЕТ ТОКЕНОВ
precedence = (
    ('left',  'EQUALS'),
    ('left', 'PLUS', 'MINUS'),
    ('left' ,'TIMES' ,'DIVIDE'),
    ('right' ,'UMINUS')
)

def p_root(p):
    ' root : file_input'

    if p[1] is None:
        p[0] = ast.Root([])
    else:
        p[0] = ast.Root(p[1])


def p_file_input_1(p):
    ' file_input : NEWLINE'
    p[0] = []



def p_file_input_2(p):
    ''' file_input : statement
                   | func_def'''
    p[0] = p[1]



def p_file_input_3(p):
    ' file_input :  file_input statement'
    p[1].extend([p[2]])
    p[0] = p[1]
    # print(p[0])

def p_file_input_4(p):
    ' file_input : file_input func_def '
    p[1].append(p[2])
    p[0] = p[1]


def p_statement(p):
    ''' statement : simple_stmt
                  | compound_stmt'''
    p[0] = p[1]


def p_simple_stmt_1(p):
    ''' simple_stmt : small_stmt NEWLINE
                    | small_stmt'''
    p[0] = p[1]


def p_small_stmt(p):
    '''small_stmt   : variable
                    | robot_operators
                    | convert
                    | digitize
                    | variant_assignment
                    | param
                    | return
                    | call_function
                    | print
                    | unary_expression
                    '''
    p[0] = p[1]


def p_robot_operators(p):
    ''' robot_operators : COMMAND robot_commands
                        | variant_call EQUALS COMMAND robot_commands
                        '''
    if len(p) > 3:
        p[0] = ast.RobotOperator(p[1],p[4])
    else: p[0] = ast.RobotOperator(None,p[2])


def p_robot_comm(p):
    ''' robot_commands : string
                       | variant_call
                       '''
    p[0] = p[1]

def p_full_expression(p):
    ''' expression : LPAREN expression RPAREN '''
    p[0] = p[2]

def p_expression(p):
    """ expression  : assignment_expression
        """
    # print("In expression", p[1])
    if len(p) == 2:
        p[0] = p[1]

def p_assignment_expression(p):
    ''' assignment_expression : binary_expression
                              | unary_expression
                              | bool
                              | digit
                              | variant_call'''
    p[0] = p[1]

def p_binary_expression(p):
    """ binary_expression   : variant_call TIMES variant_call
                            | variant_call DIVIDE variant_call
                            | variant_call MINUS variant_call
                            | variant_call PLUS variant_call
                            | variant_call PLUS string
                            | variant_call PLUS digit
                            | variant_call MINUS digit
                            | variant_call TIMES digit
                            | variant_call DIVIDE digit
        """
    p[0] = ast.BinaryOp(p[2], p[1], p[3],p[1].coord)

def p_expression_uminus(p):
    '''unary_expression : MINUS var_var %prec UMINUS
                        | MINUS variant_call %prec UMINUS'''
    p[0] = ast.UnaryOp(p[2])

def p_compound_stmt(p):
    """compound_stmt : if_stmt
                     | while_stmt
                     | until_stmt"""
    p[0] = p[1]


def p_if_stmt_1(p):
    #              1         2       3     4          5     6
    """if_stmt : IFLESS  expression THEN expression  suite pass_new_line
               | IFNLESS expression THEN expression  suite pass_new_line
               | IFHIGH  expression THEN expression  suite pass_new_line
               | IFNHIGH expression THEN expression  suite pass_new_line
               """
    p[0] = ast.If(p[1], p[2], p[4], p[5], None)

def p_if_stmt_2(p):
    ''' if_stmt : IFZERO expression suite pass_new_line
                | IFNZERO expression suite pass_new_line'''
    p[0] = ast.IfZero(p[1],p[2],p[3])

def p_while_stmt(p):
    """while_stmt : WHILE expression suite pass_new_line"""
    p[0] = ast.While(p[2], p[3], None)

def p_until_stmt(p):
    '''until_stmt : UNTIL expression suite pass_new_line '''
    p[0] = ast.Until(p[2],p[3],None)

def p_suite_2(p):
    """suite : COLON pass_new_line big_stmt pass_new_line ENDIF
             | COLON pass_new_line big_stmt pass_new_line ENDW
             | COLON pass_new_line big_stmt pass_new_line ENDU
             | COLON pass_new_line big_stmt pass_new_line ENDFUNC"""
    p[0] = ast.Suite(p[3], p[5],None)
    #print("In suite2", p[0])

def p_big_stmt(p):
    """big_stmt :  pass_new_line"""
    p[0] = []

def p_param(p):
    ''' param : identifier EQUALS PARAM '''
    #p[0] = ast.ID(p[1], None)
    p[0] = ast.Param(p[1])
    #p[0] = p[1]

def p_return(p):
    ''' return : RETURN identifier'''
    #p[0] = p[2]
    p[0] = ast.Return(p[2])

def p_func_def(p):
    ''' func_def : FUNC identifier suite pass_new_line'''
    p[0] = ast.FunctionDict(p[2],p[3])
    if function_dict.get(p[2].name):
        print('ERROR ----> function definition is already exists')
    else:
        function_dict[p[2].name] = ([ast.FunctionCall(p[2],  p[3]), 0])

def p_call_function(p):
    ''' call_function : CALL identifier variant_to_func'''
    p[0] = ast.CallFunction(p[2],p[3])

def p_call_func_none(p):
    ''' call_function : CALL identifier'''
    p[0] = ast.CallFunction(p[2],None)

def p_call_function_eq(p):
    '''call_function : identifier EQUALS CALL identifier variant_to_func'''
    p[0] = ast.CallFunction(p[4],p[5],p[1])

def p_call_function_eq_none(p):
    '''call_function : identifier EQUALS CALL identifier'''
    p[0] = ast.CallFunction(p[4],None,p[1])

def p_big_stmt_1(p):
    """big_stmt : statement"""
    p[0] = [p[1]]

# Нужно немного переделать Suite, чтобы было сегче обрабатывать
def p_big_stmt_2(p):
    """big_stmt :  big_stmt statement"""
    p[1].append(p[2])
    p[0] = p[1]

def p_pass_new_line(p):
    """pass_new_line : empty
                     | NEWLINE"""
    p[0] = []

def p_empty(p):
    """empty : """
    p[0] = ast.EmptyStatement()


def p_identifier(p):
    ''' identifier : ID '''
    # print("Identifier", p[1])
    p[0] = ast.ID(p[1], None)

def p_convert(p):
    #                1      2             3     4            5
    ''' convert : CONVERT type_specifier TO type_specifier variant_call'''
    p[0] = ast.Convert(p[2],p[4],p[5])
    #print()

def p_digitize(p):
    ''' digitize : DIGITIZE variant_call '''
    p[0] = ast.Digitize(p[2])

def p_type_specifier(p):
    ''' type_specifier : BOOL
                       | STRINGTYPE
                       | DIGITTYPE'''
    p[0] = p[1]

def p_variant_call(p):
    ''' variant_call : identifier LPAREN digit COMMA digit RPAREN
                     | identifier LPAREN variant_call COMMA variant_call RPAREN
                     | identifier LPAREN digit COMMA variant_call RPAREN
                     | identifier LPAREN variant_call COMMA digit RPAREN'''
    p[0] = ast.VariantCall(p[1], p[3], p[5])

def p_variant_to_func(p):
    ''' variant_to_func : LPAREN identifier RPAREN'''
    p[0] = p[2]

def p_variant_assignment(p):
    '''variant_assignment : variant_call EQUALS variant_call
                          | variant_call EQUALS var_var
                          | variant_call EQUALS unary_expression
                          | variant_call EQUALS binary_expression'''
    p[0] = ast.VariantAssignment(p[1],p[3])

def p_variable(p):
    #                1         2        3     4     5     6
    ''' variable : VARIANT identifier LPAREN digit COMMA digit RPAREN'''
    p[0] = ast.Variant(p[2], p[4], p[6])

def p_variable_1(p):
    #                1           2      3     4     5       6    7        8    9         10       11
    ''' variable : VARIANT identifier LPAREN digit COMMA digit RPAREN EQUALS LBRACE var_full_list RBRACE '''
    #print(p[10])
    p[0] = ast.Variant(p[2],p[4],p[6],p[10])
    #print("p_variable_1")

def p_var_var(p):
    ''' var_var  : string
                 | bool
                 | digit'''
    p[0] = [(p[1])]

def p_print(p):
    ''' print : PRINT expression
              | PRINT identifier'''
    p[0] = ast.Printed(p[2])

def p_var_list(p):
    ''' var_list : var_list COMMA var_var
                 | var_var'''
    if len(p) > 2:
        p[1].append(p[3])
        p[0] = p[1]
    else : p[0] = p[1]

def p_var_fullbr(p):
    ''' var_fullbr : LBRACE var_full RBRACE'''
    p[0] = p[2]

def p_var_full(p):
    ''' var_full : var_full SEMICOLON var_list
                 | var_list'''
    if len(p) > 2:
        p[0] = [p[1] ,';', p[3]] #p[0] = [p[1] ,';', p[3]]
        #p[1].append(p[3])
        #p[0] = p[1]
    else: p[0] = p[1]

def p_var_full_list(p):
    ''' var_full_list : var_full_list COMMA var_fullbr
                      | var_fullbr '''
    if len(p) > 2:
        p[0] = [p[1] ,'|' ,p[3] ] #p[0] = [p[1] ,'|' ,p[3] ]
        #p[1].append(p[3])
        #p[0] = p[1]
    else : p[0] = p[1]

def p_string(p):
    ''' string : STRING '''
    p[0] = ast.String(p[1],None)

def p_digit(p):
    """ digit : DIGIT"""
    p[0] = ast.Digit( p[1], None)

def p_bool(p):
    ''' bool : TRUE
             | FALSE'''
    p[0] = ast.BOOL_TOF(p[1])

def p_error(p):
    print('Unexpected token ?:', p)

parser = yacc.yacc()

def build_tree(code):
    return parser.parse(code)
