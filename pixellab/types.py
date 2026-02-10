from typing import Literal, Union

CameraView = Literal["side", "low top-down", "high top-down"]
CameraViewWithNone = Union[CameraView, Literal["none"]]
Direction = Literal[
    "south",
    "south-east",
    "east",
    "north-east",
    "north",
    "north-west",
    "west",
    "south-west",
]
DirectionWithNone = Union[Direction, Literal["none"]]
Outline = Literal[
    "single color black outline",
    "single color outline",
    "selective outline",
    "lineless",
]
Shading = Literal[
    "flat shading",
    "basic shading",
    "medium shading",
    "detailed shading",
    "highly detailed shading",
]

Detail = Literal["low detail", "medium detail", "highly detailed"]
