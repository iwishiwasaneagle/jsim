import pydantic

from jsim.Meta import State


class Vicinity(pydantic.BaseModel, State):
    vicinity: pydantic.conlist(float, min_items=9, max_items=9)

    def __getitem__(self, item):
        return self.vicinity[item]
