var downloadExcel = false;
var downloadImage = false;

$.validator.addMethod("greaterThan", function (value, element, param) {
    var $otherElement = $(param);
    return this.optional(element) || this.optional($otherElement[0]) || parseFloat(value, 10) > parseFloat($otherElement.val(), 10);
    }, jQuery.validator.format("Must be > {0} or left blank.")); // "Must be > " + $("label[for='" + $($.validator.format({0})).attr('id') + "']").text() + " or left blank.");

$.validator.addMethod("lessThan", function (value, element, param) {
    var $otherElement = $(param);
    return this.optional(element) || this.optional($otherElement[0]) || parseFloat(value) < parseFloat($otherElement.val());
    }, jQuery.validator.format("Must be < {0} or left blank.")); // "Must be < " + $("label[for='" + $($.validator.format({0})).attr('id') + "']").text() + " or left blank."));

$.validator.addMethod("greaterEqThan", function (value, element, param) {
    var $otherElement = $(param);
    return this.optional(element) || this.optional($otherElement[0]) || parseFloat(value, 10) >= parseFloat($otherElement.val(), 10);
    }, jQuery.validator.format("Must be >= {0} or left blank.")); // "Must be >= " + $("label[for='" + $($.validator.format({0})).attr('id') + "']").text() + " or left blank."));

$.validator.addMethod("lessEqThan", function (value, element, param) {
    var $otherElement = $(param);
    return this.optional(element) || this.optional($otherElement[0]) || parseFloat(value) <= parseFloat($otherElement.val());
    }, jQuery.validator.format("Must be <= {0} or left blank.")); // "Must be <= " + $("label[for='" + $($.validator.format({0})).attr('id') + "']").text() + " or left blank."));

function updateFinalProduct() {
    $("#r0").change(function(){
        // Update final product concentration
        $('#p_end').val($("#r0").val() * $("#stoich_p").val() / $("#stoich_r").val())
    });
}

function submitForm(form_url, responseHandler) {
    var formData = new FormData(document.getElementById('cake-form'))

    var formURL = form_url;
    // for (var [key, value] of formData.entries()) { console.log('formData', key, value);}
    $.ajax(
    {
        url : formURL,
        type: "POST",
        data : formData,
        processData: false,
        contentType: false,
        cache: false,
        success:function(response, textStatus, jqXHR)
            {
                // response: return data from server
                responseHandler(response);
                //document.getElementById('graph').src = response.data;
            },
        error: function(jqXHR, textStatus, errorThrown)
            {
                // if fails
                alert('CAKE failed with the following error: ' + jqXHR.responseText);
            }
    });
}

function highlightInvalidTabs(event, validator) {
    downloadExcel = false;
    downloadImage = false;
    $("a.form-tab").removeClass('error-tab')
    var errors = validator.numberOfInvalids();
    if (errors) {
      for (let i in validator.errorList) {
          var tabId = $(validator.errorList[i].element).closest('div.tab-pane')[0].id;
          $(`a[href='#${tabId}']`).addClass('error-tab');
      }
    }
}

function ExcelDownloadHandler() {
    $('#download-fit').click(function() {
        downloadExcel = true;
        $('#cake-form').submit();
    });
}

function submitCakeHandler(form) {
    $('a.form-tab').removeClass('error-tab')

    if (downloadExcel) {
        downloadExcel = false;
        form.submit();
    }

    if (downloadImage) {
        downloadImage = false;
        submitDownloadData();
    }
    else {
        $('#outputlink').trigger('click');
        document.getElementById('output-text').innerHTML = "Calculating...";

        submitForm('/cake', function (response) {
            document.getElementById('cake-result').src = response.data[0];
            document.getElementById('output-text').innerHTML = response.data[1];
        });
    }
}


function downloadHandler() {
    $('#fake-submit').click(function(e) {
        // e.preventDefault(); //STOP default action
        downloadImage = true;
        $('#cake-form').submit();
    });
}

function submitDownloadData() {
    // get all of the information in the input cake form
    var cake_data = cloneWithSelects($('#cake-form')).find(':input')
    cake_data.attr('hidden', true);
    $('#download-form').append(cake_data);
    $('#download-form').children().remove(':button')

    // now submit the form for real
    $("#download-form")[0].submit();
    // clean-up
    $('#download-form').children().remove(':input')
}

function cloneWithSelects(original) {
    var cloned = original.clone()
    // https://techbrij.com/clone-html-form-selected-options-jquery-firefox
    var originalSelects = original.find('select');
    cloned.find('select').each(function(index, item) {
        //set new select to value of old select
        $(item).val( originalSelects.eq(index).val() );
    });
    return cloned;
}