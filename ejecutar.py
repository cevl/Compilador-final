import json
import re

operators = {'=' : 'Assignment op','+' : 'Addition op','-' : 'Subtraction op',
             '/' : 'Division op','*' : 'Multiplication op','<' : 'Lessthan op',
             '>' : 'Greaterthan op', '√' : 'Square root', '∛' : 'Cube root',
             '∜' : 'Fourth root' }
operators_key = operators.keys()

data_type = {'ent' : 'integer type', 'flot': 'Floating point' , 'car' : 'Character type', 'grande' : 'long int' }
data_type_key = data_type.keys()

punctuation_symbol = { ':' : 'colon', ';' : 'semi-colon', '.' : 'dot' , ',' : 'comma',
                      '(' : 'Open round bracket', ')' : 'Close round bracket', 
                      '[' : 'Open square bracket', ']' : 'Close square bracket',
                      '{' : 'Open curly bracket', '}' : 'Close curly bracket'}
punctuation_symbol_key = punctuation_symbol.keys()

identifier = { 'print': 'function' }
identifier_key = identifier.keys()

reserved = ['sin', 'cos', 'tan','mientras', 'para', 'romper', 'continuar', 'retornar', 'si',
            'funcion', 'imprimir']
symbol_table = {}

translate = {'sin' : 'Math.sin', 'cos' : 'Math.cos', 'tan' : 'Math.tan', 'mientras' : 'while', 'para' : 'for', 'romper' : 'break', 'continuar' : 'continue',
             'retornar' : 'return', 'si' : 'if', 'funcion' : 'function',
             'imprimir': 'console.log', 'ent' : 'let', 'flot' : 'let', 'car' : 'let',
             'grande' : 'let', '=' : '=', '+' : '+', '-' : '-', '/' : '/', '*' : '*',
             '<' : '<', '>' : '>', ';' : ';', '(' : '(', ')' : ')', '[' : '[',
             '{' : '{', '}' : '}', '√' : 'Math.sqrt', '∛' : 'Math.cbrt'}

file = open("read.py", 'r', encoding='utf8')
a = file.read()
#print('object a1: ', a)
count=0
program = a.split("\n")
jprogram = []
tokend = []
for line in program:
    count = count + 1
    tokend.append([])
    #print("line#" , count, "\n" , line)
                
    tokens=line.split(' ')
    #print("Tokens are " , tokens)
    #print("Line#", count, "properties \n")
    
    if tokens[0] in data_type_key:
            if tokens[1] not in identifier:
                identifier[tokens[1]] = 'id'
                identifier_key = identifier.keys()
                
    jtokens = []
    #print('√' in line)
    for token in tokens:
        #print(token)
        if token in operators_key:
            #print("operator is ", operators[token])
            jtokens.append(token)
            tokend[-1].append({'Tipo': operators[token], 'Valor' : token})
        elif re.match('^[a-zA-Z]+$', token):
            jtokens.append(token)
            tokend[-1].append({'Tipo': 'id', 'Valor' : token})
        elif token in data_type_key:
            #print("datatype is", data_type[token])
            jtokens.append(token)
            tokend[-1].append({'Tipo': data_type[token], 'Valor' : token})
        elif token in punctuation_symbol_key:
            #print (token, "Punctuation symbol is" , punctuation_symbol[token])
            jtokens.append(token)
            tokend[-1].append({'Tipo': punctuation_symbol[token], 'Valor' : token})
        elif token in identifier_key:
            #print (token, "Identifier is" , identifier[token])
            jtokens.append(token)
            tokend[-1].append({'Tipo': 'id', 'Valor' : token})
        elif re.match('^[0-9]+$', token):
            jtokens.append(token)
            tokend[-1].append({'Tipo': 'entero', 'Valor' : token})
        elif re.match('^"[0-9 a-z A-Z]*"$', token):
            jtokens.append(token)
            tokend[-1].append({'Tipo': 'caracteres', 'Valor' : token})
        elif re.match('^[0-9]+.[0-9]+$', token):
            jtokens.append(token)
            tokend[-1].append({'Tipo': 'flotante', 'Valor' : token})
        elif token in punctuation_symbol_key:
            jtokens.append(token)
            tokend[-1].append({'Tipo': punctuation_symbol[token], 'Valor': token})
        elif token in reserved:
            jtokens.append(token)
            tokend[-1].append({'Tipo': 'reserved', 'Valor': token})
            
    #print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _  _") 
    jprogram.append(jtokens);
    
json_object = json.dumps(jprogram, indent = 4, ensure_ascii=False)
with open("tokens.json", "w", encoding='utf8') as outfile:
    outfile.write(json_object)
    
json_object = json.dumps(tokend, indent = 4, ensure_ascii=False)
with open("token.json", "w", encoding='utf8') as outfile:
    outfile.write(json_object)
    
#********** Sintactico
    
