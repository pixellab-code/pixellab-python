from typing import Literal

CameraView = Literal["side", "low top-down", "high top-down"]
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
