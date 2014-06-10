import sys
import pymssql
#iniciando variables
pos1=[]
pos2=[]
pos3=[]
pos4=[]
pos5=[]
pos6=[]
coment=[]
qry_y_titulo=[]
qry=[]
campos=[]
registros=[]
registro_tupla=[]
ini=0
fin=0
y=0
ini2=0
fin2=0
num_titulos=0
num_registros=0
num_campos=0
num_qrys=0
num_opciones=0
fin2=0



###########################################################################
#Tomar el archivo y transformarlo en cadena

REPORT=open('archivo_prueba.sql','r')
REPORT_STRING=REPORT.read()
REPORT_STRING=REPORT_STRING+'\n'
arch_report=open('reporte.txt','w')




############################################################################
#Generadores para el for

def mi_generador(n, m, s):
    while(n <= m):
      yield n
      n += s
def mi_generador(i, m, s):
    while(i <= m):
      yield i
      i += s
      
      
############################################################################
#Obtener el num de lineas del documento
      
num=REPORT_STRING.split('\n')
num_lineas=len(num)


############################################################################
#Extraer una lista con los comentarios      
fin2=3
fin2=3
for n in mi_generador(0,num_lineas, 1):

    pos1.append(REPORT_STRING.find('>',ini))
    pos2.append(REPORT_STRING.find('\n',fin))
    pos3.append(REPORT_STRING.find('-',ini2))
    pos4.append(REPORT_STRING.find('-',fin2)) 
    coment.append(REPORT_STRING[pos1[n]:pos2[n]])
    qry_y_titulo.append(REPORT_STRING[pos3[n]:pos4[n]])
    ini = pos2[n]
    fin = pos2[n] +1
    ini2 = pos4[n]
    fin2 =pos4[n]+3


#############################################################################    
#sacar espacios vacios de la cadena coment
    
num_titulos=coment.count( '')
num_titulos = num_titulos-1
for n in mi_generador(0,num_titulos,1):
    coment.remove( '')


##############################################################################    
#Imprimir las opciones del usuario
    
print "ELIJA UN REPORTE :"
print "------------------------------"
print '\n'
num=len(coment)-1
for n in mi_generador(0,num,1):
    print n,coment[n]
print n+1,'>','IMPRIMIR TODO' 


###############################################################################
#generar la lista "qry" que contenga todos los querys del documento
    
num_titulos=len(qry_y_titulo)-1
num_qrys = len(coment)
for n in mi_generador(0,num_titulos,1):    
    pos5.append(qry_y_titulo[n].find('\n'))
    qry.append(qry_y_titulo[n][pos5[n]:])
    qry=qry[:num_qrys]


###############################################################################
#Pedirle al usuario que reporte desea
    
print '\n'
y = input("Enter a valid number: ")


###############################################################################
#Cadena de conexion

conexion = pymssql.connect( "192.168.1.198", "consulta", "sociedad", "oficont")


###############################################################################
###############################################################################
#Funcion para imprimir reportes

def obt_tabla(reporte):
    af=""
    afs=""
    
    ##############################################################################    
    #Ejecutar el query

    with conexion.cursor() as cursor:
        sql = qry[reporte]
        cursor.execute(sql)


    ##############################################################################    
    #llenar una lista con los campos
    
        num_campos=len(cursor.description)-1
        for n in mi_generador(0,num_campos,1):
            campo_tupla= cursor.description[n]
            campo_lista=list(campo_tupla)
            campos.append(campo_lista[0])


    ##############################################################################        
    #llenar una lista con registros por campos
        
        registro_lista = list(cursor.fetchall())
    

    ################################################################################
    #Graficar el titulo de la tabla

        print '\n'+'--'+coment[reporte]
        arch_report.write('\n'+'--'+coment[reporte]+'\n')

        
    ##############################################################################
    #Graficar los campos de la tabla
    
    for n in mi_generador(0,num_campos,1):
        if n==num_campos:
            af= af + "|" + str(campos[n])+"\t"+'|'
        else:
            af= af + "|" + str(campos[n])+"\t"
    print af
    arch_report.write(af+'\n')


    ##############################################################################
    #Graficar los registros de la tabla

    num_registros = cursor.rowcount -1
    for i in mi_generador(0,num_registros,1):
        #print ''
        for n in mi_generador(0,num_campos,1):
            if n==num_campos:
                afs=afs + "|" + str(registro_lista[i][n])+"\t"+"|"
            else:
                afs=afs + "|" + str(registro_lista[i][n])+"\t"
        print afs
        arch_report.write(afs + '\n')
        afs = ""



#################################################################################
#Imprimir el reporte elegido en consola
        
num_opciones = len(coment)
if y == num_opciones:
    for n in mi_generador(0,num,1):
        obt_tabla(n)
elif ~(y== num_opciones): 
    obt_tabla(y)
    

#################################################################################
#Imprimir el reporte elegido en un txt    
arch_report.close()    
#################################################################################    
#Preguntar al usuario si desea seguir:
    
print  '\n' + 'desea realizar otra operacion'
print 'yes(y)/no(n)'
final = input("")
if final == n:
    print "gracias"
elif final ==y:
    print "no"

