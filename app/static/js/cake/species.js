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

    // If New Cont Add Button is Pressed, add another continuous addition row
    $(".add-cont" ).click(addContHandler);

    // If Del Cont Add Button is Pressed, remove continuous addition row if there are any
    $(".del-cont" ).click(delContHandler);

    // If New One Shot Button is Pressed, add another instantaneous addition row
    $(".add-oneshot" ).click(addOneShotHandler);

    // If Del One Shot Button is Pressed, remove instantaneous addition row if there are any
    $(".del-oneshot" ).click(delOneShotHandler);

    // If a species name changes, update the name on it's corresponding drop-down button
    $(".spec-name").change(specNameChangeHandler);

    // Configure changes in collapse control buttons during show / hide events
    $('.collapse').on('show.bs.collapse', collapseShowHandler);
    $('.collapse').on('hide.bs.collapse', collapseHideHandler);

    // Addition solution concentration must be constant between all addition forms
    $(".sol-conc").change(makeMatchingConcHandler);

    // Use for Fitting is only active if column has a value
    $(".species-col").change(enableFittingHandler);

});


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
    $(".add-cont" ).click(addContHandler);
    $(".del-cont" ).click(delContHandler);
    $(".add-oneshot" ).click(addOneShotHandler);
    $(".del-oneshot" ).click(delOneShotHandler);
    $(".spec-name").change(specNameChangeHandler);
    $('.collapse').on('show.bs.collapse', collapseShowHandler);
    $('.collapse').on('hide.bs.collapse', collapseHideHandler);
    $(".sol-conc").change(makeMatchingConcHandler);
    $(".species-col").change(enableFittingHandler);

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
    // append to the species data form
    $("#cont-add-species-" + species + "-rows").append(addContHTML);

    // make this solution concentration match others that are already set
    const curr_val = $("#rxn_info-species-" + species + "-cont_add-0-add_sol_conc").val();
    $("#rxn_info-species-" + species + "-cont_add-" + contAddNum[parseInt(species)] + "-add_sol_conc").val(curr_val);

    // add necessary event listeners
    $(".sol-conc").change(makeMatchingConcHandler);

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
    // append to the species data form
    $("#one-shot-species-" + species + "-rows").append(oneShotHTML);

    // make this solution concentration match others that are already set
    const curr_val = $("#rxn_info-species-" + species + "-one_shot-0-add_sol_conc").val();
    $("#rxn_info-species-" + species + "-one_shot-" + oneShotNum[parseInt(species)] + "-add_sol_conc").val(curr_val);

    // add necessary event listeners
    $(".sol-conc").change(makeMatchingConcHandler);

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
    // rxn_info-species-${specNum}-spec_name
    species = this.id.split("-")[2];

    // get corresponding button
    $("#species-" + species + "-control").html(`${this.value} <i class="fa fa-chevron-down pt-1 float-right" aria-hidden="true"></i>`)
}


function collapseShowHandler() {
    const button_id = $(this).attr("aria-labelledby");
    $("#" + button_id).addClass('active');
}


function collapseHideHandler() {
    const button_id = $(this).attr("aria-labelledby");
    $("#" + button_id).removeClass('active');
}


function enableFittingHandler() {
    // rxn_info-species-${specNum}-col
    species = this.id.split("-")[2];
    if( !$(this).val() ) {
        $('#rxn_info-species-' + species + '-for_fitting').prop("disabled", true);
    }
    else {
        $('#rxn_info-species-' + species + '-for_fitting').prop("disabled", false);
    }
}


