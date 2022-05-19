import copy

def parse(a):
    '''Creates character list from a string (deletes spaces).
    
    a - polynomial in string form'''

    tab = []
    j = 0
    #separetes characters in regards of defined symbols in a way that leaves multichracter variable names
    for i in range(len(a)):
        if a[i] in "+-/*()^":
            tab.append(a[j:i])
            tab.append(a[i])
            j = i+1
    tab.append(a[j:])
    #deletes empty characters and spaces
    for i in tab:
        if i == '' or i == ' ':
            tab.remove(i)

    return tab

def preoperation(a):
    '''Creates nested lists in place of parentesies.
    
    a - character list'''

    new = [] #new list
    par = [] #list of characters in parenthesis
    found = 0 #counter for safety during parenthesis traversion
    for i in range(len(a)):
        if found == 0:
            if a[i] == '(':
                found = 1
                par = [] 
            else:
                new.append(a[i]) #if there are no open parenthesis list is copied
        else:
            if a[i] == '(':
                found = found + 1 
                par.append(a[i])
            elif a[i] == ')':
                found = found - 1
                if found > 0: #when found reaches zero again it means that last open parenthesis is closed
                    par.append(a[i])
                else:
                    new.append(['(', preoperation(par)]) #when last parenthesis is closed new list is appended
            else:
                par.append(a[i])
    return new

def operation(a, operations):
    '''Creates nested lists in Lisp-like manner and .
    
    a-list of characters,
    operations-operators'''

    for i in range(len(a)):
        if isinstance(a[i], list):
            pass #does nothin because it deals with parenthesis operator or nested list
        elif a[i] in operations:
            #this ensures that another list is not wrapped in list again
            if isinstance(a[i-1], list):
                #creates s-expression
                return [a[i], a[i-1], operation(a[i+1:], operations)] 
            else:
                #in s-expression operator goes first then what comes after it and the rest continuest to wraps
                return [a[i], a[0:i], operation(a[i+1:], operations)] 
    #this means that whole list was wrapped before and now is unwrapped    
    else: 
        if len(a) == 1 and isinstance(a[0], list):
            return a[0]

        return a

def graph(a, operations):
    '''Creates graph in form of Lisp-like nested lists.
    
    a-polynomial in form of character list
    operations-operatory'''

    #searches through list for parts not turned into s-expression
    if isinstance(a[0], list):
        #if first character is a list it means it wasn't changed already
        a = operation(a, operations)
    elif a[0] in "+-*":
        #if first character is an operator it means that chenge was done and it continues to search
        a[1] = graph(a[1], operations)
        a[2] = graph(a[2], operations)
    else:
        #here is unchanged list
        a = operation(a, operations)

    return a

def deep_graph(a):
    '''Changes content of parenthesis into graph.
    
    a-polynomial in form of nested list'''

    #it looks for parenthesis and turns it contents into graphs
    #after this it continues to search for nested parenhesis
    if a[0] == '(':
        a[1] = make_a_graph(a[1])
        a[1] = deep_graph(a[1])
    elif a[0] in "+-*/^":
        a[1] = deep_graph(a[1])
        a[2] = deep_graph(a[2])
    
    return a

def delistifier(a):
    '''Extracts characters from lowest levels of graph.
    
    a-polynomial in form of nested lists'''

    #if length of list equals 1 it means that it is lowest level
    #this function is necesery for other functions to properly work on that graph
    if len(a) > 2:
        a[1] = delistifier(a[1])
        a[2] = delistifier(a[2])
    elif len(a) > 1:
        a[1] = delistifier(a[1])
    else:
        a = a[0]
    
    return a

def make_a_graph(a):
    '''Creates graph with regards of calculation order.

    a-character list'''

    step1 = operation(a, "+")
    step2 = graph(step1, "-")
    step3 = graph(step2, "*")
    step4 = graph(step3, "/")
    step5 = graph(step4, "^")

    return step5

def assemble(a):
    '''Builds string from graph.
    
    a-polynomial in form of nested lists'''

    if a[0] == '(':
        return '(' + assemble(a[1]) + ')'
    elif a[0] not in "+-/*^":
        return a
    else:
        return assemble(a[1]) + a[0] + assemble(a[2])

