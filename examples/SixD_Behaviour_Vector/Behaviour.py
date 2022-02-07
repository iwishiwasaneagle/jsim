from enum import IntEnum
from typing import Tuple

import numpy as np
import pydantic


class BehaviourEnum(IntEnum):
    rw = 0
    lf = 1
    st = 2
    sp = 3
    bt = 4
    ve = 5


class Behaviour(pydantic.BaseModel):
    p: pydantic.conlist(float, min_items=9, max_items=9)

    @pydantic.validator("p")
    def p_to_list(cls, v):
        return list(v)

    def __len__(self):
        return 9

    def __getitem__(self, item):
        return self.p[item]


class SixDBehaviours(pydantic.BaseModel):
    rw: Behaviour
    lf: Behaviour
    sp: Behaviour

    def __getitem__(self, item):
        if item == BehaviourEnum.rw:
            return self.rw
        elif item == BehaviourEnum.lf:
            return self.lf
        elif item == BehaviourEnum.st:
            raise Exception("Straight Travel is not vector based")
        elif item == BehaviourEnum.sp:
            return self.sp
        elif item == BehaviourEnum.bt:
            raise Exception("Back tracking is not vector base")
        elif item == BehaviourEnum.ve:
            raise Exception("View Enhancing is not vector based.")
        else:
            raise IndexError(f"{item=} not found in {self}")

    def __len__(self):
        return 6


class BehaviourVector(pydantic.BaseModel):
    rw: float
    lf: float
    st: float
    sp: float
    bt: float
    ve: float

    def __len__(self):
        return 6

    def __getitem__(self, item):
        if item == BehaviourEnum.rw:
            return self.rw
        elif item == BehaviourEnum.lf:
            return self.lf
        elif item == BehaviourEnum.st:
            return self.st
        elif item == BehaviourEnum.sp:
            return self.sp
        elif item == BehaviourEnum.bt:
            return self.bt
        elif item == BehaviourEnum.ve:
            return self.ve
        else:
            raise IndexError(f"{item=} not found in {self}")

    @pydantic.validator("rw", "lf", "st", "sp", "bt", "ve", each_item=False)
    @classmethod
    def sum_to_one(cls, v, values, field, config):
        if len(values) == 5:
            s = sum(values.values()) + v
            if np.isclose(s, 1):
                return v
            else:
                raise TypeError(
                    f"Values do not sum to 1 ({s},{[v] + [f for f in values.values()]})"
                )
        else:
            return v

    @classmethod
    @pydantic.validate_arguments
    def fromlist(cls, list_: Tuple[float, float, float, float, float, float]):
        return cls(
            rw=list_[0], lf=list_[1], st=list_[2], sp=list_[3], bt=list_[4], ve=list_[5]
        )

    def tolist(self):
        return [self[i] for i in range(len(self))]


if __name__ == "__main__":
    print(BehaviourVector.fromlist([0.0, 0.0, 0.0, 1.0, 0.0, 0.0]))
    print(BehaviourVector(rw=0.1, lf=0.1, st=0.1, sp=0.7, bt=0.0, ve=0.0).tolist())
