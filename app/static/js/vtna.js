var numParams = 0;
var rxns;
var specs;

$("#excess-temp").click(function (){
    if (!this.checked) {
    console.log('blah');
        $("#spec-param-temp").removeAttr("disabled");
        $("#spec-param-temp").parent(".select-wrapper").removeClass("disabled");
        $("#spec-param-temp").siblings(".select-dropdown").removeClass("disabled");
        $("#spec-param-temp").siblings(".select-dropdown").removeAttr("disabled");
        console.log($("#spec-param-temp").parent(".select-wrapper"))
    } else {
        $("#spec-param-temp").attr("disabled", true);
        $("#spec-param-temp").parent(".select-wrapper").addClass("disabled");
        $("#spec-param-temp").siblings(".select-dropdown").addClass("disabled");
        $("#spec-param-temp").siblings(".select-dropdown").attr("disabled", true);
    }
});


/*
Submission Handlers:

These functions handle the specific submission formats of each data form.
The different data forms are:

1) Upload: (ID: "#upload-submit"). Handles uploading new data and plotting it.
   Invokes the plotSuccess callback, which removes all existing parameters
   and data selections.
2) Manual Submit: (ID: "#manual-submit"). Right now, handles just zeroing the time.
   TODO: remove this altogether or fix the corresponding interface and maybe merge
   it with another form
3) Select Data: (ID: "#select-submit"). Selects which reaction data to plot.
   TODO: Have the selected data reflected in the normalization input form.
4) Add new Parameter: (ID: "#add-param-temp"). Adds a new parameter which can be used
   to fit the data. Does not actually make any ajax requests, just adds a new card
   to the front end with the additional parameters.
5) Submit Fitting Parameters: (ID: "#param-submit"). Submits all data for fitting and
   returns a plot that is time normalized and includes catalyst poisoning.

*/

// make file upload submit form automatically
$("#upload-submit").click(function() {
    // Prevent redirection with AJAX for contact form
    var form = $('#xlform');
    var form_id = 'xlform';
    var url = form.prop('action');
    var type = form.prop('method');
    var formData = getFormData(form_id);

    // submit form via AJAX
    send_form(form, form_id, url, type, modular_ajax, formData, '#response-xlform', plotSuccess);
});

// make manual fit submit form automatically
$("#manual-submit").click(function() {
    // Prevent redirection with AJAX for contact form
    var form = $('#manual-form');
    var form_id = 'manual-form';
    var url = form.prop('action');
    var type = form.prop('method');
    var formData = getFormData(form_id);

    // submit form via AJAX
    send_form(form, form_id, url, type, modular_ajax, formData, '#response-manualform', plotSuccess);
});

// make data selection submit form automatically
$("#select-submit").click(function() {
    // Prevent redirection with AJAX for contact form
    var form = $('#select-form');
    var form_id = 'select-form';
    var url = form.prop('action');
    var type = form.prop('method');
    var formData = getFormData(form_id);

    // submit form via AJAX
    send_form(form, form_id, url, type, modular_ajax, formData, '#response-selectform', plotSuccess);
});

/* Add a parameter card for new concentrations added.
The "action" of this form actually has no effect on the backend.*/
$("#add-param-temp").click(function() {
    // Prevent redirection with AJAX for contact form
    var form = $('#param-add-form');
    var form_id = 'param-add-form';
    var url = form.prop('action');
    var type = form.prop('method');
    var formData = getFormData(form_id);

    // submit form via AJAX
    send_form(form, form_id, url, type, updateParams, formData, '#response-paramform', paramSuccess);
});

// Actually submit all normalization parameters to the backend for plotting
$("#param-submit").click(function() {
    // Prevent redirection with AJAX for contact form
    var form = $('#param-form');
    var form_id = 'param-form';
    var url = form.prop('action');
    var type = form.prop('method');
    var formData = getFormData(form_id);

    // console.log(form.serialize());

    for (var [key, value] of formData.entries()) { console.log('formData', key, value);}

    // submit form via AJAX
    send_form(form, form_id, url, type, modular_ajax, formData, '#response-xlform', fitSuccess);
});


/*
Success Handlers:

These functions handle the data returned by the python backend during
an ajax request. They are all invoked within the submission handlers
above, which initiate the ajax requests. The success handlers include:

1) plotSuccess: Meant to handle new reaction data after an excel file
   upload. Currently also being used to handle the data selection and
   time zeroing.
   TODO: Remove this as the success handler for everything other than
   data upload and write specific handlers for each of those individual
   cases.
2) updateParams / paramSuccess: These handle the addition of new cards
   for each fitting parameter added. They don't actually submit and
   handle an ajax request and just do everything in the front end.
3) fitSuccess: Handles the updated plot that has been time-normalized
   Simply adds this new plot and leaves all of the submission forms
   unchanged.
*/

