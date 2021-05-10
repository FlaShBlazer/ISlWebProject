import pyrebase
from flask import *
from camera import VideoCamera

app = Flask(__name__)

config = {
    "apiKey": "AIzaSyDw5dt6V617QwA9ynrFfIARwWoaMi3OgQw",
    "authDomain": "isl-knpy.firebaseapp.com",
    "databaseURL": "https://isl-knpy-default-rtdb.firebaseio.com",
    "projectId": "isl-knpy",
    "storageBucket": "isl-knpy.appspot.com",
    "messagingSenderId": "495796655147"
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()


@app.route('/', methods=['GET', 'POST'])
def basic():
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        # noinspection PyBroadException
        try:
            auth.sign_in_with_email_and_password(email, password)
            print("Success!")
            return render_template('home.html')
        except:
            return render_template('new.html')

    return render_template('new.html')


def gen(vcamera):
    while True:
        data = vcamera.get_frame()
        frame = data[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run()
