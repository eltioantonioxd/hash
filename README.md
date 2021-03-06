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

*Nota: Para la realización de pruebas de rendimiento se limito el archivo **Rockyou.txt** a 50 líneas, asimismo para incorporar ficheros en la lectura este se debe encontrar dentro del mismo directorio*
```python
import string
import math
import hashlib
import re
import time

base = str(string.ascii_letters + string.digits + string.punctuation)
base2 = str(string.punctuation)

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

def resumen(password):
    ultimo = len(password) - 1
    Funcion1 = password[0] + password[ultimo]
    Funcion2 = str(F2(password))
    Funcion3 = str(F3(password))
    Funcion4 = str(F4(password))
    Funcion5 = str(int(math.sqrt(F3(password))))
    return (Funcion2 + Funcion3 + Funcion4 + Funcion1 + Funcion5)

def min_mas(password):
    contador = {'minusculas': 0, 'mayusculas': 0, 'tílde':0}
    for i in password:
        if re.search(r'[À-ÿ]', i):
            contador['tílde'] += 1
        elif i.islower():
            contador['minusculas'] += 1
        elif i.isupper():
            contador['mayusculas'] += 1
    return contador

def F2(password):
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
    
def F3(password):
    pares = 0
    impares = 0
    for i in range(len(password)):
        if(base.find(password[i])%2 == 0):
            pares += base.find(password[i])
        else:
            impares += base.find(password[i])
    return pares * impares 

def F4(password):
    ofuscar = ""
    cont = 0
    minMax = min_mas(password)
    if(minMax['tílde']):
        for i in range(0, len(base2), 2):
            ofuscar += base2[i] + base[i] 
            cont +=1
            if(cont >= 4):
                return ofuscar + password[0] 

    elif(minMax['mayusculas'] > 0 and minMax['minusculas'] > 0):
        for i in range(0, len(base2), 3):
            ofuscar += base2[i] + base[i] 
            cont +=1
            if(cont >= 4):
                return ofuscar + password[len(password)-1]

    elif(minMax['minusculas'] > 0 and minMax['mayusculas'] == False and len(password)%2 == 0):
        for i in range(0, len(base2), 4):
            ofuscar += base2[i] + base[i] 
            cont +=1 
            if(cont >= 4):
                return ofuscar + password[len(password)-1]
    elif(minMax['minusculas'] > 0 and minMax['mayusculas'] == False and len(password)%2 != 0):
        for i in range(0, len(base2), 7):
            ofuscar += base2[i] + base[i] 
            cont +=1 
            if(cont >= 4):
                return ofuscar + password[0] 

    elif(minMax['minusculas'] == False and minMax['mayusculas'] > 0 and len(password)%2 == 0):
        for i in range(0, len(base2), 8):
            ofuscar += base2[i] + base[i]
            cont +=1
            if(cont >= 4):
                return ofuscar + password[len(password)-1]

    elif(minMax['minusculas'] == False and minMax['mayusculas'] > 0 and len(password)%2 != 0):
        for i in range(0, len(base2), 6):
            ofuscar += base2[i] + base[i] 
            cont +=1
            print('hola')
            if(cont >= 4):
                return ofuscar + password[0] 
    elif(password.isdigit()):
        return F3(password)

def lectura(fichero):
    try:
        with open(fichero, "r", encoding='utf8') as file:
            cont = 0
            for line in file:
                palabra = line.strip()
                print("Contraseña:", palabra, "-------> Hash por defecto:",  hashR(resumen(palabra), palabra))
                cont += 1
                if(cont == 50):
                    return file.close()
    except:
        return print('Algo salio mal :(. Corrobora que la ubicación, nombre y extensión del fichero esten correctos')

def entropia(password, Base):
    H = len(password) * math.log2(Base)
    return H

def switch():
    print('Elige el algoritmo a usar o la acción a tomar:')
    print('1.- Nombre del fichero y su extensión')
    print('2.- Hash por defecto (algoritmo creado)')
    print('3.- SHA1')
    print('4.- SHA256')
    print('5.- MDN5')
    
    try:
        seguir = True
        while(seguir):
            opcion = int(input())
            
            if(opcion == 1):
                fichero = input("ingrese la ubicación, nombre y extensión del fichero: ")
                lectura(fichero)
                seguir = False

            elif(opcion ==2):
                password = input("ingrese contraseña: ")
                inicio = time.time()
                contraseña = resumen(password)
                hash25 = hashR(contraseña, password)
                print("Hash creado:", hash25, "     Entropía:", entropia(hash25, 94))
                fin = time.time()
                delta = fin-inicio
                print("Velocidad hash", delta)
                seguir = False

            elif(opcion == 3):
                password = input("ingrese contraseña: ")
                string_to_hash = password
                inicio = time.time()
                hash_object = hashlib.sha1(str(string_to_hash).encode('utf-8'))
                print('Sha1: ', hash_object.hexdigest(), "     Entropía:", entropia(hash_object.hexdigest(), 16))
                fin = time.time()
                delta = fin-inicio
                print("Velocidad hash", delta)
                seguir = False

            elif(opcion == 4):
                password = input("ingrese contraseña: ")
                string_to_hash = password
                inicio = time.time()
                hash_object = hashlib.sha256(str(string_to_hash).encode('utf-8'))
                print('Sha256: ', hash_object.hexdigest(), "     Entropía:", entropia(hash_object.hexdigest(), 16))
                fin = time.time()
                delta = fin-inicio
                print("Velocidad hash", delta)
                seguir = False

            elif(opcion == 5):
                password = input("ingrese contraseña: ")
                string_to_hash = password
                inicio = time.time()
                hash_object = hashlib.md5(str(string_to_hash).encode('utf-8'))
                print('MD5: ', hash_object.hexdigest(), "     Entropía:", entropia(hash_object.hexdigest(), 16))
                fin = time.time()
                delta = fin-inicio
                print("Velocidad hash", delta)
                seguir = False
            else:
                print('Favor escoga una opción válida')
    except ValueError:
        return False

if(switch() == False):
    print('Ups, al parecer no ingreso un dígito')

```
## Explicación del script
El hash funciona a partir de 5 funciones que operan de la siguiente forma:
- Función N°1: Suma el primer y el último caracter de la palabra. ej: crip => F1(crip) = cp
<p align="center">
  <img max-width:100%; src="https://user-images.githubusercontent.com/91589175/138577394-dc13d025-7db2-48e2-bc94-6ac60408ee14.png">