function plotSuccess(data) {
    $('#graph').attr("src", data.new_plot)

    // adjust fit params
    $( ".concentration-form" ).remove();
    // adjust the data selection
    $('#rxn-select option').remove();
    var rxn;
    var rxctr = 0;
    rxns = data.rxns
    for (rxn of rxns) {
        rxnText = rxn + " (rxn " + (rxctr+1) + ")";
        rxnValue = rxctr;

        if (data.rxns_sel.includes(rxctr)) {
            $('#rxn-select').append(`<option value="${rxnValue}" selected="selected">${rxnText}</option>`);
        }
        else {
            $('#rxn-select').append(`<option value="${rxnValue}">${rxnText}</option>`);
        }
        var htmlstr = `<div class="form-group input-field concentration-form" id="concs-label-${(rxctr+1)}">
             <input class="form-control validate" id="start-conc-${(rxctr+1)}" name="conc" required type="text" value="">
             <label for="start-conc-${(rxctr+1)}" class="active">${rxnText}</label>
             <span class="helper-text" data-error="Required. Must be integer or decimal value." data-success=""></span>
             </div>`
        $( htmlstr ).insertAfter( "#concs-label-"+rxctr );
        rxctr = rxctr + 1;
    }

    $('#spec-select option').remove();
    $('#spec-param-temp option').remove();
    var spec;
    var specctr = 0;
    specs = data.specs

    for (spec of data.specs) {
        specText = spec + " (species " + (specctr+1) + ")";
        specValue = specctr;

        if (data.specs_sel.includes(specctr)) {
            $('#spec-select').append(`<option value="${specValue}" selected="selected">${specText}</option>`);
        }
        else {
            $('#spec-select').append(`<option value="${specValue}">${specText}</option>`);
        }
        $('#spec-param-temp').append(`<option value="${specValue}">${specText}</option>`);
        specctr = specctr + 1;
    }
    $('select').formSelect();
}

/* This takes the place of the modular_ajax function when updating or adding
a new fitting parameter. It does not make an ajax request*/
function updateParams(url, type, paramData, responseid, successHandler) {
    // add a new parameter card for fitting
    let new_card  = `<div id="param-div-${numParams}" class="mt-3 mb-3 ml-3 mr-3 concentration-form">
            <a class="btn btn-block btn-secondary" data-toggle="collapse" href="#param-fit-${numParams}" role="button" aria-expanded="false" aria-controls="collapseExample">
                Fit Param ${numParams + 1}
            </a>
          </div>
          <div class="collapse ml-3 mr-3 concentration-form" id="param-fit-${numParams}">
            <hr>
            <div class="form-group my-auto">
              <label>
                <input checked="" class="filled-in" id="params-${numParams}-excess" name="params-${numParams}-excess" type="checkbox"/>
                <span>Excess</span>
              </label>
            </div>
            <div class="form-group input-field">
              <label for="params-${numParams}-species" class="active">Species</label>
              <select id="params-${numParams}-species" name="params-${numParams}-species" disabled>
              </select>
            </div>
            <div class="form-group input-field">
              <label class="active" for="params-${numParams}-order">Reactant Order</label>
              <input class="form-control" id="params-${numParams}-order" max="3" min="0" name="params-${numParams}-order" step="0.01" type="number" value="0"><span class="thumb"><span class="value"></span></span>
            </div>
            <div class="form-group input-field">
              <label class="active" for="params-${numParams}-poison">Poisoning</label>
              <input class="form-control" id="params-${numParams}-poison" max="3" min="0" name="params-${numParams}-poison" step="0.01" type="number" value="0"><span class="thumb"><span class="value"></span></span>
            </div>
            <div id="param-${numParams}-concs-label-0" class="form-group input-field pb-2"><h6>Concentrations</h6></div>
            <div class="form-group mb-0">
              <button id="delete-param-${numParams}" type="button" class="btn btn-block btn-primary pl-2 pr-2">Remove</button>
            </div>
            <hr>
          </div>`

    $("#new-param").collapse('hide');
    $( new_card ).insertBefore( "#submit-params" );
    $("[id^=start-conc-]").val('');

    // create a delete button to remove this normalization parameter
    var dummyParams = numParams;
    $( `#delete-param-${dummyParams}` ).click(function() {
        $(`#param-div-${dummyParams}`).remove();
        $(`#param-fit-${dummyParams}`).remove();
        numParams = numParams - 1;
    });

    var rxctr = 0;

    for (var [key, value] of paramData.entries()) {
        if (key === 'csrf_token') { continue; }

        if (key === 'excess') {
            if (value == 'y') {
                $(`#params-${numParams}-excess`).prop('checked', true);
                let specctr = 0
                for (spec of specs) {
                    specText = spec + " (species " + (specctr+1) + ")";
                    $(`#params-${numParams}-species`).append(`<option value="${specValue}">${specText}</option>`);
                    specctr = specctr + 1;
                }
                $('select').formSelect();
            }
            continue;
        }

        if (key === 'species') {
            $(`#params-${numParams}-species`).attr("disabled", false);
            $(`#params-${numParams}-excess`).prop('checked', false);
            let specctr = 0
            for (spec of specs) {
                specText = spec + " (species " + (specctr+1) + ")";

                if (value == specctr) {
                    $(`#params-${numParams}-species`).append(`<option value="${value}" selected="selected">${specText}</option>`);
                }
                else {
                    $(`#params-${numParams}-species`).append(`<option value="${specValue}">${specText}</option>`);
                }
                specctr = specctr + 1;
            }
            $('select').formSelect();
            continue;
        }

        if (key === 'order') {
            $(`#params-${numParams}-order`).val(value)
            continue;
        }
        if (key === 'poison') {
            $(`#params-${numParams}-poison`).val(value)
            continue;
        }

        rxnText = rxns[rxctr] + " (rxn " + (rxctr+1) + ")";
        rxnValue = rxctr;

        var htmlstr = `<div class="form-group input-field concentration-form" id="param-${numParams}-concs-label-${(rxctr+1)}">
             <input class="form-control validate" id="params-${numParams}-concs-${rxctr}" name="params-${numParams}-concs-${rxctr}" required type="text" value="${value}">
             <label for="params-${numParams}-concs-${rxctr}" class="active">${rxnText}</label>
             <span class="helper-text" data-error="Required. Must be integer or decimal value." data-success=""></span>
             </div>`
        $( htmlstr ).insertAfter( "#param-" + numParams + "-concs-label-" + rxctr);
        console.log((key, value));
        rxctr = rxctr + 1;
    }
    $('select').formSelect();
    numParams = numParams + 1;

    successHandler();
};

