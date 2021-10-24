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
- Función N°1: Suma el primer y el último caracter de la palabra. ej: Hola => F1(Hola) = Ha
- Función N°2: Verifica si el caracter i de la contraseña se encuentra en el diccionario, si es así se crea una variable auxiliar (reemplazar) que divide por 2 la posición donde se hizo match con el diccionario y se realiza un corrimiento de 6. Finalmente la variable Match se concatena con la posición de la base[reemplazar] + base[i* 2]. 
ej: abcd => F2(abcd) = gagchehf
- Función N°3: Realiza una sumatoria par e impar de la posición de los caracteres de la password encontradas en el diccionario, posteriormente suma ambos valores.
ej: crip => F3(crip) = 320
- Función N°4: Esta función permite diferenciar entre minusculas, máyusculas y acentos para que el hash final varie. Se crea una base auxiliar (base2) que permita hacer uso de caractere especiales.

- Función N°5: Obtiene la raiz de la función F3. ej: crip => F5(crip) = raiz(320) = 17.888 => 17 (sólo se considera la parte entera)
- Función resumen: está función suma las funciones anteriormente mencionadas de la siguiente forma: F2 + F3 + F4 + F1 + F5 y retorna dicha suma asociada al hash. Por último, está se corroborá en la función **hashR** que verifica si el hash obtenido es mayor o menor a 25 caracteres.
%3CmxGraphModel%3E%3Croot%3E%3CmxCell%20id%3D%220%22%2F%3E%3CmxCell%20id%3D%221%22%20parent%3D%220%22%2F%3E%3CmxCell%20id%3D%222%22%20style%3D%22edgeStyle%3DorthogonalEdgeStyle%3Brounded%3D0%3BorthogonalLoop%3D1%3BjettySize%3Dauto%3Bhtml%3D1%3BexitX%3D0.5%3BexitY%3D1%3BexitDx%3D0%3BexitDy%3D0%3BentryX%3D0.5%3BentryY%3D0%3BentryDx%3D0%3BentryDy%3D0%3B%22%20edge%3D%221%22%20source%3D%223%22%20parent%3D%221%22%3E%3CmxGeometry%20relative%3D%221%22%20as%3D%22geometry%22%3E%3CmxPoint%20x%3D%221969.9999999999995%22%20y%3D%22239.9999999999999%22%20as%3D%22targetPoint%22%2F%3E%3C%2FmxGeometry%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%223%22%20value%3D%22crip%22%20style%3D%22rounded%3D0%3BwhiteSpace%3Dwrap%3Bhtml%3D1%3B%22%20vertex%3D%221%22%20parent%3D%221%22%3E%3CmxGeometry%20x%3D%221910%22%20y%3D%22120%22%20width%3D%22120%22%20height%3D%2260%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%224%22%20style%3D%22edgeStyle%3DorthogonalEdgeStyle%3Brounded%3D0%3BorthogonalLoop%3D1%3BjettySize%3Dauto%3Bhtml%3D1%3BexitX%3D0%3BexitY%3D0.5%3BexitDx%3D0%3BexitDy%3D0%3B%22%20edge%3D%221%22%20source%3D%228%22%20target%3D%2210%22%20parent%3D%221%22%3E%3CmxGeometry%20relative%3D%221%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%225%22%20style%3D%22edgeStyle%3DorthogonalEdgeStyle%3Brounded%3D0%3BorthogonalLoop%3D1%3BjettySize%3Dauto%3Bhtml%3D1%3BexitX%3D1%3BexitY%3D0.5%3BexitDx%3D0%3BexitDy%3D0%3BentryX%3D0.5%3BentryY%3D0%3BentryDx%3D0%3BentryDy%3D0%3B%22%20edge%3D%221%22%20source%3D%228%22%20parent%3D%221%22%3E%3CmxGeometry%20relative%3D%221%22%20as%3D%22geometry%22%3E%3CmxPoint%20x%3D%222199.9999999999995%22%20y%3D%22329.9999999999999%22%20as%3D%22targetPoint%22%2F%3E%3C%2FmxGeometry%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%226%22%20style%3D%22edgeStyle%3DorthogonalEdgeStyle%3Brounded%3D0%3BorthogonalLoop%3D1%3BjettySize%3Dauto%3Bhtml%3D1%3BexitX%3D0%3BexitY%3D0.75%3BexitDx%3D0%3BexitDy%3D0%3BentryX%3D0.5%3BentryY%3D0%3BentryDx%3D0%3BentryDy%3D0%3B%22%20edge%3D%221%22%20source%3D%228%22%20target%3D%2214%22%20parent%3D%221%22%3E%3CmxGeometry%20relative%3D%221%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%227%22%20style%3D%22edgeStyle%3DorthogonalEdgeStyle%3Brounded%3D0%3BorthogonalLoop%3D1%3BjettySize%3Dauto%3Bhtml%3D1%3BexitX%3D1%3BexitY%3D0.75%3BexitDx%3D0%3BexitDy%3D0%3BentryX%3D0.5%3BentryY%3D0%3BentryDx%3D0%3BentryDy%3D0%3B%22%20edge%3D%221%22%20source%3D%228%22%20target%3D%2216%22%20parent%3D%221%22%3E%3CmxGeometry%20relative%3D%221%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%228%22%20value%3D%22F2(crip)%22%20style%3D%22rounded%3D0%3BwhiteSpace%3Dwrap%3Bhtml%3D1%3B%22%20vertex%3D%221%22%20parent%3D%221%22%3E%3CmxGeometry%20x%3D%221910%22%20y%3D%22240%22%20width%3D%22120%22%20height%3D%2260%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%229%22%20style%3D%22edgeStyle%3DorthogonalEdgeStyle%3Brounded%3D0%3BorthogonalLoop%3D1%3BjettySize%3Dauto%3Bhtml%3D1%3BexitX%3D0.5%3BexitY%3D1%3BexitDx%3D0%3BexitDy%3D0%3BentryX%3D0.5%3BentryY%3D0%3BentryDx%3D0%3BentryDy%3D0%3BfontSize%3D12%3B%22%20edge%3D%221%22%20source%3D%2210%22%20target%3D%2218%22%20parent%3D%221%22%3E%3CmxGeometry%20relative%3D%221%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2210%22%20value%3D%22c%20(2)%22%20style%3D%22rounded%3D0%3BwhiteSpace%3Dwrap%3Bhtml%3D1%3B%22%20vertex%3D%221%22%20parent%3D%221%22%3E%3CmxGeometry%20x%3D%221660%22%20y%3D%22330%22%20width%3D%22120%22%20height%3D%2260%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2211%22%20value%3D%22%22%20style%3D%22edgeStyle%3DorthogonalEdgeStyle%3Brounded%3D0%3BorthogonalLoop%3D1%3BjettySize%3Dauto%3Bhtml%3D1%3BfontSize%3D12%3B%22%20edge%3D%221%22%20source%3D%2212%22%20target%3D%2224%22%20parent%3D%221%22%3E%3CmxGeometry%20relative%3D%221%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2212%22%20value%3D%22p%20(15)%22%20style%3D%22rounded%3D0%3BwhiteSpace%3Dwrap%3Bhtml%3D1%3B%22%20vertex%3D%221%22%20parent%3D%221%22%3E%3CmxGeometry%20x%3D%222140%22%20y%3D%22330%22%20width%3D%22120%22%20height%3D%2260%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2213%22%20style%3D%22edgeStyle%3DorthogonalEdgeStyle%3Brounded%3D0%3BorthogonalLoop%3D1%3BjettySize%3Dauto%3Bhtml%3D1%3BexitX%3D0.5%3BexitY%3D1%3BexitDx%3D0%3BexitDy%3D0%3BentryX%3D0.5%3BentryY%3D0%3BentryDx%3D0%3BentryDy%3D0%3BfontSize%3D12%3B%22%20edge%3D%221%22%20source%3D%2214%22%20target%3D%2220%22%20parent%3D%221%22%3E%3CmxGeometry%20relative%3D%221%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2214%22%20value%3D%22r%20(17)%22%20style%3D%22rounded%3D0%3BwhiteSpace%3Dwrap%3Bhtml%3D1%3B%22%20vertex%3D%221%22%20parent%3D%221%22%3E%3CmxGeometry%20x%3D%221820%22%20y%3D%22330%22%20width%3D%22120%22%20height%3D%2260%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2215%22%20style%3D%22edgeStyle%3DorthogonalEdgeStyle%3Brounded%3D0%3BorthogonalLoop%3D1%3BjettySize%3Dauto%3Bhtml%3D1%3BexitX%3D0.5%3BexitY%3D1%3BexitDx%3D0%3BexitDy%3D0%3BentryX%3D0.5%3BentryY%3D0%3BentryDx%3D0%3BentryDy%3D0%3BfontSize%3D12%3B%22%20edge%3D%221%22%20source%3D%2216%22%20target%3D%2222%22%20parent%3D%221%22%3E%3CmxGeometry%20relative%3D%221%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2216%22%20value%3D%22i%20(8)%22%20style%3D%22rounded%3D0%3BwhiteSpace%3Dwrap%3Bhtml%3D1%3B%22%20vertex%3D%221%22%20parent%3D%221%22%3E%3CmxGeometry%20x%3D%221990%22%20y%3D%22330%22%20width%3D%22120%22%20height%3D%2260%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2217%22%20style%3D%22edgeStyle%3DorthogonalEdgeStyle%3Brounded%3D0%3BorthogonalLoop%3D1%3BjettySize%3Dauto%3Bhtml%3D1%3BexitX%3D0.5%3BexitY%3D1%3BexitDx%3D0%3BexitDy%3D0%3BentryX%3D0.5%3BentryY%3D0%3BentryDx%3D0%3BentryDy%3D0%3BfontSize%3D12%3BfontColor%3D%23000000%3B%22%20edge%3D%221%22%20source%3D%2218%22%20target%3D%2226%22%20parent%3D%221%22%3E%3CmxGeometry%20relative%3D%221%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2218%22%20value%3D%22%26lt%3Bb%26gt%3B2%26lt%3B%2Fb%26gt%3B%2F2%20%2B%206%22%20style%3D%22rounded%3D0%3BwhiteSpace%3Dwrap%3Bhtml%3D1%3B%22%20vertex%3D%221%22%20parent%3D%221%22%3E%3CmxGeometry%20x%3D%221660%22%20y%3D%22430%22%20width%3D%22120%22%20height%3D%2260%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2219%22%20style%3D%22edgeStyle%3DorthogonalEdgeStyle%3Brounded%3D0%3BorthogonalLoop%3D1%3BjettySize%3Dauto%3Bhtml%3D1%3BexitX%3D0.5%3BexitY%3D1%3BexitDx%3D0%3BexitDy%3D0%3BentryX%3D0.5%3BentryY%3D0%3BentryDx%3D0%3BentryDy%3D0%3BfontSize%3D12%3BfontColor%3D%23000000%3B%22%20edge%3D%221%22%20source%3D%2220%22%20target%3D%2228%22%20parent%3D%221%22%3E%3CmxGeometry%20relative%3D%221%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2220%22%20value%3D%22%26lt%3Bb%26gt%3B17%26lt%3B%2Fb%26gt%3B%2F2%20%2B%206%22%20style%3D%22rounded%3D0%3BwhiteSpace%3Dwrap%3Bhtml%3D1%3B%22%20vertex%3D%221%22%20parent%3D%221%22%3E%3CmxGeometry%20x%3D%221820%22%20y%3D%22430%22%20width%3D%22120%22%20height%3D%2260%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2221%22%20style%3D%22edgeStyle%3DorthogonalEdgeStyle%3Brounded%3D0%3BorthogonalLoop%3D1%3BjettySize%3Dauto%3Bhtml%3D1%3BexitX%3D0.5%3BexitY%3D1%3BexitDx%3D0%3BexitDy%3D0%3BentryX%3D0.5%3BentryY%3D0%3BentryDx%3D0%3BentryDy%3D0%3BfontSize%3D12%3BfontColor%3D%23000000%3B%22%20edge%3D%221%22%20source%3D%2222%22%20target%3D%2230%22%20parent%3D%221%22%3E%3CmxGeometry%20relative%3D%221%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2222%22%20value%3D%22%26lt%3Bb%26gt%3B8%26lt%3B%2Fb%26gt%3B%2F2%20%2B%206%22%20style%3D%22rounded%3D0%3BwhiteSpace%3Dwrap%3Bhtml%3D1%3B%22%20vertex%3D%221%22%20parent%3D%221%22%3E%3CmxGeometry%20x%3D%221990%22%20y%3D%22430%22%20width%3D%22120%22%20height%3D%2260%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2223%22%20style%3D%22edgeStyle%3DorthogonalEdgeStyle%3Brounded%3D0%3BorthogonalLoop%3D1%3BjettySize%3Dauto%3Bhtml%3D1%3BexitX%3D0.5%3BexitY%3D1%3BexitDx%3D0%3BexitDy%3D0%3BentryX%3D0.5%3BentryY%3D0%3BentryDx%3D0%3BentryDy%3D0%3BfontSize%3D12%3BfontColor%3D%23000000%3B%22%20edge%3D%221%22%20source%3D%2224%22%20target%3D%2232%22%20parent%3D%221%22%3E%3CmxGeometry%20relative%3D%221%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2224%22%20value%3D%22%26lt%3Bb%26gt%3B15%26lt%3B%2Fb%26gt%3B%2F2%20%2B%206%22%20style%3D%22rounded%3D0%3BwhiteSpace%3Dwrap%3Bhtml%3D1%3B%22%20vertex%3D%221%22%20parent%3D%221%22%3E%3CmxGeometry%20x%3D%222140%22%20y%3D%22430%22%20width%3D%22120%22%20height%3D%2260%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2225%22%20style%3D%22edgeStyle%3DorthogonalEdgeStyle%3Brounded%3D0%3BorthogonalLoop%3D1%3BjettySize%3Dauto%3Bhtml%3D1%3BexitX%3D0.5%3BexitY%3D1%3BexitDx%3D0%3BexitDy%3D0%3BentryX%3D0%3BentryY%3D0.5%3BentryDx%3D0%3BentryDy%3D0%3BfontSize%3D12%3BfontColor%3D%23000000%3B%22%20edge%3D%221%22%20source%3D%2226%22%20target%3D%2233%22%20parent%3D%221%22%3E%3CmxGeometry%20relative%3D%221%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2226%22%20value%3D%22h%20(7)%20%2B%20a%20(0)%26amp%3Bnbsp%3B%22%20style%3D%22rounded%3D0%3BwhiteSpace%3Dwrap%3Bhtml%3D1%3BfontSize%3D12%3BfontColor%3D%23000000%3B%22%20vertex%3D%221%22%20parent%3D%221%22%3E%3CmxGeometry%20x%3D%221660%22%20y%3D%22530%22%20width%3D%22120%22%20height%3D%2260%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2227%22%20style%3D%22edgeStyle%3DorthogonalEdgeStyle%3Brounded%3D0%3BorthogonalLoop%3D1%3BjettySize%3Dauto%3Bhtml%3D1%3BentryX%3D0.25%3BentryY%3D0%3BentryDx%3D0%3BentryDy%3D0%3BfontSize%3D12%3BfontColor%3D%23000000%3B%22%20edge%3D%221%22%20source%3D%2228%22%20target%3D%2233%22%20parent%3D%221%22%3E%3CmxGeometry%20relative%3D%221%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2228%22%20value%3D%22o%20(14)%20%2B%20c%20(2)%22%20style%3D%22rounded%3D0%3BwhiteSpace%3Dwrap%3Bhtml%3D1%3BfontSize%3D12%3BfontColor%3D%23000000%3B%22%20vertex%3D%221%22%20parent%3D%221%22%3E%3CmxGeometry%20x%3D%221820%22%20y%3D%22530%22%20width%3D%22120%22%20height%3D%2260%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2229%22%20style%3D%22edgeStyle%3DorthogonalEdgeStyle%3Brounded%3D0%3BorthogonalLoop%3D1%3BjettySize%3Dauto%3Bhtml%3D1%3BexitX%3D0.5%3BexitY%3D1%3BexitDx%3D0%3BexitDy%3D0%3BentryX%3D0.75%3BentryY%3D0%3BentryDx%3D0%3BentryDy%3D0%3BfontSize%3D12%3BfontColor%3D%23000000%3B%22%20edge%3D%221%22%20source%3D%2230%22%20target%3D%2233%22%20parent%3D%221%22%3E%3CmxGeometry%20relative%3D%221%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2230%22%20value%3D%22k%20(10)%20%2B%20e%20(4)%22%20style%3D%22rounded%3D0%3BwhiteSpace%3Dwrap%3Bhtml%3D1%3BfontSize%3D12%3BfontColor%3D%23000000%3B%22%20vertex%3D%221%22%20parent%3D%221%22%3E%3CmxGeometry%20x%3D%221990%22%20y%3D%22530%22%20width%3D%22120%22%20height%3D%2260%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2231%22%20style%3D%22edgeStyle%3DorthogonalEdgeStyle%3Brounded%3D0%3BorthogonalLoop%3D1%3BjettySize%3Dauto%3Bhtml%3D1%3BexitX%3D0.5%3BexitY%3D1%3BexitDx%3D0%3BexitDy%3D0%3BentryX%3D1%3BentryY%3D0.5%3BentryDx%3D0%3BentryDy%3D0%3BfontSize%3D12%3BfontColor%3D%23000000%3B%22%20edge%3D%221%22%20source%3D%2232%22%20target%3D%2233%22%20parent%3D%221%22%3E%3CmxGeometry%20relative%3D%221%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2232%22%20value%3D%22n%20(13)%20%2B%20g%20(6)%22%20style%3D%22rounded%3D0%3BwhiteSpace%3Dwrap%3Bhtml%3D1%3BfontSize%3D12%3BfontColor%3D%23000000%3B%22%20vertex%3D%221%22%20parent%3D%221%22%3E%3CmxGeometry%20x%3D%222140%22%20y%3D%22530%22%20width%3D%22120%22%20height%3D%2260%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3CmxCell%20id%3D%2233%22%20value%3D%22haockeng%22%20style%3D%22rounded%3D0%3BwhiteSpace%3Dwrap%3Bhtml%3D1%3BfontSize%3D12%3BfontColor%3D%23000000%3B%22%20vertex%3D%221%22%20parent%3D%221%22%3E%3CmxGeometry%20x%3D%221910%22%20y%3D%22640%22%20width%3D%22120%22%20height%3D%2260%22%20as%3D%22geometry%22%2F%3E%3C%2FmxCell%3E%3C%2Froot%3E%3C%2FmxGraphModel%3E
## Comparativa de los hash

| Algoritmo de hash | Base utilizada | Entropia | Velocidad 1 entrada | Velocidad 10 entradas | Velocidad 20 entradas | Velocidad 50 entradas |
| ------------- | ------------- |  ------------- | ------------- |  ------------- | ------------- |   ------------- |
| Algoritmo creado  | 94  |  163.86472129194095  | 0.0007562637329101562 | 0.009054183959960938 | 0.01862621307373047 | 0.07768011093139648 |
| SHA1  | 16 |  160  | 0.0 | 0.0038712024688720703 | 0.010442495346069336 | 0.026409626007080078 |
| SHA256  | 16  |   256  | 0.0008227825164794922  | 0.006069660186767578 | 0.01511073112487793 | 0.03210568428039551 |
| MD5  | 16  |  128  | 0.0003654956817626953  | 0.004673004150390625 | 0.012891530990600586 | 0.02914571762084961 |


## Lista de tareas

- [x] Hito I
- [x] Hito II
- [x] Hito III
- [ ] Hito IV


