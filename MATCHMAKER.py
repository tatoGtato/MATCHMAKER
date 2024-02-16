import random
import string
from collections import Counter
import pandas as pd


class Persona:
  def __init__(self, id, email,nombre,telefono, edad, genero, preferencia, gustos, 
               divertidx):
    self.id = id  
    self.email = email
    self.nombre = nombre
    self.telefono = telefono
    self.edad = edad
    self.menorEdad = True if edad < 18 else False
    self.genero = genero
    self.preferencia = preferencia
    self.gustos = gustos
    self.divertidx = divertidx
    self.matches = []
    self.matches2 = []
    
  def __str__(self):
    return f"""{self.nombre} {self.edad} {self.genero} {self.preferencia} {self.divertidx}"""

  def __repr__(self):
        return f'{self.nombre} {self.edad} {self.genero} {self.preferencia}  {self.divertidx}'

  def genderFilter(self, other):
      
      if(self.genero in other.preferencia and other.genero in self.preferencia):
          return True
      else: return False  
      
  def minorFilter(self, other):
      if (self.menorEdad == other.menorEdad):
          return True
      else: return False  
      
  def ageFilter(self, other):
      if(abs(self.edad - other.edad) <= 3):
          return True 
      else: return False          
  
  def hobbieFilter(self, other):
        a = self.gustos
        b = other.gustos
        a_vals = Counter(a)
        b_vals = Counter(b)

        # convert to word-vectors
        words  = list(a_vals.keys() | b_vals.keys())
        a_vect = [a_vals.get(word, 0) for word in words]        # [0, 0, 1, 1, 2, 1]
        b_vect = [b_vals.get(word, 0) for word in words]        # [1, 1, 1, 0, 1, 0]

        # find cosine
        len_a  = sum(av*av for av in a_vect) ** 0.5             # sqrt(7)
        len_b  = sum(bv*bv for bv in b_vect) ** 0.5             # sqrt(4)
        dot    = sum(av*bv for av,bv in zip(a_vect, b_vect))    # 3
        cosine = dot / (len_a * len_b)     
        return cosine


  def divertidxFilter(self, other):
    if (self.divertidx != other.divertidx):
        return True
    else: return False  



def displayMatches(concursantes):
    for i in concursantes:
        print(f"{i.id} - NOMBRE: {i.nombre} MATCHES: {i.matches}")
        print("\n")

def randomlyGenerateObjects(n):
    concursantes = []
    for i in range (0, n):
        concursantes.append(Persona(i,
                                    random.choice(string.ascii_letters), 
                                    random.randrange(20,23,1),                                    
                                    random.choice(["m","f", "nb", "o"]),
                                    [
                                        random.choice(["m","f", "nb", "o"]),
                                        random.choice(["m","f", "nb", "o", ""])
                                    ],
                                    [
                                       random.choice(["a","b","c","d"]), 
                                       random.choice(["e","f","g","h"]),
                                       random.choice(["i","j","k","l"]),
                                       random.choice(["m","n","o","p"]),
                                       random.choice(["q","r","s","t"]),
                                    ],
                                    random.choice(["Intro","Extro","Ambi"]),
                                    ))
    
    return concursantes       

def initialFilter(conc):
    for i in conc:
        for j in conc:
            if (i != j and i.minorFilter(j)):
                i.matches.append(j)

def gendFilters(concursantes):
    for i in concursantes:
        for j in i.matches:
            if (i.genderFilter(j) == True):
                i.matches2.append(j)
        i.matches = []

def ageFilters(concursantes):
    for i in concursantes:
        for j in i.matches2:
            if (i.ageFilter(j) == True):
                i.matches.append(j)
        i.matches2 = []
        
def diverFilter(concursantes):
    for i in concursantes:
        for j in i.matches:
            if (i.divertidxFilter(j) == True):
                i.matches2.append(j)
        i.matches = []

#UNA LISTRA SORTIARLA Y COGER EL TOP n
def hobbFilter(concursantes, n):
    for i in concursantes:
        cosineVals = {}
        if (i.matches2 != []):
            for j in i.matches2:
                cosineVals[j] = i.hobbieFilter(j) 
            cosineValsSorted = dict(sorted(cosineVals.items(), key=lambda item: item[1], reverse=True))
            i.matches.append(list(cosineValsSorted)[0])

                   
        i.matches2 = []

def matchmaker(concursantes):
    initialFilter(concursantes)
    gendFilters(concursantes)
    ageFilters(concursantes)
    diverFilter(concursantes)
    hobbFilter(concursantes, 1)

    
def matchmakerMinus(concursantes):
    initialFilter(concursantes)
    gendFilters(concursantes)
    hobbFilter(concursantes, 1)


def solveForMatchButNoMatch(matches):
    for i in matches:
        for j in matches:
            if(i != j):
                if (i in j.matches and j not in i.matches):
                    i.matches.append(j)

def solveForUnMatches(matches):
    genteMatcheada = []
    for i in matches:
        for j in matches:
            if(i != j):
                if (i in j.matches and j in i.matches):
                    if (i not in genteMatcheada):
                        genteMatcheada.append(i)
    print(len(genteMatcheada))
    genteSola = [item for item in matches if item not in genteMatcheada]
    print(len(genteSola))
    print(genteSola)
    matchmakerMinus(genteSola)
    
    
#conc = randomlyGenerateObjects(30)


df = pd.read_excel('Matchmaker.xlsx', sheet_name='Sheet1') 


afortunados = df.values.tolist()
afortunados_instances = []

    
def setUpDataBase(afortunados, afortunados_instances):
    
    for p in afortunados:
        afortunados_instances.append(Persona(*p))
    
    for p in afortunados_instances:
        prefsToList = list(p.preferencia.split(";"))
        print(prefsToList)
        prefsToList.remove("")
        p.preferencia = prefsToList
        
        gustosToList = list(p.gustos.split(";"))
        p.gustos = gustosToList

    

setUpDataBase(afortunados, afortunados_instances)

print(afortunados_instances)

print("MATCHESS")
matchmaker(afortunados_instances)
displayMatches(afortunados_instances)

print("\n")
print("MATCHESS BUT NO MATCHES SOLVED")
solveForMatchButNoMatch(afortunados_instances)
displayMatches(afortunados_instances)

print("\n")
print("UNMATCHESS SOLVED")
solveForUnMatches(afortunados_instances)
displayMatches(afortunados_instances)

