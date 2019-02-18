//
function slider_vals(input, output) {
    var slider = document.getElementById(input);
    var output = document.getElementById(output);
    output.value = slider.value; // Display the default slider value

    // Update the current slider value (each time you drag the slider handle)
    slider.oninput = function() {
      output.value = this.value;
      // re-submit the form when the values of the sliders are changed.
      document.getElementById('cycle-form').submit();
    }
}

slider_vals("Gap", "Gapval")
slider_vals("Thickness", "Thicknessval")

function clear() {
    $("#clearrates").on("click", function (event) {
        $('.rate').val('0.0')
        $('.income-check').val('false')
    });

    $("#clearcolors").on("click", function (event) {
        $('.color').val('#000000')
    });
};

// javascript for addrow found at https://bootsnipp.com/snippets/402bQ
function addrow(rows) {
    var counter = rows+1;

    $("#delrow, delcolorrow").on("click", function (event) {
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
            var prefixes = ['f', 'r', 'incoming']
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
            var prefixes = ['f', 'r', 'incoming'];
            for (prefix in prefixes) {
                $('#' + prefixes[prefix] + '_color-picker-component' + counter).colorpicker({
                    popover: { placement: 'right' },
                    format: 'hex',
                    autoInputFallback: false,
                });
            }

            var newRow = $('<tr id="row' + counter + '">');
            var cols = "";
            cols += '<td>' + counter + '</td>';
            cols += '<td><input type="text" id="f_rate' + counter + '" class="form-control rate" name="f_rate' + counter + '" value="1.0"/></td>';
            cols += '<td><input type="text" id="r_rate' + counter + '" class="form-control rate" name="r_rate' + counter + '" value="0.0"/></td>';
            cols += '<td><input id="incoming' + counter + '" class="form-control" type="checkbox"</td>'

            newRow.append(cols);
            $("table.rates-list").append(newRow);

            counter++;
        }
    });
};
