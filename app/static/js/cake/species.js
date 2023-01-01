let specNum = 1;

// list of ints. Index is species number and value is number of additions (continuous or one-shot) for that species.
let contAddNum = [1];
let oneShotNum = [1];

$(document).ready(function() {

    // If New Cont Add Button is Pressed, add another continuous addition row
    $( ".add-cont" ).click(addContHandler);

    // If Del Cont Add Button is Pressed, remove continuous addition row if there are any
    $( ".del-cont" ).click(delContHandler);

    // If New One Shot Button is Pressed, add another instantaneous addition row
    $( ".add-oneshot" ).click(addOneShotHandler);

    // If Del One Shot Button is Pressed, remove instantaneous addition row if there are any
    $( ".del-oneshot" ).click(delOneShotHandler);

});

function addContHandler() {
    // figure out which species this is being applied to
    const species = this.id.split("-")[3];
    // generate boilerplate html for the new addition form
    const addContHTML = makeContAddHTML(parseInt(species), contAddNum);
    // append to the species data form
    $("#cont-add-species-" + species + "-rows").append(addContHTML);
    // increment contAddNum
    contAddNum[parseInt(species)] += 1;
}

function delContHandler() {
    // figure out which species this is being applied to
    const species = this.id.split("-")[3];

    if (contAddNum[parseInt(species)] > 1) {
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
    // increment contAddNum
    oneShotNum[parseInt(species)] += 1;
}

function delOneShotHandler() {
    // figure out which species this is being applied to
    const species = this.id.split("-")[3];

    if (oneShotNum[parseInt(species)] > 1) {
        // remove the HTML element
        $("#one-shot-species-" + species + "-rows").children().last().remove();
        // decrement oneShotNum
        oneShotNum[parseInt(species)] -= 1;
    }
}

function makeContAddHTML(specNum, contAddNum) {
  const contAddNumSpec = contAddNum[specNum];

  const html =
  `<div class="form-row m-1">
     <!--Addition Solution Concentration [add_sol_conc]: float-->
     <div class="form-group col">
       <label for="rxn_info-species-${specNum}-cont_add-${contAddNumSpec}-add_sol_conc">Addition Solution Conc.</label>
       <input class="form-control" data-toggle="tooltip" id="rxn_info-species-${specNum}-cont_add-${contAddNumSpec}-add_sol_conc" name="rxn_info-species-${specNum}-cont_add-${contAddNumSpec}-add_sol_conc" required="" title="" type="text" value="" data-original-title="Concentration of reagent added.">
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
       <input class="form-control" data-toggle="tooltip" id="rxn_info-species-${specNum}-one_shot-${oneShotNumSpec}-add_sol_conc" name="rxn_info-species-${specNum}-one_shot-${oneShotNumSpec}-add_sol_conc" required="" title="" type="text" value="" data-original-title="Concentration of reagent added.">
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
