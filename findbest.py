import numpy as np
import matplotlib.pyplot as plt
import imageconstruct

SIMILARITY = 20 
# SIMILARITY controls how close RGB values need to be with eachother to be recognized as "similar."
# for all X(r1, g1, b1) and Y(r2, g2, b2), X and Y are only similar if:
# |r1 - r2| < SIMILARITY and |g1 - g2| < SIMILARITY and |b1 - b2| < SIMILARITY
# thus, the higher SIMILARITY is, the more generous it will be to say that two pixels are "similar".
NOT_SIMILAR_PENALTY = 0.999
# if two pairs of pixels are not similar at all, decrease score
SIMILAR_BONUS = 10
# if two pairs of pixels are similar, increase score by 5
EXACT_BONUS = 50
# if two pairs of pixels are the same, increase score by 50

def SimilarityOfRange(range1, range2):
    similarity_score = 0
    if (not len(range1) == len(range2)):
        print("These two ranges are not of the same length. (", len(range1), len(range2), ")")
    elif len(range1) == 0:
        print("These ranges are of length 0.")
    else: 
        for i in (j for j in range(len(range1)) if range1[j] != False):
            if abs(range1[i][0] - range2[i][0]) < SIMILARITY and abs(range1[i][1] - range2[i][1]) < SIMILARITY and abs(range1[i][2] - range2[i][2]) < SIMILARITY:
                similarity_score += SIMILAR_BONUS
            elif range1[i] == range2[i]:
                similarity_score += EXACT_BONUS
            else:
                similarity_score *= NOT_SIMILAR_PENALTY
    return similarity_score/(len(range1)+1)

def FindBestMatch(image1, image2, currentSide, anchorImg, placeImg, debug=False):

    total_slide_distance = len(image1) + len(image2)
    buffer = [False]*len(image2)
    image1 = buffer + image1 + buffer
    similarity_max = [0,0]
    similarity_history = []



    i = 0

    while i < total_slide_distance:

        tempTopLeft = 0
        if currentSide == 'r':
            tempTopLeft = [anchorImg.topright[0], (anchorImg.topright[1] - placeImg.image.height) + i]
        if currentSide == 'l':
            tempTopLeft = [anchorImg.topleft[0] - placeImg.image.width, anchorImg.topleft[1] - placeImg.image.height + i]
        if currentSide == 'b':
            tempTopLeft = [anchorImg.bottomleft[0] - placeImg.image.width + i, anchorImg.bottomleft[1]]
        if currentSide == 't':
            tempTopLeft = [anchorImg.topleft[0] - placeImg.image.width + i, anchorImg.topleft[1] - placeImg.image.height]

        if debug:
            if not imageconstruct.ValidPlacement(tempTopLeft, placeImg.image.width, placeImg.image.height):
                print("invalid placement", currentSide)
                print(tempTopLeft,"is temptopleft")
                imageconstruct.PlacePointOnCanvas(tempTopLeft)
            else:
                imageconstruct.PlacePointOnCanvas(tempTopLeft, 2)
                pass
        
        similarity_score_temp = SimilarityOfRange(image1[i:i+len(image2)], image2)
        similarity_history.append(similarity_score_temp)

        if similarity_score_temp > similarity_max[0]:
            similarity_max[0] = similarity_score_temp
            similarity_max[1] = i

        i += 1

    if debug:
        title = "Line graph for "+currentSide+" side of "+anchorImg.name
        x = np.arange(0,i)
        y = similarity_history
        plt.title(title)
        plt.xlabel("simval")
        plt.ylabel("i")
        plt.plot(x, y, color ="red")
        plt.show()


    return similarity_max
    
def FindBestAll(image1, image2, debug=False):
    best = [0,0,"x"]

    r1_l2 = FindBestMatch(image1.image.right_rgb, image2.image.left_rgb, "r", image1, image2, debug)
    best = r1_l2+["r"] if r1_l2[0] > best[0] else best
    l1_r2 = FindBestMatch(image1.image.left_rgb, image2.image.right_rgb, "l", image1, image2, debug)
    best = l1_r2+["l"] if l1_r2[0] > best[0] else best
    t1_b2 = FindBestMatch(image1.image.top_rgb, image2.image.bottom_rgb, "t", image1, image2, debug)
    best = t1_b2+["t"] if t1_b2[0] > best[0] else best
    b1_t2 = FindBestMatch(image1.image.bottom_rgb, image2.image.top_rgb, "b", image1, image2, debug)
    best = b1_t2+["b"] if b1_t2[0] > best[0] else best

    return best

    
