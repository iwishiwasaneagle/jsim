import numpy as np
from Coord import Coord
from loguru import logger
from VicinityState import VICINITY_INDICES, VicinityState

from jsim.Environment import Environment
from jsim.Util import RasterMap, VectorMap


def _CONVERT_UKCEH_TO_LCID(vmap: VectorMap):
    logger.debug(f"Converting UKCEH IDs to LCIDs for {vmap=}")
    labels_conversion = {
        1: 23,
        2: 24,
        3: 22,
        4: 29,
        5: 26,
        6: 26,
        7: 26,
        8: 27,
        9: 28,
        10: 27,
        11: 27,
        12: 27,
        13: 1000,  # Saltwater
        14: 1000,  # Freshwater
        15: 27,
        16: 27,
        17: 27,
        18: 27,
        19: 27,
        20: 29,
        21: 29,
    }
    k = np.array(list(labels_conversion.keys()))
    v = np.array(list(labels_conversion.values()))
    mapping_ar = np.zeros(k.max() + 1, dtype=v.dtype)
    mapping_ar[k] = v
    vmap.gdf["lcid"] = mapping_ar[vmap.gdf["_mode"].astype(np.uint8)]

    logger.debug(f"Converted UKCEH IDs to LCIDs for {vmap=}")
    return vmap


class LR_Env(Environment):
    dem: RasterMap
    slope: RasterMap
    lcid: VectorMap
    lcid_arr: np.ndarray

    start_alt: float

    scale: float

    def __init__(self, start: Coord, scale: float, dem: str, slope: str, lcid: str):
        logger.debug(f"Instantiating LR_Env with {start=} and {scale=}")
        self.dem = RasterMap(dem)
        logger.debug(f"{self.dem=} initiated")
        self.slope = RasterMap(slope)
        logger.debug(f"{self.slope=} initiated")
        self.lcid = _CONVERT_UKCEH_TO_LCID(VectorMap(lcid))
        logger.debug(f"{self.lcid=} initiated")

        self.scale = scale

        self.reset(
            start,
        )

    def reset(self, start: Coord) -> VicinityState:
        logger.debug(f"Resetting with {start=}")
        self.start_alt = next(self.dem[start.x, start.y])

        return self._get_vicinity(start)

    def _get_vicinity(self, pos: Coord) -> VicinityState:
        x, y = VICINITY_INDICES[0, :] + pos.x, VICINITY_INDICES[1, :] + pos.y

        vic_dem = list(self.dem[y, x])
        vic_slope = np.arctan(np.deg2rad(list(self.slope[y, x]))).tolist()
        vic_alt = (np.array(vic_dem) - self.start_alt).tolist()

        xt, yt = self.dem.xy(y, x)
        vic_lcid = self.lcid[xt, yt]["lcid"].to_list()
        try:
            return VicinityState(
                dem=vic_dem,
                alt_diff=vic_alt,
                slope=vic_slope,
                lcid=vic_lcid,
            )
        except Exception as e:
            logger.debug(f"{vic_dem=}, {vic_slope=}, {vic_alt=}, {vic_lcid=}, {pos=}")
            raise e

    def step(self, pa: Coord) -> VicinityState:
        return self._get_vicinity(pa)
