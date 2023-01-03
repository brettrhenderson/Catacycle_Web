
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
            $('#fit-submit').val('Simulate')
            $('#download-fit').val('Download Sim')
        } else{
            // hide the time input for simulations
            $('#time_params').collapse('hide');
            $('#xl_params').collapse('show');
            // change the simulate button text to say fit
            $('#fit-submit').val('Fit')
            $('#download-fit').val('Download Fit')
        }
    });
});

