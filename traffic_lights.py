def detect_traffic_signals(maze_image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns a list of
    nodes in which traffic signals are present in the image

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `traffic_signals` : [ list ]
            list containing nodes in which traffic signals are present

    Example call:
    ---
    traffic_signals = detect_traffic_signals(maze_image)
    """
    traffic_signals = []
    y = 100
    x = 100
    alpha = "ABCDEFG"
    numb = "1234567"
    str1 = ''
    while y <= 700:
        px = maze_image[y, x]
        if x < 700:
            if px[2] == 255:
                str1 = alpha[x // 100 - 1] + numb[y // 100 - 1]
                traffic_signals.append(str1)
            x += 100
        else:
            if px[2] == 255:
                str1 = alpha[x // 100 - 1] + numb[y // 100 - 1]
                traffic_signals.append(str1)
            x = 100
            y += 100
    return traffic_signals
