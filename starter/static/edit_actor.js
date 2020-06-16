const submit = document.getElementById('submit');
const actor_id = document.getElementById('actor_id').innerHTML;

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
    fetch('/actors/' + actor_id, {
        method: 'patch',
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
});

const return_button = document.getElementById('return');
return_button.addEventListener('click', function(){
    window.open('/all', '_self');
})