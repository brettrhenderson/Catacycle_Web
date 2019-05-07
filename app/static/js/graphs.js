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


function link_click_to_carousel(id, carouselid, carousel_num) {
    $(id).on("click", function (event) {
        $(carouselid).carousel(carousel_num);

    });
}

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

function add_colorpicker(id, auto_lighten, other_id) {
    if (auto_lighten) {
        $(id).colorpicker({
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
        })
        .on('change', function (e) {
            col_lightness = e.color.api('lightness');
            lighten = e.color.api('lighten', 0.5).api('lightness')
            lighter = Math.max(col_lightness + 20, lighten)
            new_lightness = Math.min(lighter, 90)
            $(other_id)
            .colorpicker('setValue', e.color.api('lightness', new_lightness).toHexString());
             // .colorpicker('setValue', e.color.api('lighten', '0.50').api('fade', '0.4').api('desaturate', '0.0').toHexString());
        });
    }
    else {
        $(id).colorpicker({
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
                cval = "#000000"
                if (prefixes[prefix] == 'r') {
                    cval = "#333333"
                }
                ccols += `<td>
                             <div id="${prefixes[prefix]}_color-picker-component${counter}" class="input-group colorpicker-component">
                                 <input id="${prefixes[prefix]}_color${counter}" name="${prefixes[prefix]}_color${counter}" type="text" value=${cval} class="form-control color"/>
                                 <span class="input-group-append">
                                     <span class="input-group-text colorpicker-input-addon"><i></i></span>
                                 </span>
                             </div>
                         </td>`;
            }

            newcolorRow.append(ccols);
            $("table.color-list").append(newcolorRow);
            add_colorpicker('#f_color-picker-component' + counter, true, '#r_color-picker-component' + counter);
            add_colorpicker('#r_color-picker-component' + counter, false, 'none');

            var newRow = $('<tr id="row' + counter + '">');
            var cols = "";
            cols += '<td>' + counter + '</td>';
            cols += '<td><input type="text" id="f_rate' + counter + '" class="form-control rate" name="f_rate' + counter + '" value="1.0"/></td>';
            cols += '<td><input type="text" id="r_rate' + counter + '" class="form-control rate" name="r_rate' + counter + '" value="0.0"/></td>';
            cols += '<td><input id="is_incoming' + counter + '" name="is_incoming' + counter + '" class="form-control" type="checkbox"</td>'
            cols += '<td><input id="is_outgoing' + counter + '" name="is_outgoing' + counter + '" class="form-control" type="checkbox"</td>'

            newRow.append(cols);
            $("table.rates-list").append(newRow);

            counter++;
        }
    })
};

function submitForm(csrf_token, form_url, response_handler) {
    var postData = $('#cycle-form').serialize();
    console.log(postData);
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
            document.getElementById('graph').src = response.data[0];
            document.getElementById('straight-graph').src = response.data[1];
        });

    });
}

function downloadHandler() {
    var permanent = ['csrf_token', 'scale_type', 'gap', 'thickness', 'f_rate_straight', 'r_rate_straight', 'f_color_straight', 'r_color_straight'];
    var cycleForm = $('#cycle-form').serializeArray();
    for(let i = 0; i < cycleForm.length; i++){
        if (permanent.includes(cycleForm[i].name)){
            $('<input />').attr('type', 'hidden')
            .attr('name', cycleForm[i].name)
            .attr('value', cycleForm[i].value)
            .appendTo('#download-form');
        }
    }
    $('<input />').attr('type', 'hidden')
        .attr('name', "image_index")
        .attr('value', $('#imageCarousel .active').index())
        .appendTo('#download-form');

    $('#fake-submit').on("click", function(e)
    {
        var cycleForm = $('#cycle-form').serializeArray();

        // create the changing fields
        for(let i = 0; i < cycleForm.length; i++){
            if (!permanent.includes(cycleForm[i].name)) {
                $('<input />').attr('type', 'hidden')
                .attr('name', cycleForm[i].name)
                .attr('value', cycleForm[i].value)
                .appendTo('#download-form');
            }
        }

        for(let i = 0; i < cycleForm.length; i++){
            console.log(1, cycleForm[i].name, cycleForm[i].value, $("#download-form input[name=" + cycleForm[i].name + "]").val());
            $("#download-form input[name=" + cycleForm[i].name + "]").val(cycleForm[i].value);
            console.log(2, cycleForm[i].name, cycleForm[i].value, $("#download-form input[name=" + cycleForm[i].name + "]").val());
        }
        console.log($("#download-form input[name=image_index]").val());
        $("#download-form input[name=image_index]").val($('#imageCarousel .active').index());
        console.log($("#download-form input[name=image_index]").val());
        console.log($('#download-form')[0]);
        $("#download-form")[0].submit();

        // remove the changing fields
        for(let i = 0; i < cycleForm.length; i++){
            if (!permanent.includes(cycleForm[i].name)) {
                $("#download-form input[name=" + cycleForm[i].name + "]").remove();
            }
        }

    });
}