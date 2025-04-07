let lin = false;
let lol = false;
let sg = false;

// Instantiate the collapsible element under sg checkbox
$(document).ready(function() {
    $('#intercept-box').prop("disabled", true);
    $('#fitlol').collapse('hide');
    $('#loltest').collapse('hide');
    $('#sg_win_collapse').collapse('hide');

    // If line checkbox state changes, uncheck the exp checkbox show or hide the fitlol as appropriate
    $("#fit_eq" ).change(function() {
        if($(this).val() === 'Linear') {
            // show the time input for simulations
            $('#intercept-box').prop("disabled", false);
            $('#fitlol').collapse('show');
            if (lol) {
                $('#loltest').collapse('show');
            }
            lin = true;
        } else if ($(this).val() === 'Exponential') {
            // show the time input for simulations
            $('#intercept-box').prop("disabled", false);
            $('#fitlol').collapse('hide');
            $('#loltest').collapse('hide');
            lin = false;
        } else{
            // hide the time input for simulations
            $('#intercept-box').prop("disabled", true);
            $('#fitlol').collapse('hide');
            $('#loltest').collapse('hide');
            lin = false;
        }
    });

    // If line checkbox state changes, uncheck the exp checkbox show or hide the fitlol as appropriate
    $( "#lol-box" ).change(function() {
        if(this.checked) {
            // show the time input for simulations
            $('#loltest').collapse('show');
            lol = true;
        } else{
            // hide the time input for simulations
            $('#loltest').collapse('hide');
            lol = false;
        }
    });

    // If sg checkbox state changes, show or hide the sg_win_collapse as appropriate
    $( "#sg-box" ).change(function() {
        if(this.checked) {
            // show the time input for simulations
            $('#sg_win_collapse').collapse('show');
            sg = true;
        } else{
            // hide the time input for simulations
            $('#sg_win_collapse').collapse('hide');
            sg = false;
        }
    });
});