function paramSuccess() {
    console.log("Success!!");
};

function fitSuccess(data) {
    $('#graph').attr("src", data.new_plot)
    $('select').formSelect();
}


/*
UTILITIES:

These functions are generic helpers for sending form data to the python backend
and handling the responses without refreshing the webpage. They are invoked when
any of the form submission buttons are clicked.
*/

// Code modified from https://medium.com/javascript-in-plain-english/how-to-form-submissions-with-flask-and-ajax-dfde9891c620
function getFormData(form) {
    // creates a FormData object and adds chips text
    var formData = new FormData(document.getElementById(form));
    for (var [key, value] of formData.entries()) { console.log('formData', key, value);}
    return formData
}

function send_form(form, form_id, url, type, inner_ajax, formData, responseid, successHandler) {
    // form validation and sending of form items
    if ( form[0].checkValidity() && isFormDataEmpty(formData) == false ) { // checks if form is empty
        event.preventDefault();
        // inner AJAX call
        inner_ajax(url, type, formData, responseid, successHandler);
    }
    else {
        // first, scan the page for labels, and assign a reference to the label from the actual form element:
        var labels = document.getElementsByTagName('LABEL');
        for (var i = 0; i < labels.length; i++) {
            if (labels[i].htmlFor != '') {
                 var elem = document.getElementById(labels[i].htmlFor);
                 if (elem)
                    elem.label = labels[i];
            }
        }

        // then find all invalid input elements (form fields)
        var Form = document.getElementById(form_id);
        var invalidList = Form.querySelectorAll(':invalid');

        if ( typeof invalidList !== 'undefined' && invalidList.length > 0 ) {
            // errors were found in the form (required fields not filled out)

            // for each invalid input element (form field) return error
            for (var item of invalidList) {
                if (item.label) {
                    M.toast({html: "Please correctly fill the "+item.label.innerHTML+"", classes: 'bg-danger text-white'});
                    $(responseid).html('');
                }
            }
        }
        else {
            M.toast({html: "Another error occured, please try again.", classes: 'bg-danger text-white'});
            $(responseid).html('');
        }
    }
}


function isFormDataEmpty(formData) {
    // checks for all values in formData object if they are empty
    for (var [key, value] of formData.entries()) {
        if (key != 'csrf_token') {
            if (value != '' && value != []) {
                return false;
            }
        }
    }
    return true;
}

function modular_ajax(url, type, formData, responseid, successHandler) {
    // Most simple modular AJAX building block
    var result = '';
    $.ajax({
        url: url,
        type: type,
        data: formData,
        processData: false,
        contentType: false,
        beforeSend: function() {
            // show the preloader (progress bar)
            $(responseid).html("<div class='progress'><div class='indeterminate'></div></div>");
        },
        complete: function () {
            // hide the preloader (progress bar)
            $(responseid).html("");
        },
        success: function ( data ){
            if ( !$.trim( data.feedback )) { // response from Flask is empty
                toast_error_msg = "An empty response was returned.";
                toast_category = "danger";
            }
            else { // response from Flask contains elements
                toast_error_msg = data.feedback;
                toast_category = data.category;
                successHandler(data);
            }

        },
        error: function(xhr) {console.log("error. see details below.");
            console.log(xhr.status + ": " + xhr.responseText);
            toast_error_msg = "An error occured";
            toast_category = "danger";
        },
    }).done(function() {
        M.toast({html: toast_error_msg, classes: 'bg-' +toast_category+ ' text-white'});
    });
};

var csrf_token = "{{ csrf_token() }}";

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});