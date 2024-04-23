from __future__ import annotations

from typing import Callable, Optional, Protocol

from nicegui import ui

import sqlite3


class Item(Protocol):
    title: str


dragged: Optional[card] = None

def initialize_db():
    conn = sqlite3.connect('dragdrop.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY,
            item_title TEXT,
            from_column TEXT,
            to_column TEXT
        )
    ''')
    conn.commit()
    conn.close()

initialize_db()

class column(ui.column):

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
        global dragged  # pylint: disable=global-statement # noqa: PLW0603
        self.unhighlight()

        from_column = dragged.parent_slot.parent.name
        to_column = self.name

        # Save to database
        conn = sqlite3.connect('dragdrop.db')
        c = conn.cursor()
        c.execute('insert into actions (item_title, from_column, to_column) values (?,?,?)', (dragged.item.title, from_column, to_column)) 
        conn.commit()
        conn.close()

        dragged.parent_slot.parent.remove(dragged)
        with self:
            card(dragged.item)
        self.on_drop(dragged.item, self.name)
        dragged = None


class card(ui.card):

    def __init__(self, item: Item) -> None:
        super().__init__()
        self.item = item
        with self.props('draggable').classes('w-full cursor-pointer bg-grey-1'):
            ui.label(item.title)
        self.on('dragstart', self.handle_dragstart)

    def handle_dragstart(self) -> None:
        global dragged  # pylint: disable=global-statement # noqa: PLW0603
        dragged = self