def found(a, v):
    '''Checs if variable exist in graph.
    
    a-polynomial in form of nested lists,
    v-variable name'''

    if a[0] in "+-*/^":
        f1 = found(a[1], v)
        f2 = found(a[2], v)
    elif a[0] == v:
        return True
    else:
        return False

    return f1 or f2

def extension(a, v):
    '''Extends graph in regards to polynomial integration rules.

    a-polynomial in form of nested lists,
    v-variable name'''

    if a[0] == '(':
        pass
    elif a[0] not in "+-/*^":
        a = ["*", a, v] #attaches variable to constant
    elif a[0] in "+-":
        #goes throgh other parts of polynomial
        a[1] = extension(a[1], v)
        a[2] = extension(a[2], v)
    elif a[0] in "*":
        #Checks in which part of graph is located variable
        if found(a, v):
            if isinstance(a[1], list) and found(a[1], v):
                #searches again in direction of variable
                a[1] = extension(a[1], v)
            elif isinstance(a[2], list) :
                a[2] = extension(a[2], v)
            elif a[2] == v:
                #integrates variable when found
                a[2] = ["*", ['(', ["/", "1", "2"]], ["^", v, "2"]]
            elif a[1] == v:
                a[1] = ["*", ['(', ["/", "1", "2"]], ["^", v, "2"]]
        else:
            a = ['*', a, v]
    elif a[0] in "^":
        if a[1] == v:
            #integrates variable to the power
            a = ["*", ['(', ["/", "1", str(int(a[2]) + 1)]], ["^", v, str(int(a[2]) + 1)]]

    return a

def integration(a, var):
    '''Integrates polynomial in form of a graph.
    
    a-polynomial in form of nested lists,
    var-list of variables'''

    extended = a
    for i in var:
        extended = extension(extended, i)

    #adds constant
    return ["+", "C", extended]

def calculate(a, variable, value):
    '''Calculates polynomial.
    
    a-polynomial in form of nested lists,
    variable-name of variable,
    value-value of variable'''

    if a[0] == "(":
        return calculate(a[1], variable, value)
    elif a[0] == "+":
        return float(calculate(a[1], variable, value)) + float(calculate(a[2], variable, value))
    elif a[0] == "-":
        return float(calculate(a[1], variable, value)) - float(calculate(a[2], variable, value))
    elif a[0] == "*":
        return float(calculate(a[1], variable, value)) * float(calculate(a[2], variable, value))
    elif a[0] == "/":
        return float(calculate(a[1], variable, value)) / float(calculate(a[2], variable, value))
    elif a[0] == "^":
        return float(calculate(a[1], variable, value)) ** float(calculate(a[2], variable, value))
    elif a == variable:
        return value
    else:
        return float(a)

def prepareFunction(a):
    '''Changes polynomial from string to grapg in form of nested lists.
    
    a-polynomial in form of string'''

    parsed = parse(a)
    prepared = preoperation(parsed)
    graph1 = make_a_graph(prepared)
    ready = deep_graph(graph1)
    final = delistifier(ready)

    return final

def integrate(function, variables):
    '''Integrates polynomial in regards of variables.
    Returns integrated polynomial in form of string.
    
    equation-polynomial,
    variables-list of variables names'''

    #creates graph
    final = prepareFunction(function)
    #integrates graph
    result = integration(final, variables)

    return assemble(result)


def integrateFile(input="input.txt", output="output.txt", r=False):
    '''Reads file and integrates polynomial writen in there  
    and writes result to file.

    input-path to input file(default input.txt),
    output-path to output file(default output.txt),
    r-bool variable, checks if integrated polynomial will be returned to console'''
    
    try:
        with open(input, "r") as f:
            a = f.read()
            a = a.strip('\n')
    except Exception as e:
        return "Invalid file path!"
    
    #separetes variables from polynomial
    try:
        function, variables = a.split(" ")
    except Exception as e:
        return "Invalid input file. Maybe there are too much spaces?"

    if function == "" or variables == "":
        return "Invalid input file!"

    check = checkFunction(function)
    if check != "OK":
        return check

    if variables[0] != 'd':
        return "Integration written incorrectly!"
    #rozdziela zmienne
    var = variables.split("d")
    var.remove('')

    if len(var) < 1:
        return "No variables to integrate!"

    result = integrate(function, var)
    
    with open(output, "a") as f:
        f.write(result)
        f.write('\n')

    if r:
        return result

