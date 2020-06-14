import{isURL} from './checkURL.js';
// const button = document.getElementById("login");

// function logIn() {
//     console.log('Log in');
//     fetch("http:/localhost:3001/success")
//     .then(window.open( "https://dev-l0ayxsy2.auth0.com/authorize?audience=CA&response_type=token&client_id=qnY6u1FIxnfHYX1nBFjCskAsxPrRc2EC&redirect_uri=http://127.0.0.1:3001/success", "_self") )
   
//   const url = document.getElementById("input").value;
//   console.log(url + " submitted");

//   isURL(url);

//   fetch("http://localhost:3001/postURL", {
//     method: "POST",
//     mode: "cors",
//     headers: {
//       "Content-Type": "application/json"
//     },
//     body: JSON.stringify({
//       input: {
//         url: `${url}`
//       }
//     })
//   })
//     .then(res => res.json())
//     .then(function(res) {
//       let text1 = 'Polarity: ';
//       let text2 = 'Polarity Confidence: ';
//       document.getElementById(
//         "response"
//       ).innerHTML = `${text1.bold()} ${res.polarity}\xa0\xa0\xa0${text2.bold()}`
//                     + `${res.polarity_confidence.toFixed(2)}`;
//     });
}

export{logIn};
