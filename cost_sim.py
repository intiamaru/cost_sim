#import decimal
from __future__ import division

#VARIABLES
'''
a = [500,100,300,200,400]
b = [{'name':'I1','units':20,'value':20},
     {'name':'I2','units':10,'value':50}]
c = [{'name_from':'I1','units_from':5,'name_to':'IA','units_to':30}]
d = [{'name':'IA','year':2010,'units':2,'price':8},
     {'name':'IA','year':2010,'units':5,'price':7},
     {'name':'IA','year':2010,'units':4,'price':10},
     {'name':'IA','year':2011,'units':11,'price':6},
     {'name':'IA','year':2011,'units':4,'price':5},
     {'name':'IA','year':2011,'units':3,'price':4},
     {'name':'IA','year':2011,'units':1,'price':7}
     ]
'''
var_selecor = '-->'

def get_variables(file_name):
    var_dict = {}
    f = open(file_name, 'r')
    var = ''
    for line in f.readlines():        
        if var_selecor in line:
            #variable
            var = line.strip(var_selecor).strip('\n')
            var_dict[var] = ''
        else:
            #text
            var_dict[var] = var_dict[var] + line
    return var_dict

def feed_variables(file_name):
    orig_var_dict =  get_variables(file_name)
    var_dict = {}
    code = ''
    for elem in orig_var_dict:        
        if '[' in orig_var_dict[elem] and ']' in orig_var_dict[elem]:
            code = code + '\n' + elem + ' = ' +  orig_var_dict[elem].strip('\n')
            ev = eval(orig_var_dict[elem].strip('\n'))
            var_dict[elem] = ev
        if orig_var_dict[elem][0] == '|':
            text = orig_var_dict[elem].strip('\n')
            var_dict[elem] = table_to_object(text)
    return var_dict

def object_to_text_table(table):
    text_table = ''
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
#proceso
def process_simulation(year):
    batch_cost = sum(a)
    print '==================================='
    print 'A. Costo de lote: ' + str(batch_cost)

    item_totals = []
    for item in b:
        try:
            item_totals.append(item['units'] * item['value'])
        except TypeError:
            print "Tipos incorrectos, revise " +item['units'] +"-"+ item['value']
    oc_cost = sum(item_totals)

#obtain unit cost
    print '==================================='
    print 'B. Costo unitario: '
    elem_info = {}
    for item in b:
        item['factor'] = item['units'] * item['value'] / oc_cost
        item['cost'] = batch_cost * item['factor']
        item['unit_cost'] = item['cost'] / item['units']
        print str(item['name']) + ': ' + str(item['unit_cost'])
        elem_info[item['name']] = item
        
    #element transformations
    print '==================================='
    print 'C. Costo unitario transformaciones: '
    for item in c:
        origin_unit_cost = elem_info[item['name_from']]['unit_cost']
        output_cost = origin_unit_cost * item['units_from']
        output_unit_cost = output_cost / item['units_to']
        print str(item['name_to']) + ": " + str(output_unit_cost)
        new_item = {'name': item['name_to'], 'cost': output_cost,
                    'unit_cost': output_unit_cost, 'units': item['units_to']}
        elem_info[item['name_to']] = new_item

    print '==================================='
    print 'D. Calc costo de ventas: '
    
    total_sales = []
    total_sales_cost = []
    for item in d:
        if item['year'] == year :
            unit_cost = elem_info[item['name']]['unit_cost']
            sales_cost = item['units'] * unit_cost
            sales_value = item['units'] * item['price']
            profit = sales_value - sales_cost
            item['sales_value'] = sales_value
            item['sales_cost'] = sales_cost
            item['profit'] = profit
            total_sales.append(sales_value)
            total_sales_cost.append(sales_cost)
            #print str(item['name']) + ": "
            #print 'Venta: ' + str(sales_value)
            #print 'Costo Venta: ' + str(sales_cost)
            #print 'Utilidad: ' + str(profit)
    print 'Costo de Venta detallado'
    print object_to_text_table(d)
            
    print '==================================='
    print 'R. Resultados (' + str(year) + '): '
    print 'Vent Total: ' + str(sum(total_sales))
    print 'Costo Venta Total: ' + str(sum(total_sales_cost))
    final_profit = sum(total_sales) - sum(total_sales_cost)
    print 'Utilidad: ' + str(final_profit)
    print 'Porcentaje Utilidad: ' + str( final_profit / sum(total_sales) * 100 )


var_dict = feed_variables('L888B.txt')
a = var_dict['a']
b = var_dict['b']
c = var_dict['c']
d = var_dict['d']
process_simulation(2013)
