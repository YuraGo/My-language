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
# UNTIL asd(0,1) :
#     asd(0,0) = asd(0,0) + 1
#     IFHIGH asd(0,0) THEN 5:
#         asd(0,1) = FALSE
#     ENDIF
#     PRINT asd
# ENDU
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
# FUNC Factor:
# VARIANT new[1,1]
# new = PARAM
# new[0,0] = new[0,0] - 1
# PRINT new
# IFZERO new[0,0]:
# PRINT new
# RETURN new
# ENDIF
# new = CALL Factor (new)
# ENDFUNC
#
# VARIANT tr[1,1] = {{3,'factorial',TRUE}}
# PRINT tr
# tr = CALL Factor (tr)
# PRINT tr
# '''


# data = '''
# FUNC Factor:
# VARIANT new[1,1]
# new = PARAM
# new[0,0] = new[0,0] - 1
# PRINT new
# RETURN new
# ENDFUNC
#
# VARIANT tr[1,1] = {{3,'factorial',TRUE}}
# PRINT tr
# tr = CALL Factor (tr)
# PRINT tr
# '''


# data = '''
# FUNC factor:
# VARIANT count[1,1]
# VARIANT qwe[1,1]
# VARIANT new[1,1]
# count = PARAM
# qwe[0,0] = count[0,0]
# IFNZERO (count[0,0]-1):
#     count[0,0] = count[0,0] - 1
#     new = CALL factor (count)
#     new[0,0] = new[0,0] * qwe[0,0]
#     RETURN new
# ENDIF
# IFZERO (count[0,0]-1):
# RETURN count
# ENDIF
# ENDFUNC
#
# VARIANT tr[1,1] = {{7,'factorial',TRUE}}
# PRINT tr
# tr = CALL factor (tr)
# PRINT tr
# '''


# def factorial(count):
#     if count==1:
#         return 1
#     else:
#         qwe = count
#         count-=1
#         new = factorial(count)
#         new*=qwe
#     return new
#
# f = factorial(7)
# print ("factorial of 5 is ",f)


# data = '''
# VARIANT com[1,1] = { {'LEFT LOOKDOWN',TRUE,2} }
# VARIANT str[2,2] = { {'asd www zxc 56 asd'},{'www',FALSE,88;99} }
# com[0,0] = com[0,0] + ' DOWN'
# PRINT str
# str[2,0] = COMMAND com[0,0]
# str[3,0] = COMMAND 'LOOKRIGHT'
# str[4,0] = COMMAND 'LOOKLEFT'
# str[5,0] = COMMAND 'LOOKUP'
# PRINT str
# PRINT map
# '''

