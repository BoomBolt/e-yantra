def detect_vertical_roads_under_construction(maze_image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns a list
    containing the missing vertical links

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `vertical_roads_under_construction` : [ list ]
            list containing missing vertical links

    Example call:
    ---
    vertical_roads_under_construction = detect_vertical_roads_under_construction(maze_image)
    """
    vertical_roads_under_construction = []

    y = 150
    x = 100
    alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    numb = [1, 2, 3, 4, 5, 6, 7]
    str1 = ''
    while y < 700:
        px = maze_image[y, x]
        if x < 700:
            if px[0] == 255:
                str1 = alpha[x // 100 - 1] + str(numb[y // 100 - 1]) + '-' + alpha[x // 100 - 1] + str(numb[y // 100])
                vertical_roads_under_construction.append(str1)
            x += 100
        else:
            if px[0] == 255:
                str1 = alpha[x // 100 - 1] + str(numb[y // 100 - 1]) + '-' + alpha[x // 100 - 1] + str(numb[y // 100])
                vertical_roads_under_construction.append(str1)
            x = 100
            y += 100

    return vertical_roads_under_construction


