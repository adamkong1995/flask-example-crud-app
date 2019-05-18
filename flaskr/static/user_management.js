const buttons = document.querySelectorAll('.updateBtn');

Array.from(buttons).forEach(button => {
    button.addEventListener('click', e => {
        short_name = document.querySelector(`#i${e.target.id}`).value;
        isActive = document.querySelector(`#c${e.target.id}`).checked;
        update_short_name(e.target.id, short_name, isActive)
    });
});

const update_short_name = (id, short_name, isActive) => {
    fetch('/user_management', {
        method: 'post',
        headers:{
            'Accept': 'application/json',
            'Content-type': 'application/json'
        },
        body: JSON.stringify({ id, short_name, isActive })
    });
};