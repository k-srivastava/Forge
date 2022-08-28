import sys

import pygame

from forge.core.engine import display, image
from forge.core.managers import event as f_event, mouse
from forge.core.physics import vector


def create_image_function() -> None:
    print('Image created.')


def main() -> None:
    window = display.Display(800, 800, 'Image Tests', 120)

    create_image = f_event.Event('create-image')
    create_image += create_image_function

    flower = image.Image('assets/flower.png', vector.Vector2D(200, 200), name='flower1')

    image_pool = image.ImagePool('custom', _images=[flower])
    image_pool.add_to_renderer()

    current_idx = 2

    mouse_visible = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

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
