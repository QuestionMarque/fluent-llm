from execution_engine.models.workflow import Workflow, Step


def simple_distribution():
    return Workflow(
        steps=[
            Step(
                type="reagent_distribution",
                params={
                    "volume_uL": 50,
                    "liquid": "DPBS",
                    "liquid_class": "Water_Free",
                    "tip_type": "FCA_DiTi_200uL",
                    "source": "Trough_25mL:A1",
                    "target": "Plate_96:A1"
                }
            )
        ]
    )


def distribution_with_incubation():
    return Workflow(
        steps=[
            Step(
                type="reagent_distribution",
                params={
                    "volume_uL": 30,
                    "liquid": "DPBS",
                    "liquid_class": "Water_Free",
                    "tip_type": "FCA_DiTi_50uL",
                    "source": "Trough_25mL:A1",
                    "target": "Plate_96:B1"
                }
            ),
            Step(
                type="incubate",
                params={
                    "time_s": 300,
                    "location": "Heated_Incubator",
                    "labware": "Plate_96"
                }
            )
        ]
    )


def distribution_mix_incubate():
    return Workflow(
        steps=[
            Step(
                type="reagent_distribution",
                params={
                    "volume_uL": 20,
                    "liquid": "DPBS",
                    "liquid_class": "Water_Free",
                    "tip_type": "FCA_DiTi_50uL",
                    "source": "Trough_25mL:A1",
                    "target": "Plate_96:C1"
                }
            ),
            Step(
                type="mix",
                params={
                    "volume_uL": 15,
                    "cycles": 3,
                    "target": "Plate_96:C1",
                    "liquid_class": "Water_Free",
                    "tip_type": "FCA_DiTi_50uL" 
                }
            ),
            Step(
                type="incubate",
                params={
                    "time_s": 600,
                    "location": "Heated_Incubator",
                    "labware": "Plate_96"
                }
            )
        ]
    )

# very simple example with just get_tips with all parameters
def just_tips():
    return Workflow(
        steps = [
            Step(
                type = "get_tips",
                params = {
                    "diti_type":"FCA_DiTi_200uL",
                    "airgap_volume":70, 
                    "airgap_speed":100, 
                    "tip_indices":[0,1,2,3,4,5,6,7]
                }
            ),
        ]
    )

# transfer samples from first column of sample_plate to first column of dilution_plate
def transfer_samples_plate_to_plate():
    return Workflow(
        steps = [
            Step(
                type = "get_tips",
                params = {
                    "diti_type":"FCA_DiTi_200uL",
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 50,
                    "labware": "sample_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offsets":[0,1,2,3,4,5,6,7],
                    "tip_indices": [0,1,2,3,4,5,6,7]
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 50,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offsets":[0,1,2,3,4,5,6,7],
                    "tip_indices": [0,1,2,3,4,5,6,7]
                }
            ),
            Step(
                type = "drop_tips_to_location",
                params = {
                    "labware":"DiTi_waste"
                }
            )
        ]
    )

# transfer samples from tubes to first column of dilution_plate
def transfer_samples_tubes_to_plate():
    return Workflow(
        steps = [
            Step(
                type = "get_tips",
                params = {
                    "diti_type":"FCA_DiTi_200uL",
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 100,
                    "labware": "tube_runner",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(8))
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 100,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(8))
                }
            ),
            Step(
                type = "drop_tips_to_location",
                params = {
                    "labware":"DiTi_waste"
                }
            )
        ]
    )

# add diluent from diluent trough to dilution plate, transfer samples from tubes to first two columns of dilution_plate and mix
def dilute_samples_from_tube():
    return Workflow(
        steps = [
            Step(
                type = "get_tips",
                params = {
                    "diti_type":"FCA_DiTi_200uL",
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 100,
                    "labware": "diluent_reservoir",
                    "liquid_class": "Water_Free_Multi",
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 50,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Multi",
                    "well_offset":list(range(8))
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 50,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Multi",
                    "well_offset":list(range(8,16))
                }
            ),
            Step(
                type = "drop_tips_to_location",
                params = {
                    "labware":"DiTi_waste"
                }
            ),
            Step(
                type = "get_tips",
                params = {
                    "diti_type":"FCA_DiTi_200uL",
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 50,
                    "labware": "tube_runner",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(8))
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 50,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(8))
                }
            ),
            Step(
                type = "drop_tips_to_location",
                params = {
                    "labware":"DiTi_waste"
                }
            ),
            Step(
                type = "get_tips",
                params = {
                    "diti_type":"FCA_DiTi_200uL",
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 50,
                    "labware": "tube_runner",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(8,16))
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 50,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(8,16))
                }
            ),
            Step(
                type = "drop_tips_to_location",
                params = {
                    "labware":"DiTi_waste"
                }
            ),            
        ]
    )

