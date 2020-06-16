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

//Edit Movie    
const movieEditBtns = document.querySelectorAll('.movie-edit-button');
for (let i = 0; i < movieEditBtns.length; i++) {
    const btn = movieEditBtns[i];
    btn.onclick = function(e) {
        e.preventDefault();
        const movieId = e.target.dataset['id'];
        fetch ('/movies/' + movieId)  
         .then(window.open('/movies/' + movieId, '_self'));
    }};

//Edit Actor    
const actorEditBtns = document.querySelectorAll('.actor-edit-button');
for (let i = 0; i < actorEditBtns.length; i++) {
    const btn = actorEditBtns[i];
    btn.onclick = function(e) {
        e.preventDefault();
        const actorId = e.target.dataset['id'];
        fetch ('/actors/' + actorId)     

            .then(window.open('/actors/' + actorId, '_self'));
    }};

post_movie_button = document.getElementById('post-movie-button');
post_movie_button.addEventListener('click', function(e){
    e.preventDefault();
    console.log('open new movie page');
    window.open('/new_movie', '_self');
}, false
);

post_actor_button = document.getElementById('post-actor-button');
post_actor_button.addEventListener('click', function(e){
    e.preventDefault();
    console.log('open new movie page');
    window.open('/new_actor', '_self');
}, false
);
