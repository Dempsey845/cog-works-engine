import math

import pygame

from component import Component
from components.transform import Transform
from components.sprite import Sprite

def rotate_point(px, py, cx, cy, angle_rad):
    s, c = math.sin(angle_rad), math.cos(angle_rad)
    px -= cx
    py -= cy
    xnew = px * c - py * s
    ynew = px * s + py * c
    return xnew + cx, ynew + cy

def dot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

def project_polygon(axis, poly):
    dots = [dot(axis, point) for point in poly]
    return min(dots), max(dots)

def polygons_intersect(poly1, poly2):
    for polygon in (poly1, poly2):
        for i1 in range(len(polygon)):
            i2 = (i1 + 1) % len(polygon)
            p1 = polygon[i1]
            p2 = polygon[i2]
            edge = (p2[0] - p1[0], p2[1] - p1[1])
            axis = (-edge[1], edge[0])
            min1, max1 = project_polygon(axis, poly1)
            min2, max2 = project_polygon(axis, poly2)
            if max1 < min2 or max2 < min1:
                return False
    return True

def draw_line(surface,x1, y1, x2, y2, colour):
    pygame.draw.line(surface, colour, (x1, y1), (x2, y2), 2)

class Collider2D(Component):
    def __init__(self, width=0, height=0, offset_x=0, offset_y=0, debug=False):
        super().__init__()
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.debug = debug
        self.transform = None
        self.local_corners = []
        self.points = []

    def start(self):
        self.transform = self.game_object.get_component(Transform)
        if not self.transform:
            self.transform = Transform()
            self.game_object.add_component(self.transform)

        sprite = self.game_object.get_component(Sprite)
        if sprite:
            width, height = sprite.image.get_size()
            self.width = width
            self.height = height

        # Local corners relative to bottom-centre
        self.local_corners = [
            (-self.width / 2, -self.height),  # top-left
            (self.width / 2, -self.height),  # top-right
            (self.width / 2, 0),  # bottom-right
            (-self.width / 2, 0)  # bottom-left
        ]
        self.update(0)

    def update(self, dt):
        theta = math.radians(self.transform.rotation)

        # Pivot at bottom-centre of the object
        cx = self.transform.x + self.offset_x
        cy = self.transform.y + self.offset_y

        # Apply transform scale to local corners
        scaled_corners = [(x * self.transform.scale_x, y * self.transform.scale_y) for x, y in self.local_corners]

        # Rotate and translate scaled corners around the pivot
        self.points = [rotate_point(cx + x, cy + y, cx, cy, theta) for x, y in scaled_corners]

    def render(self, surface):
        if not self.debug or not self.points:
            return

        camera = self.game_object.scene.camera_component
        colour = (255, 0, 0)  # Red

        for i in range(len(self.points)):
            x1, y1 = self.points[i]
            x2, y2 = self.points[(i + 1) % len(self.points)]

            # Convert world → screen using camera offset
            x1 -= camera.offset_x
            y1 -= camera.offset_y
            x2 -= camera.offset_x
            y2 -= camera.offset_y

            draw_line(surface, x1, y1, x2, y2, colour)

    def intersects(self, other: "Collider2D") -> bool:
        if not self.points or not other.points:
            return False
        return polygons_intersect(self.points, other.points)
