import keras
from keras.preprocessing.image import img_to_array
from skinSegmentation_RealtimePredictions import *

class_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
model = keras.models.load_model(r"C:\Users\flash\PycharmProjects\ISlProject\Numbers_dataset_segment.h5")


def classify(image):
    image = cv2.resize(image, (128, 128))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    proba = model.predict(image)
    idx = np.argmax(proba)
    return class_names[idx]


class VideoCamera(object):
    def __init__(self):
        self.stream = cv2.VideoCapture(0)

    def get_frame(self):
        ret, image = self.stream.read()
        image = cv2.flip(image, 1)
        top, right, bottom, left = 100, 250, 400, 550
        roi = image[top:bottom, right:left]
        gray = extractSkin(roi)
        cv2.imshow('gray', gray)
        predictions = classify(gray)
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(image, predictions, (0, 130), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 2)
        ret, jpeg = cv2.imencode('.jpg', image)
        data = [jpeg.tobytes(), predictions]
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            self.stream.release()
            cv2.destroyAllWindows()
        return data
