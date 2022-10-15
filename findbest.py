import numpy as np
import matplotlib.pyplot as plt

SIMILARITY = 20 
# SIMILARITY controls how close RGB values need to be with eachother to be recognized as "similar."
# for all X(r1, g1, b1) and Y(r2, g2, b2), X and Y are only similar if:
# |r1 - r2| < SIMILARITY and |g1 - g2| < SIMILARITY and |b1 - b2| < SIMILARITY
# thus, the higher SIMILARITY is, the more generous it will be to say that two pixels are "similar".
NOT_SIMILAR_PENALTY = 0.99
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

def FindBestMatch(image1, image2):

    total_slide_distance = len(image1) + len(image2)
    buffer = [False]*len(image2)
    image1 = buffer + image1 + buffer
    similarity_max = [0,0]
    similarity_history = []

    i = 0

    while i < total_slide_distance:
        
        similarity_score_temp = SimilarityOfRange(image1[i:i+len(image2)], image2)
        similarity_history.append(similarity_score_temp)


        if similarity_score_temp > similarity_max[0]:
            similarity_max[0] = similarity_score_temp
            similarity_max[1] = i

        i += 1

    #x = np.arange(0,i)
    #y = similarity_history
    #plt.title("Line graph")
    #plt.xlabel("simval")
    #plt.ylabel("i")
    #plt.plot(x, y, color ="red")
    #plt.show()


    return similarity_max
    
def FindBestAll(image1, image2):
    best = [0,0,"x"]

    r1_l2 = FindBestMatch(image1.image.right_rgb, image2.image.left_rgb)
    best = r1_l2+["r"] if r1_l2[0] > best[0] else best
    l1_r2 = FindBestMatch(image1.image.left_rgb, image2.image.right_rgb)
    best = l1_r2+["l"] if l1_r2[0] > best[0] else best
    t1_b2 = FindBestMatch(image1.image.top_rgb, image2.image.bottom_rgb)
    best = t1_b2+["t"] if t1_b2[0] > best[0] else best
    b1_t2 = FindBestMatch(image1.image.bottom_rgb, image2.image.top_rgb)
    best = b1_t2+["b"] if b1_t2[0] > best[0] else best

    return best

    
