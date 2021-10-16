# Actividad 4 - Hash

La presente actividad consiste en generar un algoritmo de hash a fin de resguardar los sitios web vulnerables en los sitios chilenos. En este sentido, dicho algoritmo debe
cumplir una seríe de restricciones las cuales son:
- El número de caracteres final del texto procesado, debe ser fijo y no menor de 25 caracteres. Este número no debe variar, aunque el texto de entrada sea más largo.
- Se requiere que el programa pueda recibir como entrada, tanto un string o texto mediante STDIN, cómo también mediante archivos con múltiples entradas separadas por el salto de línea.
- Cualquier ligero cambio al texto de entrada, debe cambiar el resultado final del algoritmo.
- El procesamiento del texto de entrada, debe  ser rápido, no debe tomar mucho tiempo, independiente de la cantidad de texto de entrada. **Se recomienda el uso de operaciones matemáticas al texto de entrada, a fin de optimizar la velocidad de procesamiento del texto de entrada**
- Adicionalmente se requiere que posea a lo menos dos opciones:
    - una que procese el texto de entrada y calcule el Hash de estas entradas (sea por STDIN, cómo mediante un archivo)
    - Y otra opción que sólo calcule la entropía del texto de entrada. En este último caso, debe arrojar mediante STDOUT que entropía posee cada texto de entrada (El formato       de la salida a STDOUT, debe mostrar tanto el texto analizado, cómo la entropía calculada separada por un delimitador que permita diferenciar los diferentes campos).

## Algoritmo de hash creado
A continuación, se presenta el algoritmo de hash generado para la experiencia. 

*Nota: Para la realización de pruebas de rendimiento se limito el archivo **Rockyou.txt** a 50 líneas*
```python
import string
import math
import hashlib #se importa esta librería para efectuar un análisis en relación a los algoritmos de hash tradicionales

base = str(string.ascii_letters + string.digits + string.punctuation) #base 94 generada (es ASCII - espacios en blancos)
base2 = str(string.punctuation) #Variable auxiliar para generar caracteres especiales
#Función que permite corroborar si el hash obtenido es igual a 25, en caso contrario se corta el hash o se emplea recursividad si el resumen es menor
def hashR(hash, password):  
    neWord = hash
    if(len(hash) > 25):
        neWord = hash[:25]
        return neWord
    elif(len(hash) < 25):
        hash2 = resumen(password)
        neWord += hash2
        return hashR(neWord, password)
    else:
        return neWord

def resumen(password): #Función de hash creada
    ultimo = len(password) - 1
    Funcion1 = password[0] + password[ultimo] #Funcion 1 que toma el primer y ultimo caracter del string 
    Funcion2 = str(F2(password)) 
    Funcion3 = str(F3(password))
    Funcion4 = str(F4(password))
    Funcion5 = str(int(math.sqrt(F3(password))))
    return (Funcion2 + Funcion3 + Funcion4 + Funcion1 + Funcion5) #Funciones creadas para emplear un hash en particular

def F2(password): #F2 que retornara una serie de caracteres en relación al largo del hash empleado, además de verificar si algún caracter de la password esta en el diccionario
    match = ""
    cont=0
    if(len(password) >= 4):
        for i in range(len(password)):
            remplazar = int(base.find(password[i])/2 + 6) 
            match += base[remplazar] + base[i*2]
            cont += 1
            if(cont >= 4):
                return match
    else: 
        match = base[int(base.find(password[0])/2) + 7] + base2[int(base.find(password[len(password)-1])/2)] + base[int(base.find(password[len(password)-2])/2)] +"<#?"
        return match
    

def F3(password): #F3 realiza una sumatoria de números pares e impares para posteriormente multiplar los valores obtenidos
    pares = 0
    impares = 0
    for i in range(len(password)):
        if(base.find(password[i])%2 == 0):
            pares += base.find(password[i])
        else:
            impares += base.find(password[i])
    return pares * impares 

def F4(password): #F4 ofusca la contraseña empleada por medio de la varianle auxiliar base2 que contiene caracteres especiales
    ofuscar = ""
    cont = 0
    if(len(password)%2 == 0 and password.isalnum() == True): #Dependiendo del password empleado se retornarán valores distintos
        for i in range(0, len(base2), 3):
            ofuscar += base2[i] + base[i]
            cont +=1
            if(cont >= 4):
                return ofuscar
    elif(len(password)%2 == 0 and password.isalnum() == False):
        for i in range(0, len(base2), 4):
            ofuscar += base2[i] + base[i]
            cont +=1 
            if(cont >= 4):
                return ofuscar
    else:
        for i in range(0, len(base2), 8):
            ofuscar += base2[i] + base[i]
            cont +=1
            if(cont >= 4):
                return ofuscar

def lectura(fichero): #Función que permite leer el Fichero ingresado. Cabe recalcar que dicho fichero debe estar en la misma ruta que el Algoritmo
    with open("./"+fichero, "r", encoding='utf8') as file:
        cont = 0
        for line in file:
            palabra = line.strip()
            print("Contraseña:", palabra, "Hash por defecto:",  hashR(resumen(palabra), palabra))
            cont += 1
            if(cont == 50):
                return file.close()
def entropia(password): #Función que retorna la entropía del hash (Por el momento los hash sha1, sha256 y md5 se les asumio la misma base que el algoritmo creado)
    H = len(password) * math.log2(len(base))
    return H

#Función tipo switch case que tomá una opción ingresada por el usuario y devuelve la acción que selecciono
def switch():
    print('Elige el algoritmo a usar o la acción a tomar:')
    print('1.- Nombre del fichero y su extensión')
    print('2.- Hash por defecto (algoritmo creado)')
    print('3.- SHA1')
    print('4.- SHA256')
    print('5.- MDN5')

    opcion = int(input())
    
    if(opcion == 1):
        fichero = input("ingrese el nombre y la extensión del fichero: ")
        lectura(fichero)

    elif(opcion ==2):
        password = input("ingrese contraseña: ")
        contraseña = resumen(password)
        hash25 = hashR(contraseña, password)
        print("Hash creado:", hash25, "     Entropía:", entropia(hash25))

    elif(opcion == 3):
        password = input("ingrese contraseña: ")
        string_to_hash = password
        hash_object = hashlib.sha1(str(string_to_hash).encode('utf-8'))
        print('Sha1: ', hash_object.hexdigest(), "     Entropía:", entropia(hash_object.hexdigest()))

    elif(opcion == 4):
        password = input("ingrese contraseña: ")
        string_to_hash = password
        hash_object = hashlib.sha256(str(string_to_hash).encode('utf-8'))
        print('Sha256: ', hash_object.hexdigest(), "     Entropía:", entropia(hash_object.hexdigest()))
    
    elif(opcion == 5):
        password = input("ingrese contraseña: ")
        string_to_hash = password
        hash_object = hashlib.md5(str(string_to_hash).encode('utf-8'))
        print('MD5: ', hash_object.hexdigest(), "     Entropía:", entropia(hash_object.hexdigest()))
switch()
```
## Comparativa Hash Algorithm


### Ditribución de rendimiento

## Lista de tareas

- [x] \(Hito I)
- [x] \Hito II
- [ ] \Hito III
- [ ] \Hito IV

- [x] #739
- [ ] https://github.com/octo-org/octo-repo/issues/740
- [ ] Add delight to the experience when all tasks are complete :tada:
