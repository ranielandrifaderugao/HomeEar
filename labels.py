sound = {'0':{'sound':'crying baby',
              'color':(0,255,255), #cyan 
              'priority':'0'},
         '1':{'sound':'doorknock',
              'color':(128,0,255), #purple 
              'priority':'0'},
         '2':{'sound':'doorbell',
              'color':(255,50,0), #orange 
              'priority':'0'},
         '3':{'sound':'emergency alarm',
              'color':(255,0,50), #red 
              'priority':'0'},
         '4':{'sound':'kettle whistle',
              'color':(0,255,0), #green
              'priority':'1'},
         '5':{'sound':'telephone',
              'color':(255,255,0), #yellow
              'priority':'1'},
         '6':{'sound':'water running',
              'color':(255,255,255), #white 
              'priority':'1'}
         }

location = {'0':{'location':'living room',
                 'excluded':['4','6']},
            '1':{'location':'kitchen',
                 'excluded':[]},
            '2':{'location':'bedroom',
                 'excluded':['4','6']},
            '3':{'location':'bathroom',
                 'excluded':['4','5']},
            '4':{'location':'dining room',
                 'excluded':['4','6']},
            '5':{'location':'general',
                 'excluded':[]},
            '6':{'location':'',
                 'excluded':[]}
            }

'''sound = {'0':{'sound':'doorbell',
              'color':(255,50,0), #orange
              'priority':'0'},
         '1':{'sound':'doorknock',
              'color':(128,0,255), #purple
              'priority':'0'},
         '2':{'sound':'emergency alarm',
              'color':(255,0,0), #red
              'priority':'0'},
         '3':{'sound':'kettle click',
              'color':(0,255,255), #cyan
              'priority':'1'},
         '4':{'sound':'kettle whistle',
              'color':(255,0,255), #pink
              'priority':'1'},
         '5':{'sound':'microwave beep',
              'color':(0,255,0), #green
              'priority':'1'},
         '6':{'sound':'telephone',
              'color':(0,0,255), #blue
              'priority':'1'},
         '7':{'sound':'wakeup alarm',
              'color':(255,255,0), #yellow
              'priority':'0'},
         '8':{'sound':'washing machine',
              'color':(255,255,0), #light green
              'priority':'1'},
         '9':{'sound':'water running',
              'color':(255,255,255), #white 
              'priority':'1'}
         }
         
location = {'0':{'location':'living room',
                 'excluded':[]},
            '1':{'location':'kitchen',
                 'excluded':[]},
            '2':{'location':'bedroom',
                 'excluded':[]},
            '3':{'location':'bathroom',
                 'excluded':['3','4','5','6']},
            '4':{'location':'dining room',
                 'excluded':['3','4','5','8','9']},
            '5':{'location':'general',
                 'excluded':[]},
            '6':{'location':'',
                 'excluded':[]}
            }
location = {'0':{'location':'living room',
                 'excluded':['3','4','5','8','9']},
            '1':{'location':'kitchen',
                 'excluded':[]},
            '2':{'location':'bedroom',
                 'excluded':['3','4','5','8','9']},
            '3':{'location':'bathroom',
                 'excluded':['3','4','5','6']},
            '4':{'location':'dining room',
                 'excluded':['3','4','5','8','9']},
            '5':{'location':'general',
                 'excluded':[]},
            '6':{'location':'',
                 'excluded':[]}
            }
'''
