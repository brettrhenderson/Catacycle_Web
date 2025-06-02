/*
  Global Variables:
  Keep track of the total number of species and the number of additions (of each type)
  for each species. These variables are needed when determining how to add and delete
  HTML elements when adding or removing species and additions.
*/

let specNum = 1;
const specPerRow = 4;

// list of ints. Index is species number and value is number of additions (continuous or one-shot) for that species.
let contAddNum = [0];
let oneShotNum = [0];


/*
  Add Event listeners to all buttons that modify number of species and additions.
  Also include listeners for modifications to species data (e.g. species name)
  that should be reflected in changes to the HTML.
*/
$(document).ready(function() {

    // Handle Addition of New Species
    $("#addspec").click(addSpeciesHandler);

    // Delete Species
    $("#delspec").click(delSpeciesHandler);

    bindSpeciesListeners(0);

});


/*
  Event Listener Binders
*/

function bindSpeciesListeners(specNum) {
    // If New Cont Add Button is Pressed, add another continuous addition row
    $("#add-cont-species-" + specNum).click(addContHandler);
    // If Del Cont Add Button is Pressed, remove continuous addition row if there are any
    $("#del-cont-species-" + specNum).click(delContHandler);
    // If New One Shot Button is Pressed, add another instantaneous addition row
    $("#add-oneshot-species-" + specNum).click(addOneShotHandler);
    // If Del One Shot Button is Pressed, remove instantaneous addition row if there are any
    $("#del-oneshot-species-" + specNum).click(delOneShotHandler);
    // If a species name changes, update the name on it's corresponding drop-down button
    $("#system-species-" + specNum + "-spec_name").change(specNameChangeHandler);
    // Configure changes in collapse control buttons during show / hide events
    $("#species-" + specNum).on('show.bs.collapse', collapseShowHandler);
    $("#species-" + specNum).on('hide.bs.collapse', collapseHideHandler);
    $("#cont-add-species-" + specNum).on('show.bs.collapse', collapseShowHandler);
    $("#cont-add-species-" + specNum).on('hide.bs.collapse', collapseHideHandler);
    $("#one-shot-species-" + specNum).on('show.bs.collapse', collapseShowHandler);
    $("#one-shot-species-" + specNum).on('hide.bs.collapse', collapseHideHandler);
}


/*
  Event Listener Handlers
  A handler for every event in the $(document).ready() event handler above.
*/
function addSpeciesHandler() {
    // generate html both for the drop down button for the species and the species data container
    const [html_button, html_data] = makeSpeciesHTML(specNum);

    // add the button to the button panel (create new row every 4 species)
    row = Math.floor(specNum / specPerRow);
    col = specNum % specPerRow;
    if (col == 0) {    // Make a new row
        html_button_row = `<div id="species-button-row-${row}" class="form-row"></div>`;
        $("#species-buttons").append(html_button_row);
    }
    // actually add the button to the appropriate row
    $("#species-button-row-" + row).append(html_button);

    // add the species data to the collapsible species container
    $("#species-data").append(html_data);

    // initialize all event listeners for this new species
    bindSpeciesListeners(specNum);

    if (apply) {
          $("[id^='system-species-'][id$='-apply_col']").collapse('show');
    } else {
          $("[id^='system-species-'][id$='-apply_col']").collapse('hide');
    }

    // increment specNum and append to contAddNum and oneShotNum
    specNum += 1;
    contAddNum.push(0);
    oneShotNum.push(0);
}


function delSpeciesHandler() {
    // get the row and column of the species button being removed
    row = Math.floor((specNum - 1) / specPerRow);
    col = (specNum - 1) % specPerRow;

    // Make sure at least one species is left
    if (row == 0 && col == 0) {}
    else {
        if (col == 0) {  // this is the last button in the row, the row needs to be removed
            $("#species-buttons").children().last().remove();
        }
        else {           // remove the last button in the row
            $("#species-button-row-" + row).children().last().remove();
        }
        // remove the actual species data panel
        $("#species-data").children().last().remove();

        // decrement specNum
        specNum -= 1;
    }
}


