// initialize csrf token
var token = ''

// count number of steps in tables
var counter = 4;

function setToken(token_val) {
    token = token_val;
}


function slider_vals(input, output) {
    var slider = document.getElementById(input);
    var output = document.getElementById(output);
    output.value = slider.value; // Display the default slider value

    // Update the current slider value (each time you drag the slider handle)
    slider.oninput = function() {
        output.value = this.value;
    }
}

slider_vals("gap", "gapval")
slider_vals("thickness", "thicknessval")

function clear() {
    $("#clearrates").on("click", function (event) {
        $('.rate').val('0.0')
        $('.income-check').val('false')
    });

    $("#clearcolors").on("click", function (event) {
        // $('.color').val('#000000')
        var prefixes = ['f', 'r', 'incoming'];
        for (prefix in prefixes) {
            for (i = 1; i < counter; i++) {
                $('#' + prefixes[prefix] + '_color-picker-component' + i).colorpicker('setValue', '#000000')
            }
        }
    });
}

// javascript for addrow found at https://bootsnipp.com/snippets/402bQ
function addrow(rows) {
    counter = rows+1;

    $("#delrow, #delcolorrow").on("click", function (event) {
        if (counter > 2) {
            $("#rate-body")[0].deleteRow(-1);
            $("#color-body")[0].deleteRow(-1);
            counter -= 1
        }
    });

    $("#addcolorrow, #addrow").on("click", function () {
        if (counter < 11) {
            var newcolorRow = $('<tr id="crow' + counter + '">');
            var ccols = "";
            ccols += '<td>' + counter + '</td>';
            var prefixes = ['f', 'r']
            for (prefix in prefixes) {
                ccols += `<td>
                             <div id="${prefixes[prefix]}_color-picker-component${counter}" class="input-group colorpicker-component">
                                 <input id="${prefixes[prefix]}_color${counter}" name="${prefixes[prefix]}_color${counter}" type="text" value="#000000" class="form-control color"/>
                                 <span class="input-group-append">
                                     <span class="input-group-text colorpicker-input-addon"><i></i></span>
                                 </span>
                             </div>
                         </td>`;
            }

            newcolorRow.append(ccols);
            $("table.color-list").append(newcolorRow);
            var prefixes = ['f', 'r'];
            for (prefix in prefixes) {
                $('#' + prefixes[prefix] + '_color-picker-component' + counter).colorpicker({
                    autoInputFallback: false,
                    popover: { placement: 'right' },
                    format: 'hex',
                    extensions: [
                        {
                            name: 'swatches', // extension name to load
                            options: { // extension options
                                colors: {
                                    'black': '#000000',
                                    'gray': 'gray',
                                    'red': 'red',
                                    'blue': 'blue',
                                    'defaultf1': '#4286f4',
                                    'defaultf2': '#e2893b',
                                    'defaultf3': '#de5eed',
                                    'defaultf4': '#dd547d',
                                    'defaultr1': '#82abed',
                                    'defaultr2': '#efb683',
                                    'defaultr3': '#edb2f4',
                                    'defaultr4': '#ef92ae',
                                },
                                namesAsValues: false
                            }
                        }
                    ]
                });
            }

            var newRow = $('<tr id="row' + counter + '">');
            var cols = "";
            cols += '<td>' + counter + '</td>';
            cols += '<td><input type="text" id="f_rate' + counter + '" class="form-control rate" name="f_rate' + counter + '" value="1.0"/></td>';
            cols += '<td><input type="text" id="r_rate' + counter + '" class="form-control rate" name="r_rate' + counter + '" value="0.0"/></td>';
            cols += '<td><input id="is_incoming' + counter + '" class="form-control" type="checkbox"</td>'
            cols += '<td><input id="is_outgoing' + counter + '" class="form-control" type="checkbox"</td>'

            newRow.append(cols);
            $("table.rates-list").append(newRow);

            counter++;
        }
    })
};

function submitForm(csrf_token, form_url, response_handler) {
    var postData = $('#cycle-form').serialize();
    // console.log(postData);
    var formURL = form_url;

    $.ajax(
    {
        url : formURL,
        type: "POST",
        crossDomain: true,
        data : postData,
        success:function(response, textStatus, jqXHR)
        {
            // response: return data from server
            response_handler(response);
            //document.getElementById('graph').src = response.data;
            // console.log(response.data);
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
    $('#cycle-form').submit(function(e)
    {
        e.preventDefault(); //STOP default action
        submitForm(csrf_token, '/graphs', function (response) {
            document.getElementById('graph').src = response.data;
        });

    });
}
