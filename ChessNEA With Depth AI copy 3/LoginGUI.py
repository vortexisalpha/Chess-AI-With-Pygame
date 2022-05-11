import PySimpleGUI as sg
import time
from main2 import *

accountArray = [['admin', 'admin']]

def index2D(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return (i, x.index(v))

def getIfUsernameAndPasswordFromTextFile(username, password):
    with open('accounts.txt', 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            print(lines[i].split(', '))
            if lines[i].split(',')[0] == username and lines[i].split(', ')[1] == password:
                
                return True
        return False

def appendUsernameAndPasswordToTextFile(username, password):
    with open('accounts.txt','a') as f:
        f.writelines('\n'+str(username) + ', ' + str(password))
    f.close()

def replaceUsernameAndPassword(oldUsername,oldPassword, username,password):
    indexGathered = False
    with open('accounts.txt', 'r') as f:# gets index of username/password to return
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].split(',')[0] == oldUsername and lines[i].split(', ')[1] == oldPassword:
                indexGathered = True
                index = i
                lines[index] = str(username) + ', ', str(password)
    f.close()
    if indexGathered:
        with open('accounts.txt', 'w') as f:
            f.writelines(lines[index])
            f.close()
    else:
        sg.Popup('Error finding your login details')

def login():
    layout = [  [sg.Text('Log In')], 
            [sg.Text('Enter Username'), sg.InputText(key = 'tempusername')],  
            [sg.Text('Enter Password'), sg.InputText(key = 'temppassword')],   
            [sg.Button('Login'), sg.Button("Go Back")]
            ]

    window = sg.Window('Login-GUI', layout, margins = (100, 50), return_keyboard_events=True).Finalize()
    active = True
    
    while active == True or sg.WIN_CLOSED:
        event, values = window.read()
        if event == 'Login':
            
            tempusername = values['tempusername']
            temppassword = values['temppassword']
            print(tempusername,temppassword)
            if getIfUsernameAndPasswordFromTextFile(tempusername, temppassword) == True:
                print("yes")
                window.close()
                return True, values['tempusername'], values['temppassword']
                    
            else:
                sg.Popup('your information is not correct')     
        if event == sg.WIN_CLOSED :
                window.close()
                return False, 'admin', 'admin' 
        if event == "Go Back":
            window.close()
            return False, 'admin', 'admin' 
    
def createAccount():
    layout = [  [sg.Text('Log In')], 
            [sg.Text('Enter Username'), sg.InputText(key = 'tempusername')],  
            [sg.Text('Enter Password'), sg.InputText(key = 'temppassword')],   
            [sg.Text('Re-Enter Password'), sg.InputText(key = 'reenterpassword')],
            [sg.Button('Create Account'), sg.Button("Go Back")]
            ]


    window = sg.Window('Login-GUI', layout, margins = (100, 50), return_keyboard_events=True).Finalize()
    active = True
    
    while active == True or sg.WIN_CLOSED:
        event, values = window.read()
        if event == 'Create Account':
            if values['reenterpassword'] == values['temppassword']:
                username = values['tempusername']
                password = values['temppassword']
                window.close()
                return username, password
            else:
                sg.Popup('your passwords do not match')     
        if event == sg.WIN_CLOSED :
                window.close()
                return 'admin', 'admin' 
        if event == "Go Back":
            window.close()
            return 'admin', 'admin'



def changeUsernameOrPassword():
    layout = [  [sg.Text('Change Username/Password')], 
            [sg.Text('Enter Username'), sg.InputText(key = 'tempusername')],  
            [sg.Text('Enter Password'), sg.InputText(key = 'temppassword')],   
            [sg.Text('Re-Enter Password'), sg.InputText(key = 'reenterpassword')],
            [sg.Button('Change'), sg.Button("Go Back")]
            ]

    window = sg.Window('Login-GUI', layout, margins = (100, 50), return_keyboard_events=True).Finalize()
    active = True
    
    while active == True or sg.WIN_CLOSED:
        event, values = window.read()
        if event == 'Change':
            if values['reenterpassword'] == values['temppassword']:
                username = values['tempusername']
                password = values['temppassword']
                window.close()
                return username, password
            else:
                sg.Popup('your passwords do not match')     
        if event == sg.WIN_CLOSED :
                window.close()
                return 'null', 'null' 
        if event == "Go Back":
            window.close()
            return 'null', 'null'

active = True
loggedin = False
layout = [  [sg.Text('MENU')], 
            [sg.Button('Create Account'), ],  
            [sg.Button('Change Username/Password')],    
            [sg.Button('Login')],
            [sg.Button('Play')],
            [sg.Button('Close Window')]
            ]

window = sg.Window('Login-GUI', layout, margins = (100, 50), return_keyboard_events=True).Finalize()
    
while active == True or sg.WIN_CLOSED:
    
    event, values = window.read()
 
    if event == "Close Window" or event == sg.WIN_CLOSED:
        active = False
        break       
    elif event == "Create Account": 
        active = True
        username, password = createAccount()
        if username != 'null':
            loggedin = True
            appendUsernameAndPasswordToTextFile(username, password)
    elif event == "Change Username/Password":
        active = True
        if loggedin:
            try:
                oldUsername = username
                oldPassword = password
            except:
                oldUsername = currentUsername
                oldPassword = currentPassword
            username , password = changeUsernameOrPassword()
            replaceUsernameAndPassword(oldUsername, oldPassword, username,password)
        else:
            sg.Popup('Error: Not Logged In')

    elif event == "Login":
        active == True
        
        loggedin, currentUsername, currentPassword = login()
        

    elif event == "Play":
        if loggedin == True:
            window.close()
            newGame = mainSystem()
            checkmate = newGame.gameRunner()
            if checkmate == True:
                sg.Popup('Checkmate')
        else:
            sg.Popup('Error: Not Logged In')

                
window.close()
