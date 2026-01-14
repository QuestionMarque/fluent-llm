"""Compiler for converting IR jobs into Fluent control worklists.

The compiler traverses the steps defined in an IR job and produces a list
of strings formatted according to the Gemini WorkList (.gwl) syntax
accepted by Tecan Fluent and Freedom EVOware.  Each string corresponds to
a single record in the worklist.  The mapping between IR operations and
worklist record types is deliberately simple for this prototype.  Refer
to the Tecan worklist documentation for the full set of record types and
parameters【6713682743180†L32-L40】【246479156155221†L96-L131】.

TODO: Support multi‑pipetting, mix commands, reagent distribution (R;),
flush (F;), break (B;), set DiTi type (S;) and comments (C;).  Many
record parameters (e.g., RackID, RackType, TubeID, LiquidClass, TipMask)
are optional or context dependent; consult the FluentControl manual to
implement them correctly.
"""

from typing import List
from .ir import IRJob, IRStep


def well_to_position(well: str) -> int:
    """Convert an alphanumeric well ID (e.g. 'A1') to a numeric position (1–96).

    The mapping is based on Tecan's convention where wells are counted
    from rear to front and left to right, with eight rows (A–H) in each
    column.  For example, A2 → 9【6713682743180†L91-L97】.
    """
    row = well[0].upper()
    col = int(well[1:])
    row_index = ord(row) - ord('A')
    # Ensure row_index is between 0 and 7
    if not (0 <= row_index < 8):
        raise ValueError(f"Invalid row letter in well ID: {well}")
    if col < 1 or col > 12:
        raise ValueError(f"Column out of range in well ID: {well}")
    return (col - 1) * 8 + row_index + 1


def compile_ir(job: IRJob) -> List[str]:
    """Compile an IR job into a list of worklist record lines.

    Args:
        job: The IR job to compile.

    Returns:
        A list of strings, each representing a line in the .gwl file.

    Raises:
        ValueError: If an unknown operation is encountered or required
            arguments are missing.
    """
    worklist_lines: List[str] = []
    for step in job.steps:
        if step.op == "transfer":
            src_labware = step.args.get("source_labware")
            src_well = step.args.get("source_well")
            dest_labware = step.args.get("dest_labware")
            dest_well = step.args.get("dest_well")
            vol = step.args.get("volume_uL")
            liquid_class = step.args.get("liquid_class", "Water")
            if None in (src_labware, src_well, dest_labware, dest_well, vol):
                raise ValueError(f"Missing argument for transfer in step {step.id}")
            src_pos = well_to_position(src_well)
            dest_pos = well_to_position(dest_well)
            # Build Aspirate record (A)
            # Format: A;RackLabel;RackID;RackType;Position;TubeID;Volume;LiquidClass;TipType;TipMask;ForcedRackType
            aspirate_line = f"A;{src_labware};;;{src_pos};;{vol:.2f};{liquid_class};;;"
            # Build Dispense record (D)
            dispense_line = f"D;{dest_labware};;;{dest_pos};;{vol:.2f};{liquid_class};;;"
            worklist_lines.append(aspirate_line)
            worklist_lines.append(dispense_line)
        elif step.op == "wash":
            scheme = step.args.get("scheme", 1)
            # Format: W<scheme>;
            worklist_lines.append(f"W{scheme};")
        elif step.op == "decontaminate":
            # Format: WD;
            worklist_lines.append("WD;")
        else:
            # Unknown operations cause compilation failure
            raise ValueError(f"Unknown operation '{step.op}' in step {step.id}")
    return worklist_lines