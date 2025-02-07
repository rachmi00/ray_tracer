from vector import Vector3
from scene import Scene
from sphere import Sphere
from light import Light
from typing import Tuple

import math

class Renderer:
    def __init__(self, scene: Scene, canvas_width: int, canvas_height: int, viewport_width: float, viewport_height: float, viewport_distance: float, camera_position: Vector3, background_color: tuple):
        self.scene = scene
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.viewport_distance = viewport_distance
        self.camera_position = camera_position
        self.background_color = background_color

    def canvas_to_viewport(self, x: int, y: int) -> Vector3:
        return Vector3(x * self.viewport_width / self.canvas_width, y * self.viewport_height / self.canvas_height, self.viewport_distance)

    def intersect_ray_sphere(self, O: Vector3, D: Vector3, sphere: Sphere) -> Tuple[float, float]:
        CO = O - sphere.center
        a = D.dot(D)
        b = 2 * CO.dot(D)
        c = CO.dot(CO) - sphere.radius * sphere.radius
        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            return float('inf'), float('inf')

        t1 = (-b + math.sqrt(discriminant)) / (2 * a)
        t2 = (-b - math.sqrt(discriminant)) / (2 * a)

        return t1, t2

    def trace_ray(self, O: Vector3, D: Vector3, t_min: float, t_max: float, recursion_depth: int = 3) -> Tuple[int, int, int]:
        closest_t = float('inf')
        closest_sphere = None

        for sphere in self.scene.spheres:
            t1, t2 = self.intersect_ray_sphere(O, D, sphere)
            if t1 >= t_min and t1 <= t_max and t1 < closest_t:
                closest_t = t1
                closest_sphere = sphere
            if t2 >= t_min and t2 <= t_max and t2 < closest_t:
                closest_t = t2
                closest_sphere = sphere

        if closest_sphere is None:
            return self.background_color

        # Compute intersection point and normal
        P = O + D * closest_t
        N = (P - closest_sphere.center).normalize()

        # Compute lighting
        local_color = closest_sphere.color
        intensity = self.compute_lighting(P, N, -D, closest_sphere.specular)

        # Compute reflected color
        if recursion_depth <= 0 or closest_sphere.reflective <= 0:
            return (int(local_color[0] * intensity), int(local_color[1] * intensity), int(local_color[2] * intensity))

        R = self.reflect_ray(-D, N)
        reflected_color = self.trace_ray(P, R, 0.001, float('inf'), recursion_depth - 1)

        # Blend local and reflected color
        return (
            int(local_color[0] * (1 - closest_sphere.reflective) * intensity + reflected_color[0] * closest_sphere.reflective),
            int(local_color[1] * (1 - closest_sphere.reflective) * intensity + reflected_color[1] * closest_sphere.reflective),
            int(local_color[2] * (1 - closest_sphere.reflective) * intensity + reflected_color[2] * closest_sphere.reflective)
        )

    def reflect_ray(self, R: Vector3, N: Vector3) -> Vector3:
        return N * 2 * N.dot(R) - R

    def compute_lighting(self, P: Vector3, N: Vector3, V: Vector3, s: float) -> float:
        intensity = 0.0

        for light in self.scene.lights:
            if light.type == "ambient":
                intensity += light.intensity
            else:
                if light.type == "point":
                    L = (light.position - P).normalize()
                    t_max = 1
                else:
                    L = light.direction.normalize()
                    t_max = float('inf')

                # Shadow check
                shadow_sphere, shadow_t = self.closest_intersection(P, L, 0.001, t_max)
                if shadow_sphere is not None:
                    continue

                # Diffuse reflection
                n_dot_l = N.dot(L)
                if n_dot_l > 0:
                    intensity += light.intensity * n_dot_l / (N.length() * L.length())

                # Specular reflection
                if s != -1:
                    R = self.reflect_ray(L, N)
                    r_dot_v = R.dot(V)
                    if r_dot_v > 0:
                        intensity += light.intensity * (r_dot_v / (R.length() * V.length())) ** s

        return intensity

    def closest_intersection(self, O: Vector3, D: Vector3, t_min: float, t_max: float) -> Tuple[Sphere, float]:
        closest_t = float('inf')
        closest_sphere = None

        for sphere in self.scene.spheres:
            t1, t2 = self.intersect_ray_sphere(O, D, sphere)
            if t1 >= t_min and t1 <= t_max and t1 < closest_t:
                closest_t = t1
                closest_sphere = sphere
            if t2 >= t_min and t2 <= t_max and t2 < closest_t:
                closest_t = t2
                closest_sphere = sphere

        return closest_sphere, closest_t

    def render_scene(self):
        from PIL import Image
        image = Image.new("RGB", (self.canvas_width, self.canvas_height), self.background_color)
        pixels = image.load()

        for x in range(-self.canvas_width // 2, self.canvas_width // 2):
            for y in range(-self.canvas_height // 2, self.canvas_height // 2):
                D = self.canvas_to_viewport(x, y)
                color = self.trace_ray(self.camera_position, D, 1, float('inf'))
                pixels[x + self.canvas_width // 2, y + self.canvas_height // 2] = color

        image.show()