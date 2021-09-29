import streamlit as st
#from streamlit import caching (#caching.clear_cache())
from PIL import Image
import face_recognition
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt
import plotly.graph_objects as go

import cv2
import time

from _imports._config import *
from _imports._same_components import *
from _imports._process import *
from _imports._take_picture import *

import os
import glob

plt.style.use("ggplot")

##### defining functions ####

def load_image(image_file, size = (225, 225)):
    '''
    load single image on web page
    '''  
    return Image.open(image_file).resize(size, Image.ANTIALIAS)

def show_images(list_images, component, clean = False, nb_images = 3):
    '''
    load images from a list of files
    ''' 
    if clean:
        for compon in component:#clean component
            compon.text('')
        list_images.clear()#clean images lists        
    else:
        for i, image in enumerate(list_images):
            if i < nb_images:
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
            
            result_dict[im1.name+"_"+im2.name] = {
                "im1": im1.name,
                "im2": im2.name,
                "distance": dist(
                    im_enc1=encodings[list_images.index(im1)],
                    im_enc2=encodings[list_images.index(im2)]
                )
            }                       
    
    return result_dict

def which_plot(ch_plot = 'Pyplot'):
    if ch_plot == "Pyplot":
        return pyplot_result
    if ch_plot == "Plotly":
        return plotly_result
    return None

def compute_distance(list_images, ch_dist, ch_plot, component, nb_images):
    # show progress anime
    im = component.image(PATH_IMG_PROGRESS) 
    # if we reach a number of pics, we compare them 
    if len(list_images) == nb_images:
        # debut du calcul de ressemblance
        result = get_distances(get_encodings(list_images=list_images), list_images = list_images, ch_dist = ch_dist)
        #write result
        c_col = component.columns(2)
        c_col[0].write(result)
        #plot result
        f_plot = which_plot(ch_plot=ch_plot)
        f_plot(result=result, ch_dist=ch_dist, component=c_col[1])
    #clean image progress
    im.empty()


def pyplot_result(result, ch_dist, component):
    x = [cle for cle in result.keys()]
    y = [valeur["distance"] for valeur in result.values()]
    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.set_xticklabels(labels = x, rotation=45, ha='right')
    component.pyplot(fig)  
    
def plotly_result(result, ch_dist, component):
    x = [cle for cle in result.keys()]
    y = [valeur["distance"] for valeur in result.values()]
    fig = go.Figure(data=go.Bar(x=x, y=y))
    fig.update_layout(title = f'')
    component.plotly_chart(fig )
    
         
# button to clear the list of images
def clean_space(list_images, component, nb_images):
    show_images(list_images, component = component, clean=True, nb_images = nb_images)    
    
#### end defining functions ####


### Program start #####
@st.cache(allow_output_mutation=True)
def get_static_store():
    """This dictionary is initialized once and can be used to store the files uploaded"""
    return []

def main():
    #init
    st.title("My APP")
    
    #*******sidebar********#
    sidebar = st.sidebar
    #navigation 
    rad_menu = cmp_choose_menu(component=sidebar)
    sidebar.markdown("---")
    
    
    if rad_menu == "Compute distance":
            
        #choose a distance
        choix_distance = cmp_choose_dist(component = sidebar)
        #choose a number of pic to compare
        number_pic = cmp_choose_number(component = sidebar)
        #choose style graph
        choix_plot = cmp_choose_graph(component=sidebar) 
        #*******end of sidebar******#
        
        list_of_image_upload = get_static_store()
        
        # format of file updated
        # UploadedFile(id=1, name='keita.jpg', type='image/jpeg', size=42885)
        # options for multiple files: "accept_multiple_files=True"
        img_uploaded = st.file_uploader("Upload three images", type=TYPE_IMAGE)

        # show file already loaded
        cols = st.columns(int(number_pic))  
        
        # get loaded files 
        if img_uploaded and len(list_of_image_upload)<int(number_pic):
            list_of_image_upload.append(img_uploaded)
            show_images(list_of_image_upload, component = cols, nb_images = int(number_pic))           
            
        # show file already loaded
        cols_btn = st.columns(2)
        #empty space for result
        my_slot_ = st.container()
        my_slot_.write("")  
        #adding button
        cols_btn[0].button(label = "Compute", on_click = compute_distance, args = [list_of_image_upload, choix_distance, choix_plot, my_slot_, int(number_pic)])
        cols_btn[1].button(label = "Clear file list", on_click = clean_space, args = [list_of_image_upload, cols, int(number_pic)])
    if rad_menu == "Home":
        st.write("Home")
    if rad_menu == "ML Recommender":
        st.write("ML Recommender")
    if rad_menu == "About":
        st.write("About")
            
    if rad_menu == "Face Similarity Search":
        #choose a distance
        choix_distance = cmp_choose_dist(component = sidebar)
        #choose a number of pic to compare
        number_pic = cmp_choose_number(component = sidebar, title="How many best pics similarity")
        #choose style graph
        choix_plot = cmp_choose_graph(component=sidebar)
        #ADD
        st.markdown("Were Are going to <ins>match</ins> yours pictures with our databases pictures", unsafe_allow_html = True)
        #st.write("Were Are going to match yours pictures with our databases pictures")
        with st.expander(label = "Options"):
            _img_uploaded = None            
            
            st.markdown(f"**<ins>Data Folder:</ins>** <i>{PATH_FOLDER_STATIC_IMG}</i>", unsafe_allow_html = True)
            save_pic = st.checkbox(label = "Add my picture to your database", value = True)
            
            rd_choice = ['Upload', 'Take a Picture']
            rd_val = st.radio('choix', rd_choice)
            
            pict_cols_btn = st.columns(4)
            vid_place_col = st.columns(2)
            vid_place = vid_place_col[0].empty()
            #st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            if rd_val == 'Upload':
                _img_uploaded = st.file_uploader("Upload an image", type=TYPE_IMAGE, key = "img_compare")
            if rd_val == 'Take a Picture':
                _img_uploaded = None
                btns = cmp_btn_pic(pict_cols_btn)
                process_take_picture(btn_start=btns[0], btn_stop=btns[1], btn_take = btns[2], btn_clear=btns[3], image_placeholder=vid_place, place_pict_take=vid_place_col[1], st=st)
            
        if _img_uploaded:
            resultat = compute_all_data(img_path=_img_uploaded, folder_path=PATH_FOLDER_STATIC_IMG, type_image=TYPE_IMAGE_UPLOAD)
            st.write(resultat)
        
    if rad_menu == "Take a picture":
        
        st.write("Take a picture")
        forms = st.form('Forms')
        with forms:
            col1, col2, col3, col4 = st.columns(4)
            btn_start = col1.form_submit_button("Start")
            btn_stop = col2.form_submit_button("Stop")
            btn_take = col3.form_submit_button("Take Picture")
            btn_clear = col4.form_submit_button("Clear Picture")
            
            _vid_place_1, _vid_place_2 = st.columns(2)
            image_placeholder = _vid_place_1.empty()
            place_pict = _vid_place_2.empty()
        
        process_take_picture(btn_start=btn_start,
                             btn_stop=btn_stop,
                             btn_take = btn_take,
                             btn_clear=btn_clear,
                             image_placeholder=image_placeholder,
                             place_pict_take=place_pict,
                             st=st,
                             forms=forms
        ) 
         
        


#Main program
if __name__ == '__main__':
    main()    
