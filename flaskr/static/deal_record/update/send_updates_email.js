const send_updates_email = async () => {
    await buttonStatus('start');
    let to = await document.querySelector('#to').value;
    let cc = await document.querySelector('#cc').value;

    await get_update_tosend()
    .then(data => sendUpdate(to, cc, data))
}

const get_update_tosend = async () => {
    tosendList = [];
    var tosends = document.querySelectorAll('.rowTosend');
    tosends.forEach(tosend => {
        if (tosend.querySelector('.form-check-input').checked) {
            tosendList.push(tosend.querySelector('.form-check-input').id);
        }
    })
    return tosendList;
}

const sendUpdate = async (to, cc, tosends) => {
    let res = await fetch('/update_email_send', {
        method: 'post', 
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }, 
        body: JSON.stringify({to:to, cc:cc, id:tosends})
        });
    let result = await res.json()
    await buttonStatus(result.status)
}

const buttonStatus = status => {
    let sendBtn = document.querySelector('#sendUpdateEmail');
    sendBtn.disabled = true;
    try{
        document.querySelector('#status').remove();
    } finally {
        if (status === 'start'){
            sendBtn.insertAdjacentHTML('beforeend', `<div class="spinner-grow spinner-grow-sm ml-2" id="status" role="status">
                                                        <span class="sr-only">Loading...</span>
                                                    </div>`)
        }else if (status === 'done'){
            sendBtn.insertAdjacentHTML('beforeend', `<span class="oi oi-check ml-2" id="status"></span>`);
            showEmailModal();
        }else {
            sendBtn.insertAdjacentHTML('beforeend', `<span class="oi oi-x ml-2" id="status"></span>`);
        }
        return
    }
}

const refreshUpdateModal = () => {
    document.querySelector('#updateToSend').innerHTML = '';
    var div_toSend = document.querySelector('#updateToSend');
    div_toSend.insertAdjacentHTML('beforeend', `<div class="row mt-2">
                                                    <div class="col-lg-5">
                                                        <h6>No outstanding project update.</h6>
                                                    </div>
                                                </div>`)
}

document.getElementById('sendUpdateEmail').addEventListener('click', send_updates_email)