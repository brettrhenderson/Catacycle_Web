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



// add a parameter card for new concentrations added.
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
                <input checked="" class="filled-in" id="is-excess-${numParams}" type="checkbox"/>
                <span>Excess</span>
              </label>
            </div>
            <div class="form-group input-field">
              <label for="spec-param-${numParams}" class="active">Species</label>
              <select id="spec-param-${numParams}" name="species" disabled>
              </select>
            </div>
            <div class="form-group range-field">
              <label for="rxn-order-${numParams}">Reactant Order</label>
              <input class="form-control-range" id="rxn-order-${numParams}" max="3" min="0" name="order" step="0.01" type="range" value="0"><span class="thumb"><span class="value"></span></span>
            </div>
            <div class="form-group range-field">
              <label for="poisoning-${numParams}">Poisoning</label>
              <input class="form-control-range" id="poisoning-${numParams}" max="3" min="0" name="poisoning" step="0.01" type="range" value="0"><span class="thumb"><span class="value"></span></span>
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
    var dummyParams = numParams;
    $( `#delete-param-${dummyParams}` ).click(function() {
        $(`#param-div-${dummyParams}`).remove();
        $(`#param-fit-${dummyParams}`).remove();
    });

    var rxctr = 0;

    for (var [key, value] of paramData.entries()) {
        if (key === 'csrf_token') { continue; }

        if (key === 'excess') {
            if (value == 'y') {
                $("#is-excess-" + numParams).prop('checked', true);
                let specctr = 0
                for (spec of specs) {
                    specText = spec + " (species " + (specctr+1) + ")";
                    $('#spec-param-' + numParams).append(`<option value="${specValue}">${specText}</option>`);
                    specctr = specctr + 1;
                }
                $('select').formSelect();
            }
            continue;
        }

        if (key === 'species') {
            $(`#spec-param-${numParams}`).attr("disabled", false);
            $("#is-excess-" + numParams).prop('checked', false);
            let specctr = 0
            for (spec of specs) {
                specText = spec + " (species " + (specctr+1) + ")";

                if (value == specctr) {
                    $('#spec-param-' + numParams).append(`<option value="${value}" selected="selected">${specText}</option>`);
                }
                else {
                    $('#spec-param-' + numParams).append(`<option value="${specValue}">${specText}</option>`);
                }
                specctr = specctr + 1;
            }
            $('select').formSelect();
            continue;
        }

        if (key === 'order') {
            $("#rxn-order-" + numParams).val(value)
            continue;
        }
        if (key === 'poison') {
            $("#poisoning-" + numParams).val(value)
            continue;
        }

        rxnText = rxns[rxctr] + " (rxn " + (rxctr+1) + ")";
        rxnValue = rxctr;

        var htmlstr = `<div class="form-group input-field concentration-form" id="param-${numParams}-concs-label-${(rxctr+1)}">
             <input class="form-control validate" id="param-${numParams}-start-conc-${(rxctr+1)}" name="conc" required type="text" value="${value}">
             <label for="param-${numParams}-start-conc" class="active">${rxnText}</label>
             <span class="helper-text" data-error="Required. Must be integer or decimal value." data-success=""></span>
             </div>`
        $( htmlstr ).insertAfter( "#param-" + numParams + "-concs-label-" + rxctr);
        console.log((key, value));
        rxctr = rxctr + 1;
    }

    numParams = numParams + 1;

    successHandler();
};

function paramSuccess() {
    console.log("Success!!");
};


// make file upload submit form automatically
$("#param-submit").click(function() {
    // Prevent redirection with AJAX for contact form
    var form = $('#param-form');
    var form_id = 'param-form';
    var url = form.prop('action');
    var type = form.prop('method');
    var formData = getFormData(form_id);

    for (var [key, value] of formData.entries()) { console.log('formData', key, value);}

    // submit form via AJAX
    send_form(form, form_id, url, type, modular_ajax, formData, '#response-xlform', plotSuccess);
});