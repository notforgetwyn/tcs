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
    LEFT,
    RIGHT,
    SNAKE_BODY_COLOR,
    SNAKE_HEAD_COLOR,
    TEXT_COLOR,
    UP,
    DOWN,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.models.food import Food
from src.models.game_state import GameState
from src.models.snake import Snake
from src.ui.font_manager import get_font


class GameplayScene:
    """Playable gameplay scene with autosave support."""

    def __init__(self, app, game_state: GameState | None = None) -> None:
        self.app = app
        self.font = get_font(32)
        self.large_font = get_font(56)
        self.elapsed_since_move = 0
        self.is_game_over = False
        self.score = 0

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
        if event.type != pygame.KEYDOWN:
            return True

        if event.key == pygame.K_ESCAPE:
            if self.is_game_over:
                self.app.save_service.clear()
            else:
                self._persist_progress()
            self.app.change_scene("menu")
            return True

        if self.is_game_over:
            if event.key == pygame.K_r:
                self.app.start_new_game()
            return True

        direction_map = {
            pygame.K_UP: UP,
            pygame.K_w: UP,
            pygame.K_DOWN: DOWN,
            pygame.K_s: DOWN,
            pygame.K_LEFT: LEFT,
            pygame.K_a: LEFT,
            pygame.K_RIGHT: RIGHT,
            pygame.K_d: RIGHT,
        }
        new_direction = direction_map.get(event.key)
        if new_direction is not None:
            self.snake.set_direction(new_direction)

        return True

    def update(self, delta_ms: int) -> None:
        if self.is_game_over:
            return

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
        score_surface = self.font.render(f"分数: {self.score}", True, TEXT_COLOR)
        screen.blit(score_surface, (16, 12))

        if not self.is_game_over:
            hint_surface = self.font.render(
                "移动: WASD / 方向键  返回菜单: ESC",
                True,
                TEXT_COLOR,
            )
            screen.blit(hint_surface, (16, 42))

    def _draw_game_over(self, screen: pygame.Surface) -> None:
        title_surface = self.large_font.render("游戏结束", True, GAME_OVER_COLOR)
        subtitle_surface = self.font.render(
            "按 R 重新开始，按 ESC 返回菜单",
            True,
            TEXT_COLOR,
        )
        score_surface = self.font.render(f"最终分数: {self.score}", True, TEXT_COLOR)

        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
        score_rect = score_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

        screen.blit(title_surface, title_rect)
        screen.blit(subtitle_surface, subtitle_rect)
        screen.blit(score_surface, score_rect)

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
