console.log('connected to static folder');

// function getMovies() {
//     fetch('http://0.0.0.0:8080/')}

// getMovies();    
const coll = document.getElementsByClassName("collapsible");

for (let i = 0; i < coll.length; i++) {
  print(i);  
  coll[i].addEventListener("click", function() {
    console.log('expand');
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
} 