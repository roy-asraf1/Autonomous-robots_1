import pygame
import sys
import time
from Drone import Drone
from Map import Map
from Graph import Graph
from Tools import find_safe_starting_position
from DocumentLogger import DistanceLogger
from PathMarker import PathMarker  # הוספנו את הייבוא של PathMarker


SCREEN_WIDTH = 1000  # Increased width to accommodate buttons
SCREEN_HEIGHT = 800
DRONE_MAX_VELOCITY = 0.5  # meters per second, reduced speed
DRONE_ACCELERATION_RATE = 0.2  # meters per second^2, reduced acceleration
ROTATION_ANGULAR_VELOCITY = 100  # degrees per second
MAXIMUM_TILT = 10  # degrees
BATTERY_DURATION = 480  # seconds
SAFETY_MARGIN = 20  # Distance from the black area
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

def setup_pygame():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('2D simulator screen')
    return screen

def create_map_and_drone():
    map_width = SCREEN_WIDTH - 200  # Adjusting map width to leave space for buttons
    map_obj = Map("Maps/p12.png", map_width, SCREEN_HEIGHT)
    drone_x, drone_y = find_safe_starting_position(map_obj, SAFETY_MARGIN)
    drone = Drone(drone_x, drone_y, DRONE_MAX_VELOCITY, DRONE_ACCELERATION_RATE, ROTATION_ANGULAR_VELOCITY, MAXIMUM_TILT, BATTERY_DURATION)
    return map_obj, drone

def initialize_loggers_and_markers(drone):
    distance_logger = DistanceLogger(drone)
    path_marker = PathMarker(4, (255, 255, 0))  # Radius 4 for yellow path
    blue_path_marker = PathMarker(2, (0, 0, 255))  # Radius 2 for blue path
    return distance_logger, path_marker, blue_path_marker

def setup_buttons():
    start_button_rect = pygame.Rect(SCREEN_WIDTH - 180, 50, BUTTON_WIDTH, BUTTON_HEIGHT)
    stop_button_rect = pygame.Rect(SCREEN_WIDTH - 180, 110, BUTTON_WIDTH, BUTTON_HEIGHT)
    return start_button_rect, stop_button_rect

def draw_buttons(screen, start_button_rect, stop_button_rect):
    pygame.draw.rect(screen, (0, 255, 0), start_button_rect)
    pygame.draw.rect(screen, (255, 0, 0), stop_button_rect)
    font = pygame.font.Font(None, 36)
    start_text = font.render("Start", True, (0, 0, 0))
    stop_text = font.render("Stop", True, (0, 0, 0))
    screen.blit(start_text, (start_button_rect.x + 10, start_button_rect.y + 10))
    screen.blit(stop_text, (stop_button_rect.x + 10, stop_button_rect.y + 10))

def handle_keydown(event, drone, game_running):
    if game_running:
        if event.key == pygame.K_LEFT:
            drone.roll = max(drone.roll - ROTATION_ANGULAR_VELOCITY * 0.1, -MAXIMUM_TILT)
        elif event.key == pygame.K_RIGHT:
            drone.roll = min(drone.roll + ROTATION_ANGULAR_VELOCITY * 0.1, MAXIMUM_TILT)
        elif event.key == pygame.K_UP:
            drone.pitch = max(drone.pitch - ROTATION_ANGULAR_VELOCITY * 0.1, -MAXIMUM_TILT)
        elif event.key == pygame.K_DOWN:
            drone.pitch = min(drone.pitch + ROTATION_ANGULAR_VELOCITY * 0.1, MAXIMUM_TILT)
        elif event.key == pygame.K_w:
            drone.yaw += ROTATION_ANGULAR_VELOCITY * 0.1
        elif event.key == pygame.K_s:
            drone.yaw -= ROTATION_ANGULAR_VELOCITY * 0.1
        elif event.key == pygame.K_SPACE:
            if drone.altitude == 0:
                drone.altitude = 1  # Takeoff
            else:
                drone.altitude = 0  # Landing

