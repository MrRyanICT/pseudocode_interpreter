reserved_words = ('begin','main','program','end','declare','function','procedure','if', 'else','endif','do','then','repeat','until',
                  'case','while','endwhile','for','next','endfor','case')
allowed_data_types = ('integer', 'string','char', 'boolean','real', 'array')
allowed_array_types = ('integer', 'string', 'char', 'boolean','real')


class Variable:
    def __init__(self):
        self.variable_name = ''
        self.variable_data_type = ''
        self.variable_values = 0
        self.array_index_start = 0
        self.array_index_end = 0
        self.array_data_type = ''



import copy

from typing import Dict, Tuple, Union, List, TextIO
import string
import re
ALPHA = string.ascii_letters
from colorama import init, Fore, Back, Style
init()









def Read_File(file_extension):
    file = open(file_extension, 'r')
    lines = []
    for line in file:
        temp =line.replace('\n', '').strip().replace('\t', '').replace('  ', ' ')
        # ^^remove starting and ending whitespace, tabs, and end of line character^^
        lines.append(re.sub(r'\b(?<!")(\w+)(?!")\b', lambda match: match.group(1).lower(), temp))
        # ^^ makes everything lowercase except text within ""
    return lines


class PsuedoFuncs:
    @staticmethod
    def LEFT(ThisString: str, x :int) -> str:
        return ThisString[:x]
    @staticmethod
    def RIGHT(ThisString: str, x :int) -> str:
        return ThisString[x:]
    @staticmethod
    def MID(ThisString: str, x :int, y: int) -> str:
        return ThisString[x:x+y]
    @staticmethod
    def LENGTH(ThisString: str) -> int:
        return len(ThisString)
    @staticmethod
    def LCASE(ThisString: str) -> str:
        if len(ThisString) != 1:
            raise Exception("ERROR: CHAR type not given")
        return ThisString.lower()
    @staticmethod
    def UCASE(ThisString: str) -> str:
        if len(ThisString) != 1:
            raise Exception("ERROR: CHAR type not given")
        return ThisString.upper()
    @staticmethod
    def TO_UPPER(ThisString: str) -> str:
        return ThisString.upper()
    @staticmethod
    def TO_LOWER(ThisString: str) -> str:
        return ThisString.lower()
    @staticmethod
    def NUM_TO_STR(x: Union[int, float]) -> str:
        return str(x)
    @staticmethod
    def STR_TO_NUM(x: str) -> Union[int, float]:
        if '.' in x:
            return float(x)
        else:
            return int(x)
    @staticmethod
    def IS_NUM(ThisString: str) -> bool:
        try:
            float(ThisString)
            return True
        except ValueError:
            return False
    @staticmethod
    def ASC(ThisChar: str) -> int:
        if len(ThisChar) != 1:
            raise Exception("ERROR: CHAR type not given")
        return ord(ThisChar)

    @staticmethod
    def _CHR(x: int) -> str:
        try:
            y = chr(x)
            return y
        except Exception as e:
            raise e

    @staticmethod
    def _INT(x: float) -> int:
        return int(x)
    @staticmethod
    def RAND(x: int) -> float:
        from random import uniform
        return uniform(0.0, float(x))



