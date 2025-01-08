from PIL import Image

option1 = 0
name = "Nothing"

image = Image.open("/Users/alexander.tully26/Downloads/Colorful_bird.jpeg")  # Change Image here

def sharpen_image(image, intensity=1):
 
    pixels = image.load()
    width, height = image.size

    # Create a copy of the original image to store the result
    output_image = Image.new("RGB", (width, height))
    output_pixels = output_image.load()

    # Sharpening kernel
    kernel = [
        [0, -1,  0],
        [-1, 5, -1],
        [0, -1,  0]
    ]

    offset = len(kernel) // 2

    for x in range(width):
        for y in range(height):
            r_total, g_total, b_total = 0, 0, 0

            # Apply kernel to the neighborhood
            for dx in range(-offset, offset + 1):
                for dy in range(-offset, offset + 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:  # Check bounds
                        k = kernel[dx + offset][dy + offset]
                        r, g, b = pixels[nx, ny]
                        r_total += r * k
                        g_total += g * k
                        b_total += b * k

            # Clamp the results to valid color range [0, 255]
            r = min(255, max(0, int(r_total * intensity)))
            g = min(255, max(0, int(g_total * intensity)))
            b = min(255, max(0, int(b_total * intensity)))

            output_pixels[x, y] = (r, g, b)

    return output_image


while (option1 != 1) and (option1 != 2) and (option1 != 3):
    option1 = int(input("Choose sharpening intensity: Low (1), Medium (2), or High (3)? "))

    if option1 == 1:
        sharpened_image = sharpen_image(image, intensity=1)
        sharpened_image.save("sharpened_low.jpg")
        name = "sharpened_low"
        ishow = sharpened_image

    elif option1 == 2:
        sharpened_image = sharpen_image(image, intensity=1.5)
        sharpened_image.save("sharpened_medium.jpg")
        name = "sharpened_medium"
        ishow = sharpened_image

    elif option1 == 3:
        sharpened_image = sharpen_image(image, intensity=2)
        sharpened_image.save("sharpened_high.jpg")
        name = "sharpened_high"
        ishow = sharpened_image

    else:
        print("Value was not an option. Please try again.")

print(f"You can find the image under the name {name}.jpg, and it will open on your computer now...")
ishow.show()
