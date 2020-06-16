const submit = document.getElementById('submit');
submit.addEventListener('click', function(e){
    e.preventDefault();
    console.log('submitted');
    const name = document.getElementById('name').value;
    const release_date = document.getElementById('release_date').value;
    let actors = [];
    for (let option of document.getElementById('actors').options){
        if (option.selected) {
            actors.push(option.value);
        }
    }
    fetch('/new_movie', {
        method: 'post',
        body: JSON.stringify({
            'name': name,
            'release_date': release_date,
            'actors': actors

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