data = '''
VARIANT lookR[2,1] = { {'LOOKRIGHT',2,FALSE},{'RIGHT',2,TRUE} }
VARIANT lookL[2,1] = { {'LOOKLEFT',2,FALSE},{'LEFT',2,TRUE} }
VARIANT lookD[2,1] = { {'LOOKDOWN',2,FALSE},{'DOWN',2,TRUE} }
VARIANT lookU[2,1] = { {'LOOKUP',2,FALSE},{'UP',2,TRUE} }
VARIANT pathArr[9,7]
VARIANT cicl[2,1] = {{TRUE,0,''},{TRUE,0,''}}
VARIANT countStr[1,1] = {{0,TRUE}}
VARIANT countRow[1,1] = {{0,TRUE}}
VARIANT help[1,1]
VARIANT extCord[1,2] = {{TRUE,'', 7; TRUE,'',1}}
VARIANT maxY[1,1] = {{9,'',TRUE}}
VARIANT maxX[1,1] = {{7,'',FALSE}}
VARIANT check[1,1]

cicl[1,0] = maxY[0,0] * maxX[0,0]
PRINT cicl
pathArr[2,2] = 'BOT'
VARIANT cord[1,2] = { {2,FALSE,'' ; 2,FALSE,''} }
VARIANT weight[1,1] = {{1,'',TRUE}}

PRINT map
WHILE cicl[0,0]:
    weight[0,0] = weight[0,0] + 1
    WHILE countStr[0,0]:
        WHILE countRow[0,0]:
        help[0,0] = weight[0,0] - 1
            IFZERO (fillmap[countStr[0,0], countRow[0,0]] - help[0,0]):

                IFHIGH countStr[0,0] THEN 0:
                    help[0,0] = countStr[0,0]
                    help[0,0] = help[0,0] - 1
                    IFZERO fillmap[ help[0,0], countRow[0,0] ]:
                        fillmap[ help[0,0], countRow[0,0] ] = weight[0,0]

                    ENDIF
                ENDIF

                IFLESS countStr[0,0] THEN (maxY[0,0] - 1):
                help[0,0] = countStr[0,0]
                help[0,0] = help[0,0] + 1
                    IFZERO fillmap[ help[0,0], countRow[0,0] ]:
                        fillmap[ help[0,0], countRow[0,0] ] = weight[0,0]

                    ENDIF
                ENDIF

                IFHIGH countRow[0,0] THEN 0:
                help[0,0] = countRow[0,0]
                help[0,0] = help[0,0] - 1
                    IFZERO fillmap[ countStr[0,0], help[0,0] ]:

                        fillmap[ countStr[0,0], help[0,0] ] = weight[0,0]

                    ENDIF
                ENDIF


                IFLESS countRow[0,0] THEN (maxX[0,0] - 1):
                help[0,0] = countRow[0,0]
                help[0,0] = help[0,0] + 1
                    IFZERO fillmap[ countStr[0,0], help[0,0] ]:
                        fillmap[ countStr[0,0], help[0,0] ] = weight[0,0]

                    ENDIF
                ENDIF


                help[0,0] = countStr[0,0] - extCord[0,0]
                help[0,1] = countRow[0,0] - extCord[0,1]
                IFLESS help[0,0] THEN 0:
                    help[0,0] = - help[0,0]
                ENDIF
                IFLESS help[0,1] THEN 0:
                    help[0,1] = - help[0,1]
                ENDIF
                help[0,0] = help[0,0] + help[0,1]
                IFZERO (help[0,0] - 1):
                    PRINT cicl
                    fillmap[extCord[0,0],extCord[0,1]] = weight[0,0]
                    cicl[0,0] = FALSE
                ENDIF
            ENDIF
        countRow[0,0] = countRow[0,0] + 1
        IFNLESS countRow[0,0] THEN maxX[0,0]:
            countRow[0,0] = FALSE
        ENDIF
        ENDW

    countRow[0,0] = 0
    countRow[0,0] = TRUE
    countStr[0,0] = countStr[0,0] + 1
    IFNLESS countStr[0,0] THEN maxY[0,0]:
        countStr[0,0] = FALSE
    ENDIF
    ENDW

    countStr[0,0] = 0
    countStr[0,0] = TRUE
    cicl[0,0] = cicl[0,0] + 1
    IFNLESS cicl[0,0] THEN cicl[1,0]:
        cicl[0,0] = FALSE
    ENDIF
ENDW
fillmap[7,1] = 'EXIT'
PRINT fillmap

VARIANT skip[1,1] = {{TRUE,0,''}}
PRINT weight
VARIANT com[1,1]



WHILE weight[0,0]:
    weight[0,0] = weight[0,0] - 1
    skip[0,0] = 0
    IFHIGH extCord[0,0] THEN 0:
        help[0,0] = extCord[0,0]
        help[0,0] = help[0,0] - 1
        IFZERO fillmap[ help[0,0], extCord[0,1] ] - weight[0,0]:
            extCord[0,0] = extCord[0,0] - 1
            com[0,0] = com[0,0] + 'DOWN '
            skip[0,0] = 1
        ENDIF
    ENDIF
    IFZERO skip[0,0]:
        help[0,0] = maxY[0,0] - 1
        IFLESS extCord[0,0] THEN help[0,0]:
            help[0,0] = extCord[0,0]
            help[0,0] = help[0,0] + 1
            IFZERO fillmap[ help[0,0], extCord[0,1]] - weight[0,0]:
                extCord[0,0] = extCord[0,0] + 1
                com[0,0] = com[0,0] + 'UP '
                skip[0,0] = 1
            ENDIF
        ENDIF
    ENDIF

    IFZERO skip[0,0]:

        IFHIGH extCord[0,1] THEN 0:
            help[0,0] = extCord[0,1]
            help[0,0] = help[0,0] - 1
            IFZERO fillmap[ extCord[0,0],  help[0,0]] - weight[0,0]:
                extCord[0,1] = extCord[0,1] - 1
                com[0,0] = com[0,0] + 'LEFT '
                skip[0,0] = 1
            ENDIF
        ENDIF
    ENDIF

    IFZERO skip[0,0]:
        help[0,0] = maxX[0,0] - 1
        IFLESS extCord[0,1] THEN help[0,0]:
            help[0,0] = extCord[0,1]
            help[0,0] = help[0,0] + 1
            IFZERO fillmap[ extCord[0,0], help[0,0] ] - weight[0,0]:
                extCord[0,1] = extCord[0,1] + 1
                com[0,0] = com[0,0] + 'RIGHT '
            ENDIF
        ENDIF
    ENDIF

IFZERO weight[0,0]:
    weight[0,0] = FALSE
ENDIF

ENDW

PRINT com[0,0]
PRINT map
'''




result = build_tree(data)
#print(result)

exec = visit2_0.bypass_ast()
exec.Read()
exec.visit(result)
#exec.Print()
#print(exec.decl_buf)
