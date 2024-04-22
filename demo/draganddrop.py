from __future__ import annotations

from typing import Callable, Optional, Protocol

from nicegui import ui

import json

import tools.file as file

filename = "demo/tools/obj_status.json"


class Item(Protocol):
    title: str


dragged: Optional[card] = None


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
        if dragged is not None:
            from_column_name = dragged.parent_slot.parent.name
            to_column_name = self.name
            dragged.parent_slot.parent.remove(dragged)
            with self:
                card(dragged.item)
            self.on_drop(dragged.item, self.name)
            card_name = dragged.item.title
            print(f'Card "{card_name}" moved from {from_column_name} to {to_column_name}')
            dragged = None

            # str todo
            str_obj_status = file.read_from_file(filename)
            obj_status = json.loads(str_obj_status)

            # 1- remove card from old column object.json
            for row_index in obj_status:
                for status  in row_index:
                    if status["col"] == from_column_name:
                        todos = status["todos"]
                        index = todos.index(card_name)
                        todos.pop(index)

            
            # 2- add card to new column object.json
            
            for row_index in obj_status:
                for status  in row_index:
                    if status["col"] == to_column_name:
                        todos = status["todos"]
                        todos.append(card_name)

            # 3- update object.json
            file.write_to_file(filename, json.dumps(obj_status, indent=4))


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
