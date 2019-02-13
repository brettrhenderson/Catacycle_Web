// javascript found at https://bootsnipp.com/snippets/402bQ

function addrow(rows) {
    var counter = rows+1;

    $("#addrow").on("click", function () {
        if (counter < 11) {
            var newRow = $("<tr>");
            var cols = "";

            cols += '<td>' + counter + '</td>';
            cols += '<td><input type="text" id="f_rate' + counter + '" class="form-control" name="f_rate' + counter + '" value="0"/></td>';
            cols += '<td><input type="text" id="r_rate' + counter + '" class="form-control" name="r_rate' + counter + '" value="0"/></td>';
            cols += '<td><input type="button" class="ibtnDel btn btn-md btn-danger "  value="Delete"></td>';

            newRow.append(cols);
            $("table.rates-list").append(newRow);
            counter++;
        }
    });

    $("table.rates-list").on("click", ".ibtnDel", function (event) {
        $(this).closest("tr").remove();
        counter -= 1
    });
};