# perform serial dilution in plate dilution_plate without changing tips
def serial_dilution():
    return Workflow(
        steps = [
            Step(
                type = "get_tips",
                params = {
                    "diti_type":"FCA_DiTi_200uL",
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(8))
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(8,16)),
                }
            ),
            Step(
                type = "mix_volume",
                params = {
                    "volumes":40,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Mix",
                    "well_offsets":list(range(8,16)),
                    "cycles":2
                }
            ),
            Step(
                type= "empty_tips",
                params = {
                    "labware": "dilution_plate",
                    "liquid_class": "Empty Tip",
                    "well_offsets": list(range(8,16)),
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(8,16))
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(16,24)),
                }
            ),
            Step(
                type = "mix_volume",
                params = {
                    "volumes":40,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Mix",
                    "well_offsets":list(range(16,24)),
                    "cycles":2
                }
            ),
            Step(
                type= "empty_tips",
                params = {
                    "labware": "dilution_plate",
                    "liquid_class": "Empty Tip",
                    "well_offsets": list(range(16,24)),
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(16,24))
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(24,32)),
                }
            ),
            Step(
                type = "mix_volume",
                params = {
                    "volumes":40,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Mix",
                    "well_offsets":list(range(24,32)),
                    "cycles":2
                }
            ),
            Step(
                type= "empty_tips",
                params = {
                    "labware": "dilution_plate",
                    "liquid_class": "Empty Tip",
                    "well_offsets": list(range(24,32)),
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(24,32))
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(32,40)),
                }
            ),
            Step(
                type = "mix_volume",
                params = {
                    "volumes":40,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Mix",
                    "well_offsets":list(range(32,40)),
                    "cycles":2
                }
            ),
            Step(
                type= "empty_tips",
                params = {
                    "labware": "dilution_plate",
                    "liquid_class": "Empty Tip",
                    "well_offsets": list(range(32,40)),
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(32,40))
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(40,48)),
                }
            ),
            Step(
                type = "mix_volume",
                params = {
                    "volumes":40,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Mix",
                    "well_offsets":list(range(40,48)),
                    "cycles":2
                }
            ),
            Step(
                type= "empty_tips",
                params = {
                    "labware": "dilution_plate",
                    "liquid_class": "Empty Tip",
                    "well_offsets": list(range(40,48)),
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(40,48))
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(48,56)),
                }
            ),
            Step(
                type = "mix_volume",
                params = {
                    "volumes":40,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Mix",
                    "well_offsets":list(range(48,56)),
                    "cycles":2
                }
            ),
            Step(
                type= "empty_tips",
                params = {
                    "labware": "dilution_plate",
                    "liquid_class": "Empty Tip",
                    "well_offsets": list(range(48,56)),
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(48,56))
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(56,64)),
                }
            ),
            Step(
                type = "mix_volume",
                params = {
                    "volumes":40,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Mix",
                    "well_offsets":list(range(56,64)),
                    "cycles":2
                }
            ),
            Step(
                type= "empty_tips",
                params = {
                    "labware": "dilution_plate",
                    "liquid_class": "Empty Tip",
                    "well_offsets": list(range(56,64)),
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(56,64))
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(64,72)),
                }
            ),
            Step(
                type = "mix_volume",
                params = {
                    "volumes":40,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Mix",
                    "well_offsets":list(range(64,72)),
                    "cycles":2
                }
            ),
            Step(
                type= "empty_tips",
                params = {
                    "labware": "dilution_plate",
                    "liquid_class": "Empty Tip",
                    "well_offsets": list(range(64,72)),
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(64,72))
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(72,80)),
                }
            ),
            Step(
                type = "mix_volume",
                params = {
                    "volumes":40,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Mix",
                    "well_offsets":list(range(72,80)),
                    "cycles":2
                }
            ),
            Step(
                type= "empty_tips",
                params = {
                    "labware": "dilution_plate",
                    "liquid_class": "Empty Tip",
                    "well_offsets": list(range(72,80)),
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(72,80))
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(80,88)),
                }
            ),
            Step(
                type = "mix_volume",
                params = {
                    "volumes":40,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Mix",
                    "well_offsets":list(range(80,88)),
                    "cycles":2
                }
            ),
            Step(
                type= "empty_tips",
                params = {
                    "labware": "dilution_plate",
                    "liquid_class": "Empty Tip",
                    "well_offsets": list(range(80,88)),
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(80,88))
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(88,96)),
                }
            ),
            Step(
                type = "mix_volume",
                params = {
                    "volumes":40,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Mix",
                    "well_offsets":list(range(88,96)),
                    "cycles":2
                }
            ),
            Step(
                type= "empty_tips",
                params = {
                    "labware": "dilution_plate",
                    "liquid_class": "Empty Tip",
                    "well_offsets": list(range(88,96)),
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 25,
                    "labware": "dilution_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":list(range(88,96))
                }
            ),
            Step(
                type = "drop_tips_to_location",
                params = {
                    "labware":"DiTi_waste"
                }
            ),
        ]
    )

