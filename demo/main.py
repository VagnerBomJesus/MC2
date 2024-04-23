#!/usr/bin/env python3

import draganddrop as dnd
from nicegui import ui

def handle_drop(todo: dnd.ToDo, location: str):
    ui.notify(f'"{todo.title}" is now in {location}')
    
with ui.row():
    with dnd.Column('Devices', on_drop=handle_drop):
        dnd.Card(dnd.ToDo('Device1', config={'status': 'active'}))  # Adicionando configuração de exemplo
        dnd.Card(dnd.ToDo('Device2', config={'status': 'inactive'}))

    # Functions Column with logical operators
    with dnd.Column('Functions', on_drop=handle_drop):
        dnd.Card(dnd.ToDo('=', config={'description': 'equality'}))
        dnd.Card(dnd.ToDo('>', config={'description': 'greater than'}))
        dnd.Card(dnd.ToDo('<', config={'description': 'less than'}))
        dnd.Card(dnd.ToDo('>=', config={'description': 'greater than or equal to'}))
        dnd.Card(dnd.ToDo('<=', config={'description': 'less than or equal to'}))

    # Actions Column
    with dnd.Column('Actions', on_drop=handle_drop):
        dnd.Card(dnd.ToDo('Alert', config={'action_type': 'warning'}))
        dnd.Card(dnd.ToDo('Trigger Valve', config={'action_type': 'mechanical'}))
        dnd.Card(dnd.ToDo('Something Else?', config={'action_type': 'custom'}))

with ui.row():
    with dnd.Column('Sensor', on_drop=handle_drop):
        pass

    with dnd.Column('Sensor Data', on_drop=handle_drop):
        pass

    with dnd.Column('Function', on_drop=handle_drop):
        pass

    with dnd.Column('Action', on_drop=handle_drop):
        pass

ui.run()
