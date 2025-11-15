let sim = false;


// Instantiate the collapsible element under simulate checkbox
$(document).ready(function() {
    $('#time_params').collapse('hide');
    $('#xl_params').collapse('show');

    // If simulate checkbox state changes, show or hide the time params as appropriate
    $( "#sim-box" ).change(function() {
        if(this.checked) {
            // show the time input for simulations
            $('#time_params').collapse('show');
            $('#xl_params').collapse('hide');
            // change the fit button text to say simulate
            $('#fit-submit').val('Simulate');
            $('#download-fit').val('Download Simulation');
            $('.bounds-input').prop("disabled", true);
            $("[id^='system-species-'][id$='-for_fitting']").prop('disabled', true);
            $("[id^='system-species-'][id$='-mol_end']").prop('disabled', true);
            $("[id^='system-species-'][id$='-col']").prop('disabled', true);
            $("[id^='system-species-'][id$='-ord_min']").prop('disabled', true);
            $("[id^='system-species-'][id$='-ord_max']").prop('disabled', true);
            $("[id^='system-species-'][id$='-pois_min']").prop('disabled', true);
            $("[id^='system-species-'][id$='-pois_max']").prop('disabled', true);
            $('.temp_col').prop("disabled", true);
            $('#manip_fit').collapse('hide');
            $('#manip_sim').collapse('show');
            sim = true;
        } else{
            // hide the time input for simulations
            $('#time_params').collapse('hide');
            $('#xl_params').collapse('show');
            // change the simulate button text to say fit
            $('#fit-submit').val('Fit');
            $('#download-fit').val('Download Fit');
            $('.bounds-input').prop("disabled", false);
            $("[id^='system-species-'][id$='-for_fitting']").prop('disabled', false);
            $("[id^='system-species-'][id$='-mol_end']").prop('disabled', false);
            $("[id^='system-species-'][id$='-col']").prop('disabled', false);
            $("[id^='system-species-'][id$='-ord_min']").prop('disabled', false);
            $("[id^='system-species-'][id$='-ord_max']").prop('disabled', false);
            $("[id^='system-species-'][id$='-pois_min']").prop('disabled', false);
            $("[id^='system-species-'][id$='-pois_max']").prop('disabled', false);
            $('.temp_col').prop("disabled", false);
            $('#manip_fit').collapse('show');
            $('#manip_sim').collapse('hide');
            sim = false;
        }
    });
});

