import pygame

import forge.core.engine.display as display
import forge.core.engine.image as image
import forge.core.engine.sprite as sprite
import forge.core.managers.mouse as mouse
import forge.core.physics.vector as vector


def main():
    window = display.Display(800, 800, 'Image Tests', 120)

    flower = image.Image('flower', 'assets/flower.png', vector.Vector2D(200, 200))
    flower.add_to_renderer()

    flower_sprite = sprite.Sprite('assets/flower.png')

    mouse_visible = True
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            mouse_visible = not mouse_visible
            mouse.modify_visibility(mouse_visible)

        if mouse.is_pressed(mouse.MouseButton.LEFT):
            flower.position = mouse.position() - vector.Vector2D(60, 60)

        window.update()
        window.render()

        flower_sprite.render(window._surface, vector.Vector2D(500, 500))


if __name__ == '__main__':
    main()
