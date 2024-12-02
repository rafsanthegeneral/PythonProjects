
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-analytics.js";
// import { getDatabase, set, get, update, remove, ref, child } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-database.js";
import { getFirestore, collection, getDocs } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-firestore.js";

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

// const db = getDatabase();
// // use for Real Time Database
// function getAllData() {
//   const dbRef = ref(db); // Reference to the root of the database
//   get(dbRef)
//     .then((snapshot) => {
//       if (snapshot.exists()) {
//         console.log("All data:", snapshot.val()); // Output all data
//       } else {
//         console.log("No data found!");
//       }
//     })
//     .catch((error) => {
//       console.error("Error fetching data:", error); // Handle errors
//     });
// }

// // Fetch all data
// //getAllData();
// // use for Firestore Database
const db = getFirestore(app);
async function getAllDocuments() {
  try {
    // Reference the collection
    const colRef = collection(db, "test");

    // Fetch all documents in the collection
    const snapshot = await getDocs(colRef);

    // Check if the collection has documents
    if (!snapshot.empty) {
      // Clear the existing content in #showdata
      const showDataElement = document.querySelector("#showdata");
      showDataElement.innerHTML = ""; // Reset the content

      // Iterate through documents and display them
      snapshot.forEach((doc) => {
        const data = doc.data();
        const dataString = `Document ID: ${doc.id}, Name: ${data.ref}`;
        console.log(data);
        document.querySelector("#showdata").innerHTML = JSON.stringify(doc.data());
        // Create a paragraph element for each document
        // const para = document.createElement("p");
        // para.textContent = dataString;

        // // Append the paragraph to #showdata
        // showDataElement.appendChild(para);
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
// Call the function
getAllDocuments();