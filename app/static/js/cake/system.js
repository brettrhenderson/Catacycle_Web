/*
  Global Variables:
  Keep track of the total number of species and the number of additions (of each type)
  for each species. These variables are needed when determining how to add and delete
  HTML elements when adding or removing species and additions.
*/

// list of ints. Index is species number and value is number of subtractions (continuous or aliq) for that species.
let subContNum = 0;
let aliqNum = 0;


/*
  Add Event listeners to all buttons that modify number of species and additions.
  Also include listeners for modifications to species data (e.g. species name)
  that should be reflected in changes to the HTML.
*/

$(document).ready(function() {
    $("#t_cont_sub").prop("disabled", true);
    // If New One Shot Button is Pressed, add another discrete addition row
    $("#add-aliq").click(addSubAliqHandler);
    // If Del One Shot Button is Pressed, remove discrete addition row if there are any
    $("#del-aliq").click(delSubAliqHandler);
    // Configure changes in collapse control buttons during show / hide events
    $("#aliq").on('show.bs.collapse', collapseShowHandler);
    $("#aliq").on('hide.bs.collapse', collapseHideHandler);
});

function addSubAliqHandler() {
    // generate boilerplate html for the new addition form
    const aliqHTML = makeAliqHTML(aliqNum);
    // check if there is an existing addition. If not, use default value
    const aliq_0 = $("#aliq-0")
    // append to the species data form
    $("#aliq-rows").append(aliqHTML);
    $('#aliq-rows [data-toggle="tooltip"]').tooltip();

    if (aliq_0.length > 0) {
        $("#aliq-" + aliqNum).val(aliq_0.val());
    }
    // increment subAliqNum
        aliqNum += 1;
}

function delSubAliqHandler() {
    if (aliqNum > 0) {
        // remove the HTML element
        $("#aliq-rows").children().last().remove();
        // decrement subAliqNum
        aliqNum -= 1;
    }
}

function makeAliqHTML(aliqNum) {
  const html =
  `<div class="form-row m-1">
     <!--Volume Removed [sub_aliq]: float-->
     <div class="form-group col">
       <label for="system-aliq-${aliqNum}-sub_aliq">Volume Removed</label>
       <input class="form-control" data-toggle="tooltip" id="system-aliq-${aliqNum}-sub_aliq" name="system-aliq-${aliqNum}-sub_aliq" title="" type="text" value="" data-original-title="Volume of solution removed in volume_unit">
     </div>
     <!--At Time [t_aliq]: float-->
     <div class="form-group col">
       <label for="system-aliq-${aliqNum}-t_aliq">At Time</label>
       <input class="form-control" data-toggle="tooltip" id="system-aliq-${aliqNum}-t_aliq" name="system-aliq-${aliqNum}-t_aliq" title="" type="text" value="" data-original-title="Time when aliquot extraction occurred">
     </div>
   </div>`

   return html;
}