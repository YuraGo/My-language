import parser
from parser import build_tree
import visit2_0


#data = '''
#IFLESS 5 THEN 6 :
#COMMAND "UP, DOWN"
#ENDIF
#'''
#VARIANT my(1,1) = {{TRUE,'str',2; FALSE,'check',22},{FALSE,'try',5}}
#my(1,1) = try(1,1)
#CONVERT STRINGTYPE TO DIGITTYPE my(1,1)




#VARIANT my(2,4) = {{TRUE,'str',2,1,98; FALSE,'check',45; TRUE,'s',6,1;  FALSE,'check',22},{FALSE,'try',5;'';2;0}}


#data = '''
#VARIANT my(2,4) = {{TRUE,'str',2,1,98; FALSE,'check',45; TRUE,'s',6,1;  FALSE,'check',22},{FALSE,'try',5;'';2;0}}
#VARIANT ty(1,1) = {{FALSE,'gik',2}}
#my(0,0) = tr(1,1)
#'''
#
# data = '''
# VARIANT my(2,4) = {{TRUE,'str',2,1,98; FALSE,'check',45; TRUE,'s',6,1; FALSE,'check',22},{FALSE,'try',5;'';2;0}}
# my(0,0) = -TRUE
#
#
# '''

# data = '''
# VARIANT my2(2,2)
# VARIANT asd(2,2) = { {FALSE,'tr',5 ; TRUE,'asf',46},{FALSE; TRUE,'rrrr',456} }
# VARIANT art(2,1) = { {TRUE,'art',999},{FALSE,'gg',777} }
# VARIANT frt(1,1) = { {TRUE,'tttt',888} }
# asd(5,3) = art(0,0)
# asd(4,0) = frt(0,0)
# asd(3,3) = asd(0,0)
# asd(7,5) = art(1,0)
# PRINT asd
# '''

# data = '''
# VARIANT asd(2,2) = { {FALSE,'tr',5 ; TRUE,'asf',46},{FALSE; TRUE,'rrrr',456} }
# VARIANT qwe(1,2) = { {TRUE,'qwe',99; TRUE,'zxc',77} }
# PRINT asd
# asd(3,3) = asd(0,0)
# PRINT asd
# '''

# data = '''
# VARIANT asd(2,2) = { {FALSE,'tr',0 ; TRUE,'asf',46},{FALSE; TRUE,'rrrr',456} }
# WHILE asd(0,1) :
#     asd(0,0) = asd(0,0) + 1
#     IFHIGH asd(0,0) THEN 5:
#         asd(0,1) = FALSE
#     ENDIF
#     PRINT asd
# ENDW
# '''

# data = '''
# VARIANT asd(2,2) = { {FALSE,'tr',0 ; TRUE,'asf',46},{FALSE; TRUE,'rrrr',456} }
# PRINT asd
# IFHIGH asd(0,0) THEN 5:
# asd(0,1) = FALSE
# ENDIF
# asd(0,0) = asd(0,0) + 8
# IFHIGH asd(0,0) THEN 5:
# asd(0,1) = FALSE
# ENDIF
# PRINT asd
# '''

#
# data = '''
# VARIANT asd(2,2) = { {FALSE,'tr',5 ; TRUE,'asf',46},{FALSE; TRUE,'rrrr',456} }
# VARIANT qwe(1,1) = { {55} }
# PRINT asd
# asd(0,0) = asd(0,0) + 'eee'
# PRINT asd
# asd(0,0) = asd(0,0) + 22
# PRINT qwe
# asd(0,0) = qwe(0,0) + 45
# PRINT asd
# asd(0,0) = asd(0,0) + 88
# '''

