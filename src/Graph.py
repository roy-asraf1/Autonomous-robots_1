import pygame

class Graph:
    @staticmethod
    def draw_drone(screen, drone):
        pygame.draw.circle(screen, (0, 255, 0), [int(drone.x), int(drone.y)], 5)

    @staticmethod
    def draw_buttons(screen, game_running, start_button_rect, stop_button_rect):
        start_color = (0, 255, 0) if game_running else (255, 255, 255)
        stop_color = (255, 0, 0) if not game_running else (255, 255, 255)
        
        pygame.draw.rect(screen, start_color, start_button_rect)
        pygame.draw.rect(screen, stop_color, stop_button_rect)
        
        font = pygame.font.Font(None, 36)
        Graph._draw_text(screen, 'Start', start_button_rect, font)
        Graph._draw_text(screen, 'Stop', stop_button_rect, font)

    @staticmethod
    def _draw_text(screen, text, rect, font):
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (rect.x + 20, rect.y + 10))

    @staticmethod
    def draw_path(screen, path, color, radius):
        for position in path:
            pygame.draw.circle(screen, color, position, radius)

    @staticmethod
    def draw_map(screen, map_image):
        screen.blit(map_image, map_image.get_rect())

    @staticmethod
    def draw_saved_points(screen, saved_points, color, radius):
        for point in saved_points:
            pygame.draw.circle(screen, color, point, radius)