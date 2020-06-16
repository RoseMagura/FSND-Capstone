submit = document.getElementById('submit');
submit.addEventListener('click', function(e){
    e.preventDefault();
    console.log('submitted');
    const name = document.getElementById('name').value;
    const age = document.getElementById('age').value;
    const gender = document.getElementById('gender').value;
    let movies = [];
    for (let option of document.getElementById('movies').options){
        if (option.selected) {
            movies.push(option.value);
        }
    }
    
    fetch('/new_actor', {
        method: 'post',
        body: JSON.stringify({
            'name': name,
            'age': age,
            'gender': gender,
            'movies': movies

        }),
        headers : {
            'Content-Type': 'application/json'
        }
    })
})