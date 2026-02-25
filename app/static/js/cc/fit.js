let fit_eq = 'None';
let lof = false;
let smooth_eq = 'Default';

// Instantiate the collapsible element under sg checkbox
$(document).ready(function() {
    $('#intercept-box').prop("disabled", true);
    $('#fitlof').collapse('hide');
    $('#loftest').collapse('hide');
    $('#pthresh').collapse('hide');
    $('#sg_win_collapse').collapse('hide');

    // If line checkbox state changes, uncheck the exp checkbox show or hide the fitlof as appropriate
    $("#fit_eq" ).change(function() {
        if($(this).val() === 'Linear') {
            // show the time input for simulations
            $('#intercept-box').prop("disabled", false);
            $('#fitlof').collapse('show');
            if (lof) {
                $('#lof_test').collapse('show');
                $('#lof_test-options option[value="Rainbow"]').show();
                $('#lof_test-options option[value="Harvey-Collier"]').show()
            }
            fit_eq = 'Linear';
        } else if (['Logarithmic', 'Exponential', 'Tangential', 'Michaelis-Menten', 'Langmuir'].includes($(this).val())) {
            // show the time input for simulations
            $('#intercept-box').prop("disabled", false);
            $('#fitlof').collapse('show');
            if (lof) {
                $('#loftest').collapse('show');
                $('#lof_test-options option[value="Rainbow"]').hide();
                $('#lof_test-options option[value="Harvey-Collier"]').hide()
                const currentVal = $('#lof_test-options').val();
                if (['Rainbow', 'Harvey-Collier'].includes(currentVal)) {
                    $('#lof_test-options').val('RMSE');
                    lof_test = 'Default';
                    }
                }
            fit_eq = 'Default';
        } else{
            // hide the time input for simulations
            $('#intercept-box').prop("disabled", true);
            $('#fitlof').collapse('hide');
            $('#loftest').collapse('hide');
            fit_eq = 'None';
        }
    });

    // If line checkbox state changes, uncheck the exp checkbox show or hide the fitlof as appropriate
    $("#lof-box" ).change(function() {
        if(this.checked) {
            // show the time input for simulations
            $('#loftest').collapse('show');
            if (['RMSE'].includes($('#lof_test-options').val())) {
                $('#lof_method-options option[value="min"]').show();
                $('#lof_method-options option[value="max"]').hide();
                $('#lof_method-options option[value="first"]').hide();
                $('#lof_method-options option[value="last"]').hide();
                $('#lof_method-options').val('min');
                }
            lof = true;
        } else{
            // hide the time input for simulations
            $('#loftest').collapse('hide');
            lof = false;
        }
    });

    // If line checkbox state changes, uncheck the exp checkbox show or hide the fitlof as appropriate
    $("#lof_test-options" ).change(function() {
        if (['RMSE', 'MAE'].includes($(this).val())) {
            // show the time input for simulations
            $('#lof_method-options option[value="min"]').show();
            $('#lof_method-options option[value="max"]').hide();
            $('#lof_method-options option[value="first"]').hide();
            $('#lof_method-options option[value="last"]').hide();
            $('#pthresh').collapse('hide');
            const currentVal = $('#lof_method-options').val();
            if (['max', 'first', 'last'].includes(currentVal)) {
                $('#lof_method-options').val('min');
                }
        } else if($(this).val() === 'R2') {
            // show the time input for simulations
            $('#lof_method-options option[value="max"]').show();
            $('#lof_method-options option[value="min"]').hide();
            $('#lof_method-options option[value="first"]').hide();
            $('#lof_method-options option[value="last"]').hide();
            $('#pthresh').collapse('hide');
            const currentVal = $('#lof_method-options').val();
            if (['min', 'first', 'last'].includes(currentVal)) {
                $('#lof_method-options').val('max');
                }
        } else{
            // hide the time input for simulations
            $('#lof_method-options option[value="max"]').show();
            $('#lof_method-options option[value="first"]').show();
            $('#lof_method-options option[value="last"]').show();
            $('#lof_method-options option[value="min"]').hide();
            $('#pthresh').collapse('show');
            const currentVal = $('#lof_method-options').val();
            if (['min'].includes(currentVal)) {
                $('#lof_method-options').val('last');
                }
        }
    });

    // If smooth_eq state changes, show or hide the sg_win_collapse as appropriate
    $( "#smooth_eq" ).change(function() {
        if($(this).val() === 'Savitsky-Golay') {
            // show the time input for simulations
            $('#sg_win_collapse').collapse('show');
            smooth_eq = 'Savitsky-Golay';
        } else if (['monotonic', 'concave'].includes($(this).val())) {
            // hide the time input for simulations
            $('#sg_win_collapse').collapse('hide');
            smooth_eq = 'Default';
        } else{
            // hide the time input for simulations
            $('#sg_win_collapse').collapse('hide');
            smooth_eq = 'None';
        }
    });
});
