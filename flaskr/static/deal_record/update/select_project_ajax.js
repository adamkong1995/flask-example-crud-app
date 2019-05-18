$(document).ready(function(){
    $("#project").on('changed.bs.select', function(e, clickedIndex, isSelected, previousValue){
        ajax_refresh_deal_info(this.value);
    });
    
    $('.submitButton').click(function(e){
        if (this.id === 'submitButton'){
            alert('Please select a project to update');
            return;
        }

        var update_content = $('#update1').val();
        if (update_content === ''){
            alert("Please input the project update");
            return;
        }else {
            add_update(this.id, update_content);
            $('#update1').val('');
        }
    });

    $('.confirmUpdate').click(function(e){
        var update_content = $(`#pastupdate${this.id}`).val();
    
        if ($(`#isSent${this.id}`).prop('checked') == true){
            edit_update(this.id, update_content, "Y");
            $("#updateConfirmBox").modal('hide');
        } else {
            edit_update(this.id, update_content, "N");
            $("#updateConfirmBox").modal('hide');
        }
    });

    $('.confirmDelete').click(function(e){
        delete_update(this.id);
        $("#deleteConfirmBox").modal('hide');
    });
});

function ajax_refresh_deal_info(id){
    $.ajax({
        url: "/project_update",
        data: {"submitButton": id},
        type: "POST",
        success: function(response){
            $("#first_column").css('visibility','visible');
            $('#project_name').val(response.deal)
            $("#group").val(response.group);
            $("#pic").val(response.im_name);
            $("#description").val(response.description);
            $('.submitButton').prop("id", response.deal_id);
            delete_past_update_element();
            create_past_update_element(response.update);
        },
        error: function(error){
            alert("Error");
        }
    });
}

function add_update(deal_id, update_content){
    $.post('/project_update_add', {'deal_id': deal_id, 'update_content': update_content});
    ajax_refresh_deal_info(deal_id);
}


function edit_update(update_id, update_content, isSend){
    $.post('/project_update_edit', {'update_id': update_id, 'update_content': update_content, 'isSend': isSend});
    ajax_refresh_deal_info($('.submitButton').attr('id'));
}

function delete_update(update_id){
    $.post('/project_update_delete', {'update_id': update_id});
    ajax_refresh_deal_info($('.submitButton').attr('id'));
}

function create_past_update_element(update_content) {
    var json_update_content = JSON.parse(update_content);
    var i = 0;

    json_update_content.forEach(data => {
        const update_id = data['update_id']
        var row = $(`<div class="row mt-3" id="row${i}">`);
        row.prependTo('#previous_update');
        $(`<div class="col-3 col-lg-1" id="col1${i}">`).appendTo(row);

        if (data['isSent'] === "Y"){
            $(`<div class="form-check">
                <input class="form-check-input" type="checkbox" value="" checked="checked" id="isSent${update_id}">
               </div>`).appendTo(`#col1${i}`);
        } else {
            $(`<div class="form-check">
                <input class="form-check-input" type="checkbox" value="" id="isSent${update_id}">
               </div>`).appendTo(`#col1${i}`);
        }
        $(`<div class="col-9 text-right col-lg-2 text-lg-left" id="col2${i}">"`).appendTo(row);
        $(`<div class="form-group" id="date${i}">`).appendTo(`#col2${i}`);
        $('<h6>').text(data['date_created']).appendTo(`#date${i}`);

        $(`<div class="col-lg-7" id="col3${i}">`).appendTo(row);
        $(`<textarea class="form-control" id="pastupdate${update_id}" row="1">`).text(data['update_content']).appendTo(`#col3${i}`);
        $(`<div class="col-lg-1 mt-2 mt-lg-0" id="col4${i}">"`).appendTo(row);
        $(`<div class="row" id="col4${i}row1">`).appendTo(`#col4${i}`)
        $(`<div class="row mt-1" id="col4${i}row2">`).appendTo(`#col4${i}`)

        $(`<button class="btn btn-info btn-sm btn-block no-print edit" id="${update_id}">`).text('Update').appendTo(`#col4${i}row1`);
        $(`<button class="btn btn-danger btn-sm btn-block no-print delete" id="${update_id}">`).text('Delete').appendTo(`#col4${i}row2`);
        i++;
    })

    $('.edit').click(function(e){
        const update_id = this.id;
        const update_content = $(`#pastupdate${update_id}`).val();

        if (update_content === ''){
            alert("Please input the project update");
            return;
        }else {
            $('.confirmUpdate').prop("id", this.id);
            $('#updateConfirmBox').modal('show');  
        }
    });

    $('.delete').click(function(e){
        $('.confirmDelete').prop("id", this.id);
        $('#deleteConfirmBox').modal('show');  
    })
}

function delete_past_update_element(){
    $('#previous_update').empty();
};