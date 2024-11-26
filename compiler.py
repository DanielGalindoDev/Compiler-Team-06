
from tokrules import tokens
from tokrules import Token_Info
import ply.yacc as yacc
import sys
import linkedList



# -------- Defincion de datos importantes ------ #


class SemanticError(Exception):
    def __init__(self,message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message

class NameCollsion(Exception):
    def __init__(self, name, lineDefinition,lineRedefinition):
        super().__init__()
        self.message = f"Name Collision for \"{name}\" at line {lineRedefinition}. Previously declared at line {lineDefinition}."

    def __str__(self):
        return self.message

class OutOfMemory(Exception): 
    pass

class GhostVariable(Exception):
    def __init__(self, name, line):
        super().__init__()
        self.message = f"GhostVariable at line {line}. No previously declared variable \"{name}\"."

    def __str__(self):
        return self.message

class NestedIf(Exception):
    pass



class SymbolTable(): 

    def __init__(self):
        self.variables = [{},{}]

    
    def addVariable(self,name,type,line,scope):        
        if name in self.variables[1]:
            raise NameCollsion(name,self.variables[1][name][1],line)
        
        if scope == 0: 
            if name in self.variables[0]:
                raise NameCollsion(name,self.variables[0][name][1],line)
        
        self.variables[scope][name] = (type,line)
    
    def variableExist(self,name,scope,line): 

        if scope == 0: 

            if name in self.variables[0]:
                return self.variables[0][name][0]
            elif name in self.variables[1]:
                return self.variables[1][name][0]
            else: 
                raise GhostVariable(name,line)
        else: 
            if name in self.variables[1]:
                return self.variables[1][name][0]
            else: 
                raise GhostVariable(name,line)


class TAC(): 

    def __init__(self,operation, operand1, operan2, result,indentation):
        
        self.indentation = indentation
        self.operation = operation
        self.operand1= operand1
        self.operand2 = operan2
        self.result = result
    


class Program():
    
    def __init__(self): 
        self.registers = {
            't1' : 0, 
            't2' : 0, 
            't3' : 0, 
            't4' : 0, 
            't5' : 0
        }

        self.ip = -1
        self.program = linkedList.LinkedList()
        self.lastScope = -1
        self.scopeStack = [-1]
        self.scopeTop = -1

    
    def addInstruction(self,operation,operand1,operand2,result,indentation = 0):
        self.ip = self.ip + 1
        self.program.insertAtEnd(TAC(operation,operand1,operand2,result,indentation))
    
    def addInstruction_Index(self,operation,operand1,operand2,result,index,indentation = 0):
        self.ip = self.ip + 1
        self.program.insertAtIndex(TAC(operation,operand1,operand2,result,indentation),index)
    
    def copyInstruction(self,tac,indent = 1):
        self.ip = self.ip + 1
        tac.indentation = tac.indentation * indent
        self.program.insertAtEnd(tac)
        
    def findRegister(self):
        for key in self.registers:
            if self.registers[key] == 0:
                self.registers[key] = 1 
                return key
        raise OutOfMemory

    def freeRegister(self,name):
        if name in self.registers: 
            self.registers[name] = 0
    
    def firstInstruction(self):
        if self.scopeTop == 0: 
            if self.scopeStack[0] == -1:
                self.scopeStack[0] = self.ip
    
    def newScope(self):
        if self.scopeTop == 0: 
            raise NestedIf
        self.scopeTop = self.scopeTop + 1
    
    def exitScope(self): 
        self.scopeTop = -1
        self.scopeStack[0] = -1
    
    def cancelFirstInstruction(self):
        self.scopeStack[0] = -1

    def writeInstructions(self):
        with open("a.py",'w') as file: 

            message = None
            last_operation = None
            keep_indentation = 0
            indentation = 0

            if(self.program.head):
                current_node = self.program.head

                while(current_node):
                    
                    keep_indentation = current_node.data.indentation

                    if last_operation != None: 
                            if last_operation == 'if':
                                indentation = indentation + 1
                            elif keep_indentation == 0: 
                                indentation = 0

                    if current_node.data.operation == 'if':        
                        indent = indentation * '\t'
                        message = indent + current_node.data.operation + '(' + current_node.data.operand1 + ')' + ':' + '\n'
                    elif current_node.data.operation == 'i':
                        indent = '\t' * indentation
                        message = indent + current_node.data.result + '=' + '-' + current_node.data.operand1 + '\n'
                    elif current_node.data.operation == 'd' or current_node.data.operation == 'dv':
                        indent = '\t' * indentation
                        message = indent + current_node.data.result + '=' + 'int' + '('+ current_node.data.operand1 + ')'+ '\n'
                    elif current_node.data.operation == 'p':
                        indent = '\t' * indentation
                        message = indent + current_node.data.result + '=' + 'float' + '(' + current_node.data.operand1 + ') ' + '\n'
                    elif current_node.data.operation == '=' or current_node.data.operation == 'v': 
                        indent = '\t' * indentation
                        message = indent + current_node.data.result + '=' + current_node.data.operand1 + '\n'
                    else: 
                        indent = '\t' * indentation
                        message = indent + current_node.data.result + '='  + current_node.data.operand1 + current_node.data.operation + current_node.data.operand2 + '\n'

                   
                    
                    file.write(message)
                    if current_node.data.operation == 'v' or current_node.data.operation == 'dv' or current_node.data.operation == 'p':
                        indent = '\t' * indentation
                        extra = indent + 'print' + '(' + 'f' + '"' + current_node.data.result + ' = ' + '{' + current_node.data.result + '}' + '"' ')' + '\n'
                        file.write(extra)
                    
                    last_operation = current_node.data.operation
                    current_node = current_node.next



        

    
   
# --- Variable Global --- #

symbolTable = SymbolTable()
program_instructions = Program()


# ---- Definición de reglas de producción ----- #


def p_A(p): 
    'A : TYPE MAIN LP RP LB B RB'

    if p[1].type != 'int':
        raise SemanticError("The primary function \"main\" only can have a return type of \"int\"")

# statementList -> statement
def p_B(p): 
    'B : C'

# statementList -> statement statementList
def p_B2(p): 
    'B : C B'

# variable_declaration -> definition = expression ; 
def p_C(p): 
    'C : D EQUAL E SEMICOLON'

    indentation = 0
    if program_instructions.scopeTop == 0: 
        indentation = 1


    if p[1].type != p[3].type: 
        if p[1].type == 'char' or p[3].type == 'char': 
            raise SemanticError(f"Sematic Error at line {p.lineno(2)}. Incompatible Data Types!")
    
    symbolTable.addVariable(p[1].string,p[1].type,p.lineno(2),program_instructions.scopeTop)

    if p[3].value == None: 
        if p[1].type != p[3].type:
            if p[1].type == 'int': 
                program_instructions.addInstruction('dv',p[3].string,None,p[1].string,indentation)
            elif p[1].type == 'float': 
                program_instructions.addInstruction('p',p[3].string,None,p[1].string,indentation)
        else:
            program_instructions.addInstruction('v',p[3].string,None,p[1].string,indentation)

        program_instructions.freeRegister(p[3].string)
    else: 
        if p[3].type == 'char':
            program_instructions.addInstruction('v',p[3].string,None,p[1].string,indentation)
        elif p[1].type != p[3].type: 
            if p[1].type == 'int':
                p[3].value = int(p[3].value)
            elif p[1].type == 'float': 
                p[3].value = float(p[3].value)
            program_instructions.addInstruction('v',str(p[3].value),None,p[1].string,indentation)
        else: 
            program_instructions.addInstruction('v',str(p[3].value),None,p[1].string,indentation)
    
    program_instructions.firstInstruction()




# variable_declaration -> definition ; 
def p_C2(p): 
    'C : D SEMICOLON'

    symbolTable.addVariable(p[1].string,p[1].type,p.lineno(2),program_instructions.scopeTop)


# definition -> type id
def p_D(p): 
    'D : TYPE ID'
    p[1].string = p[2].string
    p[0] = p[1]

# expression -> expresion MATH1 factor
def p_E(p): 
    'E : E MATH1 F'

    indentation = 0
    if program_instructions.scopeTop == 0: 
        indentation = 1

    if p[1].type == 'char' or p[3].type == 'char':
        raise SemanticError(f"Semantic Error at line {p.lineno(2)}. \"char\" data type can be in arithmetic operations.")
    
    if p[1].value != None and p[3].value != None: 
        if p[2].string == '+': 
            p[1].value = p[1].value + p[3].value
        else: 
            p[1].value = p[1].value - p[3].value
        p[0] = p[1]

    else: 

        operand1 = None
        operand2 = None

        if p[1].value == None: 
            operand1 = p[1].string
        else: 
            operand1 = str(p[1].value)
        
        if p[3].value == None: 
            operand2 = p[3].string
        else: 
            operand2 = str(p[3].value)
        

        register = program_instructions.findRegister()
        program_instructions.addInstruction(p[2].string,operand1,operand2,register,indentation)
        program_instructions.firstInstruction()

        
        type = 'int'
        if p[1].type == 'float' or p[3].type == 'float':
            type = 'float'
        
        p[0] = Token_Info(register,type)

        if p[1].value == None:
            program_instructions.freeRegister(p[1].string)
        
        if p[3].value == None: 
            program_instructions.freeRegister(p[3].string)
    

# expression -> factor
def p_E2(p): 
    'E : F'
    p[0] = p[1]

# factor -> factor MATH2 term
def p_F(p): 
    'F : F MATH2 G'

    indentation = 0
    if program_instructions.scopeTop == 0: 
        indentation = 1

    if p[1].type == 'char' or p[3].type == 'char':
        raise SemanticError(f"Semantic Error at line {p.lineno(1)}. \"char\" data type can be in arithmetic operations.")
    
    if p[1].value != None and p[3].value != None: 
        
        if p[2].string == '*': 
            if p[3].type == 'float':
                p[1].type = 'float'
            p[1].value = p[1].value * p[3].value
        else: 
            p[1].value = p[1].value / p[3].value
            p[1].type = 'float'
        p[0] = p[1]
    
    else: 

        operand1 = None
        operand2 = None

        if p[1].value == None: 
            operand1 = p[1].string
        else: 
            operand1 = str(p[1].value)
        
        if p[3].value == None: 
            operand2 = p[3].string
        else: 
            operand2 = str(p[3].value)
        
        register = program_instructions.findRegister()
        program_instructions.addInstruction(p[2].string,operand1,operand2,register,indentation)
        program_instructions.firstInstruction()

        type = 'int'
        if p[2].string == '/':
            type = 'float'
            
        elif p[1].type == 'float' or p[3].type == 'float':
            type = 'float'

        p[0] = Token_Info(register,type)

        if p[1].value == None:
            program_instructions.freeRegister(p[1].string)
        
        if p[3].value == None: 
            program_instructions.freeRegister(p[3].string)
        
       
# factor -> term
def p_F2(p): 
    'F : G'
    p[0] = p[1]


# term -> ( expression )
def p_G(p): 
    'G : LP E RP'
    p[0] = p[2]

# term -> constant
def p_G2(p): 
    'G : CONSTANT'
    p[0] = p[1]

# term -> id
def p_G3(p): 
    'G : ID'
    p[0] = Token_Info(p[1].string,symbolTable.variableExist(p[1].string,program_instructions.scopeTop,p.lineno(1)))

# term -> MATH1 term
def p_G4(p): 
    'G : MATH1 G'

    indentation = 0
    if program_instructions.scopeTop == 0: 
        indentation = 1

    if p[2].type == 'char':
        raise SemanticError(f"Semantic Error at line {p.lineno(1)}. \"char\" data type can be in arithmetic operations.")
    
    if p[2].value != None: 
        p[2].value = - p[2].value
        p[0] = p[2]
    else: 
        register = program_instructions.findRegister()
        program_instructions.addInstruction('i',p[2].string,None,register,indentation)
        program_instructions.firstInstruction()

        p[0] = Token_Info(register,p[2].type)
    
# statement -> assignment
def p_C3(p): 
    'C : ID EQUAL E SEMICOLON'

    type = symbolTable.variableExist(p[1].string,program_instructions.scopeTop,p.lineno(1))

    indentation = 0
    if program_instructions.scopeTop == 0: 
        indentation = 1


    if type != p[3].type: 
        if type == 'char' or p[3] == 'char': 
            raise SemanticError(f"Sematic Error at line {p.lineno(2)}. Incompatible Data Types!")
        
    if p[3].value == None: 
        if type == p[3].type: 
            if type == 'int': 
                program_instructions.addInstruction('dv',p[3].string,None,p[1].string,indentation)
            elif type == 'float':
                program_instructions.addInstruction('dv',p[3].string,None,p[1].string,indentation)
            else: 
                program_instructions.addInstruction('v',p[3].string,None,p[1].string,indentation)

        program_instructions.freeRegister(p[3].string)
    else:
        if p[3].type == 'char':
            program_instructions.addInstruction('v',p[3].string,None,p[1].string,indentation)
        elif type != p[3].type: 
            if type == 'int':
                p[3].value = int(p[3].value)
            elif type == 'float':
                p[3].value = float(p[3].value)
            program_instructions.addInstruction('v',str(p[3].value),None,p[1].string,indentation)
        else: 
            program_instructions.addInstruction('v',str(p[3].value),None,p[1].string,indentation)
    
    program_instructions.firstInstruction()


# statement -> if ( boolean_expression ) { statementList }
def p_C4(p):
    'C : K LP H RP LB B RB'

    if p[3][0] == 'nt':
        if p[3][1].value != None:
            if not p[3][1].value: 
                end = program_instructions.ip +1
                for i in range(program_instructions.scopeStack[0],end):
                    program_instructions.program.remove_at_index(program_instructions.scopeStack[0])
                    program_instructions.ip = program_instructions.ip - 1
        else: 
            program_instructions.addInstruction_Index('if',p[3][1].string,None,None,program_instructions.scopeStack[0])
    else:

        if p[3][1].value != None and p[3][2].value != None:

            if p[3][0] == 'and':
                result = p[3][1].value and p[3][2].value
                if not result:
                    end = program_instructions.ip +1
                    for i in range(program_instructions.scopeStack[0],end):
                        program_instructions.program.remove_at_index(program_instructions.scopeStack[0])
                        program_instructions.ip = program_instructions.ip - 1
            else: 
                result = p[3][1].value or p[3][2].value
                if not result:
                    end = program_instructions.ip +1
                    for i in range(program_instructions.scopeStack[0],end):
                        program_instructions.program.remove_at_index(program_instructions.scopeStack[0])
                        program_instructions.ip = program_instructions.ip - 1

        elif p[3][1].value == None and p[3][2].value == None: 

            if p[3][0] == 'and':
                program_instructions.addInstruction_Index('if',p[3][1].string,None,None,program_instructions.scopeStack[0]-1)
                program_instructions.addInstruction_Index('if',p[3][2].string,None,None,program_instructions.scopeStack[0]+1,1)
            else:
                program_instructions.addInstruction_Index('if',p[3][1].string,None,None,program_instructions.scopeStack[0]-1)
                
                program_instructions.copyInstruction(program_instructions.program.copyNode(program_instructions.scopeStack[0]),0)
                program_instructions.program.remove_at_index(program_instructions.scopeStack[0])
                program_instructions.ip = program_instructions.ip - 1
                program_instructions.addInstruction('if',p[3][1].string,None,None)

                end = program_instructions.ip - 1
                for i in range(program_instructions.scopeStack[0],end):
                    program_instructions.copyInstruction(program_instructions.program.copyNode(i))





        else: 
            result = False
            pos = 0
            if p[3][1].value != None: 
                result = p[3][1].value
                pos = 2
            else: 
                result = p[3][2].value
                pos = 1
            
            if [3][0] == 'and':
                if not result: 
                    for i in range(program_instructions.scopeStack[0],program_instructions.ip +1):
                        program_instructions.program.remove_at_index(program_instructions.scopeStack[0])
                        program_instructions.ip = program_instructions.ip - 1
                else: 
                    program_instructions.addInstruction_Index('if',p[3][pos].string,None,None,program_instructions.scopeStack[0])
            else: 
                if not result:
                    program_instructions.addInstruction_Index('if',p[3][pos].string,None,None,program_instructions.scopeStack[0])

 
    program_instructions.exitScope()


def p_K(p): 
    'K : IF'
    program_instructions.lastScope = program_instructions.ip
    
    try: 
        program_instructions.newScope()
    except NestedIf:
        print(f"Nested IFs at line {p.lineno(1)}.")
        raise NestedIf

# boolean_expression -> boolean_term || boolean_term
def p_H(p): 
    'H : I OR I'
    p[0] = ('or',p[1],p[3])

# boolean_expression -> boolean_term && boolean_term
def p_H1(p):
    'H : I AND I'
    p[0] = ('and',p[1],p[3])

# boolean_expression -> boolean term
def p_H2(p): 
    'H : I'
    p[0] = ('nt',p[1])

# boolean_term -> expression RELATION expression
def p_I(p): 
    'I : E RELATION E'

    if p[1].type == 'char' or p[3] == 'char':
        raise SemanticError(f"Semantic Error at line {p.lineno(1)}. \"char\" data type can be in logical operations.")
    
    change = 0
    result = 0
    register = None
    temp = None
    
    if p[1].type != p[3].type: 
            if p[1].type == 'int':
                change = 1
            else: 
                change = 3

    if p[1].value != None and p[3].value != None: 

        if change != 0: 
            p[change].value = float(p[change].value)
        
        if p[2].string == '<':
            result = p[1].value < p[3].value
        elif p[2].string == '>':
            result = p[1].value > p[3].value
        else: 
            result = p[1].value == p[3].value

        p[0] = Token_Info(None,None,result)
    
    else: 

        operand1 = None
        operand2 = None

        if p[1].value == None: 
            operand1 = p[1].string
        else: 
            operand1 = str(p[1].value)
        
        if p[3].value == None: 
            operand2 = p[3].string
        else: 
            operand2 = str(p[3].value)

        if change == 1: 

            register = program_instructions.findRegister()
            program_instructions.addInstruction('p',operand1,None,register)
            temp = register 
            register = program_instructions.findRegister()
            program_instructions.addInstruction(p[2].string,temp,operand2,register)

        elif change == 3: 
                
            register = program_instructions.findRegister()
            program_instructions.addInstruction('p',operand2,None,register)
            temp = register 
            register = program_instructions.findRegister()
            program_instructions.addInstruction(p[2].string,operand1,temp,register)
        
        else: 

            register = program_instructions.findRegister()
            program_instructions.addInstruction(p[2].string,operand1,operand2,register)
        
        program_instructions.cancelFirstInstruction()
            
        p[0] = Token_Info(register)
        
        program_instructions.freeRegister(temp)
        program_instructions.freeRegister(register)
        

# Manejo de Errores
def p_error(p):
    print(f"Syntax error at line {p.lineno}. Token read \"{p.type} : {p.value.string}\"")

# ---------------------------------------------- #

n = len(sys.argv)

if n < 2 or n > 2: 
    print("python <nombre_archivo>.py")
else: 

    with open(sys.argv[1]) as file: 
        file_content = file.read()
    
    parser = yacc.yacc()

    try: 
        parser.parse(file_content)
        program_instructions.writeInstructions()
    except SemanticError as a:
        print(a)
    except NameCollsion as b: 
        print(b)
    except OutOfMemory:
        print("Arquitecture no capable to process the size of the expressions")
    except GhostVariable as c: 
        print(c)
    except NestedIf:
        pass
    
    


    

    
