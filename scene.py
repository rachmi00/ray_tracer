from sphere import Sphere
from light import Light

class Scene:
    def __init__(self):
        self.spheres = []
        self.lights = []

    def add_sphere(self, sphere: Sphere):
        self.spheres.append(sphere)

    def add_light(self, light: Light):
        self.lights.append(light)