function submitForm(csrf_token, form_url, responseHandler) {
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
                //if fails
                alert('Form Submission Failed with the following error: ' + errorThrown);
            }
    });

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token)
            }
        }
    })
}

function submitHandler(csrf_token) {
    $('#cake-form').submit(function(e)
    {
        e.preventDefault(); //STOP default action
        $('#outputlink').trigger('click');
        document.getElementById('output-text').innerHTML = "Calculating...";

        submitForm(csrf_token, '/cake', function (response) {
            console.log(response[0]);
            document.getElementById('cake-result').src = response.data[0];
            document.getElementById('output-text').innerHTML = response.data[1];
        });

    });
}

function downloadHandler() {
    $('#download-form').submit(function(e)
    {
        e.preventDefault(); //STOP default action

        // get all of the information in the input cake form
        var cake_data = cloneWithSelects($('#cake-form')).find(':input')
        cake_data.attr('hidden', true);
        $('#download-form').append(cake_data);
        $('#download-form').children().remove(':button')

        console.log(cake_data);

        // now submit the form for real
        console.log($("#download-form")[0]);
        console.log($("#download-form")[0].submit);
        $("#download-form")[0].submit();
        // clean-up
        $('#download-form').children().remove(':input')
    });
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