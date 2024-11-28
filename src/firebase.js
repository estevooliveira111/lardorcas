import { initializeApp } from "firebase/app";
import { getFirestore } from 'firebase/firestore';
import { getStorage } from "firebase/storage";

const firebaseApp = initializeApp({
  apiKey: "AIzaSyDQGBD9aTfl1GJsWdRRft6U6_Ta1YLjzME",
  authDomain: "firego-82472.firebaseapp.com",
  projectId: "firego-82472",
  storageBucket: "firego-82472.firebasestorage.app",
  messagingSenderId: "847498805922",
  appId: "1:847498805922:web:0c37f075dd63c564efcdfb",
  measurementId: "G-GX2MF0J7Q7"
});

const db = getFirestore(firebaseApp);
const storage = getStorage(firebaseApp);

export { firebaseApp, db, storage };
