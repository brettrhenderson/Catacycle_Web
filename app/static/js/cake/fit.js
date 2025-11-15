let rate_eq_2 = false;


// Instantiate the collapsible element under simulate checkbox
$(document).ready(function() {
    $('#k2_hide').collapse('hide');

    // If simulate checkbox state changes, show or hide the time params as appropriate
    $( "#rate_eq_type" ).change(function() {
        if($(this).val() === 'standard') {
            $('#k2_hide').collapse('hide');
            rate_eq_2 = true;
        } else{
            // hide the time input for simulations
            $('#k2_hide').collapse('show');
            rate_eq_2 = false;
        }
    });
});

