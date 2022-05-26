#Created on Fri Feb  25 15:07:00 2022
# @author: Annajoydejesus

##3-DOF RPP Cylindrical Manipulator (Group 21_MEXE3203)

# THIS IS TO REMOVE THE PANDAS' FUTURE WARNING POPPING UP ON THE BOX
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import PySimpleGUI as sg
import pandas as pd
import numpy as np
import math

# GUI code

sg.theme('DarkRed')

# Excel read code

EXCEL_FILE = '3-DOF RPP Cylindrical Manipulator Data.xlsx'
df = pd.read_excel(EXCEL_FILE)

# Lay-out code

layout = [
    [sg.Text('Fill out the following fields:')],
    [sg.Text('a1 = '), sg.InputText(key='a1', size=(20, 10)), sg.Text('T1 = '), sg.InputText(key='T1', size=(20, 10))],
    [sg.Text('a2 = '), sg.InputText(key='a2', size=(20, 10)), sg.Text('d2 = '), sg.InputText(key='d2', size=(20, 10))],
    [sg.Text('a3 = '), sg.InputText(key='a3', size=(20, 10)), sg.Text('d3 = '), sg.InputText(key='d3', size=(20, 10))],
    [sg.Button('Solve Forward Kinematics')],
    [sg.Frame('Position Vector: ', [[
        sg.Text('X= '), sg.InputText(key='X', size=(10, 1)),
        sg.Text('Y= '), sg.InputText(key='Y', size=(10, 1)),
        sg.Text('Z= '), sg.InputText(key='Z', size=(10, 1))]])],
    [sg.Frame('H0_3 Transformation Matrix = ', [[sg.Output(size=(60, 15))]])],
    [sg.Submit(), sg.Button('Clear Input'), sg.Exit()]
]

# Window Code
window = sg.Window('Cylindrical-RPP Manipulator Forward Kinematics', layout)


def clear_input():
    for key in values:
        window[key]('')
    return None


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear Input':
        clear_input()
    if event == 'Solve Forward Kinematics':
        # Forward Kinematics Codes

        # link lengths in cm
        a1 = values['a1']
        a2 = values['a2']
        a3 = values['a3']

        T1 = values['T1']
        d2 = values['d2']
        d3 = values['d3']

        T1 = (float(T1) / 180.0) * np.pi  # Theta 1 in radians

        DHPT = [[float(T1), (0.0 / 180.0) * np.pi, 0, float(a1)],
                [(270.0 / 180.0) * np.pi, (270.0 / 180.0) * np.pi, 0, float(a2) + float(d2)],
                [(0.0 / 180.0) * np.pi, (0.0 / 180.0) * np.pi, 0, float(a3) + float(d3)]]

        i = 0
        H0_1 = [[np.cos(DHPT[i][0]), -np.sin(DHPT[i][0]) * np.cos(DHPT[i][1]), np.sin(DHPT[i][0]) * np.sin(DHPT[i][1]), DHPT[i][2] * np.cos(DHPT[i][0])],
                [np.sin(DHPT[i][0]), np.cos(DHPT[i][0]) * np.cos(DHPT[i][1]), -np.cos(DHPT[i][0]) * np.sin(DHPT[i][1]), DHPT[i][2] * np.sin(DHPT[i][0])],
                [0, np.sin(DHPT[i][1]), np.cos(DHPT[i][1]), DHPT[i][3]],
                [0, 0, 0, 1]]

        i = 1
        H1_2 = [[np.cos(DHPT[i][0]), -np.sin(DHPT[i][0]) * np.cos(DHPT[i][1]), np.sin(DHPT[i][0]) * np.sin(DHPT[i][1]), DHPT[i][2] * np.cos(DHPT[i][0])],
                [np.sin(DHPT[i][0]), np.cos(DHPT[i][0]) * np.cos(DHPT[i][1]), -np.cos(DHPT[i][0]) * np.sin(DHPT[i][1]), DHPT[i][2] * np.sin(DHPT[i][0])],
                [0, np.sin(DHPT[i][1]), np.cos(DHPT[i][1]), DHPT[i][3]],
                [0, 0, 0, 1]]

        i = 2
        H2_3 = [[np.cos(DHPT[i][0]), -np.sin(DHPT[i][0]) * np.cos(DHPT[i][1]), np.sin(DHPT[i][0]) * np.sin(DHPT[i][1]), DHPT[i][2] * np.cos(DHPT[i][0])],
                [np.sin(DHPT[i][0]), np.cos(DHPT[i][0]) * np.cos(DHPT[i][1]), -np.cos(DHPT[i][0]) * np.sin(DHPT[i][1]), DHPT[i][2] * np.sin(DHPT[i][0])],
                [0, np.sin(DHPT[i][1]), np.cos(DHPT[i][1]), DHPT[i][3]],
                [0, 0, 0, 1]]

        # print("H0_1 = ")
        # print(np.matrix(H0_1))
        # print("H1_2 = ")
        # print(np.matrix(H1_2))
        # print("H2_3 = ")
        # print(np.matrix(H2_3))

        H0_2 = np.dot(H0_1, H1_2)
        H0_3 = np.dot(H0_2, H2_3)

        print("H0_3 = ")
        print(np.matrix(H0_3))

#Position Vector

        X0_3 = H0_3[0, 3]
        print('X = ')
        print(X0_3)

        Y0_3 = H0_3[1, 3]
        print('Y = ')
        print(Y0_3)

        Z0_3 = H0_3[2, 3]
        print('Z = ')
        print(Z0_3)

    if event == 'Submit':
        df = df.append(values, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Data saved!')
        clear_input()
window.close()

