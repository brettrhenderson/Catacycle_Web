// initialize csrf token
let token = ''

// count number of steps in tables
let counters = {1: 5, 2: 5};

// initialize a list of default colors
let colorDefaults = ['#026FDD', '#FB7602', '#672CA2', '#BA2B2B', '#BC30AF', '#33962E', '#C03F17', '#000000', '#026FDD', '#FB7602', '#672CA2', '#BA2B2B', '#BC30AF', '#33962E', '#C03F17'];

let basicContent = $('#cycle-card').children().clone();

// get the content of a basic cycle table
let content1 = $('#cycle-card').children();

// keep track of the content of both cycles
let content2 = $('#cycle-card').children().clone();

// keep track of which cycle is active
let activeCycle = 1;

// Check if new cycle has already been added
let newCycle = 0;

$('#add-cycle').on("click", function (event) {
    if (this.innerHTML == "Add Cycle") {
        this.innerHTML = 'Delete Cycle';
        var newcycle = `<label class="btn btn-secondary highlight">
                        <input type="radio" name="cycleradios" id="cycle2" autocomplete="off"> Cycle 2
                    </label>`
        $('#cycle-radio').append(newcycle);

        // make second cycle opposite direction of first
        if (content1.find('#flip')[0].checked) {
            content2.find('#flip')[0].checked = false;
        }
        else {
            content2.find('#flip')[0].checked = true;
        }

        $('#rotation').val(0)    // reset the rotation of the first cycle to 0 when the second is added or deleted

        $('#cycle2').on("change", function (event) {
            if (activeCycle == 1) {
                // save current state of cycle 2
                //content1 = $('#cycle-card')[0].innerHTML;
                // change card content back to cycle 2
                $('#cycle-card').empty()
                $('#cycle-card').append(content2);
                activeCycle = 2;
                setup_card();
                $('#translation').prop("disabled", false);
                // console.log("Switched to Cycle 2")
            }
        });

        var cycleselect = `<div id="cycle-check" class="btn-group btn-group-xs btn-group-toggle" data-toggle="buttons">
                    <label id="check1-label" class="btn btn-secondary active highlight">
                        <input class="submitter" type="checkbox" name="cycle1-check" id="cycle1-check" autocomplete="off" checked> Cycle 1
                    </label>
                    <label id="check2-label" class="btn btn-secondary active highlight">
                        <input class="submitter" type="checkbox" name="cycle2-check" id="cycle2-check" autocomplete="off" checked> Cycle 2
                    </label>
                </div>
                <div id="vert-check-div" class="btn-group btn-group-xs btn-group-toggle pl-3" data-toggle="buttons">
                    <label id="vert-check-label" class="btn btn-secondary highlight">
                        <input class="submitter" type="checkbox" name="is_vert" id="vert-check" autocomplete="off"> Vertical
                    </label>
                </div>`
        $('#cycle-select').append(cycleselect);

        // auto-submit form when these new buttons are toggled
        $('.submitter').on("change", extraSubmit)

        // auto-submit when new cycle is added
        extraSubmit()

        // enable translation in styling
        $('#translation').prop("disabled", false);

        if (!newCycle) {
            // Get the snackbar DIV
            var x = $("#snackbar");

            // Add the "show" class to DIV
            x.addClass("show");

            // After 3 seconds, remove the show class from DIV
            setTimeout(function(){ x.removeClass("show"); }, 6800);

            // highlight the styling tab
            var y = $(".noticer");

            // Add the "show" class to DIV
            y.addClass("notice");

            // After 3 seconds, remove the show class from DIV
            setTimeout(function(){ y.removeClass("notice"); }, 6800);
            newCycle = 1;
        }

    }
    else {
        if (confirm("Are you sure you want to Remove Cycle 2? \nAll input data for it will be lost!")) {
            this.innerHTML = 'Add Cycle';
            $('#cycle-radio').children().last().remove();
            if (!$("#cycle1-label").hasClass("active")){
                $("#cycle1-label").addClass("active");
                activeCycle = 1;
                // change card content back to cycle 1
                $('#cycle-card').empty()
                $('#cycle-card').append(content1);
                setup_card();
                content2 = basicContent;
                // console.log("Switched to Cycle 1")
            }
            $('#cycle-select').children().remove();
            // disable translation again
            $('#translation').prop("disabled", false);
            $('#rotation').val(0)    // reset the rotation of the first cycle to 0 when the second is deleted
            // auto-submit when new cycle is removed
            extraSubmit();
        }
    }

});

$('#cycle1').on("change", function (event) {
    if (activeCycle == 2) {
        // save current state of cycle 2
        // content2 = $('#cycle-card')[0].innerHTML;
        // change card content back to cycle 1
        $('#cycle-card').empty()
        $('#cycle-card').append(content1);
        activeCycle = 1;
        setup_card();
        // console.log("Switched to Cycle 1")
    }
});

