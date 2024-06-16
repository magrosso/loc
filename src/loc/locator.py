from enum import Enum
from functools import partial, partialmethod
from typing import Self


class LocKey(Enum):
    ID = "id"
    CLASS = "class"
    TYPE = "type"
    NAME = "name"

    def __str__(self) -> str:
        return self.value


class ControlType(Enum):
    BUTTON = "Button"
    EDIT = "Edit"
    COMBO_BOX = "Combobox"

    def __str__(self) -> str:
        return self.value


class Loc:
    class Op(Enum):
        AND = "and"
        PARENT = ">"

    def __init__(self, key: LocKey = LocKey.ID, val: str | ControlType = "") -> None:
        # empty values or values with space characters must be quoted!
        if isinstance(val, ControlType):
            val = val.value
        else:
            val = f'"{val}"' if " " in val or not val else val
        self.loc: str = f"{key}:{val}"

    @classmethod
    def button(cls) -> Self:
        return cls(LocKey.TYPE, ControlType.BUTTON)

    @classmethod
    def edit(cls) -> Self:
        return cls(LocKey.TYPE, ControlType.EDIT)

    @classmethod
    def combobox(cls) -> Self:
        return cls(LocKey.TYPE, ControlType.COMBO_BOX)

    def __add__(self, rhs: Self) -> Self:
        self.loc = f"{self.loc} {Loc.Op.AND.value} {rhs}"
        return self

    def __gt__(self, rhs: Self) -> Self:
        self.loc = f"{self.loc} {Loc.Op.PARENT.value} {rhs}"
        return self

    def __str__(self) -> str:
        return self.loc

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.key}, {self.val})"


# create Locator objects with TYPE KEY
LocType = partial(Loc, key=LocKey.TYPE)


class Locator(Enum):
    LOC_1 = Loc(LocKey.ID, " 1 ") + Loc(LocKey.NAME, "")
    LOC_2 = Loc(LocKey.ID, "ID 4")
    LOC_3 = (
        Loc(LocKey.ID, "ID 1")
        + Loc(LocKey.CLASS, "CLASS 2")
        + Loc(LocKey.NAME, "NAME 3")
    )
    LOC_4 = LocType(val=ControlType.BUTTON) + Loc(LocKey.CLASS, "CLASS 332") + Loc(
        LocKey.NAME, "NAME-4"
    ) > Loc(LocKey.ID, "_id_")
    LOC_5 = LocType(val=ControlType.COMBO_BOX)
    LOC_6 = LocType(val=ControlType.BUTTON) + Loc(LocKey.ID, "U")
    LOC_7 = LocType(val=ControlType.EDIT) > Loc(LocKey.NAME) + Loc.button() + Loc(
        LocKey.ID, "I"
    )
    LOC_8 = LocType(val=ControlType.EDIT) + LocType(
        val=ControlType.COMBO_BOX
    ) + LocType(val=ControlType.BUTTON) > LocType(val=ControlType.EDIT)

    def __str__(self) -> str:
        return str(self.value)


def main() -> None:
    for num, loc in enumerate(Locator, 1):
        print(f"loc {num} = '{loc}'")


if __name__ == "__main__":
    main()
