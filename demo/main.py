#!/usr/bin/env python3
from dataclasses import dataclass

import draganddrop as dnd

from nicegui import ui

import json

import tools.file as file

filename = "demo/tools/obj_status.json"

str_obj_status = file.read_from_file(filename)

obj_status = json.loads(str_obj_status)

input_text = ""  # This variable will store the current input value

new_input_text = "" # This variable will store the


@dataclass
class ToDo:
    title: str


def handle_drop(todo: ToDo, location: str):
    ui.notify(f'"{todo.title}" is now in {location}')

def on_input_change(event):
    global input_text
    input_text = event.value
    print("USERNAME", input_text)



def on_submit():
    if input_text:
        str_obj_status = file.read_from_file(filename)
        new_input_text = f"new_{input_text}.json" 
        file.write_to_file(new_input_text, str_obj_status)

        obj_status = json.loads(str_obj_status)

        for row_index in obj_status:
            with ui.row():
                for status  in row_index:
                    with dnd.column(status["col"], on_drop=handle_drop):
                        todos = status["todos"]
                        if len(todos) > 0:
                            for todo in todos:
                                dnd.card(ToDo(todo))
                        else:
                            print(f'No todos in {status["col"]}')
            












'''with ui.row():
    with dnd.column('Devices', on_drop=handle_drop):
        dnd.card(ToDo('Device1'))
        dnd.card(ToDo('Device2'))
    with dnd.column('fucntions', on_drop=handle_drop):
        dnd.card(ToDo('='))
        dnd.card(ToDo('>'))
        dnd.card(ToDo('<'))
        dnd.card(ToDo('=>'))
        dnd.card(ToDo('=<'))
    with dnd.column('Actions', on_drop=handle_drop):
        dnd.card(ToDo('alert'))
        dnd.card(ToDo('trigger valve'))
        dnd.card(ToDo('something else?'))
        

with ui.row():
    with dnd.column('Sensor', on_drop=handle_drop):
        print()

    with dnd.column('Sensor Data', on_drop=handle_drop):
        print()

    with dnd.column('Function', on_drop=handle_drop):
        print()


    with dnd.column('Action', on_drop=handle_drop):
        print()
'''

username_input = ui.input(
    placeholder='Enter username', 
    on_change=on_input_change)

submit_button = ui.button('Submit', on_click=on_submit)

ui.run()
