 const firebaseConfig = {
     apiKey: "AIzaSyCeCVHV_iY0xXeTWBUiFGlvSTQturRngWU",
     authDomain: "fil-flutter-f31f2.firebaseapp.com",
    databaseURL: "https://fil-flutter-f31f2-default-rtdb.firebaseio.com",
     projectId: "fil-flutter-f31f2",
     storageBucket: "fil-flutter-f31f2.appspot.com",
     messagingSenderId: "701218164702",
     appId: "1:701218164702:web:f132c9d586e4a36c7ad74f"
   };

 firebase.initializeApp(firebaseConfig);
 const db = firebase.firestore();

 db.collection(`/job_request/${region}/requests`).get().then((snapshot) =>{
    snapshot.docs.forEach(doc =>{
        console.log(doc.data());
    });
 });

 db.collection(`/job_request/${region}/requests`).onSnapshot(snapshot =>{
     snapshot.docs.forEach(doc=>{
         console.log(doc.data());
     });
 });







// function renderJobs(snapshot){
//     output = `<table class="table">
//         <thead>
//             <th scope="col">Address</th>
//             <th scope="col">Postal Code</th>
//             <th scope="col">Service Type</th>
//             <th scope="col">Booking Type</th>
//         </thead>
//     `

//     output += "</table>"
// }