# data = '''
# VARIANT asd(2,2) = { {FALSE,'tfr458',5 ; TRUE,'FALSEasfTRUE',46},{FALSE; TRUE,'rrrr',456} }
# PRINT asd
# CONVERT STRINGTYPE TO DIGITTYPE asd(0,0)
# PRINT asd
# CONVERT STRINGTYPE TO BOOL asd(0,1)
# PRINT asd
# CONVERT BOOL TO STRINGTYPE asd(0,1)
# PRINT asd
# '''

# data='''
# VARIANT my(1,1)
# PRINT my
# IFLESS my(0,2) THEN 5:
# PRINT my
# CONVERT BOOL TO STRINGTYPE my(5,5)
# ENDIF
# PRINT my
# '''

# data = '''
# VARIANT asd(2,2) = { {FALSE,'tfr458',5 ; TRUE,'FALSEasfTRUE',46},{FALSE; TRUE,'rrrr',456} }
# PRINT asd
# DIGITIZE asd(0,0)
# PRINT asd
# CONVERT STRINGTYPE TO BOOL asd(0,1)
# PRINT asd
# '''

# data = '''
# FUNC Das:
#
# VARIANT asd(1,1) = {{99,'rar',TRUE}}
# VARIANT zxc(1,1)
# zxc = PARAM
# PRINT zxc
# RETURN zxc
# zxc(2,2) = asd(0,0)
# zxc(0,0) = asd(0,0)
# PRINT zxc
# RETURN zxc
# ENDFUNC
#
# VARIANT qwe(2,1) = { {55,FALSE,'foo'},{88,TRUE,'ggg'} }
# VARIANT gg(2,2) = {{45,TRUE,'ala';FALSE,111,'bad'},{456;1236}}
# PRINT qwe
# qwe = CALL Das (gg)
# PRINT qwe
# '''

# def factorial(x):
#     if x==1:
#         return 1
#     else:
#         z = x
#         x-=1
#         y = factorial(x)
#         y*=z
#         return y
#
# f=factorial(5)
# print ("factorial of 5 is ",f)



# data = '''
# FUNC gad:
# VARIANT()
# ENDFUNC
# '''

# data = '''
# VARIANT tr(1,1) = {{3,'factorial',TRUE}}
# tr(0,0) = tr(0,0) * tr(0,0)
# PRINT tr
# '''

# data = '''
# VARIANT tr(1,1) = {{0,'factorial',TRUE}}
# VARIANT qwe(1,1) = {{1,'factorial',TRUE}}
# VARIANT gg(3,2) = { {45,TRUE,'ala' ; FALSE,111,'bad'} , { 456,TRUE ; 1236,FALSE} , {55,FALSE,'foo' ; 88,TRUE,'ggg'} }
# PRINT gg
# gg(qwe(0,0),tr(0,0)) = qwe(tr(0,0),tr(0,0))
# PRINT gg
# '''


# data = '''
# FUNC factor:
# VARIANT count(1,1)
# VARIANT qwe(1,1)
# VARIANT new(1,1)
# count = PARAM
# PRINT count
# qwe(0,0) = count(0,0)
# IFNZERO (count(0,0)-1):
#     count(0,0) = count(0,0) - 1
#     PRINT count
#     new = CALL factor (count)
#     new(0,0) = new(0,0) * qwe(0,0)
#     RETURN new
# ENDIF
# IFNZERO (count(0,0)-1):
# RETURN count
# ENDIF
# ENDFUNC
#
# VARIANT tr(1,1) = {{3,'factorial',TRUE}}
# PRINT tr
# tr = CALL factor (tr)
# PRINT tr
# '''

data = '''
VARIANT card(3,3)
VARIANT com(1,1) = { {'UP RIGHT RIGHT',TRUE,2},{4} }
VARIANT str(1,1) = { {'asd www zxc 56 asd'} }
PRINT map
COMMAND com(0,0)
PRINT map
'''

result = build_tree(data)
#print(result)

exec = visit2_0.bypass_ast()
exec.Read()
exec.visit(result)
#exec.Print()
print(exec.decl_buf)
