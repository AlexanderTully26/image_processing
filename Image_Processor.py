from PIL import Image
import random

tool_selection = 0
option1 = 0
quesionf = 0
name = "Nothing"
filterlistnum = 0
namenum = 0


#image = Image.open("/Users/alexander.tully26/Downloads/AirCarTest.jpg")

image = Image.open("/Users/alexander.tully26/Downloads/Screen Shot Jan 8 2025 from PNG to JPG.jpg") #Change Image here

filterlist = [image]

def grayscale(image): 
    """Basic Equal Balance"""
    pixels = image.load()
    width, height = image.size
 
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            gray = int((r + g + b)/3)
            pixels[x, y] = (gray, gray, gray)
    return image


def grayscaleVTwo(image):
    """Weight"""
    pixels = image.load()
    width, height = image.size
 
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            gray = int((r + g)/3+r)
            pixels[x, y] = (gray, gray, gray)
    return image

def grayscaleVThree(image):
    """only green channel values"""
    pixels = image.load()
    width, height = image.size
 
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            gray = r
            pixels[x, y] = (gray, gray, gray)

    return image

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


#while (tool_selection != 1) and (tool_selection != 2) and (tool_selection != 3):
while tool_selection not in [1, 2, 3, 4, 5, 6]:
    print("Which tool would you like to use?")
    tool_selection = int(input("Grayscale (1), Blurring (2), Dithering (3), Sharpening (4), Smoothing (5), Laplacian (6)? "))

    if tool_selection == 1: #GrayScale
        option1 = int(input("Whould you like to use basic grayscale (1), Decomposition grayscale (2) or only green channel values (3)?"))
        
        if option1 == 1: 
            grayscale_basic_image = grayscale(image)
            grayscale_basic_image.save("grayscale_basic_image.jpg")
        # print("You can find the image under the name ")
            name = "grayscale_basic_image"
            ishow = grayscale_basic_image

        elif option1 == 2:
            Decomposition_grayscale_image = grayscaleVTwo(image)
            Decomposition_grayscale_image.save("Weight_grayscale_image.jpg")
    #     print("You can find the image under the name Weight_grayscale")
            name = "Decomposition_grayscale_image"
            ishow = Decomposition_grayscale_image

        elif option1 == 3:
            green_channel_grayscale_image = grayscaleVThree(image)
            green_channel_grayscale_image.save("green_channel_grayscale_image.jpg")
            name = "green_channel_grayscale_image"
            ishow = green_channel_grayscale_image

    elif tool_selection == 2: # Blurring
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

    elif tool_selection == 3: # Dithering 
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

    elif tool_selection == 4: #Sharpening 
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

    elif tool_selection == 5: #Smoothing
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

    elif tool_selection == 6: #laplacian
        laplacian_image = laplacian_filter(image.copy())
        laplacian_image.save("laplacian_filter.jpg")
        name = "laplacian_filter"
        ishow = laplacian_image

    else:
        print("Value was not an option try again")

    print("Making Image...")
    print("It will show photo but return to console to continue.")
    filterlist.append(ishow)
    filterlistnum += 1
    print("You can find the image under the name", name + str(namenum) + ".jpg, and it will open on your computer now...")
    ishow.show()

    while quesionf == 0:
        quesionf = int(input("Would you like to do finnish editing the image(1), add another filter (2), or undo the last filter (3)"))
        
        if quesionf == 2: 
            tool_selection = 0
            image = ishow
            namenum = random.randint(2, 1000)     

        elif quesionf == 1:
            tool_selection = 1

        elif quesionf == 3: 
            if filterlistnum == 0:
                print("Can not be undone, choose a diferent option")
            else: 
                tool_selection = 0
                filterlist.pop(filterlistnum)
                filterlistnum -= 1
                image = filterlist[filterlistnum]
                image.show()
                print("(May not look undone but it is)")
                
            quesionf = 0
            
          
           
    quesionf = 0    

            
    

print("You can find your final image under the name", name + str(namenum) + ".jpg, and it will open on your computer now...")
print("Thank You")
ishow.show()