# add diluent from diluent_trough to dilution_plate and add samples from plate (full plate)
def dilute_samples_from_full_plate():
    return Workflow(
        steps = [
            Step(
                type = "reagent_distribution",
                params = {
                    "labware_empty_tips": "diluent_trough",
                    "volumes": 25,
                    "sample_count": 96,
                    "DiTi_type": "FCA_DiTi_1000uL",
                    "DiTi_waste": "DiTi_waste",
                    "labware_source": "diluent_trough",
                    "labware_target": "dilution_plate",
                    "selected_wells_source":0,
                    "selected_wells_target":list(range(96)),
                    "liquid_class": "Water_Free_Multi",
                }
            ),
            Step(
                type = "sample_transfer",
                params = {
                    "labware_empty_tips": "Liquid_waste",
                    "volumes": 25,
                    "sample_count": 96,
                    "DiTi_type": "FCA_DiTi_200uL",
                    "DiTi_waste": "DiTi_waste",
                    "labware_source": "sample_plate",
                    "labware_target": "dilution_plate",
                    "selected_wells_source": list(range(96)),
                    "selected_wells_target": list(range(96)),
                    "liquid_class": "Water_Free_Single",
                    "tips_per_well_source": 1,
                }
            )
        ]
    )

# transfer samples from tubes to plate (3 replicates per sample):
def sample_tube_to_plate_replicates():
    return Workflow(
        steps = [
            Step(
                type = "sample_transfer",
                params = {
                    "labware_empty_tips": "Liquid_waste",
                    "volumes": 50,
                    "sample_count": 16,
                    "DiTi_type": "FCA_DiTi_10000uL",
                    "DiTi_waste": "DiTi_waste",
                    "labware_source": "tube_runner",
                    "labware_target": "dilution_plate",
                    "selected_wells_source": list(range(16)),
                    "selected_wells_target": list(range(96)),
                    "liquid_class": "Water_Free_Multi",
                    "sample_direction": "ColumnWise",
                    "number_replicates": 3,
                    "replicate_direction": "RowWise",
                    "tips_per_well_source": 1,
                }
            )
        ]
    )

# get plate from hotel, fill with reagent, add sample, return to hotel
def fill_plate_hotel():
    return Workflow(
        steps = [
            Step(
                type = "transfer_labware",
                params = {
                    "labware_name":"96_plate",
                    "target_location":"Nest_61mm",
                    "target_position":1,
                }
            ),
            Step(
                type = "reagent_distribution",
                params = {
                    "labware_empty_tips": "Liquid_waste",
                    "volumes": 50,
                    "sample_count": 16,
                    "DiTi_type": "FCA_DiTi_1000uL",
                    "DiTi_waste": "DiTi_waste",
                    "labware_source": "reagentA",
                    "labware_target": "96_plate",
                    "selected_wells_source":0,
                    "selected_wells_target":list(range(96)),
                    "liquid_class": "Water_Free_Multi",
                }
            ),
            Step(
                type = "get_tips",
                params = {
                    "diti_type":"FCA_DiTi_200uL",
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 50,
                    "labware": "sample_tubes",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":[0,1,2,3,4,5,6,7]
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 50,
                    "labware": "96_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":[0,1,2,3,4,5,6,7]
                }
            ),
            Step(
                type = "drop_tips_to_location",
                params = {
                    "labware":"DiTi_waste"
                }
            ),
            Step(
                type = "get_tips",
                params = {
                    "diti_type":"FCA_DiTi_200uL",
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes": 50,
                    "labware": "sample_tubes",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":[8,9,10,11,12,13,14,15]
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes": 50,
                    "labware": "96_plate",
                    "liquid_class": "Water_Free_Single",
                    "well_offset":[8,9,10,11,12,13,14,15]
                }
            ),
            Step(
                type = "drop_tips_to_location",
                params = {
                    "labware":"DiTi_waste"
                }
            ),
            Step(
                type = "transfer_labware",
                params = {
                    "labware_name":"96_plate",
                    "target_location":"Hotel",
                    "target_position":1,
                }
            ),
        ]
    )

