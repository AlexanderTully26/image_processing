from PIL import Image

option1 = 0
name = "Nothing"

image = Image.open("/Users/alexander.tully26/Downloads/Colorful_bird.jpeg")  # Change Image here

def color_dithering(image, palette_size):

    pixels = image.load()
    width, height = image.size
    
    # Normalize color levels to fit the palette
    def quantize_color(value, levels):
        step = 256 // levels
        return step * round(value / step)

    levels = int(palette_size ** (1/3))  # Compute color levels for each channel
    for y in range(height):
        for x in range(width):
            old_r, old_g, old_b = pixels[x, y]
            
            # Quantize colors
            new_r = quantize_color(old_r, levels)
            new_g = quantize_color(old_g, levels)
            new_b = quantize_color(old_b, levels)
            
            # Update pixel with quantized color
            pixels[x, y] = (new_r, new_g, new_b)
            
            # Compute quantization error
            err_r = old_r - new_r
            err_g = old_g - new_g
            err_b = old_b - new_b

            # Spread the error to neighboring pixels (Floyd-Steinberg weights)
            for dx, dy, factor in [(1, 0, 7/16), (-1, 1, 3/16), (0, 1, 5/16), (1, 1, 1/16)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    nr, ng, nb = pixels[nx, ny]
                    pixels[nx, ny] = (
                        min(255, max(0, int(nr + err_r * factor))),
                        min(255, max(0, int(ng + err_g * factor))),
                        min(255, max(0, int(nb + err_b * factor)))
                    )
    
    return image


while (option1 != 1) and (option1 != 2) and (option1 != 3):
    option1 = int(input("Choose a dithering level: 4 colors (1), 16 colors (2), or 64 colors (3)? "))

    if option1 == 1:
        dithered_image = color_dithering(image, palette_size=4)
        dithered_image.save("dithered_4_colors.jpg")
        name = "dithered_4_colors"
        ishow = dithered_image

    elif option1 == 2:
        dithered_image = color_dithering(image, palette_size=16)
        dithered_image.save("dithered_16_colors.jpg")
        name = "dithered_16_colors"
        ishow = dithered_image

    elif option1 == 3:
        dithered_image = color_dithering(image, palette_size=64)
        dithered_image.save("dithered_64_colors.jpg")
        name = "dithered_64_colors"
        ishow = dithered_image

    else:
        print("Value was not an option. Please try again.")

print(f"You can find the image under the name {name}.jpg, and it will open on your computer now...")
ishow.show()
