from PIL import Image
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

IMG_HEIGHT = 10000
IMG_WIDTH = 10000
CANVAS = Image.new(mode="RGB", size=(IMG_WIDTH, IMG_HEIGHT))

TAKEN_POINTS_POLYS = []

def PlaceOnCanvas(image):
    CANVAS.paste(image.image, tuple(image.topleft))

def ValidPlacement(origin, width, height):
    for polygon in TAKEN_POINTS_POLYS:
        if polygon.contains(Point(origin[0], origin[1])): return False
        if polygon.contains(Point(origin[0]+width, origin[1])): return False
        if polygon.contains(Point(origin[0], origin[1]+height)): return False
        if polygon.contains(Point(origin[0]+width, origin[1]+height)): return False
    return True

pointImage = Image.open("images/point.png")
pointImageTwo = Image.open("images/point2.png")

def PlacePointOnCanvas(coords, style=1):
    CANVAS.paste(pointImageTwo if style==2 else pointImage, tuple(coords))