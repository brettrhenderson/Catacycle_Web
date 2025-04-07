let apply = false;

// Instantiate the collapsible element under simulate checkbox
$(document).ready(function() {
    //$('#apply_upload_collapse').collapse('hide');

    // If simulate checkbox state changes, show or hide the time params as appropriate
    $( "#apply-box" ).change(function() {
        if(this.checked) {
            // show the time input for simulations
            $('#apply_upload_collapse').collapse('show');
            $('#apply_col').collapse('show');
            $("[id^='system-species-'][id$='-apply_col']").collapse('show');
            apply = true;
        } else{
            // hide the time input for simulations
            $('#apply_upload_collapse').collapse('hide');
            $('#apply_col').collapse('hide');
            $("[id^='system-species-'][id$='-apply_col']").collapse('hide');
            apply = false;
        }
    });
});

$(document).ready(function() {
    $("##apply-box").change(function() {
        if (this.checked) {
            $("[id^='system-species-'][id$='-apply_col']").collapse('show');
        } else {
            $("[id^='system-species-'][id$='-apply_col']").collapse('hide');
        }
    });
});