def definitiveIntegration(function, start, end, variable):
    '''Performs definitive integration.
    Returns calculated integral.
    Works only for polynomial of one variable.
    
    function-polynomial,
    start-beggining of integration,
    end-end of intrgration,
    variable-variable name'''

    #creates graph
    final = prepareFunction(function)
    #integrates graph
    result = extension(final, variable)

    return calculate(result, variable, end) - calculate(result, variable, start)


def definitiveIntegrationFile(input="input.txt", output="output.txt", r=False):
    '''Reads file and performs definitive integration. 
    Writes result to output file.

    input-path to input file(default input.txt),
    output-path to output file(default output.txt)'''
    
    try:
        with open(input, "r") as f:
            a = f.read()
            a = a.strip('\n')
    except Exception as e:
        return "Invalid file path!"
    
    #oddziela zmienne od równania
    try:
        function, restraints, var = a.split(" ")
    except Exception as e:
        return "Invalid input file. Maybe there are too much spaces?"

    if function == "" or restraints == "" or var == "":
        return "Invalid input file!"

    check = checkFunction(function)
    if check != "OK":
        return check

    #rozdziela początek i koniec przedzialu całkowania
    res = restraints.split(',')
    if len(res) != 2:
        return "Amount of variables defining area of integration is incorrect (correct 2: begining and end)"

    if var[0] != 'd':
        return "Integration written incorrectly!"

    var = var[1:]
    if var == "":
        return "Invalid variable!"

    if var not in function:
        return "Variable is not present in polynomial!"

    f = function.split(var)
    fun = ''.join(f)
    for i in fun:
        if i.isalpha():
            return "Beside integrated variable other variables are invalid!"

    result = definitiveIntegration(function,res[0], res[1], var)
    
    with open(output, "a") as f:
        f.write(str(result))
        f.write('\n')

    if r:
        return result

def checkFunction(function):
    operators = "+-/*^"
    parentasies = "()"
    for i in range(len(function)):
        if function[i] in operators:
            if i == 0 or i == len(function)-1:
                return "Lone operator '" + function[i] + "'!"
            elif function[i-1] in operators or function[i+1] in operators:
                return "Lone operator '" + function[i] + "'!"

    for i in range(len(function)-1):
        if function[i] + function[i+1] == parentasies:
            return "Empty parenthasis!"

    par=0
    for i in function:
        if i == '(':
            par = par + 1
        if i == ')':
            par = par - 1
    if par != 0:
        return "Not enough parenthasis!"

    for i in range(len(function)):
        if function[i] == '/':
            j = i-1
            while function[j] not in operators+parentasies and j >= 0:
                if function[j].isalpha():
                    return "Variables cannot be divided! Program is not advanceed enugh."
                j = j-1
            j = i+1
            while function[j] not in operators+parentasies and j < len(function):
                if function[j].isalpha():
                    return "Variables cannot be divided! Program is not advanceed enugh."
                j = j+1

    for i in range(len(function)):
        if function[i] == '(':
            if i > 0 and not function[i-1] in operators:
                return "Parts in parenthasis must be separeted from other parts with operator!"

            j = i+1
            p = 1
            while p > 0 and j < len(function):
                if function[j].isalpha():
                    return "Variables cannot be placed inside parenhtesis! Program is not advanceed enugh."
                if function[j] == '(':
                    p = p + 1
                elif function[j] == ')':
                    p = p - 1
                j = j+1
        elif function[i] == ')':
            if i < len(function) - 1 and not function[i+1] in operators:
                return "Parts in parenthasis must be separeted from other parts with operator!"

    return "OK"
