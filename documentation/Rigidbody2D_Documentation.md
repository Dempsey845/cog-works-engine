# Rigidbody2D Component Documentation

## Overview
The `Rigidbody2D` component is a 2D physics body used in the engine to simulate physical behaviour for game objects.  
It supports **box** and **circle** colliders, static or dynamic bodies, friction, elasticity, and optional velocity-controlled movement.

---

## Features
- Supports **box** and **circle** shapes.
- Can be **static** (immovable) or **dynamic** (affected by physics).
- Adjustable **mass**, **friction**, and **elasticity**.
- Optional **rotation freezing**.
- Optional **velocity-controlled** movement to manually set velocity with extra collision checks.
- Debug mode to visualise physics shapes and rays.

---

## Constructor Parameters

| Parameter            | Type    | Default | Description |
|---------------------|---------|---------|-------------|
| `shape_type`        | str     | `"box"` | `"box"` or `"circle"` collider shape |
| `width`             | float   | 0       | Width of the box (ignored for circle) |
| `height`            | float   | 0       | Height of the box (ignored for circle) |
| `radius`            | float   | 0       | Radius of the circle (ignored for box) |
| `mass`              | float   | 1.0     | Mass of the body (minimum 0.0001) |
| `static`            | bool    | False   | If True, body will not move |
| `debug`             | bool    | False   | Render debug visuals if True |
| `freeze_rotation`   | bool    | False   | Prevents rotation if True |
| `friction`          | float   | 0.7     | Friction coefficient of the shape |
| `elasticity`        | float   | 0.0     | Elasticity coefficient of the shape |
| `velocity_controlled` | bool  | False   | If True, velocity is manually controlled using `desired_velocity` and collision rays |

---

## `velocity_controlled` Explanation
When `velocity_controlled` is **enabled**, the Rigidbody ignores normal physics-driven horizontal movement.  
Instead:  
- You manually set `desired_velocity` each frame.  
- The Rigidbody applies that velocity while performing extra **ray casts** to detect collisions.  
- This prevents fast-moving objects from "tunnelling" through other colliders.  
- Vertical velocity (gravity) is preserved automatically.  

---

## Main Methods

### `start()`
Initialises the Rigidbody component, retrieves the `Transform`, and creates the physics body.

### `reset_to_start()`
Recreates the Rigidbody and body in its starting state.

### `_create_body()`
Internal method that sets up the Pymunk `Body` and `Shape` based on the collider type and Rigidbody parameters.

### `apply_force(fx, fy)`
Applies a force vector `(fx, fy)` at the Rigidbody's world position.

### `render(surface)`
Draws debug visuals including shape outline, center of mass, local axes, and collision rays (if `velocity_controlled`).

### `fixed_update(dt)`
Updates Rigidbody physics each fixed timestep:  
- Updates `velocity` if `velocity_controlled`.  
- Updates `Transform` position and rotation based on the physics body.

### `check_horizontal_collision(vx, dt)`  
Returns a horizontal velocity considering raycast collisions to prevent tunnelling.

### `check_vertical_collision(vy, dt)`  
Returns vertical velocity considering raycast collisions with ceiling.

### `check_grounded()`  
Checks if the Rigidbody is standing on the ground using a raycast.

### `_check_ceiling(ray_length)`  
Internal helper to check collisions with the ceiling.

### `_get_ray_start(direction)`  
Calculates the starting point for horizontal collision rays.

### `_limit_velocity(body, gravity, damping, dt)`  
Internal velocity clamp function to prevent exceeding `max_speed`.

---

## Debug Visuals
When `debug=True`, the following are drawn:  
- Collider shape outline (box or circle).  
- Center of mass (green dot).  
- Local X (blue) and Y (yellow) axes.  
- Collision rays (cyan) when `velocity_controlled`.

---

## Notes
- Rigidbody automatically links with the `Transform` of the GameObject.  
- Raycast collision checks help prevent tunnelling at high speeds.  
- `freeze_rotation=True` sets the physics moment of inertia to infinity.  

