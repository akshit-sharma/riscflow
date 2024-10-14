
numLines = 0


def get_zeros(num):
    # with max length from numLines, convert num to string with prefix 0s
    return f'{num:0{len(str(numLines))}d}'


def set_numLines(num):
    global numLines
    numLines = num
