// Allow for collapsible display
const coll = document.getElementsByClassName("collapsible");

for (let i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
} 

const coll2 = document.getElementsByClassName("collapsible2");

for (let i = 0; i < coll2.length; i++) {
  coll2[i].addEventListener("click", function() {
    this.classList.toggle("active");
    let content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}; 

//Delete movie
const movieDeleteBtns = document.querySelectorAll('.movie-delete-button');
for (let i = 0; i < movieDeleteBtns.length; i++) {
    const btn = movieDeleteBtns[i];
    btn.onclick = function(e) {
        e.preventDefault();
        window.confirm('Are you sure you want to permanently delete this?');
        const movieId = e.target.dataset['id'];

        fetch ('/movies/' + movieId, {
            method: 'DELETE'
        })     
        .then (
            fetch('/all')
            .then(window.open('/all', '_self'))
            )       
    }};

//Delete Actor    
const actorDeleteBtns = document.querySelectorAll('.actor-delete-button');
for (let i = 0; i < actorDeleteBtns.length; i++) {
    const btn = actorDeleteBtns[i];
    btn.onclick = function(e) {
        e.preventDefault();
        window.confirm('Are you sure you want to permanently delete this?');
        const actorId = e.target.dataset['id'];
        fetch ('/actors/' + actorId, {
            method: 'DELETE'
        })     
        .then (
            fetch('/all')
            .then(window.open('/all', '_self'))
            );
    }};