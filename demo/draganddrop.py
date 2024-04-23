from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Optional, Protocol, Dict, Any
import json
import sqlite3

from nicegui import ui

class Item(Protocol):
    title: str
    config: Dict[str, Any]

@dataclass
class ToDo:
    title: str
    config: Dict[str, Any] = field(default_factory=dict)

dragged: Optional[Card] = None

def initialize_db():
    conn = sqlite3.connect('dragdrop.db')
    conn.execute('PRAGMA foreign_keys = ON')  # Enables foreign key support
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS item_configurations (
            item_title TEXT PRIMARY KEY,
            config TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY,
            item_title TEXT,
            from_column TEXT,
            to_column TEXT,
            FOREIGN KEY (item_title) REFERENCES item_configurations(item_title) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

initialize_db()

class Column(ui.column):
    def __init__(self, name: str, on_drop: Optional[Callable[[Item, str], None]] = None) -> None:
        super().__init__()
        with self.classes('bg-blue-grey-2 w-60 p-4 rounded shadow-2'):
            ui.label(name).classes('text-bold ml-1')
        self.name = name
        self.on('dragover.prevent', self.highlight)
        self.on('dragleave', self.unhighlight)
        self.on('drop', self.move_card)
        self.on_drop = on_drop

    def highlight(self) -> None:
        self.classes(remove='bg-blue-grey-2', add='bg-blue-grey-3')

    def unhighlight(self) -> None:
        self.classes(remove='bg-blue-grey-3', add='bg-blue-grey-2')

    def move_card(self) -> None:
        global dragged
        self.unhighlight()
        if dragged:
            from_column = dragged.parent_slot.parent.name
            to_column = self.name
            dragged.parent_slot.parent.remove(dragged)
            with self:
                Card(dragged.item)
            if self.on_drop:
                self.on_drop(dragged.item, self.name)

            conn = sqlite3.connect('dragdrop.db')
            c = conn.cursor()
            c.execute('INSERT INTO actions (item_title, from_column, to_column) VALUES (?,?,?)',
                      (dragged.item.title, from_column, to_column))
            conn.commit()
            conn.close()
            dragged = None

class Card(ui.card):
    def __init__(self, item: Item) -> None:
        super().__init__()
        self.item = item
        self.dialog = ui.dialog()

        with self.props('draggable').classes('w-full cursor-pointer bg-grey-1 p-4 border rounded shadow-lg'):
            ui.label(item.title)
            with ui.context_menu():
                ui.menu_item('Configure', lambda: self.open_configuration_dialog())
                ui.separator()
                ui.menu_item('Close', auto_close=False)
        self.on('dragstart', self.handle_dragstart)

    def open_configuration_dialog(self):
        self.dialog.clear()
        with self.dialog:
            with ui.card().classes('w-64'):
                ui.label(f'Configure {self.item.title}')
                for param, value in self.item.config.items():
                    ui.input(value=value, label=param, on_change=lambda event, p=param: self.update_config(p, event.value))
                ui.button('Save', on_click=lambda: self.dialog.close())
        self.dialog.open()

    def update_config(self, param: str, value: Any):
        self.item.config[param] = value
        self.save_config_to_db()

    def save_config_to_db(self):
        config_json = json.dumps(self.item.config)
        with sqlite3.connect('dragdrop.db') as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO item_configurations (item_title, config)
                            VALUES (?, ?)
                            ON CONFLICT(item_title) DO UPDATE SET
                            config = excluded.config, last_updated = CURRENT_TIMESTAMP''',
                      (self.item.title, config_json))
            conn.commit()

    def handle_dragstart(self) -> None:
        global dragged
        dragged = self

# Additional logic for app initialization and other features can be added here