</p>

- Función N°2: Verifica si el caracter i de la contraseña se encuentra en el diccionario, si es así se crea una variable auxiliar (reemplazar) que divide por 2 la posición donde se hizo match con el diccionario y se realiza un corrimiento de 6. Finalmente la variable Match se concatena con la posición de la base[reemplazar] + base[i* 2]. 
ej: crip => F2(crip) = haockeng

<p align="center">
  <img max-width:100%; src="https://user-images.githubusercontent.com/91589175/138577347-fd9b4575-5778-4b10-9b57-4add2ffaf6c9.png">
</p>

- Función N°3: Realiza una sumatoria par e impar de la posición de los caracteres de la password encontradas en el diccionario, posteriormente suma ambos valores.
ej: crip => F3(crip) = 320.

<p align="center">
  <img max-width:100%; src="https://user-images.githubusercontent.com/91589175/138577769-23944b3c-006f-4382-b2dd-31949a2be949.png">
</p>

- Función N°4: Esta función permite diferenciar entre minusculas, máyusculas y acentos para que el hash final varie. Se crea una base auxiliar (base2) que permita hacer uso de caractere especiales. *Nota: la base2 esta compuesta por string.punctuation*

<p align="center">
  <img max-width:100%; src="https://user-images.githubusercontent.com/91589175/138578423-329a4c53-796c-4856-98c5-afe32a2a7a45.png">
</p>

- Función N°5: Obtiene la raiz de la función F3. ej: crip => F5(crip) = raiz(320) = 17.888 => 17 (sólo se considera la parte entera).

<p align="center">
  <img max-width:100%; src="https://user-images.githubusercontent.com/91589175/138577599-8df0bcec-2f43-4197-85fe-314f4095a47b.png">
</p>

- Función resumen: está función suma las funciones anteriormente mencionadas de la siguiente forma: F2 + F3 + F4 + F1 + F5 y retorna dicha suma asociada al hash. Por último, está se corroborá en la función **hashR** que verifica si el hash obtenido es mayor o menor a 25 caracteres.

<p align="center">
  <img max-width:100%; src="https://user-images.githubusercontent.com/91589175/138578816-30a4882a-1317-43ba-8c9f-92a7f8dbad94.png">
</p>

## Comparativa de los hash

| Algoritmo de hash | Base utilizada | Entropia | Velocidad 1 entrada | Velocidad 10 entradas | Velocidad 20 entradas | Velocidad 50 entradas |
| ------------- | ------------- |  ------------- | ------------- |  ------------- | ------------- |   ------------- |
| Algoritmo creado  | 94  |  163.86472129194095  | 0.0007562637329101562 | 0.009054183959960938 | 0.01862621307373047 | 0.07768011093139648 |
| SHA1  | 16 |  160  | 0.0009992122650146484 | 0.0038712024688720703 | 0.010442495346069336 | 0.026409626007080078 |
| SHA256  | 16  |   256  | 0.0008227825164794922  | 0.006069660186767578 | 0.01511073112487793 | 0.03210568428039551 |
| MD5  | 16  |  128  | 0.0003654956817626953  | 0.004673004150390625 | 0.012891530990600586 | 0.02914571762084961 |


