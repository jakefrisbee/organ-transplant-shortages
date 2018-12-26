# -*- coding: utf-8 -*-
import os
import csv

###
#
# Initial Setup
#
###

currentDir = os.path.dirname(__file__)
dataFile = 'VS17MORT.txt'
dataFile = os.path.join(currentDir, dataFile)
outputFile = os.path.join(currentDir, '2017potential.csv')

#load exclusions into a Python sets (fastest lookup)
exclusions3 = set()
exclusions4 = set()
exclusionsFile = 'ICD10-exclusions.txt'
with open(exclusionsFile) as fileobject:
    for line in fileobject:
        if len(line.rstrip()) == 3:
            exclusions3.add(line.rstrip())
        elif len(line.rstrip()) == 4:
            exclusions4.add(line.rstrip())
        else:
            print('unknown exclusion in exclusion file')
            
#load inclusions into Python set
inclusions3 = set()
inclusions4 = set()
inclusionsFile = 'ICD10-inclusions.txt'
with open(inclusionsFile) as fileobject:
    for line in fileobject:
        if len(line.rstrip()) == 3:
            inclusions3.add(line.rstrip())
        elif len(line.rstrip()) == 4:
            inclusions4.add(line.rstrip())
        else:
            print('unknown inclusion in inclusion file')
       
# output list headers
output = []
output.append(
        ['residentStatus'
          ,'month'
          ,'gender'
          ,'ageInYears' 
          ,'maritalStatus'
          ,'dayOfWeek'
          ,'autopsy'
          ,'race'
          ,'hispanicOrigin'
          ,'icd10'
          ,'all icd10']
        )
###
#
# functions
#
###
def addToOutput(line):
    #print("not excluded: ", count)
    output.append( [
          line[19] #'residentStatus'
          ,line[64:66] #'month'
          ,line[68] #'gender'
          ,ageInYears #'ageInYears' 
          #,'placeOfDeath': line[82]
          ,line[83] #'maritalStatus'
          ,line[84] #'dayOfWeek'
          ,line[108] #'autopsy'
          ,line[444:446] #'race'
          ,line[483:486] #'hispanicOrigin'
          ,line[145:149].rstrip() #'icd10'
          ,line[343:443] #all ICD10
                ])    

###
#
# Loop through data file
#
###
    
    
with open(dataFile) as fileobject:
    
    for line in fileobject:
        # calculate age in years
        ageIndicator = line[69]
        
        if ageIndicator == '9':
            ageInYears = None
        elif ageIndicator == '1':
            ageInYears = int(line[70:73]) * 1
        elif ageIndicator == '2':
            ageInYears = int(line[70:73]) / 12
        elif ageIndicator == '3':
            ageInYears = int(line[70:73]) / 365
        else:
            ageInYears = 0.5
        
        #remove over age 75
        if ageInYears == None or ageInYears > 75:
            continue
        
        #remove non-inpatient deaths
        #1 is inpatient hospital, ignore everything else
        placeOfDeath = line[82]
        if placeOfDeath != '1':
            continue 
        
        #get all ICD 10 codes for patient
        icd10s = line[343:443].split(' ')
        # remove blank strings
        icd10s = [x for x in icd10s if x]
        
        #check all ICD codes for exclusions, 3 character and 4 character
        include = True
        for i in icd10s:
            if i[:3] in exclusions3:
                #ignore
                include = False
                break
            elif i[:4] in exclusions4:
                #ignore
                include = False
                break
        
        #has passed all exclusions, find an inclusion
        include = False
        for i in icd10s:
            if i[:3] in inclusions3:
                include = True
                break
            elif i[:4] in inclusions4:
                include = True
                break
        
        if include:
            addToOutput(line)

###
#
# Write results
#
###

print('Rows that passed:', len(output))
print('Washington Post method has 27k to 41k for 2016 after applying reduction factor')

with open(outputFile, 'w',newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(output)
