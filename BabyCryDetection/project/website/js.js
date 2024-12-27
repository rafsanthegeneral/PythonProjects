
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-analytics.js";
// import { getDatabase, set, get, update, remove, ref, child } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-database.js";
import { getFirestore, collection, getDocs, onSnapshot } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-firestore.js";
import { getMessaging, getToken, onMessage } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-messaging.js";

const firebaseConfig = {
  apiKey: "AIzaSyBbFkqMEJ2FPcEC7GtUKAod8MQtIEktP4g",
  authDomain: "babycryproject.firebaseapp.com",
  databaseURL: "https://babycryproject-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "babycryproject",
  storageBucket: "babycryproject.firebasestorage.app",
  messagingSenderId: "13056733919",
  appId: "1:13056733919:web:87ad5f6921b8b509bf6f6a",
  measurementId: "G-N62K9XB6SL"

};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const db = getFirestore(app);
const messaging = getMessaging(app);

// if ('Notification' in window && Notification.permission !== 'granted') {
//   Notification.requestPermission().then(permission => {
//     if (permission === 'granted') {
//       console.log('Notification permission granted.');
//     } else {
//       console.log('Notification permission denied.');
//     }
//   });
// }

// setTimeout(() => {
//   if (Notification.permission === 'granted') {
//     new Notification('Reminder!', {
//       body: 'Time to check your app!',
//     });
//   }
// }, 500);


// Function to listen for real-time updates in the "cry" collection
function GetCryData() {
  try {
    const colRef = collection(db, "cry");

    // Real-time listener using onSnapshot
    onSnapshot(colRef, (snapshot) => {
      const showCryDataElement = document.querySelector("#showcrydata");
      showCryDataElement.innerHTML = ""; // Clear existing content

      if (!snapshot.empty) {
        snapshot.forEach((doc) => {
          const data = doc.data();
          console.log(data);
          const time = data.time;
          const p = document.createElement("p");
          p.textContent = time || "No time available"; // Fallback text if time is undefined

          // Append the <p> element to the container
          showCryDataElement.appendChild(p);
        });
      } else {
        console.log("No documents found in the collection!");
        showCryDataElement.textContent = "No data available.";
      }
    });
  } catch (error) {
    console.error("Error listening to documents:", error);
    document.querySelector("#showcrydata").textContent = "Error loading data.";
  }
}

// Function to listen for real-time updates in the "boundary" collection
function GetOutOfBoundaryData() {
  try {
    const colRef = collection(db, "boundary");

    // Real-time listener using onSnapshot
    onSnapshot(colRef, (snapshot) => {
      const showOutOfBoundaryDataElement = document.querySelector("#showOutOfBoundarydata");
      showOutOfBoundaryDataElement.innerHTML = ""; // Clear existing content

      if (!snapshot.empty) {
        snapshot.forEach((doc) => {
          const data = doc.data();
          console.log(data);
          const time = data.time;
          const p = document.createElement("p");
          p.textContent = time || "No time available"; // Fallback text if time is undefined

          // Append the <p> element to the container
          showOutOfBoundaryDataElement.appendChild(p);
        });
      } else {
        console.log("No documents found in the collection!");
        showOutOfBoundaryDataElement.textContent = "No data available.";
      }
    });
  } catch (error) {
    console.error("Error listening to documents:", error);
    document.querySelector("#showOutOfBoundarydata").textContent = "Error loading data.";
  }
}

// Start listening for real-time updates
GetOutOfBoundaryData();
GetCryData();
