
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-analytics.js";
// import { getDatabase, set, get, update, remove, ref, child } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-database.js";
import { getFirestore, collection, getDocs } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-firestore.js";
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

if ('Notification' in window && Notification.permission !== 'granted') {
  Notification.requestPermission().then(permission => {
    if (permission === 'granted') {
      console.log('Notification permission granted.');
    } else {
      console.log('Notification permission denied.');
    }
  });
}

setTimeout(() => {
  if (Notification.permission === 'granted') {
    new Notification('Reminder!', {
      body: 'Time to check your app!',
    });
  }
}, 500);


async function getAllDocuments() {
  try {

    const colRef = collection(db, "test");
    const snapshot = await getDocs(colRef);

    if (!snapshot.empty) {
      const showDataElement = document.querySelector("#showdata");
      showDataElement.innerHTML = "";

      snapshot.forEach((doc) => {
        const data = doc.data();
        const price = data.Book4.Price;
        document.querySelector("#showdata").innerHTML = JSON.stringify(price);

      });
    } else {
      console.log("No documents found in the collection!");
      document.querySelector("#showdata").textContent = "No data available.";
    }
  } catch (error) {
    console.error("Error fetching documents:", error);
    document.querySelector("#showdata").textContent = "Error loading data.";
  }
}



getAllDocuments();