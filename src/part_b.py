import pygame
import sys
import time
from Map import Map
from Graph import Graph
from CPU import CPU

WINDOW_WIDTH = 1000  # Increased width to accommodate buttons
WINDOW_HEIGHT = 800

def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('2D simulator screen')

    map_obj = Map("Maps/p12.png", WINDOW_WIDTH, WINDOW_HEIGHT)
    cpu = CPU(map_obj)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        cpu.run()

        # Clear the screen
        window.fill((0, 0, 0))

        # Draw the map and the player
        window.blit(map_obj.map_image, map_obj.map_image.get_rect())
        Graph.draw_drone(window, cpu.drone)

        # Draw the path
        cpu.algo.path_marker.draw(window)
        cpu.algo.blue_path_marker.draw(window)

        # Draw speedometer and battery indicator
        font = pygame.font.Font(None, 36)
        speed = (cpu.drone.speed_x**2 + cpu.drone.speed_y**2)**0.5
        speed_text = font.render(f"Speed: {speed:.2f} m/s", True, (255, 255, 255))
        battery_text = font.render(f"Battery: {cpu.drone.check_battery()} s", True, (255, 255, 255))
        window.blit(speed_text, (WINDOW_WIDTH - 180, 200))
        window.blit(battery_text, (WINDOW_WIDTH - 180, 250))

        # Update the display
        pygame.display.flip()

        if cpu.drone.check_battery() <= 0:
            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
