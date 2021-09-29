from scipy.spatial import distance



def distances_cosine(im_enc1, im_enc2):
    return distance.cosine(im_enc1, im_enc2)