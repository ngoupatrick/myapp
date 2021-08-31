import streamlit as st
from PIL import Image
import face_recognition
import numpy as np

##### defining functions ####

def load_image(image_file):
    '''
    load single image on web page
    '''
    return Image.open(image_file)

    
def get_encodings(list_images):
    '''
    create the list of encodings data
    '''
    return [face_recognition.face_encodings(face_recognition.load_image_file(image))[0] for image in list_images]
    

def get_distances(encodings, list_images):
    '''
    compute the distance between every elts in list
    '''
    combinaisons = [(im1, im2) for im1 in list_images for im2 in list_images if list_images.index(im1)<list_images.index(im2)]
    result_dict = {}
    for combinaison in combinaisons:
        im1 = combinaison[0]
        im2 = combinaison[1]
        result_dict[im1.name+"_"+im2.name] = np.linalg.norm(encodings[list_images.index(im1)] - encodings[list_images.index(im2)])
    
    return result_dict


def show_images(list_images, component):
    '''
    load images from a list of files
    '''
    for i, image in enumerate(list_images):
        component[i].image(load_image(image), width=200)
    if len(list_images) == 0:
        for i in range(3):
            component[i].text('')

#### end defining functions ####


### Program start #####
@st.cache(allow_output_mutation=True)
def get_static_store():
    """This dictionary is initialized once and can be used to store the files uploaded"""
    return []

def main():
    #init
    st.title("My APP")
    list_of_image_upload = get_static_store()
    # format of file updated
    # UploadedFile(id=1, name='keita.jpg', type='image/jpeg', size=42885)
    img_uploaded = st.file_uploader("Upload three images", type=['png','jpeg', 'jpg'])

    # show file already loaded
    my_slot = st.empty()
    cols = st.beta_columns(3)

    # get loaded files 
    if img_uploaded:    
        list_of_image_upload.append(img_uploaded)  
        show_images(list_of_image_upload, component = cols)

    # if we reach 3 pics, we compare them    
    if len(list_of_image_upload) == 3:
        # debut du calcul de ressemblance
        st.write("ok, we got 3!!! Now we process......")
        st.write(get_distances(get_encodings(list_images=list_of_image_upload), list_images = list_of_image_upload))
        

    # button to clear the list of images
    if st.button("Clear file list"):
        list_of_image_upload.clear()
        show_images(list_of_image_upload, component = cols)
        



if __name__ == '__main__':
    main()    
