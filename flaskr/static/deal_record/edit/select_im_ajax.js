$(document).ready(function(){
    $("#select_im").on('changed.bs.select', function(e, clickedIndex, isSelected, previousValue){
        ajax_refresh_project(this.value);
    });

    $('.confirmDelete').click(function(e){
        delete_project(this.id);
        $("#deleteConfirmBox").modal('hide');
    });

    $("#select_im").on('sort.bs.table', function(){
        $('.delete').click(function(e){
            $('.confirmDelete').prop("id", this.id);
            $('#deleteConfirmBox').modal('show');  
        });
    });
});

function ajax_refresh_project(im_id){
    $.ajax({
        url: "/edit",
        data: {"im_id": im_id},
        type: "POST", 
        success: function(data){
            var json_data= JSON.parse(data['deal']);
            $('#edit_table').bootstrapTable('load', json_data);
        
            $('.delete').click(function(e){
                $('.confirmDelete').prop("id", this.id);
                $('#deleteConfirmBox').modal('show');  
            });
        },
        error: function(error){
            alert("Error");
        }
    });
}

// Create buttons in bootstrap table
function TableActions(value, row, index){
    var im_id = document.querySelector('#select_im').value;

    return `<a class="btn btn-info btn-sm btn-block no-print edit" id="${row.deal_id}" href="/edit_record?deal_id=${row.deal_id}&im_id=${im_id}&im=${row.name_y}" id="submit">Edit</a><button class="btn btn-danger btn-sm btn-block no-print delete" id="${row.deal_id}" onclick="delete_button(this.id);">Delete</button><a class="btn btn-dark btn-sm btn-block no-print edit" id="${row.deal_id}" href="/project_update?deal_id=${row.deal_id}&im_id=${im_id}&im=${row.name_y}" id="submit">Update</a>`
}

function delete_project(deal_id){
    $.post('/project_delete', {'deal_id': deal_id})
        .done(function(){
            ajax_refresh_project($("#select_im").val());
    });
}

function delete_button(deal_id){
    $('.confirmDelete').prop("id", deal_id);
    $('#deleteConfirmBox').modal('show');  
}