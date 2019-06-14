import copy

import abstract_tree as ast

from parser import function_dict

class bypass_ast:

    def __init__(self, error_flag=False,ret_flag=False):

        self.decl_buf = {'global' : {}}

        self._error_flag = error_flag

        self._ret_flag = ret_flag

        self._global_count = 0

        self.robot_commands = [ 'UP','DOWN','LEFT','RIGHT','LOOKUP','LOOKDOWN','LOOKLEFT','LOOKRIGHT' ]

        self.iter = 0

        self.operators = {
            '-'  : lambda x, y: x - y,
            '+'  : lambda x, y: x + y,
            '*'  : lambda x, y: x * y,
            '/'  : lambda x, y: x / y
        }

        self.robot_coord = [2, 2]

    def Read(self):
        self.decl_buf['global']['map'] = [[['WALL',-1,False], ['WALL',-1,False], ['WALL',-1,False], ['WALL',-1,False], ['WALL',-1,False], ['WALL',-1,False],  ['WALL',-1,False]],
                                          [['WALL',-1,False], ['',0,True],      ['',0,True],      ['',0,True],      ['',0,True],      ['',0,True],       ['WALL',-1,False]],
                                          [['WALL',-1,False], ['',0,True],      ['',0,True],      ['',0,True],      ['',0,True],      ['',0,True],       ['WALL',-1,False]],
                                          [['WALL',-1,False], ['',0,True],      ['',0,True],      ['WALL',-1,False],['',0,True],      ['',0,True],       ['WALL',-1,False]],
                                          [['WALL',-1,False], ['',0,True],      ['',0,True],      ['WALL',-1,False],['',0,True],      ['',0,True],       ['WALL',-1,False]],
                                          [['WALL',-1,False], ['WALL',-1,False],['WALL',-1,False],['WALL',-1,False],['',0,True],      ['',0,True],       ['WALL',-1,False]],
                                          [['WALL',-1,False], ['',0,True],      ['WALL',-1,False],['WALL',-1,False],['',0,True],      ['',0,True],       ['WALL',-1,False]],
                                          [['WALL',-1,False], ['EXIT',0,True],  ['',0,True],      ['',0,True],      ['',0,True],      ['',0,True],       ['WALL',-1,False]],
                                          [['WALL',-1,False], ['WALL',-1,False],['WALL',-1,False], ['WALL',-1,False], ['WALL',-1,False], ['WALL',-1,False],  ['WALL',-1,False]]  ]

        self.decl_buf['global']['map'][self.robot_coord[0]][self.robot_coord[1]] = ['BOT',1,True]
        self.decl_buf['global']['fillmap'] = copy.deepcopy(self.decl_buf['global']['map'])

    def wall_check(self,i,j,look=None):
        #print(self.decl_buf['global']['map'][i][j])
        for point in self.decl_buf['global']['map'][i][j]:
            if point == 'WALL':
                return False,look
            if point == 'EXIT' and look == False:
                print('*****************************************************')
                print('<<<<<<<<<<<<<<<<<<< Exit reached! >>>>>>>>>>>>>>>>>>>')
                print('*****************************************************')
                print('')
                self._error_flag = True
                self._ret_flag = True
                return True,True
            if point == 'EXIT' and look == True:
                return True,True
        return True,False

    def update_map(self, new_i, new_j,look=None):
        flag,exit = self.wall_check(new_i, new_j,look)
        if flag == False and look != True:
            return False
        if look == True:
            return flag,exit

        i = self.robot_coord[0]
        j = self.robot_coord[1]
        self.decl_buf['global']['map'][i][j] = ['',0,True]
        self.decl_buf['global']['map'][new_i][new_j] = ['BOT',8,True]
        self.robot_coord[0] = new_i
        self.robot_coord[1] = new_j
        return True

    def visit_RobotOperator(self, n, scope_name='global',typo=None):
        if self._error_flag:
            return
        if self._ret_flag:
            return
        #print('ret_val: ',n.ret_val)
        comand = self.visit(n.operator,scope_name,typo='str')

        check_command = []
        if comand.find(' ') > -1:
            check_command = comand.split(' ')
        else:
            check_command.append(comand)
        #print('oper: ',comand)

        for chr in check_command:
            if chr not in self.robot_commands:
                print('This command does not exist > ', chr)
                self._error_flag = True
                return

        result = []
        retvar = []
        for robot in check_command:
            if self._error_flag:
                return
            if self._ret_flag:
                return
            retvar = (self.robot_act(robot))
        #print('ret: ',retvar,type(retvar[0]))
            if type(retvar[0]) == list:
                #print('list: ',retvar)
                for it in retvar:
                    result.append(it)
            else:
                result.append(retvar)
        #print('!!! res: ',result)

        #result  = retvar
        return result

    def visit(self, node, scope_name='global',typo=None):
        function_name = 'visit_' + node.__class__.__name__
        #print(function_name)
        return getattr(self, function_name)(node, scope_name,typo)#without typo

    def Print(self):
        for i in self.decl_buf['global']['map'][1]:
            print(i)

    def robot_act(self,operator):
        if operator == 'UP':
            if self.update_map(self.robot_coord[0] - 1, self.robot_coord[1]):
                return [True,0,'']
            else: return [False,0,'']
        if operator == 'DOWN':
            if self.update_map(self.robot_coord[0] + 1, self.robot_coord[1]):
                return [True,0,'']
            else: return [False,0,'']
        if operator == 'LEFT':
            if self.update_map(self.robot_coord[0], self.robot_coord[1] - 1):
                return [True,0,'']
            else: return [False,0,'']
        if operator == 'RIGHT':
            if self.update_map(self.robot_coord[0], self.robot_coord[1] + 1):
                return [True,0,'']
            else: return [False,0,'']
        if operator == 'LOOKDOWN':
            ers = True
            result = []
            count = 0
            art = []
            while ers: # Floor = True, False ; WALL = False,True; EXIT = True,True
                flag,exit = self.update_map(self.robot_coord[0] + 1 + count, self.robot_coord[1],True)
                if flag == True and exit == False:
                    count+=1
                if flag == True and exit == True:
                    count+=1
                    arrexit=[True,count,'EXIT']
                    art.append(arrexit)
                if flag == False and exit == True:
                    count+=1
                    result+=[False,count,'WALL']
                    art.append(result)
                    ers = False
                    #print('art: ',art)
                    return art
        if operator == 'LOOKUP':
            ers = True
            result = []
            count = 0
            art = []
            while ers: # Floor = True, False ; WALL = False,True; EXIT = True,True
                flag,exit = self.update_map(self.robot_coord[0] - 1 - count, self.robot_coord[1],True)
                if flag == True and exit == False:
                    count+=1
                if flag == True and exit == True:
                    count+=1
                    arrexit=[True,count,'EXIT']
                    art.append(arrexit)
                if flag == False and exit == True:
                    count+=1
                    result+=[False,count,'WALL']
                    art.append(result)
                    ers = False
                    #print('art: ',art)
                    return art
        if operator == 'LOOKRIGHT':
            ers = True
            result = []
            count = 0
            art = []
            while ers: # Floor = True, False ; WALL = False,True; EXIT = True,True
                flag,exit = self.update_map(self.robot_coord[0], self.robot_coord[1] + 1 + count,True)
                if flag == True and exit == False:
                    count+=1
                if flag == True and exit == True:
                    count+=1
                    arrexit=[True,count,'EXIT']
                    art.append(arrexit)
                if flag == False and exit == True:
                    count+=1
                    result+=[False,count,'WALL']
                    art.append(result)
                    ers = False
                    #print('art: ',art)
                    return art
        if operator == 'LOOKLEFT':
            ers = True
            result = []
            count = 0
            art = []
            while ers: # Floor = True, False ; WALL = False,True; EXIT = True,True
                flag,exit = self.update_map(self.robot_coord[0], self.robot_coord[1] - 1 - count,True)
                if flag == True and exit == False:
                    count+=1
                if flag == True and exit == True:
                    count+=1
                    arrexit=[True,count,'EXIT']
                    art.append(arrexit)
                if flag == False and exit == True:
                    count+=1
                    result+=[False,count,'WALL']
                    art.append(result)
                    ers = False
                    #print('art: ',art)
                    return art

    def visit_BOOL_TOF(self, n, scope_name='global',typo=None):
        if n.value == 'TRUE':
            return True
        return False

    def visit_Digit(self, n, scope_name='global',typo=None):
        return (int(n.value))

    def visit_String(self, n, scope_name='global',typo=None):
        if self._ret_flag == True:
            return
        n.value = n.value[1:-1]
        return n.value
        #return (str(n.value))

    def visit_Root(self, n, scope_name='global',typo=None):
        for ext in n.ext:
            self.visit(ext)

    def visit_ID(self, n, scope_name='global',typo=None):
        if self._ret_flag == True:
            return
        #print('visit_ID: ',self.decl_buf[scope_name])
        #print('scope: ',scope_name)

        check = self.decl_buf[scope_name].get(n.name) #get возвращает None если элемент не существует
        #print('check:', check)
        if not check:
            ref = self.decl_buf['global'].get(n.name)
            if not ref:
                print("Undeclared id -> {}".format(n.name))
                self._error_flag = True
                return None
            return ref
        return check

    def visit_While(self, n, scope_name='global',typo=None):
        if self._ret_flag == True:
            return
        cnt = 0
        #print(n.cond)
        condition = self.visit(n.cond, scope_name,'bool')
        #print(condition)
        if type(n.cond) == ast.ID:
            if not condition:
                self._error_flag = True
                return
            #condition = condition[1]
        #return
        while condition:
            if cnt == 100000:
                print("Runtime error at ")
                self._error_flag = True
                return
            cnt += 1

            ret = self.visit(n.stmt,scope_name)
            #print(ret)
            if ret is not None:
                return ret

            condition = self.visit(n.cond, scope_name,'bool')
            if type(n.cond) == ast.ID:
                if not condition:
                    self._error_flag = True
                    return

    def visit_Until(self, n, scope_name='global',typo=None):
        if self._ret_flag == True:
            return
        cnt = 0
        #print(n.cond)
        condition = self.visit(n.cond, scope_name,'bool')
        print(condition)
        if type(n.cond) == ast.ID:
            if not condition:
                self._error_flag = True
                return
            #condition = condition[1]
        #return
        while condition:
            if cnt == 100000:
                print("Runtime error at ")
                self._error_flag = True
                return
            cnt += 1

            ret = self.visit(n.stmt,scope_name)
            #print(ret)
            if ret is not None:
                return ret
            condition = self.visit(n.cond, scope_name,'bool')
            if type(n.cond) == ast.ID:
                if not condition:
                    self._error_flag = True
                    return
        self.visit(n.stmt,scope_name)

    def visit_Suite(self, n,scope_name='global',typo=None):
        #print("BLOCK", n.block_items)
        if self._ret_flag == True:
            return
        if n.block_items == None:
            return
        for item in n.block_items:
            if type(item) in (ast.ID, ast.Digit):
                print("Error at {}: {} without target occured".format(item.coord, type(item)))
                self._error_flag = True
                continue
            #print('check')
            self.visit(item, scope_name,typo)

    def visit_IfZero(self, n, scope_name='global',typo=None):
        if self._error_flag:
            pass
        cond = self.visit(n.cond, scope_name,'digit')
        if n.type == 'IFZERO':
            flag = True
            if cond == 0:
                #print('yaaa')
                return self.visit_Suite(n.iftrue,scope_name)
            else : condition = None
        if n.type == 'IFNZERO':
            flag = True
            #print('IFNZERO cond: ',cond)
            if cond != 0:
                return self.visit_Suite(n.iftrue,scope_name)
            else : condition = None

        #if not condition:
            #self._error_flag = True
        return

    def visit_If(self, n, scope_name='global',typo=None):
        if self._ret_flag == True:
            return
        if self._error_flag:
            print('_error_flag in If')
            return
        flag = False
        #print(n)
        condleft = self.visit(n.cond,scope_name,'digit')
        #condleft = self.visit(n.cond,scope_name=scope_name,'digit')
        condright = self.visit(n.thenc,scope_name,'digit')
        #print(condleft)
        #print(condright)

        if n.type == 'IFLESS':
            flag = True
            if condleft < condright:
                return self.visit_Suite(n.iftrue,scope_name)
            else : return
        if n.type == 'IFNLESS':
            flag = True
            if condleft >= condright:
                return self.visit_Suite(n.iftrue,scope_name)
            else : return
        if n.type == 'IFHIGH':
            flag = True
            if condleft > condright:
                #print('yaaa')
                return self.visit_Suite(n.iftrue,scope_name)
            else : return
        if n.type == 'IFNHIGH':
            flag = True
            if condleft <= condright:
                stmt = self.visit_Suite(n.iftrue,scope_name)
                #print('rrrrrrrr',stmt)
                return stmt
            else : return

        if not condition:
            self._error_flag = True
            print('if???')
            return

    def visit_BinaryOp(self,n,scope_name='global',typo=None):
        #print('BinnOP')
        #print(self._error_flag)
        if self._ret_flag == True:
            return
        if self._error_flag:
            print('_error_flag in BinaryOp')
            return
        #print(n.left)
        rvalue = self.visit(n.right, scope_name,'digit')
        #print('Type r: ',rvalue)

        #lvalue = self.visit(n.left, scope_name,'str')
        #print('Type r: ',rvalue)

        if type(rvalue) == str:
            lvalue = self.visit(n.left, scope_name,'str')
        elif type(rvalue) == int:
            lvalue = self.visit(n.left, scope_name,'digit')
        else:
            lvalue = self.visit(n.left, scope_name,'digit')


        check = self.operators[n.op](lvalue, rvalue)
        #print('result:',check)
        return check

    def visit_Variant(self,n,scope_name='global',typo=None):
        if self._ret_flag == True:
            return
        VarName = n.name.name
        #print(VarName)
        #print("a vot i variant : ")
        #print(n.list)

        if self.decl_buf[scope_name].get(VarName):
            print("Error at {}: redefinition of variable {} ".format(VarName, scope_name))
            self._error_flag = True
            return
        #if (n.xsize != None or n.ysize != None) or (n.xsize != None and n.ysize != None):
        Ysize = self.visit(n.ysize, scope_name)
        Xsize = self.visit(n.xsize, scope_name)
        #print('tyt> ',Ysize,Xsize)
        #n.ysize = Ysize
        #n.xsize = Xsize
        array = [[0]*Xsize for i in range(Ysize)] #create array
        if n.list != None:
            showstring = ''
            tr = 0
            for check in str(n.list):
                showstring+=check

            #print(showstring)
            showstring = showstring.replace('\n','')
            showstring = showstring.replace('  ','')
            showstring = showstring.replace(',',', ')
            showstring = showstring.replace("'","")
            showstring = showstring.replace('Digit(value=','')
            showstring = showstring.replace('[BOOL_TOF(value=','')
            showstring = showstring.replace('[String(value=','')
            showstring = showstring.replace('(','')
            showstring = showstring.replace('[','')
            showstring = showstring.replace(']','')
            showstring = showstring.replace(')','')
            showstring = showstring.replace(', ;,',' ;')
            #showstring = showstring.replace(',','')
            #showstring = showstring.replace('"','')
            showstring = showstring.split(',')
            #print('string: ',showstring)

            i = 0
            j = 0
            arr = []
            for it in showstring:
                #print('it :',it)
                if ';' in it:
                    arr = []
                    j+=1
                    continue
                #if it == '|':
                if '|' in it:
                    arr = []
                    j = 0
                    i+=1
                    continue
                #print('after: ',it,j,i)
                arr.append(it)
                array[i][j] = arr  #self.visit(it,scope_name)

            #print('arr: ',array)
            #if (array[0][0])!=0:
                #print('elem: ',array[0][0][0])

                # for i in range(len(array)):
                #     for j in range(len(array[i])):
                #         for k in range(len(array[i][j])):
                #             break
                        #array[i][j][k] = array[i][j][k].replace("'",'')

        #print('arr2: ',array)


        strFlag = False
        digitFlag = False
        boolFlag = False
        #print(array)
        for i in range(len(array)):
           for j in range(len(array[i])):
               strFlag = False
               digitFlag = False
               boolFlag = False
               if array[i][j]:

                   for k in range(len(array[i][j])):
                       #print('tyt: ',array[i][j][k])
                       if '"' not in array[i][j][k]:
                           array[i][j][k] = array[i][j][k].replace(' ','')
                       else:
                           flag1q = False
                           flag2q = False
                           point = ''
                           for iter in array[i][j][k]:
                               if flag1q and flag2q:
                                   break
                               if iter == '"' and flag1q==False:
                                   flag1q = True
                                   continue
                               if iter == '"' and flag1q==True:
                                   flag2q = True
                                   continue
                               if flag1q:
                                   point+=iter
                           array[i][j][k] = point
                       if array[i][j][k].isdigit():
                           digitFlag = True
                           array[i][j][k] = (int(array[i][j][k]))
                       elif array[i][j][k] == 'TRUE':
                           boolFlag = True
                           array[i][j][k] = True
                       elif array[i][j][k] == 'FALSE':
                           boolFlag = True
                           array[i][j][k] = False
                       else: strFlag = True
                   if strFlag == False:
                       strFlag = True
                       array[i][j].append('')
                   if boolFlag == False:
                       boolFlag = True
                       array[i][j].append(False)
                   if digitFlag == False:
                       digitFlag = True
                       array[i][j].append(0)
               else:
                   array[i][j] = []
                   array[i][j].append(False)
                   array[i][j].append('')
                   array[i][j].append(0)



        #print(array)
        n.list = (array)
        self.decl_buf[scope_name][VarName] = (n.list)
        #print(n.list[0][1])
        pass

    def visit_VariantCall(self,n,scope_name='global',typo=None):
        arrayName = n.name.name
        if self._ret_flag == True:
            return
        #print('Name : ' , arrayName)
        if not self.check_dict(arrayName, scope_name):
            print('Error variantCall')
            return
        value_t = (self.decl_buf[scope_name].get(arrayName))
        # mb need some check for array
        #print('index: ',n.indexY)
        Yindex = self.visit(n.indexY, scope_name,'digit')
        Xindex = self.visit(n.indexX, scope_name,'digit')
        #print('rdy: ',Yindex)
        appList = [False,'',0]
        flagY = False
        flagX = False
        if Yindex >= len(value_t):
            flagY = True
        if Xindex >= len(value_t[0]):
            flagX = True
        # print('start')
        # for k in range(len(value_t)):
        #     print(value_t[k])
        #     print('')

        #print('++++++')
        #if flagX and flagY:
                    #print(value_t[i])
        #flagX = True
        #if Yindex >= len(value_t):
            #listAll = ([appList]*(Xindex + flagX))
            #print('rang',Xindex + flagX - len(value_t[1]))
        if flagY:
            for j in range(Yindex + flagY - len(value_t)):
                value_t.append([[False,'',0]])
                self.Variant_extend(value_t)
        #
        # print('+++++++++++++++++')
        # for k in range(len(value_t)):
        #     print(value_t[k])
        #     print('')
        # print('end==================')
        if flagX:
            for i in range(len(value_t)):
                leng = len(value_t[i])
                for j in range(Xindex + flagX - leng):
                    #print(value_t[i])
                    #print('j: ',j)
                    value_t[i].append([False,'',0])
                    #value_t.append([([False,'',0])]*(Xindex+1))
            # for k in range(Xindex):
            #     value_t[j].append([False,'',0])
                #for i in range(Xindex + flagX - len(value_t[j])):
                    #value_t[j].append([False,'',0])
        # print('+++++++++++++++++')
        # for k in range(len(value_t)):
        #     print(value_t[k])
        #     print('')
        # print('end==================')
        if typo == 'digit':
            for check in reversed(value_t[Yindex][Xindex]):
                if type(check) == int:
                    #print(check)
                    return check
        if typo == 'bool':
            for check in reversed(value_t[Yindex][Xindex]):
                #print(type(check))
                if type(check) == bool:
                    #print(check)
                    return check
        if typo == 'str':
            for check in reversed(value_t[Yindex][Xindex]):
                if type(check) == str:
                    #print(check)
                    return check

        return value_t[Yindex][Xindex]

    def visit_Digitize(self,n,scope_name='global',typo=None):
        if self._ret_flag == True:
            return
        varArr = self.visit(n.array,scope_name)
        tmp = ''
        i = (len(varArr))-1
        while i >= 0:
            if type(varArr[i]) == bool:
                varArr[i] = (int(varArr[i]))
            if type(varArr[i]) == str:
                for j in range(len(varArr[i])):
                    if varArr[i][j].isdigit():
                        tmp+=varArr[i][j]
                        if j+1 < len(varArr[i]):
                            if varArr[i][j+1].isdigit() == False:
                                varArr[i] = int(tmp)
                                break
                        else :
                            varArr[i] = int(tmp)
                            break
            i-=1
        return
    # some errors? +it
    def visit_Convert(self,n,scope_name='global',typo=None):
        #print('? --->')
        #print(n.array)
        if self._ret_flag == True:
            return
        varArr = self.visit(n.array,scope_name)
        #print('convert: ',varArr)

        if n.setin == 'BOOL':
            if n.setout == 'DIGITTYPE':
                i = (len(varArr))-1
                while i != -1:
                    if type(varArr[i]) == bool:
                        varArr[i] = (int(varArr[i]))
                        return varArr
                    i-=1
                        #print('bool to dig',varArr[i])
            if n.setout == 'STRINGTYPE':
                i = (len(varArr))-1
                print('booool: ',varArr)
                while i != -1:
                    #print(type(check))
                    if type(varArr[i]) == bool:
                        varArr[i] = (str(varArr[i]))
                        #print('return: ',varArr)
                        return varArr
                    i-=1
                        #print(type(check))
                        #print('bool to str',check)
        if n.setin == 'DIGITTYPE':
            if n.setout == 'BOOL':
                i = (len(varArr))-1
                while i != 1:
                    if type(varArr[i]) == int and (varArr[i] == 1 or varArr[i] == 0):
                        varArr[i] = (bool(varArr[i]))
                        return varArr
                    i-=1
                        #print('dig to bool',varArr[i])
            if n.setout == 'STRINGTYPE':
                i = (len(varArr))-1
                while i != -1:
                    if type(varArr[i]) == int:
                        varArr[i] = (str(varArr[i]))
                        return varArr
                    i-=1
        if n.setin == 'STRINGTYPE':
            if n.setout == 'DIGITTYPE':
                tmp = ''
                i = (len(varArr))-1
                while i != 0:
                    if type(varArr[i]) == str:
                        for j in range(len(varArr[i])):
                            if varArr[i][j].isdigit():
                                tmp+=varArr[i][j]
                                if j+1 < len(varArr[i]):
                                    if varArr[i][j+1].isdigit() == False:
                                        varArr[i] = int(tmp)
                                        return
                                else :
                                    varArr[i] = int(tmp)
                                    return
                    i-=1
            if n.setout == 'BOOL':
                tmp = ''
                i = (len(varArr))-1
                while i != 0:
                    if type(varArr[i]) == str:
                        flag = (varArr[i].find('TRUE'))
                        if flag !=-1 and flag < varArr[i].find('FALSE'):
                            varArr[i] = True
                            return varArr
                        flag = (varArr[i].find('FALSE'))
                        if flag !=-1:
                            varArr[i] = False
                            return varArr
                    i-=1


        #print('bool to str',varArr[i])
        return varArr

    def visit_VariantAssignment(self,n,scope_name='global',typo=None):
        #print(n.name1)
        if self._ret_flag == True:
            return
        array1 = n.name1.name.name
        if not self.check_dict(array1, scope_name):
            print('Error variantCall')
            return
        value_1 = (self.decl_buf[scope_name].get(array1))
        #print(array1)
        Xindex1,Yindex1,flag = self.check_varCall(n.name1,value_1,scope_name)
        #print('name1: ',n.name1.indexX)
        if type(n.name1.indexX) == ast.VariantCall:
            Xindex1 = self.visit_VariantCall(n.name1.indexX,scope_name,'digit')
        if type(n.name1.indexY) == ast.VariantCall:
            Yindex1 = self.visit_VariantCall(n.name1.indexY,scope_name,'digit')
        #print('X: ',Xindex1)
        if flag == False:
            return
        pip = (self.visit(n.name1,scope_name,None))
        #print('pip:',pip)
        if isinstance(n.name2,list):
            newVar = self.visit(n.name2[0],scope_name,None)
            typo = (n.name2[0].value)
            #print('>>>> ',newVar,typo,type(newVar))
        elif type(n.name2)==ast.UnaryOp:
            newVar = (self.visit(n.name2,scope_name))
        elif type(n.name2) == ast.BinaryOp:
            newVar = self.visit(n.name2,scope_name) # typo = 'digit'
        elif type(n.name2) == ast.RobotOperator:
            newVar = self.visit(n.name2,scope_name)
            #value_1[0].append(newVar)
            i = 0
            lengY = len(value_1)
            lengX = len(value_1[Yindex1])
            for it in newVar:
                #print('war: ',it)
                if Yindex1 < lengY:
                    if Xindex1 < len(value_1[Yindex1]):
                        value_1[Yindex1][Xindex1] = it
                    else:
                        value_1[Yindex1].append(it)
                else:
                    value_1[Yindex1].append(it)
                #print(value_1[Yindex1])
                Xindex1+=1
            self.Variant_extend(value_1)
            return
            #print('var',newVar)
            #print(n.name2.obj[0].value)
            #newVar = n.name2.obj[0].value
        else : typo = 'var'
        #print(typo)


        if typo == 'var':
            #print(n.name2)
            #array2 = self.visit(n.name2,scope_name,None)
            #print('aaaaaa',array2)
            if n.name2.name.name:
                array2 = n.name2.name.name
                if not self.check_dict(array2, scope_name):
                    print('Error variantCall(410 line)')
                    return

            value_2 = self.decl_buf[scope_name].get(array2)
            #print('array2: ', value_2)
            Xindex2,Yindex2,flag = self.check_varCall(n.name2,value_2,scope_name)
            if type(n.name2.indexX) == ast.VariantCall:
                Xindex2 = self.visit_VariantCall(n.name2.indexX,scope_name,'digit')
            if type(n.name2.indexY) == ast.VariantCall:
                Yindex2 = self.visit_VariantCall(n.name2.indexY,scope_name,'digit')
            if flag == False:
                return
            #
            # print('lllllllllllllll')
            # for k in range(len(value_1)):
            #     print(value_1[k])
            #     print('')
            # print('result: ')

            value_1[Yindex1][Xindex1] = copy.deepcopy(value_2[Yindex2][Xindex2])

            # for k in range(len(value_1)):
            #     print(value_1[k])
            #     print('')

            return value_1

        i = (len(value_1[Yindex1][Xindex1]))-1
        while i != -1:
            #print(value_1[Yindex1][Xindex1][i])
            # if type(value_1[Yindex1][Xindex1][i]) == type(newVar) : # and (value_1[Yindex1][Xindex1][i] != True or value_1[Yindex1][Xindex1][i]!= False):
            #     value_1[Yindex1][Xindex1][i] = (newVar)
            #     return value_1
            # if type(value_1[Yindex1][Xindex1][i]) == type(newVar):
            #     value_1[Yindex1][Xindex1][i] = (newVar)
            #     return value_1
            if type(value_1[Yindex1][Xindex1][i]) == type(newVar):
                #if typo == 'TRUE':
                value_1[Yindex1][Xindex1][i] = newVar
                #else : value_1[Yindex1][Xindex1][i] = (False)
                return value_1
            i-=1

        return value_1

    def check_dict(self, name, scope_name='global',typo=None):

        if not self.decl_buf[scope_name].get(name):
            print("Existing error")
            self._error_flag = True
            return False
        return True

    def check_varCall(self,array,value,scope_name='global'):
        Yindex = self.visit(array.indexY, scope_name)
        Xindex = self.visit(array.indexX, scope_name)
        # if Yindex >= len(value):
        #     print('IndexError - varcall')
        #     return None,None,False
        # if Xindex >= len(value[0]):
        #     print('IndexError - varcall')
        #     return None,None,False
        return Xindex,Yindex,True

    def visit_UnaryOp(self,n,scope_name='global',typo=None):
        #print(n.obj)
        if self._ret_flag == True:
            return

        if isinstance(n.obj,list):
            varname = (self.visit(n.obj[0],scope_name))
            #print('tyt?',varname)
            #typo = self.check_typo(n.obj[0].value)
            #print(type(varname))
            #if typo == 'int':
            if type(varname) == int:
                return -varname
            elif type(varname) == str:
                return varname
            elif type(varname) == bool:
                if varname == True:
                    return False
                else: return True
                #var = self.visit(n.obj[0].value,scope_name,None)
                #print('vart ',var)
        typo = 'var'

        if typo == 'var':
            array = n.obj.name.name
            #print(array)
            if not self.check_dict(array, scope_name):
                print('Error variantCall')
                return
            value = (self.decl_buf[scope_name].get(array))
            #print(value)
            Xindex,Yindex,flag = self.check_varCall(n.obj,value,scope_name)
            if flag == False:
                self._error_flag = True
                return
            #print(Xindex,Yindex)

            i = (len(value[Yindex][Xindex]))-1
            #print(type(value[Yindex][Xindex][1]))
            while i != -1:
                #print(value[Yindex][Xindex][i])
                if type(value[Yindex][Xindex][i])==int:# and value[Yindex][Xindex][i] != True and value[Yindex][Xindex][i] != False:
                    var = value[Yindex][Xindex][i]
                    #print('var:',var)
                    value[Yindex][Xindex][i] = -var
                if type(value[Yindex][Xindex][i])==str:
                    value[Yindex][Xindex][i] = (value[Yindex][Xindex][i])
                if type(value[Yindex][Xindex][i])==bool:
                    if value[Yindex][Xindex][i] == True:
                        value[Yindex][Xindex][i] = (False)
                    else :
                        value[Yindex][Xindex][i] = (True)
                i-=1
        #print(type(value))
        return value

    def visit_Printed(self,n,scope_name='global',typo=None):
        #print(n.value.name)
        if self._ret_flag == True:
            return
        if type(n.value) == ast.VariantCall:
            print('Name: ', n.value.name.name)
            var = self.visit(n.value)
            print(var)
            return

        arrayName = n.value.name
        print('Name : ' , arrayName)
        if not self.check_dict(arrayName, scope_name):
            print('Error variantCall in Printed')
            return
        value_t = (self.decl_buf[scope_name].get(arrayName))
        #etalon = max(value_t)
        #etalon = len(str(etalon))
        #print('etalon: ',etalon)
        #space = ' '
        for k in range(len(value_t)):
            #print('?: len(str(value_t[k])): ',len(str(value_t[k])))
            #space = (etalon-len(str(value_t[k])))//len(value_t[k])
            #print('space: ',space)
            print(value_t[k])
            #print(*value_t[k], sep = (4)*' ',end='\n')
            print('')
        #print(value_t)
        return

    def check_typo(self,index):
        if isinstance(index,bool) or index == 'TRUE' or index == 'FALSE':
            return 'bool'
        elif isinstance(index,str):
            return 'str'
        elif isinstance(index,int):
            return 'int'
        else: return 'var'

    def visit_FunctionDict(self, n, scope_name='global',typo=None):
        # Добавлю новую область видимости
        self.decl_buf[n.name.name] = {}
        # Добавил аргументы в словарь
        #print("visit_FunctionDict : ",n.name.name)
        #self.visit(n.suite, n.name.name)
        # Добавил возвращаемые значения в словарь
        #self.visit(n.ret_values, n.name.name)

    def visit_Param(self,n,scope_name,typo=None):
        #print('param: ',scope_name)
        if self._ret_flag == True:
            return
        if scope_name=='global':
            #print('rapam scope')
            self._error_flag=True
        if self._error_flag == True:
            print('_error_flag in param')
            return
        #print('visit_Param : ',n.name.name)
        #vars = copy.deepcopy(self.visit(n.name,scope_name))
        #print('vars: ',vars)
        vars = copy.deepcopy(self.decl_buf[scope_name].get('param'+str(self._global_count)))
        #print('vars: ',vars)
        #print('self.decl_buf[scope_name]: ',self.decl_buf[scope_name])
        if vars != None:
            self.decl_buf[scope_name].update({n.name.name : vars})
        #print('self.decl_buf[scope_name]: ',self.decl_buf[scope_name])
        #self.decl_buf[scope_name][VarName] = (n.list)
        return

    def visit_Return(self,n,scope_name,typo=None):
        if self._ret_flag == True:
            return
        if scope_name=='global':
            self._error_flag=True
        if self._error_flag == True:
            print('cant return None')
            return
        #print('visit_Return : ',n.name.name)
        if not self.check_dict(n.name.name, scope_name):
            print('error return')
            return
        #return
        vars = copy.deepcopy(self.visit(n.name,scope_name))
        self.decl_buf[scope_name].update({'return'+str(self._global_count) : vars})
        self._ret_flag = True
        #self._error_flag = True
        return

    def visit_CallFunction(self,n,scope_name='global',typo=None):
        if self._error_flag == True:
            print('_error_flag in CallFunction')
            return
        if self._ret_flag == True:
            return

        #print(n.name.name)
        #print(' self.decl_buf.get(n.name.name):  ',self.decl_buf.get(n.name.name)  )
        # if not self.decl_buf.get(n.name.name):
        #     print("Function existing error<<<<<<<<<<")
        #     self._error_flag = True
        #     return

        # увеличивая переменную для количества вызовов функции
        #print('function_dict[n.name.name][0]:  ',function_dict[n.name.name][1])
        function_dict[n.name.name][1] += 1
        count = function_dict[n.name.name][1]
        self._global_count = count

        # формирую новое имя для области видимости имяфункции + _ +глубина рекурсии
        new_scope_name = n.name.name + "_" + str(count)
        #print('new_scope_name: ',new_scope_name)
        # копирую словарь из области видимости, которой была вызвана функция
        self.decl_buf[new_scope_name] = copy.deepcopy(self.decl_buf[n.name.name])
        #print('skok? ')
        #print('self.decl_buf[new_scope_name]',self.decl_buf[new_scope_name])
        func_dict = function_dict[n.name.name]
        #print('n.args: ',n.args)
        #var_from_decl = self.decl_buf[new_scope_name][func_dict[1][i]]
        #print('param: ',param)
        #print('func_dict: ',func_dict)
        #print('new_scope_name: ',new_scope_name)
        #print('func_dict: ',func_dict[0].suite)
        if not func_dict[0].suite:
            self._error_flag = True
            print('func_dict is empty[1050]')
            return
        #check
        #print('???:',n.args)
        if n.args!=None:
            #print('tyt? ',n.args)
            param = copy.deepcopy(self.visit(n.args, scope_name))
            #print('tyt 2?')
            param_list = 'param' + str(self._global_count)
            self.decl_buf[new_scope_name].update({str(param_list) : param})
            #print('list:',self.decl_buf)
        #print('self.decl_buf[scope_name]  ',self.decl_buf[new_scope_name])

        #print('func_dict[0].suite',func_dict)
        self.visit(func_dict[0].suite, new_scope_name)
        self._ret_flag = False
        #return
        #print('self.decl_buf[scope_name]  ',self.decl_buf[new_scope_name])
        #print('self.decl_buf[scope_name]  ',self.decl_buf[new_scope_name].get('return'))
        # удаляю область видимости при выходе из функции
        ret_value = copy.deepcopy(self.decl_buf[new_scope_name].get('return'+str(self._global_count)))
        #print('ret: ',ret_value)
        del self.decl_buf[new_scope_name]
        # уменьшая счетчик глубины рекурсии
        function_dict[n.name.name][1] -= 1
        self._global_count = function_dict[n.name.name][1]
        #print('callvar: ',n.callvar)
        #print('callvar',n.callvar)
        #newVar = copy.deepcopy(self.visit(n.callvar,scope_name))
        #print('ffff0: ',newVar)
        #newVar = copy.deepcopy(ret_value)
        #print(newVar)
        if ret_value != None:
            #print('call var: ',n.callvar.name,self._global_count)
            #print('scope: ',scope_name)
            self.decl_buf[scope_name].update({n.callvar.name: ret_value})
            #print('ret: ',self.decl_buf)
        #n.callvar = copy.deepcopy(ret_value)
        #print('????: ',n.callvar)
        return #newVar

    def Variant_extend(self,value):
        #print('val: ',value)
        test = copy.deepcopy(value)
        max = 0
        for it in test:
            if max < len(it):
                max = len(it)
        for i in range(len(value)):
            for j in range( max - len(value[i])):
                value[i].append([False,'',0])
