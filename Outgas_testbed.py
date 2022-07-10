# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 11:27:15 2022

God and creator of all: Zion Irving-Singh

In the end, we only regret the chances we didn't take. - Emma Bradford
"""
from pandas import DataFrame,concat
#import pandas as pd
from lxml.etree import fromstring


#This is here for displaying the entire dataset when viewing because pandas truncates them when they're too long
# set_option('display.max_rows', None)

#function is to find, open, and read the XML files
#the xml = temp[3:] cuts out some weird characters at the beginning of each microscale file
def openXML(Path):
    with open(f'{Path}') as file:
        temp = file.read()
        xml = temp[3:]
        return fromstring(bytes(xml, encoding='utf8'))

def listmaker(index, root, obtype):
    listname = []
    for result in root[1][1]:
        for part in result:
            listname.append(obtype(part[index].text))
    return listname

def df_maker(Path):
    return  DataFrame(dataPull(openXML(Path)), columns=['Mass', 'Sample'])



#pulls iD and mass data
def dataPull(root):
    iD = listmaker(0,root,str)
    # woah what the f-bomb? someone is reading this?
    # whats your name, stranger?
    mass = listmaker(1,root,float)
    return list(zip(mass,iD))

def newDF(startDF,index1,index2,column):
    return  DataFrame(startDF[column][index1:index2]).reset_index(drop = True, inplace = False)

def addtoWKSH(item, key, column, name, A, B, ws):
    ws[f'{column}1'] = name
    for i in range(A,B):
        ws[f'{column}{i}'] = item[key][i-2]
def main_calcs(day1DF,day2DF,day3DF):
    Asamps = newDF(day2DF,9,19,'Sample')
    Bsamps = newDF(day2DF,29,39,'Sample')
    Csamps =  concat([Asamps, Bsamps], ignore_index=True)
    
    #initial specimen mass
    initMassA = newDF(day1DF,29,39,'Mass') - newDF(day1DF,9,19,'Mass')
    initMassB = newDF(day1DF,59,69,'Mass') - newDF(day1DF,39,49,'Mass')
    initMassC = concat([initMassA, initMassB], ignore_index=True)
    
    #initial boat mass
    boatMass = concat([(newDF(day1DF,9,19,'Mass')),(newDF(day1DF,39,49,'Mass'))], ignore_index=True)
    #initial boat and specimen mass
    boatNspecMass =  concat([(newDF(day1DF,29,39,'Mass')),(newDF(day1DF,59,69,'Mass'))], ignore_index=True)
    
    # Mass lost 
    lossA = newDF(day1DF,29,39,'Mass') - newDF(day2DF,9,19,'Mass')
    lossB = newDF(day1DF,59,69,'Mass') - newDF(day2DF,29,39,'Mass')
    lossC =  concat([lossA, lossB], ignore_index=True)
    
    #Percent total mass lost
    #calculated by 
    TMLA = 100 * (lossA/initMassA)
    TMLB = 100 * (lossB/initMassB)
    TML =  concat([TMLA, TMLB], ignore_index=True)
    
    #mass collected on target
    #calculated by subtracting final target weight from inital target weight
    collectMassA = newDF(day2DF,19,29,'Mass') - newDF(day1DF,19,29,'Mass')
    collectMassB = newDF(day2DF,39,49,'Mass') - newDF(day1DF,49,59,'Mass')
    collected_mass =  concat([collectMassA, collectMassB], ignore_index=True)
    
    #Percent Condensed volatile mass collectd 
    #Calculated by dividing the mass collected on target by the initial sample mass
    CVCMA = 100 * (collectMassA/initMassA)
    CVCMB = 100 * (collectMassB/initMassB)
    CVCM =  concat([CVCMA, CVCMB], ignore_index=True)
    
    #Calculation of water weight recovered
    # WVR = (Day3 weight - Day2 weight) / initial sample mass
    WVRA = 100 * ((newDF(day3DF,9,19,'Mass') - newDF(day2DF,9,19,'Mass'))/initMassA)
    WVRB = 100 * ((newDF(day3DF,19,29,'Mass') - newDF(day2DF,29,39,'Mass'))/initMassB)
    WVR = concat([WVRA, WVRB], ignore_index=True)
    
    #calculations for blanks
    boatFin  = concat([newDF(day2DF,9,19,'Mass'), newDF(day2DF,29,39,'Mass')], ignore_index=True)
    boat_change = boatMass - boatFin
    boat_PC_change = boatFin - concat([newDF(day3DF,9,19,'Mass'), newDF(day3DF,19,29,'Mass')], ignore_index=True)
    
    tall_order = [TML,CVCM,WVR,boat_change,boat_PC_change,collected_mass]
    
    for item in tall_order[:3]:
        item.rename(columns={'Mass':'%'}, inplace=True)
    
    return tall_order


    
def script():
       
        basepath = 'C:/Users/zionirv/Documents/'    
        root1 = openXML(f'{basepath}OG1.xml')
        root2 = openXML(f'{basepath}OG2e.xml')
        root3 = openXML(f'{basepath}OG3.xml')
        
        
        timestamp1 = root1[0][2].text
        timestamp2 = root2[0][2].text
        timestamp3 = root3[0][2].text
        
        day1DF =  DataFrame(dataPull(root1), columns = ['Mass', 'Sample'])
        day2DF =  DataFrame(dataPull(root2), columns = ['Mass', 'Sample'])
        day3DF =  DataFrame(dataPull(root3), columns = ['Mass', 'Sample'])
        
        
        #The location names for the samples
        Asamps = newDF(day2DF,9,19,'Sample')
        Bsamps = newDF(day2DF,29,39,'Sample')
        Csamps =  concat([Asamps, Bsamps], ignore_index=True)
        
        #initial specimen mass
        initMassA = newDF(day1DF,29,39,'Mass') - newDF(day1DF,9,19,'Mass')
        initMassB = newDF(day1DF,59,69,'Mass') - newDF(day1DF,39,49,'Mass')
        initMassC =  concat([initMassA, initMassB], ignore_index=True)
        
        #initial boat mass
        boatMass =  concat([(newDF(day1DF,9,19,'Mass')),(newDF(day1DF,39,49,'Mass'))], ignore_index=True)
        #initial boat and specimen mass
        boatNspecMass =  concat([(newDF(day1DF,29,39,'Mass')),(newDF(day1DF,59,69,'Mass'))], ignore_index=True)
        
        # Mass lost 
        lossA = newDF(day1DF,29,39,'Mass') - newDF(day2DF,9,19,'Mass')
        lossB = newDF(day1DF,59,69,'Mass') - newDF(day2DF,29,39,'Mass')
        lossC =  concat([lossA, lossB], ignore_index=True)
        
        #Percent total mass lost
        #calculated by 
        TMLA = 100 * (lossA/initMassA)
        TMLB = 100 * (lossB/initMassB)
        TML =  concat([TMLA, TMLB], ignore_index=True)
        
        #mass collected on target
        #calculated by subtracting final target weight from inital target weight
        collectMassA = newDF(day2DF,19,29,'Mass') - newDF(day1DF,19,29,'Mass')
        collectMassB = newDF(day2DF,39,49,'Mass') - newDF(day1DF,49,59,'Mass')
        collected_mass =  concat([collectMassA, collectMassB], ignore_index=True)
        
        
      
        #Percent Condensed volatile mass collectd 
        #Calculated by dividing the mass collected on target by the initial sample mass
        CVCMA = 100 * (collectMassA/initMassA)
        CVCMB = 100 * (collectMassB/initMassB)
        CVCM =  concat([CVCMA, CVCMB], ignore_index=True)
        
        #Calculation of water weight recovered
        # WVR = (Day3 weight - Day2 weight) / initial sample mass
        WVRA = 100 * ((newDF(day3DF,9,19,'Mass') - newDF(day2DF,9,19,'Mass'))/initMassA)
        WVRB = 100 * ((newDF(day3DF,19,29,'Mass') - newDF(day2DF,29,39,'Mass'))/initMassB)
        WVR =  concat([WVRA, WVRB], ignore_index=True)
        
        #calculates using all data but only the blanks will be collected
        #targetInit =  concat([newDF(day1DF,19,29,'Mass'), newDF(day1DF,49,59,'Mass')], ignore_index=True)
        #targetFin  =  concat([newDF(day2DF,19,29,'Mass'), newDF(day2DF,39,49,'Mass')], ignore_index=True)
        boatFin  =  concat([newDF(day2DF,9,19,'Mass'), newDF(day2DF,29,39,'Mass')], ignore_index=True)
        boat_change = boatMass - boatFin
        boat_PC_change = boatFin -  concat([newDF(day3DF,9,19,'Mass'), newDF(day3DF,19,29,'Mass')], ignore_index=True)
        
        tall_order = [TML,CVCM,WVR,boat_change,boat_PC_change,collected_mass]
        
    
       # wb = Workbook()
        #ws = wb.active
        
                
        #addtoWKSH(Csamps,'Sample','A','Location',2,22,ws)
        #addtoWKSH(TML,'Mass','B','% TML',2,22,ws)
        #addtoWKSH(WVR,'Mass','C','% WVR',2,22,ws)
        #addtoWKSH(CVCM,'Mass','D','% CVCM',2,22,ws)
        
                
        #wb.save('balance.xlsx')
        

