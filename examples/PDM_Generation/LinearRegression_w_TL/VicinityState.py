import numpy as np
import pydantic

from jsim.Meta import State

Nine_X_ONE_FLOAT_FIELD = pydantic.conlist(float, max_items=9, min_items=9)

VICINITY_INDICES = np.vstack(
    [f.flatten() for f in np.meshgrid(np.arange(-1, 2), np.arange(-1, 2)[::-1])]
)

VICINITY_DISTS = np.sqrt(np.sum(np.square(VICINITY_INDICES), axis=0))


class VicinityState(State, pydantic.BaseModel):
    dem: Nine_X_ONE_FLOAT_FIELD
    slope: Nine_X_ONE_FLOAT_FIELD
    lcid: Nine_X_ONE_FLOAT_FIELD
    alt_diff: Nine_X_ONE_FLOAT_FIELD
