from PIL import Image
import findbest
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
from timeit import default_timer as timer
from imageconstruct import *

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
        image.topleft = [anchor.topright[0], anchor.topleft[1] - image.image.height + val[1]]
    if val[2] == 'l':
        image.topleft = [anchor.topleft[0] - image.image.width, anchor.topleft[1] - image.image.height + val[1]]
    if val[2] == 'b':
        image.topleft = [anchor.bottomleft[0] - image.image.width + val[1], anchor.bottomleft[1]]
    if val[2] == 't':
        image.topleft = [anchor.topleft[0] - image.image.width + val[1], anchor.topleft[1] - image.image.height]
    image.UpdatePosition()

class pieceImage:
    def __init__(self, image, anchor=False):
        self.image = Image.open(image)
        self.name = image
        self.id = id(self)

        self.image.top_rgb = GetRangeRgb(self.image, 0, self.image.width, "x", 0) #scrape top
        self.image.bottom_rgb = GetRangeRgb(self.image, 0, self.image.width, "x", self.image.height-1) #scrape bottom

        self.image.left_rgb = GetRangeRgb(self.image, 0, self.image.height, "y", 0) #scrape left
        self.image.right_rgb = GetRangeRgb(self.image, 0, self.image.height, "y", self.image.width-1) #scrape right

        if anchor:
            self.topleft = [int(IMG_WIDTH/2 - self.image.width / 2), int(IMG_HEIGHT/2 - self.image.height / 2)]
            PlacePointOnCanvas(self.topleft)
            self.bottomleft = [self.topleft[0], self.topleft[1] + self.image.height]
            PlacePointOnCanvas(self.bottomleft)
            self.topright = [self.topleft[0] + self.image.width, self.topleft[1]]
            PlacePointOnCanvas(self.topright)
            self.bottomright = [self.topright[0], self.bottomleft[1]]
            PlacePointOnCanvas(self.bottomright)
            TAKEN_POINTS_POLYS.append(Polygon([(self.topleft),(self.bottomleft),(self.topright),(self.bottomright)]))        
        else:
            self.topleft = ["False", "False"]

    def UpdatePosition(self):
            self.bottomleft = [self.topleft[0], self.topleft[1] + self.image.height]
            self.topright = [self.topleft[0] + self.image.width, self.topleft[1]]
            self.bottomright = [self.topright[0], self.bottomleft[1]]
            TAKEN_POINTS_POLYS.append(Polygon([(self.topleft),(self.bottomleft),(self.topright),(self.bottomright)]))
            print("Appending to TAKEN_POINTS_POLYS for",self.name)




one = pieceImage("images/1.png", "anchor")
two = pieceImage("images/2.png")
three = pieceImage("images/3.png")
four = pieceImage("images/4.png")

onetwo = findbest.FindBestAll(one, two)
print(onetwo)
UpdateCoordinatesFromBestSide(one, two, onetwo)

twothree = findbest.FindBestAll(two, three)
UpdateCoordinatesFromBestSide(two, three, twothree)
print(twothree)

threefour = findbest.FindBestAll(three, four)
UpdateCoordinatesFromBestSide(three, four, threefour)
print(threefour)

PlaceOnCanvas(one, True)
PlaceOnCanvas(two, True)
PlaceOnCanvas(three, True)
PlaceOnCanvas(four, True)
start = timer()
CANVAS.save("canvas.png")
elapsed_time = round(timer(), 2)
print("Saving canvas took", elapsed_time, "seconds")