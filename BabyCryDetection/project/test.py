import cv2
import numpy as np
import pyaudio
import numpy as np
import librosa
import soundfile as sf
import os
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import threading


# Load the Haar Cascade for face detection
def main():
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    # Start video capture from the webcam
    cap = cv2.VideoCapture(0)

    # Initialize tracker
    tracker = cv2.TrackerKCF_create()
    initBB = None
    tracking = False

    # Define a designated area that covers the full frame
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    boundary_scale = 0.8
    boundary_width = int(frame_width * boundary_scale)
    boundary_height = int(frame_height * boundary_scale)
    boundary_x = (frame_width - boundary_width) // 2
    boundary_y = (frame_height - boundary_height) // 2
    center_area = (boundary_x, boundary_y, boundary_width, boundary_height)
    # center_area = (frame_width // 2, frame_height // 2, frame_width // 2, frame_height // 2)
    # cv2.namedWindow('Child Monitoring System', cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty('Child Monitoring System', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        # Read a frame from the video capture

        ret, frame = cap.read()

        if not ret:
            break

        # Convert the frame to grayscale (Haar Cascade works better on grayscale images)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if initBB is not None:
            # Update the tracker
            success, box = tracker.update(frame)

            if success:
                x, y, w, h = [int(v) for v in box]

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Check if the child is outside the designated area (full frame)(Done)
                if (
                    x < center_area[0]
                    or x + w > center_area[0] + center_area[2]
                    or y < center_area[1]
                    or y + h > center_area[1] + center_area[3]
                ):
                    # send_email_alert()
                    print("[-] Out OF Boundary")
                    initBB = None  # Reset tracker
                    tracking = False
                # Check If Baby Crying

            else:
                initBB = None
                tracking = False
        else:
            # Detect faces in the grayscale frame
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )

            if len(faces) > 0:
                x, y, w, h = faces[0]
                initBB = (x, y, w, h)
                tracker = cv2.TrackerKCF_create()
                tracker.init(frame, initBB)
                tracking = True

        # Draw the designated area (full frame, optional visual aid)
        cv2.rectangle(
            frame,
            (center_area[0], center_area[1]),
            (center_area[0] + center_area[2], center_area[1] + center_area[3]),
            (255, 0, 0),
            2,
        )

        # Display the frame
        cv2.imshow("Child Monitoring System", frame)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()


def aduio_test(duration=5, fs=44100):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=1024
    )
    frames = []

    for _ in range(0, int(fs / 1024 * duration)):
        data = stream.read(1024)
        frames.append(np.frombuffer(data, dtype=np.int16))

    # stream.stop_stream()
    # stream.close()
    # p.terminate()

    audio_data = np.hstack(frames)

    # print (audio_data)
    def extract_features(audio_data, fs=44100):
        mfccs = librosa.feature.mfcc(y=audio_data.astype(float), sr=fs, n_mfcc=13)
        chroma = librosa.feature.chroma_stft(y=audio_data.astype(float), sr=fs)
        rmse = librosa.feature.rms(y=audio_data.astype(float))
        zcr = librosa.feature.zero_crossing_rate(y=audio_data.astype(float))

        features = np.hstack(
            [
                np.mean(mfccs.T, axis=0),
                np.mean(chroma.T, axis=0),
                np.mean(rmse.T, axis=0),
                np.mean(zcr.T, axis=0),
            ]
        )

        return features

    def extract_features_from_file(file_path, fs=44100):
        audio_data, _ = sf.read(file_path)
        return extract_features(audio_data, fs)

    def load_dataset(dataset_path):
        X = []
        y = []

        for label, category in enumerate(["crying", "non_crying"]):
            category_path = os.path.join(dataset_path)
            for file_name in os.listdir(category_path):
                file_path = os.path.join(category_path, file_name)
                if file_path.endswith(".ogg"):
                    features = extract_features_from_file(file_path)
                    X.append(features)
                    y.append(label)

        return X, y

    # Split data into training and testing sets
    dataset_path = "data/301_Crying_baby/"
    X, y = load_dataset(dataset_path)
    X = np.array(X)
    y = np.array(y)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train a Support Vector Classifier
    clf = SVC()
    clf.fit(X_train, y_train)

    # Predict and evaluate
    y_pred = clf.predict(X_test)
    # print(X,y)
    print("Accuracy:", accuracy_score(y_test, y_pred))

    def is_crying(audio_data, classifier, fs=44100, intensity_threshold=35):
        features = extract_features(audio_data, fs)
        prediction = classifier.predict([features])
        # Check intensity (RMSE) for hard crying detection
        rmse = librosa.feature.rms(y=audio_data.astype(float))
        average_rmse = np.mean(rmse)

        return prediction[0] == 1 and average_rmse > intensity_threshold

    if is_crying(audio_data, clf):
        print("Baby is crying!")
    else:
        pass


main()

while True:
    aduio_test()
    # audio = threading.Thread(target=aduio_test)
    # audio.start()