function addContHandler() {
    // figure out which species this is being applied to
    const species = this.id.split("-")[3];
    // generate boilerplate html for the new addition form
    const addContHTML = makeContAddHTML(parseInt(species), contAddNum);
    // make this solution concentration match others that are already set
    // check if there is an existing addition. If not, use default value
    const add_one_shot_0 = $("#system-species-" + species + "-one_shot-0-add_sol_conc")
    const add_cont_0 = $("#system-species-" + species + "-cont_add-0-add_sol_conc")
    // append to the species data form
    $("#cont-add-species-" + species + "-rows").append(addContHTML);

    if (add_one_shot_0.length > 0) {
        $("#system-species-" + species + "-cont_add-" + contAddNum[parseInt(species)] + "-add_sol_conc").val(add_one_shot_0.val());
    }
    else if (add_cont_0.length > 0) {
        $("#system-species-" + species + "-cont_add-" + contAddNum[parseInt(species)] + "-add_sol_conc").val(add_cont_0.val());
    }

    // add necessary event listeners
    $("#system-species-" + species + "-cont_add-" + contAddNum[parseInt(species)] + "-add_sol_conc").change(makeMatchingConcHandler);
    // $(".sol-conc").change(makeMatchingConcHandler);

    // increment contAddNum
    contAddNum[parseInt(species)] += 1;
}

function delContHandler() {
    // figure out which species this is being applied to
    const species = this.id.split("-")[3];

    if (contAddNum[parseInt(species)] > 0) {
        // remove the HTML element
        $("#cont-add-species-" + species + "-rows").children().last().remove();
        // decrement contAddNum
        contAddNum[parseInt(species)] -= 1;
    }
}

function addOneShotHandler() {
    // figure out which species this is being applied to
    const species = this.id.split("-")[3];
    // generate boilerplate html for the new addition form
    const oneShotHTML = makeOneShotHTML(parseInt(species), oneShotNum);
    // make this solution concentration match others that are already set
    // check if there is an existing addition. If not, use default value
    const add_one_shot_0 = $("#system-species-" + species + "-one_shot-0-add_sol_conc")
    const add_cont_0 = $("#system-species-" + species + "-cont_add-0-add_sol_conc")
    // append to the species data form
    $("#one-shot-species-" + species + "-rows").append(oneShotHTML);

    if (add_one_shot_0.length > 0) {
        $("#system-species-" + species + "-one_shot-" + oneShotNum[parseInt(species)] + "-add_sol_conc").val(add_one_shot_0.val());
    }
    else if (add_cont_0.length > 0) {
        $("#system-species-" + species + "-one_shot-" + oneShotNum[parseInt(species)] + "-add_sol_conc").val(add_cont_0.val());
    }

    // add necessary event listeners
    $("#system-species-" + species + "-one_shot-" + oneShotNum[parseInt(species)] + "-add_sol_conc").change(makeMatchingConcHandler);
    // $(".sol-conc").change(makeMatchingConcHandler);

    // increment contAddNum
    oneShotNum[parseInt(species)] += 1;
}

function delOneShotHandler() {
    // figure out which species this is being applied to
    const species = this.id.split("-")[3];

    if (oneShotNum[parseInt(species)] > 0) {
        // remove the HTML element
        $("#one-shot-species-" + species + "-rows").children().last().remove();
        // decrement oneShotNum
        oneShotNum[parseInt(species)] -= 1;
    }
}


function specNameChangeHandler() {
    // system-species-${specNum}-spec_name
    species = this.id.split("-")[2];

    // get corresponding button
    $("#species-" + species + "-control").html(`${this.value} <i class="fa fa-chevron-down pt-1 float-right" aria-hidden="true"></i>`)
}


function collapseShowHandler(event) {
    const target = event.target;
    if (this.id == target.id) {
        const button_id = $(this).attr("aria-labelledby");
        $("#" + button_id).addClass('active');
    }
}


function collapseHideHandler(event) {
    const target = event.target;
    if (this.id == target.id) {
        const button_id = $(this).attr("aria-labelledby");
        $("#" + button_id).removeClass('active');
    }
}


function makeMatchingConcHandler() {
    // "system-species-${specNum}-cont_add-${contAddNumSpec}-add_sol_conc"
    // "system-species-${specNum}-one_shot-${oneShotNumSpec}-add_sol_conc"
    species = this.id.split("-")[2];
    // if we change one concentration to a non-empty value, update all
    // concentrations for this species to that value
    if ( $(this).val() ) {
        $(".sol-conc-species-" + species).val($(this).val());
    }
}


