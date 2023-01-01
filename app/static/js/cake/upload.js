
// Instantiate the collapsible element under simulate checkbox
$(document).ready(function() {
    $('#time_params').collapse('hide');

    // If simulate checkbox state changes, show or hide the time params as appropriate
    $( "#sim-box" ).change(function() {
        if(this.checked) {
            $('#time_params').collapse('show');
        } else{
            $('#time_params').collapse('hide');
        }
    });
});