class Interp:

    def __init__(self):
        self.code = ''
        self.variable_list = []
        self.file_pool:Dict[str, TextIO] = {} # this stores .txt objects format: {FILE_NAME: FILE_OBJECT}


    def Handle_Function(_func: str, *param):
        pass


    def Handle_Variables(self, lines: list, code_start: int, code_end: int) -> Tuple[List[Variable], int]:
        # find variables
        # evals the total code then adds to variable_list
        self.variable_list = []
        line_stop = code_end-1
        for counter in range(code_start, code_end):
            if lines[counter].startswith('declare'):
                new_variable = Variable()
                if ':' not in lines[counter]:
                    print(Fore.RED + Back.WHITE + 'Error: No ":" in declaration statement')
                    exit(0)
                var_start = 7 #variable starts after "declare"
                while lines[counter][var_start] == ' ':
                    var_start += 1
                var_end = lines[counter].find(':')
                while lines[counter][var_end-1] == ' ':
                    var_end -= 1

                variable = lines[counter][var_start:var_end]
                new_variable.variable_name = variable

                if variable in reserved_words:
                    print(Fore.RED + Back.WHITE + 'Error: ' + variable + ' is a reserved word in pseudocode')
                    exit(0)

                data_type_start = lines[counter].find(':') + 1
                while data_type_start < len(lines[counter]) and lines[counter][data_type_start] in (' ', ':'):
                    data_type_start += 1
                if len(lines[counter]) <= data_type_start:
                    print(Fore.RED + Back.WHITE + 'Error: No valid data type for variable ' )
                    exit(0)
                if ' ' in lines[counter][data_type_start:]: #space in data type declaration
                    data_type_stop = lines[counter][data_type_start:].find(' ') + data_type_start
                else:
                    data_type_stop = len(lines[counter])
                while lines[counter][data_type_stop-1] == ' ':
                    data_type_stop -= 1
                data_type = lines[counter][data_type_start:data_type_stop]
                if data_type not in allowed_data_types:
                    print(Fore.RED + Back.WHITE + 'Error: ' + data_type + ' is not an allowed data type in pseudocode')
                    exit(0)
                new_variable.variable_data_type = data_type

                #check for arrays
                if data_type == 'array':
                    if '..' not in lines[counter][data_type_stop:]:
                        print(Fore.RED + Back.WHITE + 'Error: ".." needed for array declaration')
                        exit(0)
                    #look for index
                    index_start = lines[counter][data_type_stop:].find('array') + data_type_stop + 1
                    while lines[counter][index_start] == ' ':
                        index_start += 1
                    index_stop = lines[counter][index_start:].find('..') + index_start
                    while lines[counter][index_stop - 1] == ' ':
                        index_stop -= 1
                    try:
                        first_index =int(lines[counter][index_start:index_stop])
                    except:
                        print(Fore.RED + Back.WHITE + 'Error: array index is invalid')
                        exit(0)
                    index_start = lines[counter][index_stop:].find('..') + index_stop + 2

                    while lines[counter][index_start] == ' ':
                        index_start += 1
                    if 'of' not in lines[counter][index_start:]:
                        print(Fore.RED + Back.WHITE + 'Error: array declaration needs "of" a data type')
                        exit(0)
                    index_stop = lines[counter][index_start:].find('of') + index_start - 1
                    while lines[counter][index_stop - 1] == ' ':
                        index_stop -= 1
                    try:
                        second_index =int(lines[counter][index_start:index_stop])
                    except:
                        print(Fore.RED + Back.WHITE + 'Error: array index is invalid')
                        exit(0)
                    new_variable.array_index_start = first_index
                    new_variable.array_index_end = second_index
                    if new_variable.array_index_start > new_variable.array_index_end:
                        print(Fore.RED + Back.WHITE + 'Error: first array index is greater than second')
                        exit(0)



                    data_type_start = lines[counter][index_stop:].find('of') + index_stop + 2

                    while lines[counter][data_type_start] == ' ':
                        data_type_start += 1
                    data_type_stop = len(lines[counter])
                    while lines[counter][data_type_stop - 1] == ' ':
                        data_type_stop -= 1

                    array_data_type = lines[counter][data_type_start:data_type_stop]
                    if array_data_type not in allowed_array_types:
                        print(Fore.RED + Back.WHITE + 'Error: ' + array_data_type +  ' is not a valid datatype')
                        exit(0)
                    new_variable.array_data_type = array_data_type
                    #add array data
                    if array_data_type == 'string' or array_data_type == 'char':
                        blank_data = ''
                    elif array_data_type == 'integer':
                        blank_data = 0
                    elif array_data_type == 'real':
                        blank_data = 0.0
                    elif array_data_type == 'boolean':
                        blank_data = False
                    new_variable.variable_values = []
                    for counter2 in range(new_variable.array_index_start, new_variable.array_index_end + 1):
                        new_variable.variable_values.append(blank_data)
                else: #not an array
                    if data_type == 'string' or data_type == 'char':
                        blank_data = ''
                    elif data_type == 'integer':
                        blank_data = 0
                    elif data_type == 'real':
                        blank_data = 0.0
                    elif data_type == 'boolean':
                        blank_data = False
                    new_variable.variable_values = blank_data

                self.variable_list.append(copy.deepcopy(new_variable))
            else: #doesn't start with declare
                line_stop = counter
                break
        return self.variable_list, line_stop


    def Process_Output(self, line, variable_list):
        text = ''
        temp_line = line[6:]


        while True:
            while temp_line.startswith(' '):
                temp_line = temp_line[1:]
            if temp_line.startswith('"'):
                quote_loc = temp_line[1:].find('"')+1
                if quote_loc == -1:
                    print(Fore.RED + Back.WHITE + 'Error: mismatched speech marks in OUTPUT statement')
                    exit(0)
                text += temp_line[1:quote_loc]
                if quote_loc + 1 >= len(temp_line):
                    break
                temp_line = temp_line[quote_loc:]

            elif temp_line.startswith(tuple(ALPHA)):
                var_end = temp_line.find(' ')
                if var_end == -1:
                    var_end = len(temp_line)
                while temp_line[var_end - 1] == ' ':
                    var_end -= 1
                variable = temp_line[:var_end]
                found = False
                value = ''
                for v in variable_list:
                    if v.variable_name == variable:
                        found = True
                        value = v.variable_values
                        break
                if not found:
                    print(Fore.RED + Back.WHITE + 'Error: variable name ', variable, ' in OUTPUT statement not declared')
                    exit(0)
                text += str(value)
                if var_end + 1 >= len(temp_line):
                    break
                temp_line = temp_line[var_end:]
                while len(temp_line) > 0 and temp_line[0] == ' ':
                    temp_line = temp_line[1:]
                if len(temp_line) == 0:
                    break
                if temp_line[0] != '&':
                    print(Fore.RED + Back.WHITE + 'Error: text in OUTPUT must be concatenated with &')
                    exit(0)
                else:
                    temp_line = temp_line[1:]
            else:
                print(Fore.RED + Back.WHITE + 'Error: invalid syntax in OUTPUT statement')
                exit(0)
        print(text)

    def Find_First(self, text, search_elements):
        min_value = 999999
        min_element = ''
        for s in search_elements:
            loc = text.find(s)
            if loc < min_value and loc != -1:
                min_value = loc
                min_element = s
        if min_value == 999999:
            min_value = -1
        return min_value

    def Read_Variable_Value(self, variable_name, variable_list):

        variable = variable_name
        found = False
        value = ''
        for v in variable_list:
            if v.variable_name == variable:
                found = True
                value = v.variable_values
                data_type = v.variable_data_type
                break
        if not found:
            print(Fore.RED + Back.WHITE + 'Error: variable name ', variable, ' not found')
            exit(0)
        return value, data_type

    def GetInput(self, data_type):
        if data_type == 'string':
            value = input()
        elif data_type == 'char':
            value = input()
            if len(value) > 1:
                print(Fore.RED + Back.WHITE + 'Error: char data type cannot have more than one character')
                exit(0)
        elif data_type == 'real':
            try:
                value = float(input())
            except:
                print(Fore.RED + Back.WHITE + 'Error: invalid input data for real')
                exit(0)
        elif data_type == 'integer':
            try:
                value = int(input())
            except:
                print(Fore.RED + Back.WHITE + 'Error: invalid input data for integer')
                exit(0)
        elif data_type == 'boolean':
            try:
                value = input().lower()
                if value not in ('true', 'false'):
                    print(Fore.RED + Back.WHITE + 'Error: input for boolean data type must be true or false')
                    exit(0)
            except:
                print(Fore.RED + Back.WHITE + 'Error: invalid input data for boolean')
                exit(0)
        return value


    def Process_Input(self, line, variable_list) -> list:  # i really have no clue what is returned here, assuming its a list
        temp_line = line[5:]
        while True:

            while temp_line[0] == ' ':
                temp_line = temp_line[1:]

            if temp_line.startswith(tuple(ALPHA)):
                var_end = self.Find_First(temp_line, [' ', '[', ','])
                if var_end == -1:
                    var_end = len(temp_line)
                while temp_line[var_end - 1] in (' ', '[', ','):
                    var_end -= 1
                variable = temp_line[:var_end]
                found = False

                for v in variable_list:
                    if v.variable_name == variable:
                        found = True
                        data_type = v.variable_data_type
                        break
                if not found:
                    print(Fore.RED + Back.WHITE + 'Error: variable name ', variable, ' in INPUT statement not declared')
                    exit(0)

                if data_type in ('string', 'char', 'real', 'integer', 'boolean'):
                    value = self.GetInput(data_type)

                elif data_type == 'array':
                    index_start = temp_line.find('[')
                    index_stop = temp_line.find(']')
                    if index_start > index_stop or -1 in (index_start, index_stop):
                        print(Fore.RED + Back.WHITE + 'Error: invalid sytax in array assignment')
                        exit(0)
                    while temp_line[index_start] in (' ', '[') :
                        index_start += 1
                    while temp_line[index_stop - 1] in (' ', ']') :
                        index_stop -= 1
                    index_text = temp_line[index_start:index_stop]
                    if index_text.startswith(tuple(ALPHA)):

                        array_index, index_data_type = self.Read_Variable_Value(index_text, variable_list)
                        if index_data_type != 'integer':
                            print(Fore.RED + Back.WHITE + 'Error: array index must be an integer')
                            exit(0)
                    elif index_text[0].isdigit():
                        try:
                            array_index = int(index_text)
                        except:
                            print(Fore.RED + Back.WHITE + 'Error: invalid sytax in array assignment')
                            exit(0)



                for v in variable_list:
                    if v.variable_name == variable:
                        if v.variable_data_type == 'array':
                            if not v.array_index_start <= array_index <= v.array_index_end:
                                print(Fore.RED + Back.WHITE + 'Error: invalid index value in array assignment')
                                exit(0)
                            else:
                                real_index = array_index -  v.array_index_start
                                v.variable_values[real_index] = self.GetInput(v.array_data_type)
                                var_end = index_stop + 1 #as this is the end of the variable
                                break
                        else: #not an array
                            v.variable_values = value
                            break
                        break

                if var_end + 1 >= len(temp_line):
                    break
                temp_line = temp_line[var_end:]
                while len(temp_line) > 0 and temp_line[0] == ' ':
                    temp_line = temp_line[1:]
                if len(temp_line) == 0:
                    break
                if temp_line[0] == ',':
                    temp_line = temp_line[1:]


        else: #variable name doesn't start with an alpha
            print(Fore.RED + Back.WHITE + 'Error: variable name ', variable, ' in INPUT statement does not start with a letter')
            exit(0)

        return variable_list


    def Get_Variable_Value(self, line, variable_begins, variable_list):
        var_start = variable_begins
        var_end = variable_begins
        while line[var_end ] not in (' ', ',', '&'):
            var_end += 1
        variable = line[var_start:var_end]

        value, data_type = self.Read_Variable_Value(variable, variable_list)
        if data_type == 'array':
            index_start = var_end + 1



    def Process_Variable(self, line, var_start):
        pass # this was making my ide cry 


    def Process_Condition(self, lines, line_stop, variable_list) -> None:
        temp_line = lines[line_stop]
        temp_line = temp_line[2:] #remove 'if'
        while temp_line[0] == ' ':
            temp_line = temp_line[1:]

        if temp_line.startswith(tuple(ALPHA)):

            if var_end == -1:
                var_end = len(temp_line)

            variable = temp_line[:var_end]
            found = False

            for v in variable_list:
                if v.variable_name == variable:
                    found = True
                    data_type = v.variable_data_type
                    break
            if not found:
                print(Fore.RED + Back.WHITE + 'Error: variable name ', variable, ' in INPUT statement not declared')
                exit(0)

            if data_type in ('string', 'char', 'real', 'integer', 'boolean'):
                value = self.GetInput(data_type)

            elif data_type == 'array':
                index_start = temp_line.find('[')
                index_stop = temp_line.find(']')
                if index_start > index_stop or -1 in (index_start, index_stop):
                    print(Fore.RED + Back.WHITE + 'Error: invalid sytax in array assignment')
                    exit(0)
                while temp_line[index_start] in (' ', '['):
                    index_start += 1
                while temp_line[index_stop - 1] in (' ', ']'):
                    index_stop -= 1
                index_text = temp_line[index_start:index_stop]
                if index_text.startswith(tuple(ALPHA)):
                    pass




    def loop_eval(self, loops_lines:list, type: str, _cond=None):
        if type == 'while':
            while _cond:
                pass # eval code here
        elif type == 'for':
            for _ in _cond:
                pass # eval code here
            

    def line_eval(self, line, lines, variable_list: List[Variable]) -> Union[List[Variable], int]:
        if line.startswith('output'):
            self.Process_Output(line, variable_list)
        elif line.startswith('input'):
            variable_list = self.Process_Input(line, variable_list)
            return variable_list
        elif line.startswith('if'):
            line_stop = self.Process_Condition(lines,line_stop, variable_list)
            return line_stop

        elif line.startswith('openfile'):
            file_name = re.findall(r'"([^"]*)"', line)[0]
            print(file_name)
            if 'read' in line:
                file = self.psu_read_file(file_name)
        
        # elif line.startswith('while'):
        #     # check for another loop
        #     # check for endwhile
            
        #     self.loop_eval()



    # these methods are bound to the interpreter so it isnt in PsuedoFuncs

    # OPENFILE 'x.txt' FOR READ
    def psu_read_file(self, name:str) -> TextIO:
        x = open(name, 'r')
        self.file_pool[name] = x
        return x

    # OPENFILE 'x.txt' FOR WRITE
    def psu_write_file(self, name:str) -> TextIO:
        x = open(name, 'w')
        self.file_pool[name] = x
        return x

    # CLOSEFILE 'x.txt'
    def psu_close_file(self, name:str) -> None:
        self.file_pool[name].close()



    def Main_Program(self, lines):
        self.code = lines
        program_start = 0
        #check for start
        while True:
            if lines[program_start] == 'begin':
                if program_start > 0: #check for procedure or function
                    if lines[program_start - 1].startswith('procedure') or lines[program_start - 1].startswith('function'):
                        pass
                    else:
                        break
                else: #begin starts on line 0
                    break
            else:
                program_start += 1

                if program_start >= len(lines):
                    print(Fore.RED + Back.WHITE +'Error. No program start found')
                    return

        program_end = program_start + 1

        while True:
            if program_end >= len(lines):
                print(Fore.RED + Back.WHITE + 'Error. No program end found')
                return
            elif lines[program_end] == 'end':
                break
            else:
                program_end += 1


        variable_list, line_stop = self.Handle_Variables(lines, program_start + 1, program_end) # fetches all declares and variables

        while True: #run program
            self.line_eval(lines[line_stop], lines, self.variable_list)
            # if lines[line_stop].startswith('output'):
            #     self.Process_Output(lines[line_stop], self.variable_list)
            # elif lines[line_stop].startswith('input'):
            #     self.variable_list = self.Process_Input(lines[line_stop], self.variable_list)
            # elif lines[line_stop].startswith('if'):
            #     line_stop = self.Process_Condition(lines,line_stop, self.variable_list)


            line_stop += 1
            if line_stop >= program_end:
                break



if __name__ == '__main__':
    interpreter = Interp()
    lines = Read_File('tester.txt')
    print(lines)
    interpreter.Main_Program(lines)
