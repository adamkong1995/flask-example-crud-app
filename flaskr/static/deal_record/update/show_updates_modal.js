const showEmailModal = () => {
    document.querySelector('#updateToSend').innerHTML = '';

    getData()
    .then(data => {
            create_update_to_send(data['updates']);
            create_recipient_list(data['emails']);
        })
    .then(()=>$('#updateEmailModal').modal('show'));
}

const getData = async () => {
    let res = await fetch('/update_email_get', {method: 'post'});
    let data = await res.json();
    return data;
}

const create_update_to_send = data => {
    const json = JSON.parse(data)
    if (Object.keys(json).length > 0){
        document.getElementById('sendUpdateEmail').disabled = false;
        json.forEach(data => {
            create_tosend_dom(data)
        })
    } else {
        document.getElementById('sendUpdateEmail').disabled = true;
        create_nosend_dom()
    }
}

const create_recipient_list = emailList => {
    var div_recipient = document.querySelector('#to');
    div_recipient.value = "";
    const json = JSON.parse(emailList);
    
    if (Object.keys(json).length > 0){
        recipient = 'demo1@test.com; demo2@test.com';
        json.forEach(data => {
            if (recipient === '') {
                recipient = data.email;
            } else {
                recipient = `${recipient} ; ${data.email}`
            }
        })
        div_recipient.value = recipient;
    } else {
        div_recipient.value = '';
    }
}

const create_tosend_dom = tosend => {
    var div_toSend = document.querySelector('#updateToSend');
    var div_row = document.createElement('div');
    div_row.setAttribute('class','row mt-2 rowTosend')
    var row_toSend = div_toSend.insertAdjacentElement('beforeend', div_row);
    row_toSend.insertAdjacentHTML('beforeend', `<div class="col-lg-1">
                                                    <div class="form-check">
                                                        <input class="form-check-input" type="checkbox" id="${tosend.update_id}" checked>
                                                    </div>
                                                </div>`)

    row_toSend.insertAdjacentHTML('beforeend', `<div class="col-lg-2">
                                                    <h6>${tosend.name}</h6>
                                                </div>`)

    row_toSend.insertAdjacentHTML('beforeend', `<div class="col-lg-9">
                                                    <textarea class="form-control" row=2 disabled>${tosend.update_content}</textarea>
                                                </div>`)
}

const create_nosend_dom = () => {
    var div_toSend = document.querySelector('#updateToSend');
    div_toSend.insertAdjacentHTML('beforeend', `<div class="row mt-2">
                                                    <div class="col-lg-5">
                                                        <h6>No outstanding project update.</h6>
                                                    </div>
                                                </div>`)
}

document.getElementById("sendEmailButton").addEventListener('click', showEmailModal)

$('#updateEmailModal').on('hidden.bs.modal', function () {
    try{
        document.querySelector('#status').remove();
    } finally {
        // No action if status spinner not exist
    }
})