from flask import Flask, render_template, Response
import cv2


OPENCV_AVFOUNDATION_SKIP_AUTH=1 
app = Flask(__name__)

# list of camera accesses
cameras = [0,1]


def find_camera(list_id):
    return cameras[int(list_id)]


def gen_frames(camera_id):
    cam = find_camera(camera_id)  
    # cam = cameras[int(id)]
    cap = cv2.VideoCapture(cam)  # 

    while True:

        # # Capture frame-by-frame. Return boolean(True=frame read correctly. )
        success, frame = cap.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  


@app.route('/video_feed/<string:list_id>/', methods=["GET"])
def video_feed(list_id):
    return Response(gen_frames(list_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html', camera_list=len(cameras), camera=cameras)


if __name__ == '__main__':
    app.run()