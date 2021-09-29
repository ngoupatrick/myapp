import os

PATH_IMG_PROGRESS = "./images/progress_1.gif"

PATH_FOLDER_DATA_MEDIA = "./_dataset_media"
PATH_FOLDER_STATIC_IMG = os.path.join(PATH_FOLDER_DATA_MEDIA, "set_images_statics")
PATH_FOLDER_UPLOAD_IMG = os.path.join(PATH_FOLDER_DATA_MEDIA, "set_images_uploads")
PATH_FOLDER_STATIC_FILE = os.path.join(PATH_FOLDER_DATA_MEDIA, "set_files_statics")
PATH_FOLDER_UPLOAD_FILE = os.path.join(PATH_FOLDER_DATA_MEDIA, "set_files_uploads")

LIST_MENU = ["Home", "Compute distance", "Face Similarity Search", "ML Recommender", "Take a picture", "About"]
LIST_DISTANCE = ['Euclédienne', 'Cosine']
LIST_GRAPH = ['Pyplot', 'Plotly']
TYPE_IMAGE = ['png','jpeg', 'jpg']

TOLERANCE_EUCLEDIENNE = 0.5
TOLERANCE_COSINE = 0.05


TYPE_IMAGE_PATH = "PATH"
TYPE_IMAGE_ARRAY = "ARRAY"
TYPE_IMAGE_UPLOAD = "UPLOAD"

def get_dname():
    _DNAME = dict()
    _DNAME["CHAMP_FULLNAME"] = "tulpe_img_fullname"
    _DNAME["CHAMP_TUPLE_NAME"] = "tuple_img_name"
    _DNAME["CHAMP_DISTANCE_COSINE"] = "distance_cosine"
    _DNAME["CHAMP_DATA"] = "compute_data"
    _DNAME["CHAMP_FACE_COMPARE"] = "face_compare"
    _DNAME["CHAMP_FACE_DISTANCE"] = "face_distance"
    return _DNAME