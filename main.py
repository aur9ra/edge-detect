from PIL import Image, ImageDraw, ImageFilter
import findbest
from timeit import default_timer as timer

IMG_HEIGHT = 10000
IMG_WIDTH = 10000
CANVAS = Image.new(mode="RGB", size=(IMG_WIDTH, IMG_HEIGHT))

def GetRangeRgb(image, pxfrom, pxto, axis, stable):
    temp = []



    if axis == "x":
        for i in (range (pxfrom, pxto)):
            temp.append(image.getpixel((i, stable)))
    elif axis == "y":
        for i in (range (pxfrom, pxto)):
            if i == image.height:
                print(pxto)
                print(i)
            temp.append(image.getpixel((stable, i)))
    return temp

def UpdateCoordinatesFromBestSide(anchor, image, val):
    if val[2] == 'r':
        image.topleft = [anchor.topright[0], (anchor.topright[1] - image.image.height) + val[1]]
    if val[2] == 'l':
        image.topleft = [anchor.topleft[0] - image.image.width, anchor.topleft[1] - image.image.height + val[1]]
    if val[2] == 'b':
        image.topleft = [anchor.bottomleft[0] - image.image.width + val[1], anchor.bottomleft[1]]
    if val[2] == 't':
        image.topleft = [anchor.topleft[0] - image.image.width + val[1], anchor.topleft[1]]


def PlaceOnCanvas(image):
    CANVAS.paste(image.image, tuple(image.topleft))





class pieceImage:
    def __init__(self, image, anchor=False):
        self.image = Image.open(image)

        self.image.top_rgb = GetRangeRgb(self.image, 0, self.image.width, "x", 0) #scrape top
        self.image.bottom_rgb = GetRangeRgb(self.image, 0, self.image.width, "x", self.image.height-1) #scrape bottom

        self.image.left_rgb = GetRangeRgb(self.image, 0, self.image.height, "y", 0) #scrape left
        self.image.right_rgb = GetRangeRgb(self.image, 0, self.image.height, "y", self.image.width-1) #scrape right

        if anchor:
            self.topleft = [int(IMG_WIDTH/2 - self.image.width / 2), int(IMG_HEIGHT/2 - self.image.height / 2)]
            self.bottomleft = [self.topleft[0], self.topleft[1] + self.image.height]
            self.topright = [self.topleft[0] + self.image.width, self.topleft[1]]
            self.bottomright = [self.topright[0], self.bottomleft[1]]
        else:
            self.topleft = ["False", "False"]

    def UpdatePosition(self):
            self.bottomleft = [self.topleft[0], self.topleft[0] + self.image.height]
            self.topright = [self.topleft[0] + self.image.width, self.topleft[0]]
            self.bottomright = [self.topright[0], self.bottomleft[1]]


start = timer()

one = pieceImage("images/1.png", "anchor")
two = pieceImage("images/2.png")

onetwo = findbest.FindBestAll(one, two)



elapsed_time = round(timer(), 2)
print("Matching and initialization of both images took", elapsed_time, "seconds")


print(onetwo)

UpdateCoordinatesFromBestSide(one, two, onetwo)
two.UpdatePosition()


PlaceOnCanvas(one)
PlaceOnCanvas(two)
CANVAS.save("canvas.png")