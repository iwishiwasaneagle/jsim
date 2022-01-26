from abc import ABC
from typing import List, Optional, Tuple

import matplotlib as mpl
import matplotlib.patches as patches
import numpy as np

from jsim.Environment.Environment import Environment
from jsim.Environment.HexEnvironment.HexCoords import (
    AxialCoord,
    OffsetCoord,
    PixelCoord,
)
from jsim.Environment.HexEnvironment.HexDirections import HexDirections
from jsim.Simulation import Simulation


class HexEnvironment(Environment, ABC):
    """
    A :class:`Environment` variation using hexagons. The implementation uses the
    `odd-q offset coordinate system
    <https://www.redblobgames.com/grids/hexagons/#coordinates-offset>`_.
    """

    def __init__(self, m: int = 20, psim: Simulation = None) -> None:
        """
        Refer to :class:`Environment` for how to use. Always call
        `super().__init(psim=psim)`

        :param m: Height and width factor of the PDM
        :type m: int
        :param psim: Pointer to the simulation
        :type psim: Simulation
        """
        super().__init__(psim=psim)

        self._shape = (m, m)

        self.pdm = np.zeros(self._shape)  # Todo: populate

    # --- Plotting helpers --- #

    def as_mpl_polygons(
        self,
        cmap: mpl.colors.LinearSegmentedColormap = mpl.cm.get_cmap("Spectral"),
        size: float = np.sqrt(1 / 3),
    ) -> List[patches.RegularPolygon]:
        """
        Helper function to convert the :class:`HexEnvironment`
        into matplotlib patches that can plotted.

        Example:
            .. code-block:: python

               import matplotlib as mpl
               import matplotlib.pyplot as plt
               from jsim.Environment import HexEnvironment

               hex = HexEnvironment()
               fig, ax = plt.subplots(1)
               ax.set_aspect("equal")
               for p in hex.as_mpl_polygons(mpl.cm.get_cmap("gray")):
                   ax.add_patch(p)
               plt.autoscale(enable=True)
               plt.show()

        :param cmap: Color map to be used (default = 'Spectral')
        :type cmap: matplotlib.colors.LinearSegmentedColormap
        :param size: The size of the hexagons (default = (1/3)^0.5)
        :type size: float
        :return: The array of matplotlib patches that represent the environment
         in cartesian coordinates
        :rtype: List[matplotlib.patches.RegularPolygon]
        """
        norm = mpl.colors.Normalize(vmin=np.min(self.pdm), vmax=np.max(self.pdm))

        offsets = []
        colors = []
        i, j = np.meshgrid(np.arange(self.shape[0]), np.arange(self.shape[1]))
        for col, row in zip(i.flatten(), j.flatten()):
            z = self.pdm[row, col]
            colors.append(cmap(norm(z)))
            offsets.append(OffsetCoord(col=col, row=row))
        return HexEnvironment.offsets_to_mpl_polygons(offsets, colors, size)

    @staticmethod
    def offsets_to_mpl_polygons(
        offsets: List[OffsetCoord],
        colors: List[Optional[Tuple[float, float, float, float]]] = None,
        size: float = np.sqrt(1 / 3),
    ) -> List[patches.RegularPolygon]:
        """
        Convert a list of offsets into a matplotlib polygons in cartesian space.

        :param offsets: The list of offset coordinates to be converted
        :type offsets: List[OffsetCoord]
        :param colors: A list of colors to be used for each polygon
        :type colors: List[Tuple[float, float, float, float]]
        :param size: The size of the hexagons (defaults = (1/3)^0.5)
        :type size: float
        :return: The list of matplotlib polygons
        :rtype: List[matplotlib.patches.RegularPolygon]
        """
        arr = []
        if colors is None:
            colors = [None for _ in offsets]

        for o, c in zip(offsets, colors):
            arr.append(HexEnvironment.offset_to_mpl_polygon(o, c, size))
        return arr

    @staticmethod
    def offset_to_mpl_polygon(
        offset: OffsetCoord,
        color: Tuple[float, float, float, float] = None,
        size: float = np.sqrt(1 / 3),
    ) -> patches.RegularPolygon:
        """
        Convert an offset into a matplotlib polygon in cartesian space.

        :param offset: The offset coordinate to be converted
        :type offset: OffsetCoord
        :param color: The color to be used for the
        :type color: List[Tuple[float, float, float, float]]
        :param size: The size of the hexagon (defaults = (1/3)^0.5)
        :type size: float
        :return: The resultant matplotlib polygon
        :rtype: matplotlib.patches.RegularPolygon
        """
        pixel = HexEnvironment.offset_to_pixel(offset, size)
        return patches.RegularPolygon(
            (pixel.x, pixel.y),
            numVertices=6,
            radius=size,
            orientation=np.pi / 6,
            fc=color,
            ec="k",
        )

    # --- Getters/Setters --- #

    @property
    def shape(self) -> Tuple[float, float]:
        """
        Get the shape of the pdm. Defaults to (m,m).

        :return: The shape of the pdm
        :rtype: Tuple[float,float]
        """
        return self._shape

    # --- Conversions --- #

    @staticmethod
    def offset_to_axial(offset: OffsetCoord) -> AxialCoord:
        """
        Convert a singular offset coordinate to an axial coordinate

        :param offset: The coordinate to be converted
        :type offset: OffsetCoord
        :return: The resultant axial coordinate
        :rtype: AxialCoord
        """
        q = offset.col
        r = (
            offset.row - (offset.col - (offset.col & 1)) / 2
        )  # use bitewise and to detect even, as it also works with negative numbers
        return AxialCoord(q=q, r=r)

    @staticmethod
    def axial_to_offset(axial: AxialCoord) -> OffsetCoord:
        """
        Convert a singular axial coordinate to an offset coordinate

        :param axial: The coordinate to be converted
        :type axial: AxialCord
        :return: The resultant offset coordinate
        :rtype: OffsetCoord
        """
        col = axial.q
        row = axial.r + (axial.q - (axial.q & 1)) / 2
        return OffsetCoord(col=col, row=row)

    @staticmethod
    def axial_to_pixel(axial: AxialCoord, size: float = np.sqrt(1 / 3)) -> PixelCoord:
        """
        Convert a singular axial coordinate to a pixel (cartesian) coordinate

        :param axial: The coordinate to be converted
        :type axial: AxialCord
        :param size: The size of the hexagon (default = (1/3)^0.5)
        :type size: float
        :return: The resultant pixel coordinate
        :rtype: PixelCoord
        """
        x = size * (3 / 2) * axial.q
        y = size * ((np.sqrt(3) / 2) * axial.q + np.sqrt(3) * axial.r)
        return PixelCoord(x=x, y=y)

    @staticmethod
    def offset_to_pixel(
        offset: OffsetCoord, size: float = np.sqrt(1 / 3)
    ) -> PixelCoord:
        """
        Convert a singular offset coordinate to a pixel (cartesian) coordinate

        :param offset: The coordinate to be converted
        :type offset: OffsetCoord
        :param size: The size of the hexagon (default = (1/3)^0.5)
        :type size: float
        :return: The resultant pixel coordinate
        :rtype: PixelCoord
        """
        # https://www.redblobgames.com/grids/hexagons/#hex-to-pixel-offset
        axial = HexEnvironment.offset_to_axial(offset)
        pixel = HexEnvironment.axial_to_pixel(axial, size)
        return pixel

    # --- Neighbor --- #

    @staticmethod
    def neighbor_coord(offset: OffsetCoord, direction: HexDirections) -> OffsetCoord:
        """
        Get the offset coordinate of the 6 neighbors from the corresponding direction.

        :param offset: The offset coordinate to use
        :type offset: OffsetCoord
        :param direction: The direction of the neighbor
        :type direction: HexDirections
        :return: The neighbor's offset coordinate
        :rtype: OffsetCoord
        """
        direction_differences = [
            # for explanation:
            # https://www.redblobgames.com/grids/hexagons/#neighbors-offset
            # even cols
            [[+1, 0], [+1, -1], [0, -1], [-1, -1], [-1, 0], [0, +1]],
            # odd cols
            [[+1, +1], [+1, 0], [0, -1], [-1, 0], [-1, +1], [0, +1]],
        ]
        parity = offset.col & 1
        diff = direction_differences[parity][direction]
        return OffsetCoord(col=offset.col + diff[0], row=offset.row + diff[1])

    @staticmethod
    def neighbors_coord(offset: OffsetCoord) -> List[OffsetCoord]:
        """
        Get the 6 neighbors of an offset coordinate.

        :param offset: The offset coordinate to use
        :type offset: OffsetCoord
        :return: A list of the 6 neighbors' offset coordinates
        :rtype: List[OffsetCoord]
        """
        return [HexEnvironment.neighbor_coord(offset, d) for d in HexDirections]

    # --- Distance --- #
    @staticmethod
    def axial_distance_between_a_b(a: AxialCoord, b: AxialCoord) -> float:
        """
        Find the linear distance between two axial coordinates

        :param a: The first coordinate
        :type a: AxialCoord
        :param b: The second coordinate
        :type b: AxialCoord
        :return: The linear distance between a and b
        :rtype: float
        """
        return (abs(a.q - b.q) + abs(a.q + a.r - b.q - b.r) + abs(a.r - b.r)) / 2

    @staticmethod
    def distance_between_a_b(a: OffsetCoord, b: OffsetCoord) -> float:
        """
        Find the linear distance between two offset coordinates

        :param a: The first coordinate
        :type a: OffsetCoord
        :param b: The second coordinate
        :type b: OffsetCoord
        :return: The linear distance between a and b
        :rtype: float
        """

        ac = HexEnvironment.offset_to_axial(a)
        bd = HexEnvironment.offset_to_axial(b)
        return HexEnvironment.axial_distance_between_a_b(ac, bd)
