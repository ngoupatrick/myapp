import streamlit as st
#from streamlit import caching (#caching.clear_cache())
from PIL import Image
import face_recognition
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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
            result_dict[im1.name+"_"+im2.name] =  dist(
                im_enc1=encodings[list_images.index(im1)],
                im_enc2=encodings[list_images.index(im2)]
            )            
    
    return result_dict

def which_plot(ch_plot = 'Pyplot'):
    if ch_plot == "Pyplot":
        return pyplot_result
    if ch_plot == "Plotly":
        return plotly_result
    return None

def compute_distance(list_images, ch_dist, ch_plot, component, nb_images):
    # show progress anime
    im = component.image("./images/progress_1.gif") 
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
    y = [valeur for valeur in result.values()]
    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.set_xticklabels(labels = x, rotation=45, ha='right')
    component.pyplot(fig)  
    
def plotly_result(result, ch_dist, component):
    x = [cle for cle in result.keys()]
    y = [valeur for valeur in result.values()]
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
    list_menu = ["Home", "Compute distance", "ML Recommender", "About"]
    rad_menu = sidebar.radio("Navigation: ", list_menu)
    if rad_menu == "Compute distance":
            
        #choose a distance
        list_distance = ['Euclédienne', 'Cosine']
        choix_distance = sidebar.radio("Choose a Distance", list_distance, key = "choix_distance")
        #choose a number of pic to compare
        number_pic = sidebar.number_input(
            label = "How many pics to compare",
            min_value = 2,
            max_value = 5,
            value = 3,
            step = 1
        )
        #choose style graph
        list_plot = ['Pyplot', 'Plotly']
        choix_plot = sidebar.radio("Choose a plot style", list_plot, key = "choix_plot")
        
        
        #*******end of sidebar******#
        
        list_of_image_upload = get_static_store()
        
        # format of file updated
        # UploadedFile(id=1, name='keita.jpg', type='image/jpeg', size=42885)
        img_uploaded = st.file_uploader("Upload three images", type=['png','jpeg', 'jpg'])

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
        


#Main program
if __name__ == '__main__':
    main()    
