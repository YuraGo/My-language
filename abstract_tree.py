import sys


def _repr(obj):
    if isinstance(obj, list):
        return '[' + (',\n '.join((_repr(e).replace('\n', '\n ') for e in obj))) + '\n]'
    else:
        return repr(obj)


class Unit:
    __slots__ = ()

    def __repr__(self):
        result = self.__class__.__name__ + '('

        indent = ''
        separator = ''
        for name in self.__slots__[:-2]:
            result += separator
            result += indent
            result += name + '=' + (
                _repr(getattr(self, name)).replace('\n', '\n  ' + (' ' * (len(name) + len(self.__class__.__name__)))))

            separator = ','
            indent = '\n ' + (' ' * len(self.__class__.__name__))

        result += indent + ')'

        return result



class Root(Unit):
    __slots__ = ('ext', 'coord', '__weakref__')
    def __init__(self, ext, coord=None):
        self.ext = ext
        self.coord = coord

class Digit(Unit):
    __slots__ = ( 'value', 'coord', '__weakref__')
    def __init__(self, value, coord=None):
        self.value = int(value)
        self.coord = coord

class String(Unit):
    __slots__= ('value','coord','__weakref__')
    def __init__(self,value,coord=None):
        self.value = value
        self.coord = coord

class FunctionDict(Unit):
    __slots__ = ('name','suite', 'coord', '__weakref__')
    def __init__(self, name, suite, coord=None):
        self.name = name
        self.suite = suite
        self.coord = coord
#---------no----\/---------------
class FunctionCall(Unit):
    __slots__ = ('name', 'suite', 'coord', '__weakref__')
    def __init__(self,  name,  suite, coord=None):
        self.name = name
        self.suite = suite
        self.coord = coord

class CallFunction(Unit):
    __slots__ = ('name', 'args' ,'callvar','coord', '__weakref__')
    def __init__(self, name, args,callvar=None ,coord=None):
        self.name = name
        self.args = args
        self.callvar = callvar

class Param(Unit):
    __slots__ = ('name', 'coord', '__weakref__')
    def __init__(self, name ,coord=None):
        self.name = name

class Return(Unit):
    __slots__ = ('name', 'coord', '__weakref__')
    def __init__(self, name ,coord=None):
        self.name = name

class If(Unit):
    __slots__ = ('cond','type','thenc' ,'iftrue', 'coord', '__weakref__')
    def __init__(self, type ,cond, thenc,iftrue, coord=None):
        self.cond = cond
        self.thenc = thenc
        self.iftrue = iftrue
        self.type = type
        self.coord = coord

class IfZero(Unit):
    __slots__ = ('cond','type','iftrue', 'coord', '__weakref__')
    def __init__(self, type ,cond,iftrue, coord=None):
        self.cond = cond
        self.iftrue = iftrue
        self.type = type
        self.coord = coord

class While(Unit):
    __slots__ = ('cond', 'stmt', 'coord', '__weakref__')
    def __init__(self, cond, stmt, coord=None):
        self.cond = cond
        self.stmt = stmt
        self.coord = coord

class Until(Unit):
    __slots__ = ('cond', 'stmt', 'coord', '__weakref__')
    def __init__(self, cond, stmt, coord=None):
        self.cond = cond
        self.stmt = stmt
        self.coord = coord

class Suite(Unit):
    __slots__ = ('block_items', 'coord', 'type','__weakref__')
    def __init__(self, block_items, type,coord=None):
        self.block_items = block_items
        self.coord = coord
        self.type = type

class Convert(Unit):
    __slots__ = ('setin', 'setout', 'array','__weakref__')
    def __init__(self, setin, setout,array,coord=None):
        self.setin = setin
        self.setout = setout
        self.array = array

class Digitize(Unit):
    __slots__ = ('array','__weakref__')
    def __init__(self,array,coord=None):
        self.array = array

class EmptyStatement(Unit):
    __slots__ = ('coord', '__weakref__')
    def __init__(self, coord=None):
        self.coord = coord

class BOOL_TOF(Unit):
    __slots__ = ('value', 'coord', '__weakref__')
    def __init__(self, value, coord=None):
        self.value = value

class Variant(Unit):
    __slots__ = ('name', 'ysize', 'xsize','list' ,'coord', '__weakref__')
    def __init__(self, name, ysize, xsize,list=None, coord=None):
        self.ysize = ysize
        self.xsize = xsize
        self.name = name
        self.list = list
        self.coord = coord

class Printed(Unit):
    __slots__ = ('value', 'coord', '__weakref__')
    def __init__(self, value, coord=None):
        self.value = value

class VariantCall(Unit):
    __slots__ = ('name', 'indexY','indexX', 'coord', '__weakref__')
    def __init__(self, name, indexY,indexX, coord=None):
        self.name = name
        self.indexY = indexY
        self.indexX = indexX
        self.coord = coord

class VariantAssignment(Unit):
    __slots__ = ('name1','name2', 'coord', '__weakref__')
    def __init__(self,name1,name2,coord=None):
        self.name1 = name1
        self.name2 = name2
        self.coord = coord

class BinaryOp(Unit):
    __slots__ = ('op', 'left', 'right', 'coord', '__weakref__')
    def __init__(self, op, left, right,coord=None):
        self.op = op
        self.left = left
        self.right = right
        self.coord = coord

class UnaryOp(Unit):
    __slots__ = ('obj', 'coord', '__weakref__')
    def __init__(self, obj, coord=None):
        self.obj = obj
        self.coord = coord

class RobotOperator(Unit):
    __slots__ = ('operator','ret_val','coord', '__weakref__')
    def __init__(self, ret_val ,operator, coord=None):
        self.operator = operator
        self.coord = coord
        self.ret_val = ret_val

class ID(Unit):
    __slots__ = ('name', 'coord', '__weakref__')
    def __init__(self, name, coord=None):
        self.name = name
        self.coord = coord
