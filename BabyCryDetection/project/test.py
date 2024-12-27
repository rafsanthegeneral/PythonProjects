import cv2
import numpy as np
import pyaudio
import numpy as np
import librosa
import soundfile as sf
import os
from pathlib import Path
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import threading
import firebase_admin
from firebase_admin import firestore
import time
from datetime import datetime
import requests
import pickle


certificate_path = Path("../../../BabyCryFirebase.json")
cred_obj = firebase_admin.credentials.Certificate(certificate_path)
firebase_admin.initialize_app(cred_obj)
db = firestore.client()


# Function to get current time
def get_internet_time():
    response = requests.get(
        "https://timeapi.io/api/Time/current/zone?timeZone=Asia/Dhaka"
    )
    response.raise_for_status()
    data = response.json()
    date_str = data["date"]  # '12/13/2024'
    time_str = data["time"]  # '11:24'
    current_datetime = datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %H:%M")
    return current_datetime


current_time = get_internet_time()
formatted_time = current_time.strftime("%d %b %I:%M %p").lower()


# Feature extraction
def extract_features(audio_data, fs=44100):
    try:
        mfccs = librosa.feature.mfcc(y=audio_data.astype(float), sr=fs, n_mfcc=13)
        rmse = librosa.feature.rms(y=audio_data.astype(float))
        zcr = librosa.feature.zero_crossing_rate(y=audio_data.astype(float))

        features = np.hstack([np.mean(mfccs.T, axis=0), np.mean(rmse), np.mean(zcr)])
        return features
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None


# Load dataset (crying and simulated mislead data)
def load_dataset(crying_path, num_fake_samples=50):
    X, y = [], []

    # Load all crying baby sounds
    for file_name in os.listdir(crying_path):
        if file_name.endswith(".ogg") or file_name.endswith(".wav"):
            file_path = os.path.join(crying_path, file_name)
            try:
                audio_data, _ = librosa.load(file_path, sr=44100)
                features = extract_features(audio_data)
                if features is not None:
                    X.append(features)
                    y.append(1)  # Label for crying sound
            except Exception as e:
                print(f"Error loading {file_name}: {e}")

    # Generate "fake" misleading sounds (random noise or silence)
    for _ in range(num_fake_samples):
        fake_audio = np.random.uniform(-0.01, 0.01, 44100)  # Random noise for 1 second
        features = extract_features(fake_audio)
        if features is not None:
            X.append(features)
            y.append(0)  # Label for misleading sound

    print(f"Loaded {len(X)} samples. Crying: {y.count(1)}, Non-crying: {y.count(0)}")
    return np.array(X), np.array(y)


# Train SVM model
def train_model():
    crying_path = "data/301_Crying_baby/"
    X, y = load_dataset(crying_path)

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train an SVM classifier
    model = SVC(kernel="linear", probability=True)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print(f"Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")

    # Save the model
    with open("crying_detector.pkl", "wb") as f:
        pickle.dump(model, f)
    print("Model saved as 'crying_detector.pkl'.")


# Real-time audio monitoring using trained model
def audio_test(duration=5, fs=44100):
    # Load the trained model
    with open("crying_detector.pkl", "rb") as f:
        model = pickle.load(f)
    print("Model loaded. Listening for crying sounds...")

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=1024
    )

    try:
        while True:
            # Record audio
            frames = []
            for _ in range(0, int(fs / 1024 * duration)):
                data = stream.read(1024, exception_on_overflow=False)
                frames.append(np.frombuffer(data, dtype=np.int16))
            audio_data = np.hstack(frames)

            # Extract features and predict
            features = extract_features(audio_data)
            if features is not None:
                prediction = model.predict([features])
                if prediction[0] == 1:
                    # data = {
                    #     "time": formatted_time,
                    #     "Staus": "Baby Crying",
                    # }

                    # doc_ref = db.collection("cry").document()
                    # doc_ref.set(data)
                    print("Baby is crying!")
                else:
                    print("No crying detected.")
    except KeyboardInterrupt:
        print("Audio monitoring stopped.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


# Video processing function
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
    # audio = threading.Thread(target=aduio_test)
    # audio.start()

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

                    # data = {
                    #     "time": formatted_time,
                    #     "Staus": "Out Of Boundary",
                    # }

                    # doc_ref = db.collection("boundary").document()
                    # doc_ref.set(data)
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


# Run audio and video monitoring simultaneously
if __name__ == "__main__":
    train_model()
    # Start audio monitoring in a separate thread
    audio_thread = threading.Thread(target=audio_test, daemon=True)
    audio_thread.start()

    # Start video monitoring in the main thread
    main()

# while True:
#     aduio_test()
# audio = threading.Thread(target=aduio_test)
# audio.start()
