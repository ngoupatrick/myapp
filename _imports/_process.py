import os, glob
import face_recognition

from _imports._config import *
from _imports._distance import *

#init
_DNAME = get_dname()

#check the images
def check_images_loaded(img_path, type_image = TYPE_IMAGE_PATH):
    if type_image == TYPE_IMAGE_PATH:
        return os.path.isfile(img_path)
    if type_image == TYPE_IMAGE_UPLOAD:
        return True

#check if the folder (database images) exist
def check_folder_images(folder_path = PATH_FOLDER_STATIC_IMG):
    return os.path.isdir(folder_path)

#get the folder (database images) files
def get_files_database(folder_path = PATH_FOLDER_STATIC_IMG):
    return glob.glob(os.path.join(folder_path,'*g'))

#get the number of faces on images loaded
def get_number_faces(img_path):
    return len(face_recognition.face_locations(face_recognition.load_image_file(img_path)))

#get the encodings of faces
#https://medium.com/codex/face-recognition-25f7421a2268
#`face_recognition.face_encodings` generate a face encoding vector of 128 values
#the algorithm notes certain important measurements on the face
# — like the color and size and slant of eyes, the gap between eyebrows, etc. 
# All these put together define the face encoding 
# — the information obtained out of the image — that is used to identify the particular face.
def get_img_encoding(img_path):
    """
    you must be sure that the image contains at least one face.
    this method return a list of encoding faces on image.
    use [0] for the first
    """
    return face_recognition.face_encodings(face_recognition.load_image_file(img_path))

#get all the encodings faces in a list of files
def get_all_encodings_face_database(file_list):
    return [face for file in file_list for face in get_img_encoding(img_path = file)]

# compute data and get back the distance
# We do this for one face on image loaded
# !IMPORTANT: il faut verifier plutard que la liste des embeding match la liste des fichiers
def compute_data(img_path, file_list, emb_face, emb_folder, tolerance = TOLERANCE_EUCLEDIENNE, DNAME = _DNAME, type_image = TYPE_IMAGE_PATH):
    dict_compare = {}
    dict_inter = {}
    for i, file in enumerate(file_list):
        temp_dict = {}
        #print("ICI")#breakpoint()
        name_img = img_path
        if type_image == TYPE_IMAGE_UPLOAD:
            name_img = img_path.name        
        
        temp_dict[DNAME["CHAMP_FULLNAME"]] = (name_img, file)
        temp_dict[DNAME["CHAMP_TUPLE_NAME"]] = (os.path.basename(name_img), os.path.basename(file))
        temp_dict[DNAME["CHAMP_DISTANCE_COSINE"]] = distances_cosine(emb_face, emb_folder[i])
        dict_inter[i] = temp_dict
    dict_compare[DNAME["CHAMP_DATA"]] = dict_inter
    dict_compare[DNAME["CHAMP_FACE_COMPARE"]] = face_recognition.compare_faces(emb_face, emb_folder, tolerance=tolerance)
    dict_compare[DNAME["CHAMP_FACE_DISTANCE"]] = face_recognition.face_distance(emb_face, emb_folder)#eucledian distance
    return dict_compare

# Now we process for all faces on image
# !IMPORTANT: il faut verifier plutard que la liste des embeding match la liste des fichiers
def compute_all_data(img_path, folder_path, tolerance = TOLERANCE_EUCLEDIENNE, DNAME = _DNAME, type_image = TYPE_IMAGE_PATH):
    #check the path or images given
    if not check_images_loaded(img_path=img_path, type_image=type_image): return {} 
    if not check_folder_images(folder_path=folder_path): return{}    
    #get info on folder and images
    file_list = get_files_database(folder_path=folder_path)
    nb_faces_on_image = get_number_faces(img_path=img_path)
    #count the number of faces on image
    if nb_faces_on_image == 0: return{}
    #get encodings
    emb_folder = get_all_encodings_face_database(file_list=file_list)
    emb_faces = get_img_encoding(img_path=img_path)
    #return the computation for each faces on image
    return [compute_data(img_path=img_path, file_list=file_list, emb_face=emb_faces[i], emb_folder=emb_folder, type_image=type_image) for i in range(nb_faces_on_image)]