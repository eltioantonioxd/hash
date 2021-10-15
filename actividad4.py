import string
import math
import hashlib

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
    if(len(password)%2 == 0 and password.isalnum() == True):
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

def lectura(fichero):
    with open("./"+fichero, "r", encoding='utf8') as file:
        cont = 0
        for line in file:
            palabra = line.strip()
            print("Contraseña:", palabra, "Hash por defecto:",  hashR(resumen(palabra), palabra))
            cont += 1
            if(cont == 50):
                return file.close()
def entropia(password):
    H = len(password) * math.log2(len(base))
    return H

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