function setup_card() {
    addrow(counters[activeCycle]);
    clear();
    toggleGaps();
    // link tabs to correct carousel images
    link_click_to_carousel("#outsiderxnlink", '#imageCarousel', 1);
    link_click_to_carousel("#rateslink", '#imageCarousel', 0);
    link_click_to_carousel("#colorslink", '#imageCarousel', 0);
    link_click_to_carousel("#add-cycle", '#imageCarousel', 0);
    // link_click_to_carousel("#arrowslink", '#imageCarousel', 0);

    // add colorpickers to the outside reactions tab
    add_colorpicker('#straight_f_color-picker-component', true, '#straight_r_color-picker-component');
    add_colorpicker('#straight_r_color-picker-component', false, 'None');

    // add the colorpickers for the cycle steps
    var prefixes = ['f', 'r']
    for (prefix in prefixes) {
        for (i = 1; i < counters[activeCycle]; i++) {
            if (prefixes[prefix] == 'f') {
                add_colorpicker(`#f_color-picker-component${i}`, true, `#r_color-picker-component${i}`);
            }
            else {
                add_colorpicker(`#r_color-picker-component${i}`, false, 'None');
            }
        }
    }

    // make sure nav link matches active tab pane
    var activeLink = $(".nav-link.active")[0];
    var pane;
    for (pane of $('#cycle-card').children()) {
        if (!(pane.id == activeLink.href.split("#")[1])) {
            if ($(pane).hasClass("active")) {
                $(pane).removeClass("active show");
                // console.log('Removed active from ' + pane.id);
            }
        }
        else {
            if (!$(pane).hasClass("active")) {
                $(pane).addClass("active show");
                // console.log('Added active to ' + pane.id);
            }
        }
    }
}

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
        for (i = 1; i < counters[activeCycle]; i++) {
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

// javascript for addrow adapted from https://bootsnipp.com/snippets/402bQ
function addrow(rows) {
    // counters[activeCycle] = rows+1;

    $("#delrow, #delcolorrow").on("click", function (event) {
        if (counters[activeCycle] > 2) {
            $("#rate-body")[0].deleteRow(-1);
            $("#color-body")[0].deleteRow(-1);
            counters[activeCycle] -= 1
            // rescale gaps
            $('.indygap').each(function() {
                var $eachGap = $(this)[0]
                $eachGap.value = 32 - counters[activeCycle] - Math.floor(counters[activeCycle]/2)
            });
            $('#gap')[0].value = 32 - counters[activeCycle] - Math.floor(counters[activeCycle]/2)

            // remove indygap inputs
            if(counters[activeCycle] % 4 != 1) {
                $('#gaps-block').children().last().children().last().remove();
                $('#arrows-block').children().last().children().last().remove();
            }
            else {
                $('#gaps-block').children().last().remove();
                $('#arrows-block').children().last().remove();
            }
        }
    });

    $("#addcolorrow, #addrow").on("click", function () {
        if (counters[activeCycle] < 16) {
            // add new gap adjusters as new steps are added
            if (counters[activeCycle] % 4 != 1) {
                // new input to add
                var newGap = `<div class="form-group col-sm-3">
                                  <label for="gap_${counters[activeCycle]}">Gap ${counters[activeCycle]}:</label>
                                      <input id="gap_${counters[activeCycle]}" name="gap_${counters[activeCycle]}" class="form-control indygap" type="number" min="0"
                                          max="50" step="1" value="${31 - counters[activeCycle] - Math.floor(counters[activeCycle]/2)}" disabled>
                              </div>`;
                var newArr = `<div class="form-group col-sm-3">
                                  <label for="arr_${counters[activeCycle]}">Arrow ${counters[activeCycle]}:</label>
                                      <input id="arr_${counters[activeCycle]}" name="arr_${counters[activeCycle]}" class="form-control indyarr" type="number" min="0.1"
                                          max="5" step="0.1" value="1">
                              </div>`;
                // add to the last existing row
                $('#gaps-block').children().last().append(newGap);
                $('#arrows-block').children().last().append(newArr);
            }
            else {
                var newGap = `<div class="form-row">
                                  <div class="form-group col-sm-3">
                                      <label for="gap_${counters[activeCycle]}">Gap ${counters[activeCycle]}:</label>
                                          <input id="gap_${counters[activeCycle]}" name="gap_${counters[activeCycle]}" class="form-control indygap" type="number" min="0"
                                              max="50" step="1" value="${31 - counters[activeCycle] - Math.floor(counters[activeCycle]/2)}" disabled>
                                  </div>
                              </div>`;
                var newArr = `<div class="form-row">
                                  <div class="form-group col-sm-3">
                                      <label for="arr_${counters[activeCycle]}">Arrow ${counters[activeCycle]}:</label>
                                          <input id="arr_${counters[activeCycle]}" name="arr_${counters[activeCycle]}" class="form-control indyarr" type="number" min="0.1"
                                              max="5" step="0.1" value="1">
                                  </div>
                              </div>`;
                // add new row to the gaps-block
                $('#gaps-block').append(newGap);
                $('#arrows-block').append(newArr);
            }

            var newcolorRow = $('<tr id="crow' + counters[activeCycle] + '">');
            var ccols = "";
            ccols += '<td>' + counters[activeCycle] + '</td>';
            var prefixes = ['f', 'r']
            for (prefix in prefixes) {
                var cval = colorDefaults[counters[activeCycle] - 1];
                if (prefixes[prefix] == 'r') {
                    cval = "#404040"
                }
                ccols += `<td>
                             <div id="${prefixes[prefix]}_color-picker-component${counters[activeCycle]}" class="input-group colorpicker-component">
                                 <input id="${prefixes[prefix]}_color${counters[activeCycle]}" name="${prefixes[prefix]}_color${counters[activeCycle]}" type="text" value=${cval} class="form-control color"/>
                                 <span class="input-group-append">
                                     <span class="input-group-text colorpicker-input-addon"><i></i></span>
                                 </span>
                             </div>
                         </td>`;
            }

            newcolorRow.append(ccols);
            $("table.color-list").append(newcolorRow);
            add_colorpicker('#f_color-picker-component' + counters[activeCycle], true, '#r_color-picker-component' + counters[activeCycle]);
            add_colorpicker('#r_color-picker-component' + counters[activeCycle], false, 'none');

            var newRow = $('<tr id="row' + counters[activeCycle] + '">');
            var cols = "";
            cols += '<td width="6%">' + counters[activeCycle] + '</td>';
            cols += '<td><select id="f_rate' + counters[activeCycle] + '" class="form-control frate" name="f_rate' + counters[activeCycle] + '">';
            cols += '<option value="1">Very Low</option><option value="2">Low</option><option value="3" selected>Moderate</option>';
            cols += '<option value="4">High</option><option value="5">Very High</option></select>';
            cols += '</td>';
            cols += '<td><select id="r_rate' + counters[activeCycle] + '" class="form-control rrate" name="r_rate' + counters[activeCycle] + '">';
            cols += '<option value="0" selected>None</option><option value="1">Very Low</option><option value="2">Low</option><option value="3">Moderate</option>';
            cols += '<option value="4">High</option><option value="5">Very High</option></select>';
            cols += '</td>';
            cols += '<td width="12%"><input id="is_incoming' + counters[activeCycle] + '" name="is_incoming' + counters[activeCycle] + '" class="form-control" type="checkbox"</td>'
            cols += '<td width="12%"><input id="is_outgoing' + counters[activeCycle] + '" name="is_outgoing' + counters[activeCycle] + '" class="form-control" type="checkbox"</td>'

            newRow.append(cols);
            $("table.rates-list").append(newRow);

            counters[activeCycle]++;

            // enable or disable all gaps depending on whether the indygap box is checked
            var dis = !($('#ind-gap')[0].checked);
            $('.indygap').each(function() {
                var $eachGap = $(this)[0]
                $eachGap.disabled = dis;
                $eachGap.value = 32 - counters[activeCycle] - Math.floor(counters[activeCycle]/2)
            });

            // adjust the gap to accommodate more/less steps
            $('#gap')[0].value = 32 - counters[activeCycle] - Math.floor(counters[activeCycle]/2)
        }
    })
};

function submitForm(csrf_token, form_url, responseHandler, addArgsHandler) {
    var postData = 'csrf_token=' + $('#csrf_token')[0].value;

    // check which cycles are checked
    if ($('#cycle1-check').length) {    // there are two cycles
        postData += '&double=true'
        // check if vertical alignment is selected
        postData += '&is_vert=' + $('#vert-check')[0].checked;
        if ($('#cycle1-check')[0].checked) {    // plot cycle 1
            if ($('#cycle1')[0].checked) {    // cycle 1 is currently active form
                postData += '&' + $('#cycle-card').find(':input').serialize()
                // console.log($('#cycle-card').find(':input').serialize())
            }
            else {
                postData += '&' + content1.find(':input').serialize()
            }
            postData += '&plot_1=true'
        }
        else {
            postData += '&plot_1=false'
        }
        if ($('#cycle2-check')[0].checked) {    // plot cycle 2
            var data2;
            if ($('#cycle2')[0].checked) {    // cycle 2 is currently active form
                data2 = $('#cycle-card').find(':input').serialize()
            }
            else {
                data2 = content2.find(':input').serialize()
            }
            // edit field names for cycle 2
            var fields = data2.split('&');
            var newfields = [];
            for (field of fields) {
                newfields.push('c2_' + field)
            }
            postData += '&' + newfields.join('&');
            postData += '&plot_2=true'
        }
        else {
            postData += '&plot_2=false'
        }
    }
    else {
        postData = $('#cycle-form').serialize();
        postData += '&plot_1=true'
        postData += '&plot_2=false'
        postData += '&is_vert=false'
        postData += '&double=false'
    }

    // check which cycle form is active
    if ($('#cycle1')[0].checked) {
        postData += '&p1_active=true'
    }
    else {
        postData += '&p1_active=false'
    }

    // handle additional arguments
    if (addArgsHandler !== undefined) {
        postData = addArgsHandler(postData);
        // console.log("New Post Data: " + postData)
    }
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
            responseHandler(response);
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

function extraSubmit() {
    submitForm($('#csrf_token')[0].value, '/graphs', function (response) {
        document.getElementById('graph').src = response.data[0];
        document.getElementById('straight-graph').src = response.data[1];
    });
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
    $('#download-form').submit(function(e)
    {
        e.preventDefault(); //STOP default action

        $('<input />').attr('type', 'hidden').attr('name', "image_index")
            .attr('value', $('#imageCarousel .active').index()).appendTo('#download-form');

        // make sure to account for which cycle is selected
        if ($('#cycle1-check').length) {    // there are two cycles
            // check if vertical alignment is selected
            $('<input />').attr('type', 'hidden').attr('name', "is_vert")
                .attr('value', $('#vert-check')[0].checked).appendTo('#download-form');
            if ($('#cycle1-check')[0].checked) {    // plot cycle 1
                if ($('#cycle1')[0].checked) {    // cycle 1 is currently active form
                    // Add all cycle data as hidden members of download form
                    var cycle_data = cloneWithSelects($('#cycle-form')).find(':input')
                    // var cycle_data = $('#cycle-form').find(':input').clone();
                    cycle_data.attr('hidden', true);
                    $('#download-form').append(cycle_data)
                }
                else {
                    var data1 = cloneWithSelects(content1).find(':input')
                    // var data1 = content1.find(':input').clone();
                    data1.attr('hidden', true);
                    $('#download-form').append(data1)
                }
                $('<input />').attr('type', 'hidden').attr('name', "plot_1")
                    .attr('value', true).appendTo('#download-form');
            }
            else {
                $('<input />').attr('type', 'hidden').attr('name', "plot_1")
                    .attr('value', false).appendTo('#download-form');
                // add token for some reason
                $('<input />').attr('type', 'hidden').attr('name', "csrf_token")
                    .attr('value', $('#csrf_token')[0].value).appendTo('#download-form');
            }
            if ($('#cycle2-check')[0].checked) {    // plot cycle 2
                var data2;
                if ($('#cycle2')[0].checked) {    // cycle 2 is currently active form
                    data2 = cloneWithSelects($('#cycle-form')).find(':input')
                    // data2 = $('#cycle-card').find(':input').clone();
                    // add token for some reason
                    $('<input />').attr('type', 'hidden').attr('name', "csrf_token")
                        .attr('value', $('#csrf_token')[0].value).appendTo('#download-form');
                }
                else {
                    data2 = cloneWithSelects(content2).find(':input')
                    // data2 = content2.find(':input').clone()
                }
                // edit field names and ids for cycle 2
                data2.each(function( index ) {
                    $(this).attr('name', 'c2_' + $(this).attr('name'));
                    $(this).attr('id', 'c2_' + $(this).attr('id'))
                });
                $('#download-form').append(data2)
                $('<input />').attr('type', 'hidden').attr('name', "plot_2")
                    .attr('value', true).appendTo('#download-form');
            }
            else {
                $('<input />').attr('type', 'hidden').attr('name', "plot_2")
                    .attr('value', false).appendTo('#download-form');
            }
        }
        else {
            var cycle_data = cloneWithSelects($('#cycle-form')).find(':input')
            // var cycle_data = $('#cycle-form').find(':input').clone();
            cycle_data.attr('hidden', true);
            $('#download-form').append(cycle_data);
            $('<input />').attr('type', 'hidden').attr('name', "plot_1")
                .attr('value', true).appendTo('#download-form');
            $('<input />').attr('type', 'hidden').attr('name', "plot_2")
                .attr('value', false).appendTo('#download-form');
            $('<input />').attr('type', 'hidden').attr('name', "is_vert")
                .attr('value', false).appendTo('#download-form');
        }

        // check which cycle form is active
        if ($('#cycle1')[0].checked) {
            $('<input />').attr('type', 'hidden').attr('name', "p1_active")
                .attr('value', true).appendTo('#download-form');
        }
        else {
            $('<input />').attr('type', 'hidden').attr('name', "p1_active")
                .attr('value', false).appendTo('#download-form');
        }
        // now submit the form for real
        // console.log($('#download-form').serialize())
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