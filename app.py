from flask import Flask, render_template, Response, request, redirect

# import camera driver
from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Video streaming home page."""
    if request.method == 'POST':
        if request.form.get('Play') == 'Play':
            Camera.pause(False)
        elif request.form.get('Pause') == 'Pause':
            Camera.pause(True)
        elif request.form.get('Editor') == 'Editor':
            return redirect('/editor')
        
    return render_template('index.html')


@app.route('/editor', methods=['GET', 'POST'])
def editor():
    if request.method == 'POST':
        if request.form.get('Play') == 'Play':
            Camera.pause(False)
        elif request.form.get('Pause') == 'Pause':
            Camera.pause(True)
        elif request.form.get('Home') == 'Home':
            return redirect('/')
    
    return render_template('editor.html')


def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