function makeMatchingConcHandler() {
    // "rxn_info-species-${specNum}-cont_add-${contAddNumSpec}-add_sol_conc"
    // "rxn_info-species-${specNum}-one_shot-${oneShotNumSpec}-add_sol_conc"
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
       <label for="rxn_info-species-${specNum}-cont_add-${contAddNumSpec}-add_sol_conc">Addition Solution Conc.</label>
       <input class="form-control sol-conc sol-conc-species-${specNum}" data-toggle="tooltip" id="rxn_info-species-${specNum}-cont_add-${contAddNumSpec}-add_sol_conc" name="rxn_info-species-${specNum}-cont_add-${contAddNumSpec}-add_sol_conc" required="" title="" type="text" value="" data-original-title="Concentration of reagent added.">
     </div>
     <!--At Continuous Rate [add_cont_rate]: float-->
     <div class="form-group col">
       <label for="rxn_info-species-${specNum}-cont_add-${contAddNumSpec}-add_cont_rate">Rate of Addition</label>
       <input class="form-control" data-toggle="tooltip" id="rxn_info-species-${specNum}-cont_add-${contAddNumSpec}-add_cont_rate" name="rxn_info-species-${specNum}-cont_add-${contAddNumSpec}-add_cont_rate" required="" title="" type="text" value="" data-original-title="Rate of addition in moles_unit volume_unit^-1 time_unit^-1.">
     </div>
     <!--After Time [t_cont_rate]: float-->
     <div class="form-group col">
       <label for="rxn_info-species-${specNum}-cont_add-${contAddNumSpec}-t_cont_rate">After Time</label>
       <input class="form-control" data-toggle="tooltip" id="rxn_info-species-${specNum}-cont_add-${contAddNumSpec}-t_cont_rate" name="rxn_info-species-${specNum}-cont_add-${contAddNumSpec}-t_cont_rate" title="" type="text" value="0.0" data-original-title="Time when addition began.">
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
       <label for="rxn_info-species-${specNum}-one_shot-${oneShotNumSpec}-add_sol_conc">Addition Solution Conc.</label>
       <input class="form-control sol-conc sol-conc-species-${specNum}" data-toggle="tooltip" id="rxn_info-species-${specNum}-one_shot-${oneShotNumSpec}-add_sol_conc" name="rxn_info-species-${specNum}-one_shot-${oneShotNumSpec}-add_sol_conc" required="" title="" type="text" value="" data-original-title="Concentration of reagent added.">
     </div>
     <!--Volume Added [add_v_one_shot]: float-->
     <div class="form-group col">
       <label for="rxn_info-species-${specNum}-one_shot-${oneShotNumSpec}-add_v_one_shot">Volume Added</label>
       <input class="form-control" data-toggle="tooltip" id="rxn_info-species-${specNum}-one_shot-${oneShotNumSpec}-add_v_one_shot" name="rxn_info-species-${specNum}-one_shot-${oneShotNumSpec}-add_v_one_shot" required="" title="" type="text" value="" data-original-title="Volume of solution added in volume_unit.">
     </div>
     <!--At Time [t_one_shot]: float-->
     <div class="form-group col">
       <label for="rxn_info-species-${specNum}-one_shot-${oneShotNumSpec}-t_one_shot">At Time</label>
       <input class="form-control" data-toggle="tooltip" id="rxn_info-species-${specNum}-one_shot-${oneShotNumSpec}-t_one_shot" name="rxn_info-species-${specNum}-one_shot-${oneShotNumSpec}-t_one_shot" title="" type="text" value="0.0" data-original-title="Time when addition occured.">
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
    <!--Use For Fitting: [checkbox]-->
    <!--Greyed out if column is not given-->
    <div class="form-row">
      <div class="form-check">
        <input data-toggle="tooltip" id="rxn_info-species-${specNum}-for_fitting" name="rxn_info-species-${specNum}-for_fitting" title="" type="checkbox" value="y" data-original-title="Use this species to perform CAKE fitting." disabled>
        <label for="rxn_info-species-${specNum}-for_fitting">Use For Fitting</label>
      </div>
    </div>

    <div class="form-row">
      <!-- Species Name [spec_name]: string (def. “Species X”) -->
      <div class="form-group col">
        <label for="rxn_info-species-${specNum}-spec_name">Species Name</label>
        <input class="form-control spec-name" data-toggle="tooltip" id="rxn_info-species-${specNum}-spec_name" name="rxn_info-species-${specNum}-spec_name" placeholder="Species ${specNum + 1}" title="" type="text" value="" data-original-title="Name of species.">
      </div>
      <!--Species Type [spec_type]: “r”, “p”, or “c” -->
      <div class="form-group col">
        <label for="rxn_info-species-${specNum}-spec_type">Species Type</label>
        <select class="form-control" data-toggle="tooltip" id="rxn_info-species-${specNum}-spec_type" name="rxn_info-species-${specNum}-spec_type" required="" title="" data-original-title="Type of Species (reactant, product, catalyst)."><option value="r">Reactant</option><option value="p">Product</option><option value="c">Catalyst</option></select>
      </div>
      <!--Stoichiometry [stoich]: int (default 1 for r/p, None for c)-->
      <div class="form-group col">
        <label for="rxn_info-species-${specNum}-stoich">Stoichiometry</label>
        <input class="form-control" data-toggle="tooltip" id="rxn_info-species-${specNum}-stoich" name="rxn_info-species-${specNum}-stoich" required="" title="" type="number" value="1" data-original-title="Stoichiometric coefficient of species.">
      </div>
    </div>

    <div class="form-row">
      <!--Column [col]: int-->
      <div class="form-group col">
        <label for="rxn_info-species-${specNum}-col">Column</label>
        <input class="form-control species-col" data-toggle="tooltip" id="rxn_info-species-${specNum}-col" min="1" name="rxn_info-species-${specNum}-col" required="" title="" type="number" value="" data-original-title="Integer index, 1 is the first column.">
      </div>
      <!--Initial Moles [mol_init]: float-->
      <div class="form-group col">
        <label for="rxn_info-species-${specNum}-mol_init">Initial Moles</label>
        <input class="form-control" data-toggle="tooltip" id="rxn_info-species-${specNum}-mol_init" name="rxn_info-species-${specNum}-mol_init" title="" type="text" value="" data-original-title="Initial amount in moles.">
      </div>
      <!--Final Moles [mol_end]: float-->
      <div class="form-group col">
        <label for="rxn_info-species-${specNum}-mol_end">Final Moles</label>
        <input class="form-control" data-toggle="tooltip" id="rxn_info-species-${specNum}-mol_end" name="rxn_info-species-${specNum}-mol_end" title="" type="text" value="" data-original-title="Final amount in moles">
      </div>
    </div>

    <!--
    Group some lesser-used options into rows to save space
      1. Order Limits | Poison Limits
    -->
    <div id="limits-container-species-${specNum}">
      <div class="form-row">
        <div class="col">
          <a id="ord-control-species-${specNum}" class="btn btn-block btn-secondary collapse-control" data-toggle="collapse" href="#ord-limits-species-${specNum}" role="button" aria-expanded="false" aria-controls="ord-limits-species-${specNum}">
            Specify Order Limits
          </a>
        </div>
        <div class="col">
          <a id="pois-control-species-${specNum}" class="btn btn-block btn-secondary collapse-control" data-toggle="collapse" href="#pois-limits-species-${specNum}" role="button" aria-expanded="false" aria-controls="pois-limits-species-${specNum}">
            Specify Poisoning Limits
          </a>
        </div>

        <!--  Specify Ord Limits [0-1] [ord_lim]: [checkbox]
          This should be made collapsible.
        -->
        <div id="ord-limits-species-${specNum}" class="collapse" aria-labelledby="ord-control" data-parent="#limits-container-species-${specNum}">
          <div class="form-row m-1">
            <!--Est Order [ord_val] (default 1): float-->
            <div class="form-group col">
              <label for="rxn_info-species-${specNum}-ord_val">Est Order</label>
              <input class="form-control" data-toggle="tooltip" id="rxn_info-species-${specNum}-ord_val" name="rxn_info-species-${specNum}-ord_val" title="" type="text" value="1" data-original-title="Estimated species order">
            </div>
            <!--Min Order [ord_min] (default 0): float-->
            <div class="form-group col">
              <label for="rxn_info-species-${specNum}-ord_min">Min Order</label>
              <input class="form-control" data-toggle="tooltip" id="rxn_info-species-${specNum}-ord_min" name="rxn_info-species-${specNum}-ord_min" title="" type="text" value="0" data-original-title="Minimum species order search constraint">
            </div>
            <!--Max Order [ord_max] (default 2): float-->
            <div class="form-group col">
              <label for="rxn_info-species-${specNum}-ord_max">Max Order</label>
              <input class="form-control" data-toggle="tooltip" id="rxn_info-species-${specNum}-ord_max" name="rxn_info-species-${specNum}-ord_max" title="" type="text" value="2" data-original-title="Maximum species order search constraint">
            </div>
          </div>
        </div>

        <!--  Specify Poison Limits [0-1] [pois_lim]: [checkbox]
              This should also be made collapsible
        -->
        <div id="pois-limits-species-${specNum}" class="collapse" aria-labelledby="pois-control" data-parent="#limits-container-species-${specNum}">
          <div class="form-row m-1">
            <!--Est Poisoning [pois_val] (default 0): float-->
            <div class="form-group col">
              <label for="rxn_info-species-${specNum}-pois_val">Est Poisoning</label>
              <input class="form-control" data-toggle="tooltip" id="rxn_info-species-${specNum}-pois_val" name="rxn_info-species-${specNum}-pois_val" title="" type="text" value="0" data-original-title="Estimated species poisoning">
            </div>
            <!--Min Poisoning [pois_min] (default 0): float-->
            <div class="form-group col">
              <label for="rxn_info-species-${specNum}-pois_min">Min Poisoning</label>
              <input class="form-control" data-toggle="tooltip" id="rxn_info-species-${specNum}-pois_min" name="rxn_info-species-${specNum}-pois_min" title="" type="text" value="" data-original-title="Minimum species poisoning search constraint">
            </div>
            <!--Max Poisoning [pois_max] (default 0): float-->
            <div class="form-group col">
              <label for="rxn_info-species-${specNum}-pois_max">Max Poisoning</label>
              <input class="form-control" data-toggle="tooltip" id="rxn_info-species-${specNum}-pois_max" name="rxn_info-species-${specNum}-pois_max" title="" type="text" value="" data-original-title="Maximum species poisoning search constraint">
            </div>
          </div>
        </div>

      </div>
    </div>

    <!--
    Group some lesser-used options into rows to save space
      2. Continuous Addition | Instantaneous Addition
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