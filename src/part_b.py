import pygame
import sys
import time
from Map import Map
from Graph import Graph
from CPU import CPU

WINDOW_WIDTH = 1000  # Increased width to accommodate buttons
WINDOW_HEIGHT = 800
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('2D simulator screen')

    map_obj = Map("Maps/p12.png", WINDOW_WIDTH, WINDOW_HEIGHT)
    cpu = CPU(map_obj)

    start_button_rect = pygame.Rect(WINDOW_WIDTH - 180, 50, BUTTON_WIDTH, BUTTON_HEIGHT)
    stop_button_rect = pygame.Rect(WINDOW_WIDTH - 180, 110, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    game_running = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    game_running = True
                    cpu.drone.battery_status = 480  # Reset battery status
                    cpu.drone.z = 10  # Start at a height of 10 units
                elif stop_button_rect.collidepoint(event.pos):
                    game_running = False

        if game_running:
            cpu.run()

        # Clear the screen
        window.fill((0, 0, 0))

        # Draw the map and the player
        window.blit(map_obj.map_image, map_obj.map_image.get_rect())
        Graph.draw_drone(window, cpu.drone)

        # Draw the path
        cpu.algo.path_marker.draw(window)
        cpu.algo.blue_path_marker.draw(window)

        # Draw grey circles every 50 pixels
        for i, position in enumerate(cpu.algo.path_marker.positions):
            if i % 50 == 0:
                pygame.draw.circle(window, cpu.algo.grey_circle_color, position, cpu.algo.grey_circle_radius)

        # Draw buttons
        pygame.draw.rect(window, (0, 255, 0), start_button_rect)
        pygame.draw.rect(window, (255, 0, 0), stop_button_rect)
        font = pygame.font.Font(None, 36)
        start_text = font.render("Start", True, (0, 0, 0))
        stop_text = font.render("Stop", True, (0, 0, 0))
        window.blit(start_text, (start_button_rect.x + 10, start_button_rect.y + 10))
        window.blit(stop_text, (stop_button_rect.x + 10, stop_button_rect.y + 10))

        # Draw speedometer and battery indicator
        speed = (cpu.drone.speed_x**2 + cpu.drone.speed_y**2)**0.5
        speed_text = font.render(f"Speed: {speed:.2f} m/s", True, (255, 255, 255))
        battery_text = font.render(f"Battery: {cpu.drone.check_battery()} s", True, (255, 255, 255))
        window.blit(speed_text, (WINDOW_WIDTH - 180, 200))
        window.blit(battery_text, (WINDOW_WIDTH - 180, 250))

        # Update the display
        pygame.display.flip()

        if cpu.drone.check_battery() <= 0:
            game_running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