/*
  Functions to generate boilerplate html for new species and reagent additions.
*/
function makeContAddHTML(specNum, contAddNum) {
  const contAddNumSpec = contAddNum[specNum];

  const html =
  `<div class="form-row m-1">
     <!--Addition Solution Concentration [add_sol_conc]: float-->
     <div class="form-group col">
       <label for="system-species-${specNum}-cont_add-${contAddNumSpec}-add_sol_conc">Addition Solution Conc.</label>
       <input class="form-control sol-conc sol-conc-species-${specNum}" data-toggle="tooltip" id="system-species-${specNum}-cont_add-${contAddNumSpec}-add_sol_conc" name="system-species-${specNum}-cont_add-${contAddNumSpec}-add_sol_conc" required="" title="" type="text" value="" data-original-title="Concentration of reagent added.">
     </div>
     <!--At Continuous Rate [add_cont_rate]: float-->
     <div class="form-group col">
       <label for="system-species-${specNum}-cont_add-${contAddNumSpec}-add_cont_rate">Rate of Addition</label>
       <input class="form-control" data-toggle="tooltip" id="system-species-${specNum}-cont_add-${contAddNumSpec}-add_cont_rate" name="system-species-${specNum}-cont_add-${contAddNumSpec}-add_cont_rate" required="" title="" type="text" value="" data-original-title="Rate of addition in moles_unit volume_unit^-1 time_unit^-1.">
     </div>
     <!--After Time [t_cont_rate]: float-->
     <div class="form-group col">
       <label for="system-species-${specNum}-cont_add-${contAddNumSpec}-t_cont_rate">After Time</label>
       <input class="form-control" data-toggle="tooltip" id="system-species-${specNum}-cont_add-${contAddNumSpec}-t_cont_rate" name="system-species-${specNum}-cont_add-${contAddNumSpec}-t_cont_rate" title="" type="text" value="0.0" data-original-title="Time when addition began.">
     </div>
   </div>`;

  return html;
}

function makeOneShotHTML(specNum, oneShotNum) {
  const oneShotNumSpec = oneShotNum[specNum];

  const html =
  `<div class="form-row m-1">
     <!--Addition Solution Concentration [add_sol_conc]: float-->
     <div class="form-group col">
       <label for="system-species-${specNum}-one_shot-${oneShotNumSpec}-add_sol_conc">Addition Solution Conc.</label>
       <input class="form-control sol-conc sol-conc-species-${specNum}" data-toggle="tooltip" id="system-species-${specNum}-one_shot-${oneShotNumSpec}-add_sol_conc" name="system-species-${specNum}-one_shot-${oneShotNumSpec}-add_sol_conc" required="" title="" type="text" value="" data-original-title="Concentration of reagent added.">
     </div>
     <!--Volume Added [add_v_one_shot]: float-->
     <div class="form-group col">
       <label for="system-species-${specNum}-one_shot-${oneShotNumSpec}-add_v_one_shot">Volume Added</label>
       <input class="form-control" data-toggle="tooltip" id="system-species-${specNum}-one_shot-${oneShotNumSpec}-add_v_one_shot" name="system-species-${specNum}-one_shot-${oneShotNumSpec}-add_v_one_shot" required="" title="" type="text" value="" data-original-title="Volume of solution added in volume_unit.">
     </div>
     <!--At Time [t_one_shot]: float-->
     <div class="form-group col">
       <label for="system-species-${specNum}-one_shot-${oneShotNumSpec}-t_one_shot">At Time</label>
       <input class="form-control" data-toggle="tooltip" id="system-species-${specNum}-one_shot-${oneShotNumSpec}-t_one_shot" name="system-species-${specNum}-one_shot-${oneShotNumSpec}-t_one_shot" title="" type="text" value="0.0" data-original-title="Time when addition occured.">
     </div>
   </div>`

   return html;
}

