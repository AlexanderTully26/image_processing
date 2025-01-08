from PIL import Image

option1 = 0
name = "Nothing"

# Load the image (Replace with the desired image path)
image = Image.open("/Users/alexander.tully26/Downloads/Colorful_bird.jpeg")  # Change Image here

def box_blur(image, kernel_size=3):

    pixels = image.load()
    width, height = image.size
    output_image = Image.new("RGB", (width, height))
    output_pixels = output_image.load()
    
    offset = kernel_size // 2

    for x in range(width):
        for y in range(height):
            # Initialize accumulators for RGB
            r_total, g_total, b_total = 0, 0, 0
            count = 0

            # Loop through the kernel
            for dx in range(-offset, offset + 1):
                for dy in range(-offset, offset + 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:  # Check bounds
                        r, g, b = pixels[nx, ny]
                        r_total += r
                        g_total += g
                        b_total += b
                        count += 1

            # find average color
            r_avg = r_total // count
            g_avg = g_total // count
            b_avg = b_total // count
            output_pixels[x, y] = (r_avg, g_avg, b_avg)

    return output_image


while (option1 != 1) and (option1 != 2) and (option1 != 3):
    option1 = int(input("Would you like to apply a 3x3 box blur (1) or a 5x5 box blur (2)? "))

    if option1 == 1:
        blurred_image = box_blur(image, kernel_size=3)
        blurred_image.save("box_blur_3x3.jpg")
        name = "box_blur_3x3"
        ishow = blurred_image

    elif option1 == 2:
        blurred_image = box_blur(image, kernel_size=5)
        blurred_image.save("box_blur_5x5.jpg")
        name = "box_blur_5x5"
        ishow = blurred_image

    else:
        print("Value was not an option. Please try again.")

print(f"You can find the image under the name {name}.jpg, and it will open on your computer now...")
ishow.show()
