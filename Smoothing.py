from PIL import Image

option1 = 0
name = "Nothing"

image = Image.open("/Users/alexander.tully26/Downloads/Colorful_bird.jpeg")  # Change Image here

def smooth_image(image, intensity=1):
    """
    Apply a smoothing filter to the image.
    :param image: PIL.Image object
    :param intensity: Smoothing intensity (multiplier for repeated application of the filter)
    :return: Smoothed image
    """
    pixels = image.load()
    width, height = image.size

    # Create a copy of the original image to store the result
    output_image = Image.new("RGB", (width, height))
    output_pixels = output_image.load()

    # Smoothing kernel (3x3 average blur)
    kernel = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    kernel_size = len(kernel)
    kernel_sum = sum(sum(row) for row in kernel)
    offset = kernel_size // 2

    for _ in range(intensity):  # Apply the filter multiple times for stronger smoothing
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

                # Compute the average
                r = r_total // kernel_sum
                g = g_total // kernel_sum
                b = b_total // kernel_sum

                output_pixels[x, y] = (r, g, b)

        # Update pixels for the next pass if intensity > 1
        pixels = output_pixels.copy()

    return output_image


while option1 not in [1, 2, 3]:
    option1 = int(input("Choose smoothing intensity: Low (1), Medium (2), or High (3)? "))

    if option1 == 1:
        smoothed_image = smooth_image(image, intensity=1)
        smoothed_image.save("smoothed_low.jpg")
        name = "smoothed_low"
        ishow = smoothed_image

    elif option1 == 2:
        smoothed_image = smooth_image(image, intensity=2)
        smoothed_image.save("smoothed_medium.jpg")
        name = "smoothed_medium"
        ishow = smoothed_image

    elif option1 == 3:
        smoothed_image = smooth_image(image, intensity=3)
        smoothed_image.save("smoothed_high.jpg")
        name = "smoothed_high"
        ishow = smoothed_image

    else:
        print("Value was not an option. Please try again.")

print("You can find the image under the name {name}.jpg, and it will open on your computer now...")
ishow.show()
