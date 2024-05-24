import pygame
import sys

# Initialize Pygame
pygame.init()

# Load the map image
map_image = pygame.image.load('p11.png')

# Get dimensions of the map
map_width, map_height = map_image.get_size()

# Set up the display
window_size = (map_width, map_height)
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

# Color and radius for the past positions
past_position_color = (0, 0, 255)  # Blue color for the past positions
past_position_radius = 1  # Radius for the past positions

def is_white(pixel):
    return pixel[:3] == (255, 255, 255)

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

# Find the starting position for the drone
drone_position = find_starting_position(map_image, drone_radius)
if drone_position is None:
    print("No suitable starting position found in the map!")
    pygame.quit()
    sys.exit()

# Record the initial position
drone_positions.append(tuple(drone_position))

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
        drone_positions.append(tuple(new_position))
        past_positions.append(tuple(new_position))
        return new_position
    else:
        return position

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
        pygame.draw.circle(window, past_position_color, pos, past_position_radius)

    # Draw the drone positions (yellow markers)
    for pos in drone_positions:
        pygame.draw.circle(window, drone_color, pos, drone_radius)

    # Draw the current drone
    pygame.draw.circle(window, drone_color, drone_position, drone_radius)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()
