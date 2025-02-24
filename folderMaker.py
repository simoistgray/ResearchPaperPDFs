import os

frontpath = '/pdfFolder/'
i = 32
while i > 4:
    j = 6
    os.makedirs(frontpath + "Volume " + str(i))
    while j > 0:
        os.makedirs(frontpath + "Volume " + str(i) + "/Issue " + str(j))
        j -= 1
    i -= 1
