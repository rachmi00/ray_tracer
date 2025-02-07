from vector import Vector3

class Sphere:
    def __init__(self, center: Vector3, radius: float, color: tuple, specular: float = -1, reflective: float = 0.0):
        self.center = center
        self.radius = radius
        self.color = color
        self.specular = specular
        self.reflective = reflective