# distribute Antisera to first column of a plate
def distribute_antisera():
    return Workflow(
        steps = [
            Step(
                type = "get_tips",
                params = {
                    "diti_type": "FCA_DiTi_200uL",
                    "tip_indices":list(range(8))
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes" : [50]*4, 
                    "labware" : "Antisera_1",
                    "liquid_class" : "LIQ_CLASS_ANTISERA",
                    "well_offsets" : list(range(4)),
                    "tip_indices" : list(range(4)), 
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes" : [0] * 4 + [50] * 4, 
                    "labware" : "Antisera_2",
                    "liquid_class" : "LIQ_CLASS_ANTISERA",
                    "well_offsets" : list(range(4)),
                    "tip_indices" : list(range(4,8)), 
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [50]*8,
                    "labware" : "plate_96",
                    "liquid_class" : "LIQ_CLASS_ANTISERA",
                    "well_offsets" : list(range(8)), 
                    "tip_indices" : list(range(8)), 
                }
            ),
            Step(
                type = "drop_tips_to_location",
                params = {
                    "labware":"DiTi_waste"
                }
            )
        ]
    )

# distribute Antigens to plate
def distribute_antigens():
    return Workflow(
        steps = [
            Step(
                type = "get_tips",
                params = {
                    "diti_type" : "FCA_DiTi_1000uL",
                    "tip_indices":list(range(8))
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes" : [25*12]*8, 
                    "labware" : "LABWARE_ANTIGEN_A",
                    "liquid_class" : "LIQ_CLASS_ANTIGEN",
                    "well_offsets":[0]*8,
                    "tip_indices":list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [25]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_ANTIGEN",
                    "well_offsets" : list(range(8)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [25]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_ANTIGEN",
                    "well_offsets" : list(range(8, 16)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [25]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_ANTIGEN",
                    "well_offsets" : list(range(16,24)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [25]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_ANTIGEN",
                    "well_offsets" : list(range(24,32)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [25]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_ANTIGEN",
                    "well_offsets" : list(range(32,40)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [25]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_ANTIGEN",
                    "well_offsets" : list(range(40,48)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [25]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_ANTIGEN",
                    "well_offsets" : list(range(48,56)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [25]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_ANTIGEN",
                    "well_offsets" : list(range(56,64)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [25]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_ANTIGEN",
                    "well_offsets" : list(range(64,72)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [25]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_ANTIGEN",
                    "well_offsets" : list(range(72,80)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [25]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_ANTIGEN",
                    "well_offsets" : list(range(80,88)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [25]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_ANTIGEN",
                    "well_offsets" : list(range(88,96)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "empty_tips",
                params = {
                    "labware" : "LABWARE_ANTIGEN_A",
                    "tip_indices" : list(range(8))
                }
            ),
            Step(
                type = "drop_tips_to_location",
                params = {
                    "labware" : "DITI_WASTE",
                    "tip_indices" : list(range(8))
                }
            )
        ]
    )

# add tRBC to plate
def add_tRBC():
    return Workflow(
        steps = [
            Step(
                type = "get_tips",
                params = {
                    "diti_type" : "FCA_DiTi_1000uL",
                    "tip_indices":list(range(8))
                }
            ),
            Step(
                type = "mix_volume",
                params = {
                    "labware" : 'tRBC',
                    "volumes" : 800,
                    "liquid_class" : 'Water Mix',
                    "cycles" : 5,
                    "well_offsets" : 0
                }
            ),
            Step(
                type = "empty_tips",
                params = {
                    "labware" : 'tRBC',
                    "well_offsets" : None
                }
            ),
            Step(
                type = "aspirate_volume",
                params = {
                    "volumes":[50*12]*8,  
                    "labware":"LABWARE_TRBC",
                    "liquid_class":"LIQ_CLASS_TRBC",
                    "well_offsets":[0]*8,  
                    "tip_indices":list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [50]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_TRBC",
                    "well_offsets" : list(range(8)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [50]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_TRBC",
                    "well_offsets" : list(range(8,16)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [50]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_TRBC",
                    "well_offsets" : list(range(16,24)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [50]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_TRBC",
                    "well_offsets" : list(range(24,32)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [50]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_TRBC",
                    "well_offsets" : list(range(32,40)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [50]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_TRBC",
                    "well_offsets" : list(range(40,48)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [50]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_TRBC",
                    "well_offsets" : list(range(48,56)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [50]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_TRBC",
                    "well_offsets" : list(range(56,64)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [50]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_TRBC",
                    "well_offsets" : list(range(64,72)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [50]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_TRBC",
                    "well_offsets" : list(range(72,80)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [50]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_TRBC",
                    "well_offsets" : list(range(80,88)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "dispense_volume",
                params = {
                    "volumes" : [50]*8,
                    "labware" : "plate",
                    "liquid_class" : "LIQ_CLASS_TRBC",
                    "well_offsets" : list(range(88,96)),
                    "tip_indices" : list(range(8)),
                }
            ),
            Step(
                type = "empty_tips",
                params = {
                    "labware":"LABWARE_TRBC"
                }
            ),
            Step(
                type = "drop_tips_to_location",
                params = {
                    "labware" : "DITI_WASTE",
                    "tip_indices":list(range(8))
                }
            )
        ]
    )

