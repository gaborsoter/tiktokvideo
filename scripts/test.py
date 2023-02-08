def calculate_font_size(value):
    # min and max font size
    leftMin = 0
    leftMax = 15

    # min and max character length
    rightMin = 30
    rightMax = 15

    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))

print(calculate_font_size(5))