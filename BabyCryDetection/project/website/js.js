const video = document.getElementById('video');
const canvas = document.getElementById('overlay');
const ctx = canvas.getContext('2d');
const statusText = document.getElementById('status');

// Load Haar-like Cascade or pre-trained model
const MODEL_URL = 'https://cdn.jsdelivr.net/gh/justadudewhohacks/face-api.js/weights/';
let faceDetector;

async function loadModels() {
    await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);
    faceDetector = new faceapi.TinyFaceDetectorOptions();
}

async function startVideo() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        video.srcObject = stream;
        video.onloadedmetadata = () => {
            video.play();
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            monitorChild();
        };
    } catch (err) {
        console.error('Error accessing webcam:', err);
        alert('Please allow access to the webcam and microphone.');
    }
}

async function monitorChild() {
    while (true) {
        const detections = await faceapi.detectAllFaces(video, faceDetector);

        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw designated boundary area
        const boundaryScale = 0.8;
        const boundaryWidth = canvas.width * boundaryScale;
        const boundaryHeight = canvas.height * boundaryScale;
        const boundaryX = (canvas.width - boundaryWidth) / 2;
        const boundaryY = (canvas.height - boundaryHeight) / 2;
        ctx.strokeStyle = 'blue';
        ctx.lineWidth = 2;
        ctx.strokeRect(boundaryX, boundaryY, boundaryWidth, boundaryHeight);

        if (detections.length > 0) {
            // Draw detected face rectangle
            detections.forEach(detection => {
                const { x, y, width, height } = detection.box;
                ctx.strokeStyle = 'green';
                ctx.lineWidth = 2;
                ctx.strokeRect(x, y, width, height);

                // Check if the face is out of bounds
                if (
                    x < boundaryX || x + width > boundaryX + boundaryWidth ||
                    y < boundaryY || y + height > boundaryY + boundaryHeight
                ) {
                    statusText.textContent = "Alert: Child is out of boundary!";
                    statusText.style.color = 'red';
                } else {
                    statusText.textContent = "Child is within the boundary.";
                    statusText.style.color = 'green';
                }
            });
        } else {
            statusText.textContent = "No child detected.";
            statusText.style.color = 'orange';
        }

        // Repeat on the next animation frame
        await new Promise(requestAnimationFrame);
    }
}

// Load models and start video
loadModels().then(startVideo);