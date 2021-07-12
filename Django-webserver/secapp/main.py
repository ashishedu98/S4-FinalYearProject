# from .models import Face_detects
from views import save_recognised_face
from KNN import *

if __name__ == "__main__":
    while True:
        time.sleep(5)
        print("started")
        live_image=get_live_image()
        if (detect_faces(live_image)):
            save_recognised_face(live_image)
            # f = Face_detects(face_img=live_image)
            # f.save()
            print("saved")
        else:
            print("no faces")
            continue