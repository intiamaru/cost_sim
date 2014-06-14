from __future__ import division
from utilities import *
import sys


#VARIABLES
'''
a = [{'batch':'888B','amount':561.73},{'batch':'999','amount':100}]
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


#proceso
def process_simulation(year, batch_list=None):
    process_result = []
    expenses = []

    f = open('output.txt','w')
    #sys.stdout = f

    #prepare data
    pa = unify(a,'batch')
    pb = unify(b,'batch')
    pc = unify(c,'batch')
    pd = unify(d,'batch')
    
    for batch in pa:
        if (batch in batch_list):
            batch_cost = pa[batch][0]['amount']

            item_totals = []
            for item in pb[batch]:
                try:
                    item_totals.append(item['units'] * item['value'])
                except TypeError:
                    print "Tipos incorrectos, revise " + item['units'] +"-"+ item['value']
            oc_cost = sum(item_totals)

            #obtain unit cost
            elem_info = {}
            for item in pb[batch]:
                item['factor'] = item['units'] * item['value'] / oc_cost
                item['cost'] = batch_cost * item['factor']
                item['unit_cost'] = item['cost'] / item['units']
                elem_info[item['name']] = item
                
            #element transformations
            if batch in pc:
                for item in pc[batch]:
                    origin_unit_cost = elem_info[item['name_from']]['unit_cost']
                    print 'OUC ' + origin_unit_cost
                    output_cost = origin_unit_cost * item['units_from']
                    output_unit_cost = output_cost / item['units_to']
                    new_item = {'name': item['name_to'], 'cost': output_cost,
                                'unit_cost': output_unit_cost, 'units': item['units_to']}
                    elem_info[item['name_to']] = new_item

            #print elem_info

            result_elem = {}
            total_sales = []
            total_sales_cost = []
            for item in pd[batch]:
                if item['year'] == year :
                    unit_cost = elem_info[item['name']]['unit_cost']
                    sales_cost = item['units'] * unit_cost
                    sales_value = item['units'] * item['price']
                    profit = sales_value - sales_cost
                    item['sales_value'] = sales_value
                    item['sales_cost'] = sales_cost
                    item['profit'] = profit
                    item['perc_profit'] = str(round(profit / sales_value * 100,2)) + '%'
                    total_sales.append(sales_value)
                    total_sales_cost.append(sales_cost)
                    #print str(item['name']) + ':: Venta: ' + str(sales_value) + ' Costo Venta: ' + str(sales_cost) + ' Prct: ' + str(profit)
                    
            result_elem['year'] = year
            result_elem['total_sales'] = sum(total_sales)
            result_elem['total_sales_cost'] = sum(total_sales_cost)
            result_elem['final_profit'] = sum(total_sales) - sum(total_sales_cost)
            final_profit = sum(total_sales) - sum(total_sales_cost)
            result_elem['profit_percent'] = final_profit / sum(total_sales) * 100

            print '==================================='
            print 'R. Resultados (' + str(year) + '-' + str(batch) +'): '
            print 'Vent Total: ' + str(sum(total_sales))
            print 'Costo Venta Total: ' + str(sum(total_sales_cost))        
            print 'Utilidad: ' + str(final_profit)
            print 'Porcentaje Utilidad: ' + str( final_profit / sum(total_sales) * 100 )
            process_result.append(result_elem)

    print ""
    print "!=================Resultados del Proceso===============================!"
    print object_to_text_table(process_result)
    #f.close()
    
var_dict = feed_variables('reporte.txt')
a = var_dict['a']
b = var_dict['b']
c = var_dict['c']
d = var_dict['d']
process_simulation(2013,['1003B'])

#TDD TEST DRIVEN DEVELOPMENT
def test1():
    tsample = [{'batch':'1', 'a':'100', 'b':'1'}, {'batch':'2', 'a':'200', 'b':'2'}]
    tresult = {'1':[{'batch':'1', 'a':'100', 'b':'1'}],'2':[{'batch':'2', 'a':'200', 'b':'2'}]}
    unified = unify(tsample, 'batch')
    print unified
    assert unified == tresult
    print "Test " + sys._getframe().f_code.co_name + " ok"

def test2():
    tsample = [{'batch':'1', 'a':'100', 'b':'1'}, {'batch':'2', 'a':'200', 'b':'2'},{'batch':'2', 'a':'300', 'b':'3'}]
    tresult = {'1':[{'batch':'1', 'a':'100', 'b':'1'}],'2':[{'batch':'2', 'a':'200', 'b':'2'},{'batch':'2', 'a':'300', 'b':'3'}]}
    unified = unify(tsample, 'batch')
    print unified
    assert unified == tresult
    print "Test " + sys._getframe().f_code.co_name + " ok"

def test_app():
    test1()
    test2()
