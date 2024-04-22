#!/usr/bin/env python3
from dataclasses import dataclass

import draganddrop as dnd

from nicegui import ui

import json

import tools.file as file

filename = "demo/tools/obj_status.json"

str_obj_status = file.read_from_file(filename)

obj_status = json.loads(str_obj_status)

@dataclass
class ToDo:
    title: str


def handle_drop(todo: ToDo, location: str):
    ui.notify(f'"{todo.title}" is now in {location}')


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
ui.run()
