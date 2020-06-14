//import two JS files in js directory (after exporting)
// import {logIn} from './js/formHandler.js';
// import {isURL} from './js/checkURL.js';
// import "./styles/main.scss";
// require("regenerator-runtime/runtime");

console.log('connected');
// const button = document.getElementById("login");

const button = document.getElementById("login");
button.addEventListener("click", logIn);
function logIn() {
    console.log('Log in');
    fetch("http://127.0.0.1:5000/all")
    .then(window.open( "https://dev-l0ayxsy2.auth0.com/authorize?audience=CA&response_type=token&client_id=qnY6u1FIxnfHYX1nBFjCskAsxPrRc2EC&redirect_uri=http://127.0.0.1:5000/all", "_self")
    )};   