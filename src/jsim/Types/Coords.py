from typing import List

import numpy as np
import pydantic

from jsim.Types.Coord import Coord


class Coords(pydantic.BaseModel):
    """
    Type class hold multiple :class:`~jsim.Types.Coord.Coord` in a list.
    """

    coords: List[Coord]

    def __getitem__(self, item):
        return self.coords[item]

    def __len__(self) -> int:
        return len(self.coords)

    def to_numpy(self) -> np.ndarray:
        """
        Convert the :attr:`~jsim.Util.Types.Coords.Coords.coords` to a
        :class:`numpy.ndarray`.

        :return: A list of :attr:`~jsim.Util.Types.Coord.Coord`
        :rtype: numpy.ndarray
        """
        return np.array([(f.x, f.y) for f in self.coords])

    def append(self, item: Coord) -> None:
        """
        Add to the end of the coords list.

        :param item: The item to append
        :type item: Coord
        """
        self.coords.append(item)

    @property
    def distance(self) -> float:
        """
        The euclidean distance along the coords.
        """
        arr = self.to_numpy()
        return np.sum(np.linalg.norm(np.diff(arr, axis=0), ord=2, axis=1))