function makeSpeciesHTML(specNum) {

  const html_button =
  `<div class="form-group col-3">
     <button id="species-${specNum}-control" class="btn btn-block btn-primary collapse-control" type="button" data-toggle="collapse" data-target="#species-${specNum}" aria-expanded="false" aria-controls="species-${specNum}">
      Species ${specNum + 1}
      <i class="fa fa-chevron-down pt-1 float-right" aria-hidden="true"></i>
     </button>
   </div>`

  const html_collapse =
  `<div id="species-${specNum}" class="form-control collapse" aria-labelledby="species-${specNum}-control" data-parent="#species-container" style="">

    <div class="form-row">
      <!-- Species Name [spec_name]: string (def. “Species X”) -->
      <div class="form-group col">
        <label for="system-species-${specNum}-spec_name">Species Name</label>
        <input class="form-control spec-name" data-toggle="tooltip" id="system-species-${specNum}-spec_name" name="system-species-${specNum}-spec_name" placeholder="Species ${specNum + 1}" title="" type="text" value="" data-original-title="Name of species.">
      </div>
      <!--Initial Moles [mol0]: float-->
      <div class="form-group col">
        <label for="system-species-${specNum}-mol0">Initial Moles</label>
        <input class="form-control" data-toggle="tooltip" id="system-species-${specNum}-mol0" name="system-species-${specNum}-mol0" title="" type="number" value="0" data-original-title="Initial amount in moles">
      </div>
      <!--Column [col]: int-->
      <div class="form-group col">
        <label for="system-species-${specNum}-col">Generation Column</label>
        <input class="form-control" data-toggle="tooltip" id="system-species-${specNum}-col" name="system-species-${specNum}-col" title="" type="text" value="" data-original-title="Name or index, where 1 is the first column">
      </div>
    </div>

    <div class="collapse" id="system-species-${specNum}-apply_col">
      <!--Column [col]: int-->
      <div class="form-row">
        <div class="form-group col-4">
            <label for="system-species-${specNum}-col">Application Column</label>
            <input class="form-control" data-toggle="tooltip" id="system-species-${specNum}-col" name="system-species-${specNum}-col-apply" title="" type="text" value="" data-original-title="Name or index, where 1 is the first column">
        </div>
      </div>
    </div>

    <!--
    Group some lesser-used options into rows to save space
      Continuous Addition | Instantaneous Addition
    -->
    <div id="additions-container-species-${specNum}">
      <div class="form-row mt-2">
        <div class="col">
          <a id="cont-add-control-species-${specNum}" class="btn btn-block btn-secondary collapse-control" data-toggle="collapse" href="#cont-add-species-${specNum}" role="button" aria-expanded="false" aria-controls="cont-add-species-${specNum}">
            Continuous Addition
          </a>
        </div>
        <div class="col">
          <a id="one-shot-control-species-${specNum}" class="btn btn-block btn-secondary collapse-control" data-toggle="collapse" href="#one-shot-species-${specNum}" role="button" aria-expanded="false" aria-controls="one-shot-species-${specNum}">
            Instantaneous Addition
          </a>
        </div>

        <!--  Add Continuous Addition [0+]: [checkbox]
          Should be made collapsible
        -->
        <div id="cont-add-species-${specNum}" class="collapse" aria-labelledby="cont-add-control-species-${specNum}" data-parent="#additions-container-species-${specNum}">
          <div id="cont-add-species-${specNum}-rows">
          </div>
          <div class="form-row px-3 pt-2">
            <div class="col-sm-4">
                <button type="button" class="btn btn-sm btn-outline-primary float-left add-cont" id="add-cont-species-${specNum}">
                    <i class="fa fa-plus"></i> Addition
                </button>
            </div>
            <div class="col-sm-4"></div>
            <div class="col-sm-4">
                <button type="button" class="btn btn-sm btn-outline-primary float-right del-cont" id="del-cont-species-${specNum}">
                    <i class="fa fa-minus"></i> Addition
                </button>
            </div>
          </div>
        </div>

        <!--  Add Instantaneous Addition [0+]: [checkbox]
              Should be collabsible
        -->
        <div id="one-shot-species-${specNum}" class="collapse" aria-labelledby="one-shot-control-species-${specNum}" data-parent="#additions-container-species-${specNum}">
          <div id="one-shot-species-${specNum}-rows">
          </div>
          <div class="form-row px-3 pt-2">
            <div class="col-sm-4">
                <button type="button" class="btn btn-sm btn-outline-primary float-left add-oneshot" id="add-oneshot-species-${specNum}">
                    <i class="fa fa-plus"></i> Addition
                </button>
            </div>
            <div class="col-sm-4"></div>
            <div class="col-sm-4">
                <button type="button" class="btn btn-sm btn-outline-primary float-right del-oneshot" id="del-oneshot-species-${specNum}">
                    <i class="fa fa-minus"></i> Addition
                </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>`
  return [html_button, html_collapse];

}