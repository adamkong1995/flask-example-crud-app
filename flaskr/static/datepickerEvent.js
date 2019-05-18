// Default as today
// set the "statusUpdatedDate" start to not be earlier than "encounteredDate" start

$(document).ready(function(){
    $('#startDate').datepicker({
		format: "yyyy-mm-dd",
		autoclose: true,
		clearBtn: true
	});
	$( "#startDate" ).datepicker().on('changeDate', function(){
			$('#exitDate').datepicker(
				'setStartDate', new Date($(this).val()));
			$('#exitDate').datepicker(
				'setDate', new Date($(this).val()));
	});

	$('#exitDate').datepicker({
		format: "yyyy-mm-dd",
		autoclose: true,
		clearBtn: true
	});
	//$( "#exitDate" ).datepicker( "setDate", new Date($('#startDate').val()));

    $('#statusUpdatedDate').datepicker({
        format: "yyyy-mm-dd",
        autoclose: true,
        clearBtn: true
    });
    $( "#statusUpdatedDate" ).datepicker( "setDate", new Date());

    $('#encounteredDate').datepicker({
        format: "yyyy-mm-dd",
        autoclose: true,
        clearBtn: true
    });
    $( "#encounteredDate" ).datepicker( "setDate", new Date());
});
