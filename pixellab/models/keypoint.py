from typing import Literal, TypedDict

SkeletonLabel = Literal[
    "NOSE",
    "NECK",
    "RIGHT SHOULDER",
    "RIGHT ELBOW",
    "RIGHT ARM",
    "LEFT SHOULDER",
    "LEFT ELBOW",
    "LEFT ARM",
    "RIGHT HIP",
    "RIGHT KNEE",
    "RIGHT LEG",
    "LEFT HIP",
    "LEFT KNEE",
    "LEFT LEG",
    "RIGHT EYE",
    "LEFT EYE",
    "RIGHT EAR",
    "LEFT EAR",
]


class Keypoint(TypedDict):
    x: float
    y: float
    label: SkeletonLabel
    z_index: float = 0.0
