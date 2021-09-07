import streamlit as st
#from streamlit import caching
from PIL import Image
import face_recognition
import numpy as np
from scipy.spatial import distance
#import copy

##### defining functions ####

def load_image(image_file):
    '''
    load single image on web page
    '''  
    return Image.open(image_file).resize((225, 225), Image.ANTIALIAS)

def show_images(list_images, component, clean = False):
    '''
    load images from a list of files
    ''' 
    if clean:
        for compon in component:#clean component
            compon.text('')
        list_images.clear()#clean images lists
        #caching.clear_cache()#clean cache
    else:
        for i, image in enumerate(list_images):
            if i < 3:
                component[i].image(load_image(image), width=200) 
   

    
def get_encodings(list_images):
    '''
    create the list of encodings data
    '''
    return [face_recognition.face_encodings(face_recognition.load_image_file(image))[0] for image in list_images]

def distances_eucledienne(im_enc1, im_enc2):
    return distance.euclidean(im_enc1, im_enc2)

def distances_cosine(im_enc1, im_enc2):
    return distance.cosine(im_enc1, im_enc2)

def which_distance(ch_dist = 'Euclédienne'):
    '''
    return a callback distance to use
    <ch_dist>
    Cosine = "Eucledian distance"
    cos = "Cosine distance"
    '''
    if ch_dist == "Euclédienne":
        return distances_eucledienne
    if ch_dist == "Cosine":
        return distances_cosine
    return None

def get_distances(encodings, list_images, ch_dist = 'Euclédienne'):
    '''
    compute the distance between every elts in list
    <ch_dist>
    euc = "Euclédienne"
    cos = "Cosine"
    '''
    combinaisons = [(im1, im2) for im1 in list_images for im2 in list_images if list_images.index(im1)<list_images.index(im2)]
    result_dict = {}
    for combinaison in combinaisons:
        im1 = combinaison[0]
        im2 = combinaison[1]
        
        dist = which_distance(ch_dist)
        if dist != None:            
            result_dict[im1.name+"_"+im2.name] =  dist(
                im_enc1=encodings[list_images.index(im1)],
                im_enc2=encodings[list_images.index(im2)]
            )            
    
    return result_dict

def compute_distance(list_images, ch_dist, component):
    # if we reach 3 pics, we compare them    
    if len(list_images) == 3:
        # debut du calcul de ressemblance  
        component.write("ok, we got 3!!! Now we process......")
        component.write(get_distances(get_encodings(list_images=list_images), list_images = list_images, ch_dist = ch_dist))
        
# button to clear the list of images
def clean_space(list_images, component):
    show_images(list_images, component = component, clean=True)    
    
#### end defining functions ####


### Program start #####
@st.cache(allow_output_mutation=True)
def get_static_store():
    """This dictionary is initialized once and can be used to store the files uploaded"""
    return []

def main():
    #init
    st.title("My APP")
    
    #empty space
    my_slot = st.empty()
    
    #choose a distance
    list_distance = ['Euclédienne', 'Cosine']
    choix_distance = st.radio("Choose a Distance", list_distance)
    #my_slot.write(choix_distance)
    list_of_image_upload = get_static_store()
    
    # format of file updated
    # UploadedFile(id=1, name='keita.jpg', type='image/jpeg', size=42885)
    img_uploaded = st.file_uploader("Upload three images", type=['png','jpeg', 'jpg'])

    # show file already loaded
    cols = st.columns(3)    
    
    # get loaded files 
    if img_uploaded and len(list_of_image_upload)<3:    
        list_of_image_upload.append(img_uploaded)
        show_images(list_of_image_upload, component = cols)            
        
    # show file already loaded
    cols_btn = st.columns(2)
    #empty space for result
    my_slot_ = st.columns(1)
    #adding button
    cols_btn[0].button(label = "Compute", on_click = compute_distance, args = [list_of_image_upload, choix_distance, my_slot_[0]])
    cols_btn[1].button(label = "Clear file list", on_click = clean_space, args = [list_of_image_upload, cols])
            
        


#Main program
if __name__ == '__main__':
    main()    
