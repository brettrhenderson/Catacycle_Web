// initialize csrf token
var token = ''

// count number of steps in tables
var counter = 4;

// initialize a list of default colors
var colorDefaults = ['#026FDD', '#FB7602', '#672CA2', '#BA2B2B', '#BC30AF', '#33962E', '#C03F17', '#000000', '#000000', '#000000'];

function setToken(token_val) {
    token = token_val;
}

function toggleGaps() {
    $('#ind-gap').change(function() {
        var dis = !this.checked;
        $('.indygap').each(function() {
            var $eachGap = $(this)[0]
            $eachGap.disabled = dis;
        });
    });
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

//slider_vals("gap", "gapval")
//slider_vals("thickness", "thicknessval")
//slider_vals("headlength", "headlengthval")
//slider_vals("headwidth", "headwidthval")
//slider_vals("swoopwidth", "swoopwidthval")
//slider_vals("swoopradius", "swoopradiusval")
//slider_vals("swoopsweep", "swoopsweepval")
//slider_vals("swoopheadlength", "swoopheadlengthval")
//slider_vals("swooprotation", "swooprotationval")


function link_click_to_carousel(id, carouselid, carousel_num) {
    $(id).on("click", function (event) {
        $(carouselid).carousel(carousel_num);

    });
}

function clear() {
    $("#clearrates").on("click", function (event) {
        $('.frate').val('3')
        $('.rrate').val('0')
        $('.income-check').val('false')
    });

    $("#clearcolors").on("click", function (event) {
        // $('.color').val('#000000')
        for (i = 1; i < counter; i++) {
            $('#f_color-picker-component' + i).colorpicker('setValue', '#000000')
            $('#r_color-picker-component' + i).colorpicker('setValue', '#404040')
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
                            'def1': '#026FdD',
                            'def2': '#FB7602',
                            'def3': '#672CA2',
                            'def4': '#BA2B2B',
                            'def5': '#BC30AF',
                            'def6': '#33962E',
                            'def7': '#C03F17'
                        },
                        namesAsValues: false
                    }
                }
            ]
        })
        .on('colorpickerCreate colorpickerUpdate', function (e) {
            col_lightness = e.color.api('lightness');
            lighten = e.color.api('lighten', 0.5).api('lightness')
            lighter = Math.max(col_lightness + 25, lighten)
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
                            'def1': '#026FdD',
                            'def2': '#FB7602',
                            'def3': '#672CA2',
                            'def4': '#BA2B2B',
                            'def5': '#BC30AF',
                            'def6': '#33962E',
                            'def7': '#C03F17' 
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

            // remove indygap inputs
            if(counter % 4 != 1) {
                $('#gaps-block').children().last().children().last().remove();
            }
            else {
                $('#gaps-block').children().last().remove();
            }
        }
    });

    $("#addcolorrow, #addrow").on("click", function () {
        if (counter < 11) {
            // add new gap adjusters as new steps are added
            if (counter % 4 != 1) {
                // new input to add
                var newGap = `<div class="form-group col-sm-3">
                                  <label for="gap_${counter}">Gap ${counter}:</label>
                                      <input id="gap_${counter}" name="gap_${counter}" class="form-control indygap" type="number" min="0"
                                          max="50" step="1" value="25" disabled>
                              </div>`;
                // add to the last existing row
                $('#gaps-block').children().last().append(newGap);
            }
            else {
                var newGap = `<div class="form-row">
                                  <div class="form-group col-sm-3">
                                      <label for="gap_${counter}">Gap ${counter}:</label>
                                          <input id="gap_${counter}" name="gap_${counter}" class="form-control indygap" type="number" min="0"
                                              max="50" step="1" value="25" disabled>
                                  </div>
                              </div>`;
                // add new row to the gaps-block
                $('#gaps-block').append(newGap);
            }

            // enable or disable all gaps depending on whether the indygap box is checked
            var dis = !($('#ind-gap')[0].checked);
            $('.indygap').each(function() {
                var $eachGap = $(this)[0]
                $eachGap.disabled = dis;
            });

            var newcolorRow = $('<tr id="crow' + counter + '">');
            var ccols = "";
            ccols += '<td>' + counter + '</td>';
            var prefixes = ['f', 'r']
            for (prefix in prefixes) {
                var cval = colorDefaults[counter - 1];
                if (prefixes[prefix] == 'r') {
                    cval = "#404040"
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
            cols += '<td width="6%">' + counter + '</td>';
            cols += '<td><select id="f_rate' + counter + '" class="form-control frate" name="f_rate' + counter + '">';
            cols += '<option value="1">Very Low</option><option value="2">Low</option><option value="3" selected>Moderate</option>';
            cols += '<option value="4">High</option><option value="5">Very High</option></select>';
            cols += '</td>';
            cols += '<td><select id="r_rate' + counter + '" class="form-control rrate" name="r_rate' + counter + '">';
            cols += '<option value="0" selected>None</option><option value="1">Very Low</option><option value="2">Low</option><option value="3">Moderate</option>';
            cols += '<option value="4">High</option><option value="5">Very High</option></select>';
            cols += '</td>';
            cols += '<td width="12%"><input id="is_incoming' + counter + '" name="is_incoming' + counter + '" class="form-control" type="checkbox"</td>'
            cols += '<td width="12%"><input id="is_outgoing' + counter + '" name="is_outgoing' + counter + '" class="form-control" type="checkbox"</td>'

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
