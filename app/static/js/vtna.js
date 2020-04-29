$("#excess").click(function (){
    if (!this.checked) {
    console.log('blah');
        $("#spec-param").removeAttr("disabled");
        $("#spec-param").parent(".select-wrapper").removeClass("disabled");
        $("#spec-param").siblings(".select-dropdown").removeClass("disabled");
        $("#spec-param").siblings(".select-dropdown").removeAttr("disabled");
        console.log($("#spec-param").parent(".select-wrapper"))
    } else {
        $("#spec-param").attr("disabled", true);
        $("#spec-param").parent(".select-wrapper").addClass("disabled");
        $("#spec-param").siblings(".select-dropdown").addClass("disabled");
        $("#spec-param").siblings(".select-dropdown").attr("disabled", true);
    }
});

// make file upload submit form automatically
$("#upload-submit").click(function() {
    // Prevent redirection with AJAX for contact form
    var form = $('#xlform');
    var form_id = 'xlform';
    var url = form.prop('action');
    var type = form.prop('method');
    var formData = getXlFormData(form_id);

    // submit form via AJAX
    send_form(form, form_id, url, type, modular_ajax, formData, '#response-xlform', plotSuccess);
});

// Code modified from https://medium.com/javascript-in-plain-english/how-to-form-submissions-with-flask-and-ajax-dfde9891c620

function getXlFormData(form) {
    // creates a FormData object and adds chips text
    var formData = new FormData(document.getElementById(form));
//    for (var [key, value] of formData.entries()) { console.log('formData', key, value);}
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
    for (rxn of data.rxns) {
        rxnText = rxn + " (rxn " + (rxctr+1) + ")";
        rxnValue = rxctr;
        $('#rxn-select').append(`<option value="${rxnValue}">${rxnText}</option>`);
        var htmlstr = '<div class="form-group input-field concentration-form" id="concs-label-'+ (rxctr+1) + '">' +
            '<input class="form-control validate" id="start-conc" name="conc" required type="text" value="">' +
            '<label for="start-conc" class="active">' + rxn + ' (rxn ' + (rxctr+1) + ')</label>' +
            '<span class="helper-text" data-error="Required. Must be integer or decimal value." data-success=""></span>' +
            '</div>'
        $( htmlstr ).insertAfter( "#concs-label-"+rxctr );
        rxctr = rxctr + 1;
    }

    $('#spec-select option').remove();
    $('#spec-param option').remove();
    var spec;
    var specctr = 0;
    for (spec of data.specs) {
        specText = spec + " (species " + (specctr+1) + ")";
        specValue = specctr;
        $('#spec-select').append(`<option value="${specValue}">${specText}</option>`);
        $('#spec-param').append(`<option value="${specValue}">${specText}</option>`);
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