with open('tokens.json', 'r', encoding='utf8') as openfile:
    program = json.load(openfile)
    
    count = 0
    for line in program:
        count += 1
        #print('Line# ', count, '\n')
        
        if(line[-1] in operators):
            print('Error al final de la linea #', count, 'no se puede terminar la linea con un operador \n')
            break
        if re.match('^[a-zA-Z]+$', line[0]):
                identifier[line[0]] = 'id'
                identifier_key = identifier.keys()
                symbol_table[line[0]] = 'id'
        if(line[0] not in identifier_key):
            print('Error al principio de la linea #', count, line[0], 'no es una variable.')
            break
                
        first_id = False
        for token in line:
            if token in identifier.keys():
                if first_id == True:
                    #print('Error, se esperaba un signo de asignacion')
                    break
                first_id = True
            elif first_id == True:
                first_id = False
                
        #strline = ''.join(line)
        #if(re.match('.*[*/+-=]{2}.*', strline)):
            #print('Error en la linea #', count, 'uso invalido de operadores')
           
json_object = json.dumps(symbol_table, indent = 4, ensure_ascii=False)
with open('symbol_table.json', 'w', encoding='utf8') as st:
    st.write(json_object)
    
        
#************ semantico
    
with open('tokens.json', 'r', encoding='utf8') as openfile:
    program = json.load(openfile)
    
    count = 0
    for line in program:
        #sp.append([])
        count += 1
        print('Line# ', count, '\n')
        
        left = ''
        right = ''
        operator = ''
        for token in line:
            if token in identifier.keys():
                #sp[count-1].append(token)
                if left == '':
                    left = symbol_table[token]
                else:
                    right = symbol_table[token]
                    if left == 'char' and symbol_table[token] != 'char':
                        if operator == '=':
                            print('No puedes asignar un valor numerico a un char')
                        else:
                            print('No puedes hacer una operacion entre un char un valor numerico')
                    elif left != 'char' and symbol_table[token] == 'char':
                        if operator == '=':
                            print('No puedes asignar caracteres a una variable numerica')
                        else:
                            print('No puedes hacer una operacion entre un valor numerico y un char')
            elif token in operators.keys():
                if operator != '':
                    left = right
                operator = token
               
#**************

file = open("read.py", 'r', encoding='utf8')
a = file.read()
tokend = []
count=0
program = a.split("\n")
jprogram = []
for line in program:
    count = count + 1
    #print("line#" , count, "\n" , line)
                
    tokens=line.split(' ')
    
    if tokens[0] in data_type_key:
            if tokens[1] not in identifier:
                identifier[tokens[1]] = 'id'
                identifier_key = identifier.keys()
                
    jtokens = []
    for token in tokens:
        if token in operators_key:
            jtokens.append(translate[token])
        elif token in data_type_key:
            jtokens.append(translate[token])
        elif token in punctuation_symbol_key:
            jtokens.append(translate[token])
        elif token in identifier_key:
            jtokens.append(token)
        elif token in reserved:
            jtokens.append(translate[token])
        elif re.match('^[0-9]*$', token):
            jtokens.append(token)
        elif re.match('^"[0-9 a-z A-Z \s]*"$', token):
            jtokens.append(token)
        elif re.match('^[a-zA-Z]*$', token):
            jtokens.append(token)
            
            
        if token in operators_key:
            tokend.append({'Tipo': operators[token], 'Valor' : translate[token]})
        elif token in data_type_key:
            tokend.append({'Tipo': data_type[token], 'Valor' : translate[token]})
        elif token in punctuation_symbol_key:
            tokend.append({'Tipo': punctuation_symbol[token], 'Valor' : translate[token]})
        elif token in identifier_key or re.match('^[a-zA-Z]*$', token):
            tokend.append({'Tipo': 'id', 'Valor' : token})
        elif re.match('^[0-9]+$', token):
            tokend.append({'Tipo': 'entero', 'Valor' : token})
        elif re.match('^"[0-9 a-z A-Z]*"$', token):
            tokend.append({'Tipo': 'caracteres', 'Valor' : token})
        elif re.match('^[0-9]+.[0-9]+$', token):
            tokend.append({'Tipo': 'flotante', 'Valor' : token})
        elif token in punctuation_symbol_key:
            tokend.append({'Tipo': punctuation_symbol[token], 'Valor': token})
        elif token in reserved:
            tokend.append({'Tipo': 'reserved', 'Valor': translate[token]})
    jprogram.append(jtokens);
    #print('jtokens', jtokens)
    #print('tokend', jtokens)
    
with open('jprogram.js', 'w') as js:
    for line in jprogram:
        #print(line)
        for token in line:
            js.write(token)
            js.write(' ')
        js.write('\n')

json_object = json.dumps(tokend, indent = 4)
with open("jstoken.json", "w") as outfile:
    outfile.write(json_object)

def translate(token):
    jtoken = translate[token]
    return jtoken