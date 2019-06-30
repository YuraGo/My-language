import sys

from ply import lex
from ply.lex import TOKEN


class Lexer:

    def __init__(self, error_func):
        self.error_func = error_func
        self.filename = ''
        self.last_token = None

    def run(self):
        self.lexer = lex.lex(object=self)


    def reset_lineno(self):
        self.lexer.lineno = 1


    def input(self, text):
        self.lexer.input(text)


    def find_tok_column(self, token):
        last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
        return token.lexpos - last_cr


    def _error(self, msg, token):
        location = self._make_tok_location(token)
        self.error_func(msg, location[0], location[1])
        self.lexer.skip(1)


    def _make_tok_location(self, token):
        return (token.lineno, self.find_tok_column(token))

    tok = (
            'IFLESS','IFNLESS','IFZERO','IFNZERO','IFHIGH','IFNHIGH','THEN',
            'ENDIF','WHILE','UNTIL','ENDW','ENDU','COMMAND','TO','BOOL',
            'TRUE','FALSE','CONVERT','FUNC','ENDFUNC','RETURN','STRINGTYPE',
            'CALL','VARIANT','DIGITTYPE','PARAM','DIGITIZE','PRINT'
            )

    keyword_map = {}
    for keyword in tok:
        keyword_map[keyword] = keyword
    # keyword_map['FUNCTION'] = 'FUNCTION'

    tokens = tok + (
        'MINUS', 'PLUS',
        'LPAREN', 'RPAREN',
        'LBRACKET', 'RBRACKET',
        'LBRACE', 'RBRACE',
        'COMMA',
        'ID', 'NEWLINE',  'DIGIT',
        'EQUALS',
        'SEMICOLON','COLON',
        'TIMES','DIVIDE','STRING'
    )

    identifier = r'[a-zA-Z_][0-9a-zA-Z_]*'

    t_ignore = ' \t'

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
        return t

    t_DIGIT             = r'0|([1-9][0-9]*)'
    t_PLUS              = r'\+'
    t_MINUS             = r'\-'
    t_EQUALS            = r'='
    t_LPAREN            = r'\('
    t_RPAREN            = r'\)'
    t_LBRACKET          = r'\['
    t_RBRACKET          = r'\]'
    t_LBRACE            = r'\{'
    t_RBRACE            = r'\}'
    t_COMMA             = r','
    t_SEMICOLON         = r';'
    t_COLON             = r':'
    t_TIMES             = r'\*'
    t_DIVIDE            = r'/'


    @TOKEN(identifier)
    def t_ID(self, t):
        t.type = self.keyword_map.get(t.value, "ID")
        return t

    def t_STRING(self,t):
        r"'([^\\']+|\\'|\\\\)*'"
        #t.value = t.value[1:-1].decode("string-escape")
        #t.value = str(t.value)
        return t

    def t_error(self, t):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)

    def pprint(self):
        while True:
            tok = self.lexer.token()
            if not tok: break
            print(tok, "----->", tok.lexpos)
