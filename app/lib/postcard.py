#!/usr/bin/env python
from PIL import Image, ImageDraw

class Postcard(object):
    _card_width = 1838
    _card_height = 1238
    _image_padding = 8

    def __init__(self):
        self.images = []
        self.canvas = Image.new('RGBA', (
            self._card_width,
            self._card_height))
        self.canvas.paste((255, 255, 255), 
                (0, 0, self._card_width, self._card_height))

    def add_image(self, path):
        self.images.append(Image.open(path))

    def calculate_padding(self, x, y, grid_size):
        unused_x = self._card_width - (grid_size[0] * x)
        unused_y = self._card_height - (grid_size[1] * y)

        return (unused_x / (grid_size[0] + 1),
            unused_y / (grid_size[1] + 1))
    
    def generate_grid(self, grid_size=(3,3)):
        x = self.images[0].size[0]
        y = 50000


        for i in self.images:
            if i.size[1] < y:
                y = i.size[1]

        # Calculate even padding
        (padding_x, padding_y) = self.calculate_padding(x, y, grid_size)
        
        cx = padding_x
        cy = padding_y
        row_size = 0
        for image in self.images:
            print 'placing...'
            image = self.crop_to(image, x, y)
            self.canvas.paste(image, (cx, cy))
            cx += image.size[0] + padding_x

            print 'image: ', image.size
            row_size += 1

            # Start a new row if need be
            if row_size >= grid_size[0]:
                cy += y + padding_y
                cx = padding_x
                row_size = 0

    def crop_to(self, image, x, y):
        height = image.size[1]
        diff = int((height - y) / 2)
        img = image.crop((0, diff, x, height - diff))
        return img

    def place_banner(self, path, position='center'):
        banner = Image.open(path)

        box = (0,0)

        bottom = self._card_height - banner.size[1]
        center = self._card_width / 2 - banner.size[0] / 2

        if position == 'center':
            box = (center, bottom)
        elif position == 'left':
            box = (0, bottom)
        elif position == 'twothirds':
            box = (center, bottom - 40)

        # Draw a stroke around the box
        strokebox = (box[0] - 2, 
            box[1] - 2,
            box[0] + banner.size[0] + 1,
            box[1] + banner.size[1] + 1)

        draw = ImageDraw.Draw(self.canvas)
        draw.rectangle(strokebox, (50, 50, 50))

        self.canvas.paste(banner, box)

    def quarter(self):
        return self.canvas.resize((
                int(self._card_width / 4),
                int(self._card_height / 4)))


if __name__ == '__main__':
    import os

    card = Postcard()
    for path in os.listdir('data/larger'):
        card.add_image('data/larger/%s' % (path))

    card.generate_grid()
    card.place_banner('banner.jpg', 'left')
    card.canvas.save('canvas-3x3.jpg')

    card = Postcard()
    for path in os.listdir('data/larger'):
        card.add_image('data/larger/%s' % (path))

    card.generate_grid((2,2))
    card.place_banner('banner2.jpg', 'center')
    card.canvas.save('canvas-2x2.jpg')

    card = Postcard()
    for path in os.listdir('data/warren'):
        card.add_image('data/warren/%s' % (path))

    card.generate_grid((1,1))
    card.place_banner('banner3.jpg', 'twothirds')
    card.canvas.save('canvas-1x1.jpg')
