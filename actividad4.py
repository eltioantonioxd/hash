import string
#from googletrans import Translator

#translator = Translator()
base = str(string.ascii_letters + string.digits + string.punctuation)
base2 = str(string.punctuation)
caracter = []

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
    return Funcion2 + Funcion4 + Funcion1 + Funcion4 + Funcion3 

def F2(password):
    match = ""
    cont=0
    for i in range(len(password)):
        remplazar = int(base.find(password[i])/2 + 4) 
        match += base[remplazar]
        cont += 1
        if(cont >= 3):
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
        for i in range(0, len(base2), 8):
            ofuscar += base2[i]
            cont +=1
            if(cont >= 4):
                return ofuscar
    elif(len(password)%2 == 0 and password.isalnum() == False):
        for i in range(0, len(base2), 4):
            ofuscar += base2[i]
            cont +=1 
            if(cont >= 4):
                return ofuscar
    else:
        for i in range(0, len(base2), 3):
            ofuscar += base2[i]
            cont +=1
            if(cont >= 4):
                return ofuscar
    
        
password = input('Ingrese contraseña: ')
contraseña = resumen(password)
contraseña2 = resumen(contraseña)
hash25 = hashR(contraseña, password)
print(hash25)

'''translation = translator.translate(hash25, dest='ko')
print(translation.text)'''
