import cv2
import time
from copy import copy

def kill_video(st, key = "_video"):
    _video = st.session_state.get(key)
    if _video: 
        _video.release()
        cv2.destroyAllWindows()
        _video = None
        del st.session_state[key]

def process_take_picture(btn_start, btn_stop, btn_take, btn_clear , image_placeholder, place_pict_take, st, forms):
    stop_video = False
    video = None
    
    last_image = None
    
    if btn_start: 
        if st.session_state.get("_video"): 
            kill_video(st)
        
        stop_video = False            
            
        video = cv2.VideoCapture(0)
        video.set(cv2.CAP_PROP_FPS, 25)
        st.session_state["_video"] = video
            
        if not video.isOpened(): return 
        
        take = False
            
        while True:
            # Capture frame-by-frame
            success, image = video.read()
            if not success:
                break
            # Display the resulting frame                
            st.session_state["last_img"] = image.copy()                
            image_placeholder.image(image, channels="BGR") 
            
            time.sleep(0.05)
                    
    if btn_stop:
        kill_video(st = st)
        stop_video = True        
    
    if btn_take:
        try: 
            last_image = copy(st.session_state.get("last_img"))
            place_pict_take.image(last_image, channels = "BGR")
        except:
            return      
        
        
    if btn_clear:
        #breakpoint()
        place_pict_take.empty() 
        last_image = None
        try: del st.session_state["last_img"]
        except: return
        
        
    return last_image