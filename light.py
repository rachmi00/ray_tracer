from vector import Vector3

class Light:
    def __init__(self, type: str, intensity: float, position: Vector3 = None, direction: Vector3 = None):
        self.type = type
        self.intensity = intensity
        self.position = position
        self.direction = direction