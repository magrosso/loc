from enum import Enum
from typing import Self


# type 	ControlType
# control 	ControlType
# id 	AutomationId
# regex 	RegexName
# subname 	SubName
# index 	foundIndex (int)
# offset 	offset coordinates (x (int), y (int)) from control center
# executable 	target window by its executable name
# handle 	target window handle (int)
# desktop 	SPECIAL target desktop, no value for the key e.g. desktop:desktop and name:Calculator
# process 	NOT YET SUPPORTED target window by its executable's process id
# depth 	searchDepth (int) for finding Control (default 8)
# path 	target element by its index-based path traversal (e.g. path:2|3|8|2)


class LocKey(Enum):
    ID = "id"
    CLASS = "class"
    TYPE = "type"
    NAME = "name"
    OFFSET = "offset"

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

    def __init__(self, key: LocKey, val: str | ControlType) -> None:
        # empty values or values with space characters must be quoted!
        if isinstance(val, ControlType):
            val = val.value
        else:
            val = f'"{val}"' if " " in val or not val else val
        self.loc: str = f"{key}:{val}"

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

    # predefind locator objects
    @classmethod
    def type(cls, val: str) -> Self:
        return cls(LocKey.TYPE, val)

    @classmethod
    def button(cls) -> Self:
        return cls(LocKey.TYPE, ControlType.BUTTON)

    @classmethod
    def edit(cls) -> Self:
        return cls(LocKey.TYPE, ControlType.EDIT)

    @classmethod
    def combobox(cls) -> Self:
        return cls(LocKey.TYPE, ControlType.COMBO_BOX)

    @classmethod
    def id(cls, val: str) -> Self:
        return cls(LocKey.ID, val)

    @classmethod
    def cls(cls, val: str) -> Self:
        return cls(LocKey.CLASS, val)

    @classmethod
    def name(cls, val: str) -> Self:
        return cls(LocKey.NAME, val)

    @classmethod
    def offset(cls, val: str) -> Self:
        return cls(LocKey.OFFSET, val)


class Locator(Enum):
    LOC_1 = Loc.id(" 1 ") + Loc.name("")
    LOC_2 = Loc.id("ID 4")
    LOC_3 = Loc.id("ID 1") + Loc.cls("CLASS 2") + Loc.name("NAME 3")
    LOC_4 = Loc.button() + Loc.cls("CLASS 332") + Loc.name("NAME-4") > Loc.id("_id_")
    LOC_5 = Loc.combobox()
    LOC_6 = Loc.button() + Loc.id("U")
    LOC_7 = Loc.edit() > Loc.name("") + Loc.button() + Loc.id("I ")
    LOC_8 = Loc.edit() + Loc.combobox() + Loc.button() > Loc.edit()
    LOC_9 = Loc.offset("3.55")

    def __str__(self) -> str:
        return str(self.value)


def main() -> None:
    for num, loc in enumerate(Locator, 1):
        if isinstance(loc, Locator):
            print(f"{num}: '{loc}'")


if __name__ == "__main__":
    main()
