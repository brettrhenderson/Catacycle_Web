//
function slider_vals(input, output) {
    var slider = document.getElementById(input);
    var output = document.getElementById(output);
    output.innerHTML = slider.value; // Display the default slider value

    // Update the current slider value (each time you drag the slider handle)
    slider.oninput = function() {
      output.innerHTML = this.value;
    }
}

slider_vals("gap", "gapval")
slider_vals("thickness", "thicknessval")

// javascript for addrow found at https://bootsnipp.com/snippets/402bQ

function addrow(rows) {
    var counter = rows+1;

    $("#addrow").on("click", function () {
        if (counter < 11) {
            var newRow = $('<tr id="row' + counter + '">');
            var cols = "";

            cols += '<td>' + counter + '</td>';
            cols += '<td><input type="text" id="f_rate' + counter + '" class="form-control" name="f_rate' + counter + '" value="0"/></td>';
            cols += '<td><input type="text" id="r_rate' + counter + '" class="form-control" name="r_rate' + counter + '" value="0"/></td>';
            cols += '<td><input id="incoming' + counter + '" class="form-control" type="checkbox"</td>'

            newRow.append(cols);
            $("table.rates-list").append(newRow);

            var newcolorRow = $('<tr id="crow' + counter + '">');
            var ccols = "";

            ccols += '<td>' + counter + '</td>';
            ccols += '<td><input type="text" id="f_color' + counter + '" class="form-control" name="f_color' + counter + '" value="#000000"/></td>';
            ccols += '<td><input type="text" id="r_color' + counter + '" class="form-control" name="r_color' + counter + '" value="#000000"/></td>';
            ccols += '<td><input id="incoming_color' + counter + '" class="form-control" type="text" name="incoming_color' + counter + '" value="#000000"</td>'

            newcolorRow.append(ccols);
            $("table.color-list").append(newcolorRow);

            counter++;
        }
    });

    $("table.rates-list").on("click", ".ibtnDel", function (event) {
        if (counter > 2) {
            $("#rate-body")[0].deleteRow(-1);
            $("#color-body")[0].deleteRow(-1);
            counter -= 1
        }
    });

    $("#addcolorrow").on("click", function () {
        if (counter < 11) {
            var newcolorRow = $('<tr id="crow' + counter + '">');
            var ccols = "";

            ccols += '<td>' + counter + '</td>';
            ccols += '<td><input type="text" id="f_color' + counter + '" class="form-control" name="f_color' + counter + '" value="#000000"/></td>';
            ccols += '<td><input type="text" id="r_color' + counter + '" class="form-control" name="r_color' + counter + '" value="#000000"/></td>';
            ccols += '<td><input id="incoming_color' + counter + '" class="form-control" type="text" name="incoming_color' + counter + '" value="#000000"</td>'

            newcolorRow.append(ccols);
            $("table.color-list").append(newcolorRow);

            var newRow = $('<tr id="row' + counter + '">');
            var cols = "";

            cols += '<td>' + counter + '</td>';
            cols += '<td><input type="text" id="f_rate' + counter + '" class="form-control" name="f_rate' + counter + '" value="0"/></td>';
            cols += '<td><input type="text" id="r_rate' + counter + '" class="form-control" name="r_rate' + counter + '" value="0"/></td>';
            cols += '<td><input id="incoming' + counter + '" class="form-control" type="checkbox"</td>'

            newRow.append(cols);
            $("table.rates-list").append(newRow);

            counter++;
        }
    });

    $("table.color-list").on("click", ".ibtnDel", function (event) {
        if (counter > 2) {
            $("#rate-body")[0].deleteRow(-1);
            $("#color-body")[0].deleteRow(-1);
            counter -= 1
        }
    });
};