from .Layer import Layer
import pygame
from pygame.math import Vector2
from properties import (
    CARTOON_FONT,
    COLORS,
    WINDOW_PROPERTIES,
    BALL_PROPERTIES,
    TILE_PROPERTIES,
)


class ScoreLayer(Layer):
    def __init__(self, gameState):
        self.gameState = gameState
        self.scoreFont = pygame.font.Font(CARTOON_FONT, 30)

        self.score = 0
        self.counter = 0
        self.multiplier = 1

    def getScoreMultiplierValue(self):
        return self.multiplier * len(self.gameState.getActiveBalls())

    def incrementMultiplierValue(self):
        if self.counter == 1000:
            self.multiplier += 0.5

    def elementDestroyed(self, element):
        self.incrementMultiplierValue()
        if element.type == TILE_PROPERTIES["type"]:
            self.score += int(100 * self.getScoreMultiplierValue())
            if self.counter < 1000:
                self.counter += 100
            else:
                self.counter = 0

            self.incrementBallSpeed()
        elif element.type == BALL_PROPERTIES["type"]:
            self.score -= 100

    def incrementBallSpeed(self):
        if self.counter == 1000:
            for ball in self.gameState.getActiveBalls():
                if ball.movementVector.x > 0 and ball.movementVector.y > 0:
                    ball.movementVector += Vector2(1, 1)
                elif ball.movementVector.x < 0 and ball.movementVector.y < 0:
                    ball.movementVector += Vector2(-1, -1)
                elif ball.movementVector.x > 0 and ball.movementVector.y < 0:
                    ball.movementVector += Vector2(1, -1)
                elif ball.movementVector.x < 0 and ball.movementVector.y > 0:
                    ball.movementVector += Vector2(-1, 1)

    def render(self, window):
        scoreSurface = self.scoreFont.render(str(self.score), True, COLORS["RED"])
        scoreX = WINDOW_PROPERTIES["width"] - scoreSurface.get_width() - 10
        scoreY = WINDOW_PROPERTIES["height"] - scoreSurface.get_height() - 10
        window.blit(scoreSurface, (scoreX, scoreY))
