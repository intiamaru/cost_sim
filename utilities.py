
var_selector = '-->'

def get_variables(file_name):
    var_dict = {}
    f = open(file_name, 'r')
    var = ''
    for line in f.readlines():        
        if var_selector in line:
            #variable
            var = line.strip(var_selector).strip('\n').strip()
            var_dict[var] = ''
        else:
            #text
            if not var == '':
                var_dict[var] = var_dict[var] + line
    return var_dict


def feed_variables(file_name):
    orig_var_dict =  get_variables(file_name)
    var_dict = {}
    code = ''
    for elem in orig_var_dict:
        # codigo para interpretar arreglos
        if '[' in orig_var_dict[elem] and ']' in orig_var_dict[elem]:
            code = code + '\n' + elem + ' = ' +  orig_var_dict[elem].strip('\n')
            ev = eval(orig_var_dict[elem].strip('\n'))
            var_dict[elem] = ev
        # codigo para interpretar tablas
        if orig_var_dict[elem][0] == '|':
            text = orig_var_dict[elem].strip('\n')
            var_dict[elem] = table_to_object(text)
    return var_dict

	
def object_to_text_table(table):
    text_table = ''
    if len(table) > 0:
        column_names = table[0].keys()
        text_table = text_table + '|' + '\t\t|'.join(column_names) + '\t\t|\n'
        for row in table:
            row_str = map(str,row.values())
            text_table = text_table + '|' + '\t\t|'.join(row_str) + '\t\t|\n'
    return text_table    


def table_to_object(text):
    table = []
    lines = text.split('\n')
    title_text = "".join(lines[0].lstrip('|').rstrip('|').split())
    col_names = title_text.split('|')
    for line in lines[1:]:
        elem_dict = {}
        line_text = "".join(line.lstrip('|').rstrip('|').split())
        item_values = line_text.split('|')
        for i in range(len(item_values)):
            #print i, item_values[i]
            value = item_values[i]
            if is_number(value):
                value = num(value)
            elem_dict[col_names[i]] = value
        table.append(elem_dict)
    return table

    
def unify(table,key):
    result = {}
    #print "Unifing " + str(table)
    for elem in table:
        #print "Elem " + str(elem)
        elem_key = elem[key]
        if not elem_key in result:
            result[elem_key] = []
        result[elem_key].append(elem)
    return result


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
