from __future__ import annotations

import pygame

from src.constants import (
    BACKGROUND_COLOR,
    FOOD_COLOR,
    GAME_OVER_COLOR,
    GRID_COLOR,
    GRID_HEIGHT,
    GRID_SIZE,
    GRID_WIDTH,
    SNAKE_BODY_COLOR,
    SNAKE_HEAD_COLOR,
    TEXT_COLOR,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.core import system_keys
from src.core.input_keys import pressed_direction
from src.models.food import Food
from src.models.game_state import GameState
from src.models.snake import Snake
from src.scenes.base_scene import BaseScene
from src.ui.font_manager import get_font


class GameplayScene(BaseScene):
    """Playable gameplay scene with autosave support."""

    def __init__(self, app, game_state: GameState | None = None) -> None:
        super().__init__(app)
        self.font = get_font(32)
        self.large_font = get_font(56)
        self.elapsed_since_move = 0
        self.is_game_over = False
        self.score = 0
        self.key_edges = system_keys.KeyEdges()
        self.is_paused = False
        self.status_message = ""

        if game_state is None:
            self.move_interval_ms = self.app.settings_service.load().move_interval_ms
            self.snake = Snake()
            self.food = Food()
            self.food.respawn(set(self.snake.body))
            self._persist_progress()
        else:
            self.move_interval_ms = game_state.move_interval_ms
            self.score = game_state.score
            self.snake = Snake(
                body=list(game_state.snake_body),
                direction=game_state.direction,
                pending_growth=game_state.pending_growth,
            )
            self.food = Food(position=game_state.food_position)

    def handle_event(self, event: pygame.event.Event) -> bool:
        _ = event
        return True

    def on_enter(self) -> None:
        self.key_edges.sync("f3", system_keys.VK_F3)
        self.key_edges.sync("escape", system_keys.VK_ESCAPE)
        self.key_edges.sync("restart", system_keys.VK_R)
        self.key_edges.sync("save", system_keys.VK_E)
        self.key_edges.sync("pause", system_keys.VK_P)

    def update(self, delta_ms: int) -> None:
        if self.key_edges.just_pressed("f3", system_keys.VK_F3):
            self.app.input_debug.enabled = not self.app.input_debug.enabled
            self.app.input_debug.record_system_key("f3")

        if self.key_edges.just_pressed("escape", system_keys.VK_ESCAPE):
            self.app.input_debug.record_system_key("escape")
            if self.is_game_over:
                self.app.save_service.clear()
            else:
                self._persist_progress()
            self.app.change_scene("menu")
            return

        if self.is_game_over:
            if self.key_edges.just_pressed("restart", system_keys.VK_R):
                self.app.input_debug.record_system_key("restart")
                self.app.start_new_game()
            return

        if self.key_edges.just_pressed("pause", system_keys.VK_P):
            self.is_paused = not self.is_paused
            self.status_message = "\u5df2\u6682\u505c\uff0c\u6309 P \u7ee7\u7eed" if self.is_paused else "\u5df2\u7ee7\u7eed\u6e38\u620f"
            self.app.input_debug.record_system_key("pause")
            return

        if self.key_edges.just_pressed("save", system_keys.VK_E):
            self._persist_progress()
            self.status_message = "\u5df2\u4fdd\u5b58\u5b58\u6863"
            self.app.input_debug.record_system_key("save")
            return

        if self.is_paused:
            return

        direction = pressed_direction()
        if direction is not None:
            self.snake.set_direction(direction)

        self.elapsed_since_move += delta_ms
        if self.elapsed_since_move < self.move_interval_ms:
            return

        self.elapsed_since_move = 0
        self.snake.move()
        self._handle_collisions()
        if not self.is_game_over:
            self._persist_progress()

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND_COLOR)
        self._draw_grid(screen)
        self._draw_food(screen)
        self._draw_snake(screen)
        self._draw_hud(screen)

        if self.is_game_over:
            self._draw_game_over(screen)

    def _handle_collisions(self) -> None:
        head_x, head_y = self.snake.get_head()

        if not (0 <= head_x < GRID_WIDTH and 0 <= head_y < GRID_HEIGHT):
            self._handle_game_over()
            return

        if self.snake.collides_with_self():
            self._handle_game_over()
            return

        if self.snake.get_head() == self.food.position:
            self.score += 1
            self.snake.grow()
            try:
                self.food.respawn(set(self.snake.body))
            except ValueError:
                self._handle_game_over()

    def _draw_grid(self, screen: pygame.Surface) -> None:
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))

    def _draw_snake(self, screen: pygame.Surface) -> None:
        for index, (x, y) in enumerate(self.snake.body):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            color = SNAKE_HEAD_COLOR if index == 0 else SNAKE_BODY_COLOR
            pygame.draw.rect(screen, color, rect)

    def _draw_food(self, screen: pygame.Surface) -> None:
        x, y = self.food.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, FOOD_COLOR, rect)

    def _draw_hud(self, screen: pygame.Surface) -> None:
        score_surface = self.font.render(f"\u5206\u6570: {self.score}", True, TEXT_COLOR)
        screen.blit(score_surface, (16, 12))

        if not self.is_game_over:
            hint_surface = self.font.render(
                "\u79fb\u52a8: WASD / \u65b9\u5411\u952e  \u4fdd\u5b58: E  \u6682\u505c: P  \u8fd4\u56de\u83dc\u5355: ESC",
                True,
                TEXT_COLOR,
            )
            screen.blit(hint_surface, (16, 42))

        if self.status_message:
            status_surface = self.font.render(self.status_message, True, TEXT_COLOR)
            screen.blit(status_surface, (16, 72))

        if self.is_paused and not self.is_game_over:
            self._draw_pause_overlay(screen)

        if self.app.input_debug.enabled:
            debug_surface = self.font.render(self.app.input_debug.last_key_text, True, TEXT_COLOR)
            screen.blit(debug_surface, (16, WINDOW_HEIGHT - 34))

    def _draw_game_over(self, screen: pygame.Surface) -> None:
        title_surface = self.large_font.render("\u6e38\u620f\u7ed3\u675f", True, GAME_OVER_COLOR)
        subtitle_surface = self.font.render(
            "\u6309 R \u91cd\u65b0\u5f00\u59cb\uff0c\u6309 ESC \u8fd4\u56de\u83dc\u5355",
            True,
            TEXT_COLOR,
        )
        score_surface = self.font.render(f"\u6700\u7ec8\u5206\u6570: {self.score}", True, TEXT_COLOR)

        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
        score_rect = score_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

        screen.blit(title_surface, title_rect)
        screen.blit(subtitle_surface, subtitle_rect)
        screen.blit(score_surface, score_rect)

    def _draw_pause_overlay(self, screen: pygame.Surface) -> None:
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        title_surface = self.large_font.render("\u6e38\u620f\u6682\u505c", True, TEXT_COLOR)
        subtitle_surface = self.font.render("\u6309 P \u7ee7\u7eed\uff0c\u6309 E \u4fdd\u5b58\uff0c\u6309 ESC \u8fd4\u56de\u83dc\u5355", True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 25))
        screen.blit(title_surface, title_rect)
        screen.blit(subtitle_surface, subtitle_rect)

    def _persist_progress(self) -> None:
        self.app.save_service.save(
            GameState(
                snake_body=list(self.snake.body),
                direction=self.snake.direction,
                food_position=self.food.position,
                score=self.score,
                move_interval_ms=self.move_interval_ms,
                pending_growth=self.snake.pending_growth,
            )
        )

    def _handle_game_over(self) -> None:
        self.is_game_over = True
        self.app.save_service.clear()
