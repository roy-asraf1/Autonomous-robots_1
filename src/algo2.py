import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Load the map image
map_image = pygame.image.load('p11.png')

# Get dimensions of the map
map_width, map_height = map_image.get_size()

# Set up the display
window_size = (map_width + 400, map_height)  # Add extra width for the buttons and input fields
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("2D Drone Simulator")

# Set the color for the drone
drone_color = (255, 255, 0)  # Yellow color for the drone
drone_radius = 4  # Radius of the drone
drone_diameter = drone_radius * 2
speed = 2  # Speed of the drone

# List to store the positions the drone has been (yellow markers)
drone_positions = []

# List to store the past positions (blue markers)
past_positions = []

# List to store the saved points (grey circles)
saved_points = []

# Color and radius for the past positions
past_position_color = (0, 0, 255)  # Blue color for the past positions
past_position_radius = 1  # Radius for the past positions
grey_circle_color = (128, 128, 128)  # Grey color for saved points
grey_circle_radius = drone_radius

# Sensor button dimensions
button_width = 150
button_height = 30
button_margin = 10

# Sensor button positions
sensor_buttons = {
    "up": pygame.Rect(map_width + 25, 20, button_width, button_height),
    "down": pygame.Rect(map_width + 25, 60, button_width, button_height),
    "left": pygame.Rect(map_width + 25, 100, button_width, button_height),
    "right": pygame.Rect(map_width + 25, 140, button_width, button_height),
    "forward": pygame.Rect(map_width + 25, 180, button_width, button_height),
    "backward": pygame.Rect(map_width + 25, 220, button_width, button_height)
}

# Input fields for position and orientation
input_field_rects = {
    "x": pygame.Rect(map_width + 200, 20, 100, 30),
    "y": pygame.Rect(map_width + 200, 60, 100, 30),
    "orientation": pygame.Rect(map_width + 200, 100, 100, 30)
}

# Variables to store input values
input_values = {
    "x": "",
    "y": "",
    "orientation": ""
}

# Function to check if a pixel is white
def is_white(pixel):
    return pixel[:3] == (255, 255, 255)

# Function to find the starting position
def find_starting_position(image, radius):
    for y in range(50, image.get_height() - radius):
        for x in range(50, image.get_width() - radius):
            # Check an area of size diameter x diameter
            area_is_white = True
            for dy in range(-radius, radius):
                for dx in range(-radius, radius):
                    if (0 <= x + dx < image.get_width()) and (0 <= y + dy < image.get_height()):
                        if not is_white(image.get_at((x + dx, y + dy))):
                            area_is_white = False
                            break
                    else:
                        area_is_white = False
                        break
                if not area_is_white:
                    break
            if area_is_white:
                return [x, y]
    return None

# Function to measure distance to obstacle in a given direction
def measure_distance(position, direction, radius, image):
    x, y = position
    distance = 0
    if direction == 'up':
        while y - distance > 0 and is_white(image.get_at((x, y - distance))):
            distance += 1
    elif direction == 'down':
        while y + distance < image.get_height() and is_white(image.get_at((x, y + distance))):
            distance += 1
    elif direction == 'left':
        while x - distance > 0 and is_white(image.get_at((x - distance, y))):
            distance += 1
    elif direction == 'right':
        while x + distance < image.get_width() and is_white(image.get_at((x + distance, y))):
            distance += 1
    elif direction == 'forward':
        while y - distance > 0 and is_white(image.get_at((x, y - distance))):
            distance += 1
    elif direction == 'backward':
        while y + distance < image.get_height() and is_white(image.get_at((x, y + distance))):
            distance += 1
    return distance

# Find the starting position for the drone
drone_position = find_starting_position(map_image, drone_radius)
if drone_position is None:
    print("No suitable starting position found in the map!")
    pygame.quit()
    sys.exit()

# Record the initial position
drone_positions.append(tuple(drone_position))
past_positions.append(tuple(drone_position))
saved_points.append(tuple(drone_position))

