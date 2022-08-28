import pygame

import forge.core.engine.display as display
import forge.core.engine.image as image
import forge.core.managers.event
import forge.core.managers.mouse as mouse
import forge.core.physics.vector as vector


def create_image_function():
    print('Image created.')


def main():
    window = display.Display(800, 800, 'Image Tests', 120)

    create_image = forge.core.managers.event.Event('create-image')

    flower = image.Image('assets/flower.png', vector.Vector2D(200, 200), name='flower1')
    image_pool = image.ImagePool('custom', _images=[flower])
    image_pool.add_to_renderer()

    current_idx = 2
    create_image += create_image_function

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
            image_pool += image.Image('assets/flower.png', mouse.position(), name=f'flower{current_idx}')
            current_idx += 1
            create_image.post()

        if mouse.is_pressed(mouse.MouseButton.RIGHT):
            if current_idx == 1:
                continue

            image_pool -= image.get_image_from_name(f'flower{current_idx - 1}')
            image.delete_image_from_name(f'flower{current_idx - 1}')
            current_idx -= 1

        window.update()
        window.render()


if __name__ == '__main__':
    pygame.init()
    main()
