$(document).ready(function(){
    $.ajax({
        url: '/ajax_search_group',
        type: 'POST',
        success: function(data){
            var json_data = JSON.parse(data['group'])
            $('#group').autocomplete({
                source: Object.values(json_data),
                minLength: 0
            });
            $('#group').click(function() {
                $("#group").autocomplete("search", "" );
            });
        }
    });

    // check if inputted group is exist
    $('#group').autocomplete({
        change: function (event, ui) {
            var input_value = $('#group').val();
            var isExist  = $(".ui-autocomplete li").filter(
                                function() {
                                    return $(this).text() == input_value;
                            }).first()

            if (Object.keys(isExist).length == 2) {
                document.getElementById('group').style.borderColor = "royalblue";
                document.getElementById('group_label').style.color = "royalblue";
                $('#group_label').text("You are creating a new group");
                $('#group_id').val("-1");
            }else{
                $('#group_label').text("");
                document.getElementById('group').style.borderColor = '#ced4da';
                get_group_id(input_value);
            }
        }
    });
});

// get group id according to user input
get_group_id = (input_text) => {
    $.ajax ({
        url: '/ajax_search_group_id',
        data: {"input_text": input_text},
        type: 'POST',
        success: function(data){
            var json_data = JSON.parse(data.group);
            $('#group_id').val(json_data);
        }
    });
}