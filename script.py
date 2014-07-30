#!/usr/bin/python2.7
#-*- coding: utf-8 -*-
import os
import subprocess

def get_file(formato):
    '''
    Función para petición y validación
    de un archivo en un formato específico
    '''
    get_file = False

    while not get_file:

        # Petición de archivo .p12
        archivo = raw_input("Introduzca el archivo .%s: " % (formato))

        # Comprobando si el archivo existe
        if os.access(archivo, os.R_OK) == False:
            print "No se consiguió el archivo %s." % (archivo)

        # Comprobando que el archivo sea .p12
        elif archivo.split('.')[1] != formato:
            print "El archivo no es .%s, es .%s " % (formato, archivo.split('.')[1])

        else:
            get_file = True
            return archivo
        get_file = False

def __main__():
    print "*************************************"
    print "Iniciando script para crackear pkcs12"
    print "*************************************"

    archivo = ''
    contador = 0
    encontrado = False

    # Se pide la introducción del archivo .p12
    archivo_p12 = get_file('p12')

    # Se pide la introducción del archivo .pem
    archivo_pem = get_file('pem')

    # Se pide la introducción del archivo para el diccionario
    print "\nSe necesita un diccionario donde estén las posibles contraseñas"
    diccionario = get_file('txt')
    diccionario = open(diccionario)

    linea = diccionario.readline()
    while linea != '':
        contador += 1
        resultado = subprocess.Popen("openssl pkcs12 -in %s -clcerts -nokeys -out %s -password pass:%s" % (archivo_p12, archivo_pem, linea), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        print "Contraseñas probadas: %d" % (contador) 
        if str(resultado.stdout.readline()).__contains__("OK"):
            clave = linea
            encontrado = True
            break

        linea = diccionario.readline()

    if encontrado:
        print "La clave es %s" % (str(linea))
    else:
        print "No se encontró la clave en %s" % (diccionario.name)
        
__main__()
