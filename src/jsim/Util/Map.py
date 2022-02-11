from __future__ import annotations

import abc
import os

from jsim.Types import (
    LIST_AND_INDIVIDUAL_COORD,
    LIST_AND_INDIVIDUAL_FLOAT,
    LIST_AND_INDIVIDUAL_INT,
)


class Map(abc.ABC):
    path: str

    def __init__(self, path: str):
        if not os.path.isfile(path):
            raise FileNotFoundError(f'file "{path}" does not exist')
        self.path = path

    @abc.abstractmethod
    def set_crs(self, crs: str) -> Map:
        if crs is None:
            raise TypeError(
                'None type not allowed. Expected string such as "epsg:27700"'
            )
        elif not isinstance(crs, str):
            raise TypeError(
                f'{type(crs)} type not allowed. Expected string such as "epsg:27700"'
            )
        return self

    @abc.abstractmethod
    def at(
        self,
        x: LIST_AND_INDIVIDUAL_INT = None,
        y: LIST_AND_INDIVIDUAL_INT = None,
        coord: LIST_AND_INDIVIDUAL_COORD = None,
    ) -> LIST_AND_INDIVIDUAL_FLOAT:  # pragma: no cover
        pass

    @abc.abstractmethod
    def _at_xy(
        self, x: LIST_AND_INDIVIDUAL_INT, y: LIST_AND_INDIVIDUAL_INT
    ) -> LIST_AND_INDIVIDUAL_INT:  # pragma: no cover
        pass

    @abc.abstractmethod
    def _at_coord(
        self, coord: LIST_AND_INDIVIDUAL_COORD
    ) -> LIST_AND_INDIVIDUAL_FLOAT:  # pragma: no cover
        pass
