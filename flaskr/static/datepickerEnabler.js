$(document).ready(function(){
    $("#dateTBC").change(function(){
        if($(this).prop('checked'))
        {
            $("#startDate").prop('disabled', true);
            $("#exitDate").prop('disabled', true);
            $("#startDate").val('');
            $("#exitDate").val('');
        }
        else
        {
            $("#startDate").prop('disabled', false);
            $("#exitDate").prop('disabled', false);            
        }
    });
});