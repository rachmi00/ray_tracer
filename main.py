from scene import Scene
from sphere import Sphere
from light import Light
from vector import Vector3
from renderer import Renderer

# Initialize the scene
scene = Scene()
scene.add_sphere(Sphere(Vector3(0, -1, 3), 1, (255, 0, 0), 500, 0.2))
scene.add_sphere(Sphere(Vector3(2, 0, 4), 1, (0, 0, 255), 500, 0.3))
scene.add_sphere(Sphere(Vector3(-2, 0, 4), 1, (0, 255, 0), 10, 0.4))
scene.add_sphere(Sphere(Vector3(0, -5001, 0), 5000, (255, 255, 0), 1000, 0.5))

scene.add_light(Light("ambient", 0.2))
scene.add_light(Light("point", 0.6, Vector3(2, 1, 0)))
scene.add_light(Light("directional", 0.2, direction=Vector3(1, 4, 4)))

# Canvas dimensions
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

# Viewport dimensions
VIEWPORT_WIDTH = 1
VIEWPORT_HEIGHT = 1
VIEWPORT_DISTANCE = 1

# Camera position
CAMERA_POSITION = Vector3(0, 0, 0)

# Background color
BACKGROUND_COLOR = (255, 255, 255)

# Create the renderer and render the scene
renderer = Renderer(scene, CANVAS_WIDTH, CANVAS_HEIGHT, VIEWPORT_WIDTH, VIEWPORT_HEIGHT, VIEWPORT_DISTANCE, CAMERA_POSITION, BACKGROUND_COLOR)
renderer.render_scene()