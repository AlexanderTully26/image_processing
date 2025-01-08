from PIL import Image

option1 = 0
name = "Nothing"

image = Image.open("/Users/alexander.tully26/Downloads/Colorful_bird.jpeg")  # Change Image here

def smooth_image(image, intensity=1):

    for _ in range(intensity):  # Apply the filter multiple times for stronger smoothing
        pixels = image.load()
        width, height = image.size

        # Create a new image for the current pass
        output_image = Image.new("RGB", (width, height))
        output_pixels = output_image.load()

        # Smoothing kernel (3x3 average blur)
        kernel = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ]
        kernel_sum = sum(sum(row) for row in kernel)
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

                # Average
                r = r_total // kernel_sum
                g = g_total // kernel_sum
                b = b_total // kernel_sum

                output_pixels[x, y] = (r, g, b)

        # Update the image for the next pass
        image = output_image

    return image


def laplacian_filter(image):
  
    pixels = image.load()
    width, height = image.size

    # Create a new image to store the result
    output_image = Image.new("RGB", (width, height))
    output_pixels = output_image.load()

    # Laplacian kernel
    kernel = [
        [0, -1,  0],
        [-1, 4, -1],
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
            r = min(255, max(0, int(r_total)))
            g = min(255, max(0, int(g_total)))
            b = min(255, max(0, int(b_total)))

            output_pixels[x, y] = (r, g, b)

    return output_image


while option1 not in [1, 2, 3, 4]:
    option1 = int(input("Choose an option: Smooth Low (1), Smooth Medium (2), Smooth High (3), Laplacian Filter (4)? "))

    if option1 == 1:
        smoothed_image = smooth_image(image.copy(), intensity=1)
        smoothed_image.save("smoothed_low.jpg")
        name = "smoothed_low"
        ishow = smoothed_image

    elif option1 == 2:
        smoothed_image = smooth_image(image.copy(), intensity=2)
        smoothed_image.save("smoothed_medium.jpg")
        name = "smoothed_medium"
        ishow = smoothed_image

    elif option1 == 3:
        smoothed_image = smooth_image(image.copy(), intensity=3)
        smoothed_image.save("smoothed_high.jpg")
        name = "smoothed_high"
        ishow = smoothed_image

    elif option1 == 4:
        laplacian_image = laplacian_filter(image.copy())
        laplacian_image.save("laplacian_filter.jpg")
        name = "laplacian_filter"
        ishow = laplacian_image

    else:
        print("Value was not an option. Please try again.")

print(f"You can find the image under the name {name}.jpg, and it will open on your computer now...")
ishow.show()
