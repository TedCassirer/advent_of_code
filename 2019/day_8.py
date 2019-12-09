BLACK = 0
WHITE = 1
TRANSPARENT = 2

def get_image_data_layers(height, width):
    layer_size = width * height
    with open('2019/input/day_8') as file:
        data = [int(s) for s in file.readline().strip()]
        for layer_start in range(0, len(data), layer_size):
            layer_data = data[layer_start : layer_start+layer_size]
            layer = []
            for row_start in range(0, layer_size, width):
                layer.append(layer_data[row_start:row_start+width])
            yield layer

def count_number_of(num, layer):
    return sum(n==num for row in layer for n in row)

def to_printable_image(image):
    symbols = {
        BLACK: '░',
        WHITE: '▓',
        TRANSPARENT: 'I\'m invisible'
    }
    decoded_image = []
    for row in image:
        decoded_image.append(''.join([symbols[s] for s in row]))
    return '\n' + '\n'.join(decoded_image)


def get_pixels_matching(image, mode):
    for y, row in enumerate(image):
        for x, n in enumerate(image[y]):
            if n == mode:
                yield (y, x)


def part1():
    height, width = 6, 25
    fewest_blacks = min(get_image_data_layers(height, width), key=lambda l: len(list(get_pixels_matching(l, BLACK))))
    whites = count_number_of(WHITE, fewest_blacks)
    transparents = count_number_of(TRANSPARENT, fewest_blacks)
    return whites * transparents

    
def part2():
    height, width = 6, 25
    layers = get_image_data_layers(height, width)
    final_image = [[TRANSPARENT]*width for _ in range(height)]
    for layer in layers:
        for y, x in get_pixels_matching(final_image, TRANSPARENT):
            final_image[y][x] = layer[y][x]
    
    return to_printable_image(final_image)

if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())