# Function to move the drone
def move_drone(position, direction):
    new_position = position[:]
    if direction == 'up':
        new_position[1] -= speed
    elif direction == 'down':
        new_position[1] += speed
    elif direction == 'left':
        new_position[0] -= speed
    elif direction == 'right':
        new_position[0] += speed
    elif direction == 'forward':
        new_position[1] -= speed
    elif direction == 'backward':
        new_position[1] += speed

    # Ensure the new position is within the bounds of the image
    new_position[0] = max(drone_radius, min(map_width - drone_radius, new_position[0]))
    new_position[1] = max(drone_radius, min(map_height - drone_radius, new_position[1]))

    # Check if the new position is within the white area
    area_is_white = True
    for dy in range(-drone_radius, drone_radius):
        for dx in range(-drone_radius, drone_radius):
            if (0 <= new_position[0] + dx < map_width) and (0 <= new_position[1] + dy < map_height):
                if not is_white(map_image.get_at((new_position[0] + dx, new_position[1] + dy))):
                    area_is_white = False
                    break
            else:
                area_is_white = False
                break

        if not area_is_white:
            break

    if area_is_white:
        past_positions.append(tuple(new_position))
        return new_position
    else:
        return position

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def is_far_enough_from_all_points(point, points, min_distance):
    for p in points:
        if calculate_distance(point, p) < min_distance:
            return False
    return True

# Function to calculate all distances based on position and orientation
def calculate_all_distances(position, orientation, radius, image):
    directions = ['up', 'down', 'left', 'right', 'forward', 'backward']
    distances = {}
    for direction in directions:
        distances[direction] = measure_distance(position, direction, radius, image)
    return distances

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for direction, button in sensor_buttons.items():
                if button.collidepoint(event.pos):
                    distance_to_obstacle = measure_distance(drone_position, direction, drone_radius, map_image)
                    print(f"Distance {direction}: {distance_to_obstacle}")

            # Check if input fields are clicked
            for field in input_field_rects:
                if input_field_rects[field].collidepoint(event.pos):
                    input_values[field] = ""

        elif event.type == pygame.KEYDOWN:
            for field in input_field_rects:
                if input_values[field] == "":
                    if event.key == pygame.K_RETURN:
                        try:
                            input_values[field] = int(input_values[field])
                        except ValueError:
                            input_values[field] = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_values[field] = input_values[field][:-1]
                    else:
                        input_values[field] += event.unicode

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        drone_position = move_drone(drone_position, 'up')
    if keys[pygame.K_DOWN]:
        drone_position = move_drone(drone_position, 'down')
    if keys[pygame.K_LEFT]:
        drone_position = move_drone(drone_position, 'left')
    if keys[pygame.K_RIGHT]:
        drone_position = move_drone(drone_position, 'right')

    # Clear the screen
    window.fill((0, 0, 0))

    # Draw the map
    window.blit(map_image, (0, 0))

    # Draw the past positions (blue markers)
    for pos in past_positions:
        pygame.draw.circle(window, drone_color, pos, drone_radius)
        pygame.draw.circle(window, past_position_color, pos, past_position_radius)

    # Check distance and update the saved points list if necessary
    if is_far_enough_from_all_points(drone_position, saved_points, 200):
        saved_points.append(tuple(drone_position))

    # Draw the saved points (grey circles)
    for pos in saved_points:
        pygame.draw.circle(window, grey_circle_color, pos, grey_circle_radius)

    # Draw the current drone (yellow circle only)
    pygame.draw.circle(window, drone_color, drone_position, drone_radius)

    # Draw the path (blue points inside yellow circles)
    for pos in past_positions:
        pygame.draw.circle(window, past_position_color, pos, past_position_radius)

    # Draw sensor buttons
    for direction, button in sensor_buttons.items():
        pygame.draw.rect(window, (0, 0, 0), button)
        font = pygame.font.Font(None, 24)
        text = font.render(direction.capitalize(), True, (255, 255, 255))
        window.blit(text, (button.x + 10, button.y + 5))

    # Draw input fields
    for field, rect in input_field_rects.items():
        pygame.draw.rect(window, (255, 255, 255), rect)
        font = pygame.font.Font(None, 24)
        text = font.render(input_values[field], True, (0, 0, 0))
        window.blit(text, (rect.x + 10, rect.y + 5))

    # Calculate and display distances
    try:
        x = int(input_values['x'])
        y = int(input_values['y'])
        orientation = int(input_values['orientation'])
        distances = calculate_all_distances((x, y), orientation, drone_radius, map_image)
        for i, (direction, distance) in enumerate(distances.items()):
            text = font.render(f"{direction.capitalize()}: {distance}", True, (255, 255, 255))
            window.blit(text, (map_width + 200, 150 + i * 30))
    except ValueError:
        pass

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()
