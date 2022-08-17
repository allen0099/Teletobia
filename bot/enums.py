from enum import Enum


class PermissionLevel(Enum):
    ROOT: int = 1

    SUPER_ADMIN: int = 2

    USER: int = 3
