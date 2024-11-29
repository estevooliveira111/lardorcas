import { initializeApp } from "firebase/app";
import { getFirestore } from 'firebase/firestore';
import { getStorage } from "firebase/storage";

const firebaseApp = initializeApp({
  apiKey: "AIzaSyAfcGM8dLG1MM9WaFIED27EBrzaBse5ssw",
  authDomain: "lar-dorcas-dbaf9.firebaseapp.com",
  projectId: "lar-dorcas-dbaf9",
  storageBucket: "lar-dorcas-dbaf9.firebasestorage.app",
  messagingSenderId: "881198734839",
  appId: "1:881198734839:web:6a91b852577bb2587722f2",
  measurementId: "G-XRBHRYN892"
});

const db = getFirestore(firebaseApp);
const storage = getStorage(firebaseApp);

export { firebaseApp, db, storage };