def handle_mousebuttondown(event, start_button_rect, stop_button_rect, map_obj, drone, distance_logger, path_marker, blue_path_marker, game_running):
    if start_button_rect.collidepoint(event.pos):
        reset_drone(map_obj, drone)
        distance_logger.start_logging()
        reset_markers(path_marker, blue_path_marker)
        game_running = True
    elif stop_button_rect.collidepoint(event.pos):
        game_running = False
        distance_logger.stop_logging()
    return game_running

def reset_drone(map_obj, drone):
    drone.x, drone.y = find_safe_starting_position(map_obj, SAFETY_MARGIN)
    drone.pitch = drone.roll = drone.yaw = 0
    drone.speed_x = drone.speed_y = 0
    drone.altitude = 0
    drone.battery_status = BATTERY_DURATION

def reset_markers(path_marker, blue_path_marker):
    path_marker.positions = []
    blue_path_marker.positions = []

def update_game_state(drone, map_obj, distance_logger, path_marker, blue_path_marker, game_running, flight_start_time):
    drone.battery_status = max(0, BATTERY_DURATION - (time.time() - flight_start_time))
    if drone.battery_status == 0:
        print("Game Over: Battery depleted.")
        game_running = False
        distance_logger.stop_logging()

    drone.update_speed()

    new_x = drone.x + drone.speed_x
    new_y = drone.y + drone.speed_y

    if not map_obj.is_walkable(new_x, new_y):
        print("Game Over: Player moved out of the map or into an unwalkable area.")
        game_running = False
        distance_logger.stop_logging()
    else:
        drone.x, drone.y = new_x, new_y
        path_marker.add_position((int(new_x), int(new_y)))
        blue_path_marker.add_position((int(new_x), int(new_y)))
    return game_running

def draw_game_elements(screen, map_obj, drone, path_marker, blue_path_marker, start_button_rect, stop_button_rect):
    screen.fill((0, 0, 0))
    screen.blit(map_obj.map_image, map_obj.map_image.get_rect())
    Graph.draw_drone(screen, drone)
    path_marker.draw(screen)
    blue_path_marker.draw(screen)
    draw_circles_every_50_pixels(screen, path_marker.positions)
    draw_buttons(screen, start_button_rect, stop_button_rect)
    draw_speed_and_battery(screen, drone)

def draw_circles_every_50_pixels(screen, positions):
    grey_circle_color = (128, 128, 128)
    grey_circle_radius = 4
    for i, position in enumerate(positions):
        if i % 50 == 0:
            pygame.draw.circle(screen, grey_circle_color, position, grey_circle_radius)

def draw_speed_and_battery(screen, drone):
    font = pygame.font.Font(None, 36)
    speed = (drone.speed_x**2 + drone.speed_y**2)**0.5
    speed_text = font.render(f"Speed: {speed:.2f} m/s", True, (255, 255, 255))
    battery_text = font.render(f"Battery: {drone.battery_status:.2f} s", True, (255, 255, 255))
    screen.blit(speed_text, (SCREEN_WIDTH - 180, 200))
    screen.blit(battery_text, (SCREEN_WIDTH - 180, 250))

def main():
    screen = setup_pygame()
    map_obj, drone = create_map_and_drone()
    distance_logger, path_marker, blue_path_marker = initialize_loggers_and_markers(drone)
    start_button_rect, stop_button_rect = setup_buttons()

    game_running = False
    flight_start_time = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_keydown(event, drone, game_running)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game_running = handle_mousebuttondown(event, start_button_rect, stop_button_rect, map_obj, drone, distance_logger, path_marker, blue_path_marker, game_running)
                if game_running:
                    flight_start_time = time.time()

        if game_running:
            game_running = update_game_state(drone, map_obj, distance_logger, path_marker, blue_path_marker, game_running, flight_start_time)

        draw_game_elements(screen, map_obj, drone, path_marker, blue_path_marker, start_button_rect, stop_button_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
