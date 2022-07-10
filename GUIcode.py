# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 10:32:56 2022

God and creator of all: Zion Irving-Singh

I swear i didn't say that shit - Nick Hatcher
"""
import Outgas_testbed as ot
from PySimpleGUI import Text, FileBrowse, Input, Button, popup, theme, Window, FolderBrowse, WIN_CLOSED
from pandas import ExcelWriter
from os import startfile, path
from os.path import isfile

def main():

    def make_layout():
         theme('SandyBeach')
         panel = [
            [ Text('Sample Names', font='Helvetica 15')],
            [[ Text(f'Path {i}. '), 
              FileBrowse(target=f'KeyForInput{i}', file_types=(('XML files', '*.XML'),),),
              Input(size=(50,1), enable_events=True, key=f'KeyForInput{i}', justification='center')] for i in range(1, 4)],
            [ Text(text='For blanks please ensure it has "blank" somewhere in the name', text_color='red')],
            [[ Text(f'A{i}. '),  Input(k=f'-INA{i}-'),  Text(f'B{i}. '),  Input(k=f'-INB{i}-')] for i in range(1, 11)],
            [ Text('Please select a destination to save output file'),  FolderBrowse(target='Outputloc'),  Input(size=(50,1), enable_events=True, key='Outputloc')],
            [ Text('Please type a file name.'),  Input(size=(50,1), enable_events=True, key='Outputname')],
            [ Button('Submit'), Button('Exit'),  Button('Open File')]
            ]
         return panel
      
    def build_window():
        return  Window(title='Outgassing calculations', layout=make_layout(), size=(1000, 700), resizable=True)
    #takes the letter and uses it to call the various keys from the pysimple gui
    def val_to_list(letter):
        return [values[f'-IN{letter}{i}-'] + f' {letter}{i}' for i in range(1,11)]
    
    #def name_changer(data_list):
        #for i in data_list:
            #i = i.replace({'Sample': D})
    
    #changes the indices of the dataframes to the names input by the user
    def index_changer(dfL, D):
        lit = []
        for df in dfL:    
            dft = df.assign(Names=D)
            dft.set_index('Names',drop = True, inplace = True)
            lit.append(dft)
        return lit

    window = build_window()
    
    while True:
        event, values = window.read()
        #boolean = values['CHEKR']
        if event ==  WIN_CLOSED or event == 'Exit':
            break
            

        
        if event == 'Open File':
            try:
                startfile(values['Outputloc'] + '/' + values['Outputname'] +'.xlsx')
            except:
                 popup('Looks like you haven\'t made the file yet. Please click submit and try again', title='Error Message')
        if event == 'Submit':
          
            
            try:
                if not path.isfile(values['Outputloc'] + '/' + values['Outputname'] +'.xlsx'):
            
                    #uses inputs to create destination folder
                    writer = ExcelWriter(values['Outputloc'] + '/' + values['Outputname'] +'.xlsx', engine='xlsxwriter')
                    #variable that holds the list of user inputed names
                    D = val_to_list('A') + val_to_list('B')
                    
                    #output = values['Outputloc'] 
                    
                    #creates 3 dataframes using the XML files
                    d1df,d2df,d3df = [ot.df_maker(values[f'KeyForInput{i}']) for i in range(1,4)]
                    
                    #list of the main calculation dataframes
                    blue = index_changer((ot.main_calcs(d1df,d2df,d3df)), D)
                    
                    #concatenates the smaller DF's into one larger dataframe for excel
                    maincalcsDF = blue[0].join(blue[1].join(blue[2],lsuffix='CVCM'),lsuffix='TML',rsuffix='WVR')
                    blanksDF = blue[3].join(blue[4].join(blue[5],lsuffix=' change post conditioning'),lsuffix=' change of boat',rsuffix=' collected')
                    
                    locator = [item for item in D if 'blank' in item]
                    #writes the data to excel
                    maincalcsDF.to_excel(writer,sheet_name='Main data')
                    blanksDF.loc[locator].to_excel(writer,sheet_name='blanks data')
                    writer.save()
                    popup('Everything has been submitted, you can now close both windows.')
                else:
                    popup('That file name is already taken, please try another.', title='Error Message')
            except:
                popup('Something didn\'t work please double check all entries and try again.', title= 'Error message')
        
                
    window.close()

if __name__ == '__main__':
    main()