#!/usr/bin/env python
# additional padding space is added to the pockets, not to the fingers
import ezdxf
import math
from ezdxf import colors
from ezdxf.enums import TextEntityAlignment
from ezdxf.math import ConstructionArc
from ezdxf import units

endmill_diameter = 0.25
endmill_radius = endmill_diameter / 2
chord_length = math.sqrt(2 * endmill_radius ** 2)

plywood_thickness = 0.7
padding = 1/32
# padding = 0.111 # oversize of the holes. Does not apply to critical dimensions
notch_width = plywood_thickness
notch_length = 4

box_width = 47.5
box_length = 95.5
box_height = 7.5
nbraces = 8
ntabs = 3

finger_spacing = (box_length - (notch_length*(nbraces-2))) / (nbraces - 1)
y_finger_spacing = (box_width - ((notch_length + 2*padding) * ntabs))  / (ntabs + 1)
corner_finger_length = (box_height - 2*notch_width) / 2

# Create a new DXF document.
doc = ezdxf.new(dxfversion="R2010")
doc.header.custom_vars.append("Author", "Adam Spontarelli")
doc.units = units.IN
doc.header['$INSUNITS'] = units.CM


# Create new table entries (layers, linetypes, text styles, ...).
doc.layers.add("Pocket", color=colors.BLUE)
doc.layers.add("Plywood", color=colors.YELLOW)
doc.layers.add("Notes", color=colors.GREEN)

# DXF entities (LINE, TEXT, ...) reside in a layout (modelspace,
# paperspace layout or block definition).
msp = doc.modelspace()

def ccw_arc(sp, ep, color=colors.BLACK, layer="0"):
    if sp[0] > ep[0]:
        if sp[1] > ep[1]:
            dp =(sp[0] - chord_length, sp[1])
        else:
            dp =(sp[0], sp[1] + chord_length)
    else:
        if sp[1] > ep[1]:
            dp =(sp[0], sp[1] - chord_length)
        else:
            dp =(sp[0]+chord_length, sp[1])
    arc = ConstructionArc.from_3p(start_point=sp, end_point=ep, def_point=dp)
    arc.add_to_layout(msp, dxfattribs={"color": color, "layer": layer})

def cw_arc(sp, ep, color=colors.BLACK, layer="0"):
    if sp[0] > ep[0]:
        if sp[1] > ep[1]:
            dp =(sp[0], sp[1] - chord_length)
        else:
            dp =(sp[0] - chord_length, sp[1])
    else:
        if sp[1] > ep[1]:
            dp =(sp[0] + chord_length, sp[1])
        else:
            dp =(sp[0], sp[1] + chord_length)
    arc = ConstructionArc.from_3p(start_point=sp, end_point=ep, def_point=dp, ccw=False)
    arc.add_to_layout(msp, dxfattribs={"color": color, "layer": layer})


def pocket(start_point, width, height):
    """
    Starts bottom left and moves CCW.
    """
    end_point = (start_point[0] + width + 2*padding - 2*chord_length, start_point[1])
    msp.add_line(start_point, end_point, dxfattribs={"color": colors.BLUE, "layer": "Pocket"})

    start_point = end_point
    end_point = (start_point[0] + chord_length, start_point[1] + chord_length)
    ccw_arc(start_point, end_point, color=colors.BLUE, layer="Pocket")

    # right vert
    start_point = end_point
    end_point = (end_point[0], end_point[1]+height+2*padding - 2*chord_length)
    msp.add_line(start_point, end_point, dxfattribs={"color": colors.BLUE, "layer": "Pocket"})

    start_point = end_point
    end_point = (start_point[0] - chord_length, start_point[1] + chord_length)
    ccw_arc(start_point, end_point, color=colors.BLUE, layer="Pocket")

    # top horiz
    start_point = end_point
    end_point = (end_point[0]-width-2*padding+2*chord_length, end_point[1])
    msp.add_line(start_point, end_point, dxfattribs={"color": colors.BLUE, "layer": "Pocket"})

    start_point = end_point
    end_point = (start_point[0] - chord_length, start_point[1] - chord_length)
    ccw_arc(start_point, end_point, color=colors.BLUE, layer="Pocket")

    # left side
    start_point = end_point
    end_point = (end_point[0], end_point[1]-height-2*padding+2*chord_length)
    msp.add_line(start_point, end_point, dxfattribs={"color": colors.BLUE, "layer": "Pocket"})

    start_point = end_point
    end_point = (start_point[0] + chord_length, start_point[1] - chord_length)
    ccw_arc(start_point, end_point, color=colors.BLUE, layer="Pocket")




def top_plate(start_point = (0,0)):
    """
    Start bottom left move CCW
    """
    origin = start_point
    # horizontal line
    end_point = start_point
    x_spacing = (box_length - ((notch_length + 2 * padding) * (nbraces - 2))) / (nbraces - 1)
    for i in range(nbraces-2):
        start_point = end_point
        end_point = (end_point[0] + x_spacing, start_point[1])
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0], start_point[1] + notch_width + padding - chord_length)
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0] + chord_length, start_point[1] + chord_length)
        cw_arc(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0] + notch_length+padding*2 - chord_length*2, end_point[1])
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0] + chord_length, start_point[1] - chord_length)
        cw_arc(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0], start_point[1] - notch_width -padding + chord_length)
        msp.add_line(start_point, end_point)

    start_point = end_point
    end_point = (end_point[0] + x_spacing, start_point[1])
    msp.add_line(start_point, end_point)


    # vertical line
    # end_point = (box_length,0)
    y_spacing = (box_width - ((notch_length + 2 * padding) * ntabs)) / (ntabs + 1)
    for j in range(3):
        start_point = end_point
        end_point = (end_point[0], end_point[1]+y_spacing)
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0] - notch_width - padding + chord_length, end_point[1])
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0] - chord_length, start_point[1] + chord_length)
        cw_arc(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0], end_point[1] + notch_length + padding*2 - chord_length*2)
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0] + chord_length, start_point[1] + chord_length)
        cw_arc(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0]+notch_width + padding - chord_length, end_point[1])
        msp.add_line(start_point, end_point)

    start_point = end_point
    end_point = (end_point[0], end_point[1]+y_spacing)
    msp.add_line(start_point, end_point)


    # top horizontal. start top left, move right
    end_point = (origin[0], origin[1] + box_width)
    for i in range(nbraces-2):
        start_point = end_point
        end_point = (end_point[0] + x_spacing, end_point[1])
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0], start_point[1] - notch_width - padding + chord_length)
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0] + chord_length, start_point[1] - chord_length)
        ccw_arc(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0] + notch_length+padding*2 - chord_length*2, end_point[1])
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0] + chord_length, start_point[1] + chord_length)
        ccw_arc(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0], start_point[1]+notch_width + padding - chord_length)
        msp.add_line(start_point, end_point)

    start_point = end_point
    end_point = (end_point[0] + x_spacing, end_point[1])
    msp.add_line(start_point, end_point)


    #left edge. start bot left, move upward
    end_point = origin
    for j in range(3):
        start_point = end_point
        end_point = (end_point[0], end_point[1] + y_spacing)
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0] + notch_width + padding - chord_length, end_point[1])
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0] + chord_length, start_point[1] + chord_length)
        ccw_arc(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0], end_point[1] + notch_length + padding*2 - chord_length * 2)
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0] - chord_length, start_point[1] + chord_length)
        ccw_arc(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0]- notch_width - padding + chord_length, end_point[1])
        msp.add_line(start_point, end_point)

    start_point = end_point
    end_point = (end_point[0], end_point[1]+y_spacing)
    msp.add_line(start_point, end_point)


    # interior pockets
    for i in range(nbraces-2):
        for j in range(3):
            start_point = (origin[0] + x_spacing * (i+1)
                           + (notch_length/2 + padding)*(2*(i+1) - 1)
                           - (notch_width + 2*padding - 2*chord_length)/2,
                           origin[1] +
                           y_spacing * (j+1) + (notch_length+2*padding)*j)

            pocket(start_point, notch_width, notch_length)

# short brace
def short_brace(start_point):
    """
    Start at bottom left, go clockwise
    """
    # start_point = [-20,100]
    y_spacing = (box_width - ((notch_length + 2 * padding) * ntabs)) / (ntabs + 1)

    for i in range(ntabs):
        end_point = (start_point[0]+ y_spacing -
                     notch_width - chord_length + padding, start_point[1])
        if i >0:
            end_point = (end_point[0]+notch_width -chord_length + padding, end_point[1])
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0] + chord_length, start_point[1] + chord_length)
        ccw_arc(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0], start_point[1]+notch_width - chord_length)
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0]+notch_length, start_point[1])
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0],start_point[1]-notch_width+chord_length)
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0] + chord_length, start_point[1] - chord_length)
        ccw_arc(start_point, end_point)

        start_point = end_point

    start_point = end_point
    end_point = (start_point[0]+ y_spacing - notch_width
                 - chord_length + padding, start_point[1])
    msp.add_line(start_point, end_point)

    # short end. always one finger
    start_point = end_point
    end_point = (start_point[0], start_point[1]- corner_finger_length / 2 + chord_length)
    msp.add_line(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0] + chord_length, start_point[1] - chord_length)
    ccw_arc(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0]+notch_width-chord_length, start_point[1])
    msp.add_line(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0], start_point[1] - corner_finger_length)
    msp.add_line(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0] - notch_width + chord_length, start_point[1])
    msp.add_line(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0] - chord_length, start_point[1] - chord_length)
    ccw_arc(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0], start_point[1] - corner_finger_length / 2 + chord_length)
    msp.add_line(start_point, end_point)

    # return back down
    start_point = end_point
    for i in range(ntabs):
        end_point = (start_point[0]- y_spacing +
                     notch_width + chord_length - padding, start_point[1])
        if i >0:
            end_point = (end_point[0]-notch_width + chord_length - padding, end_point[1])
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0] - chord_length, start_point[1] - chord_length)
        ccw_arc(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0], start_point[1]-notch_width + chord_length)
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0]-notch_length, start_point[1])
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (end_point[0], start_point[1]+notch_width-chord_length)
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0] - chord_length, start_point[1] + chord_length)
        ccw_arc(start_point, end_point)

        start_point = end_point

    start_point = end_point
    end_point = (start_point[0]- y_spacing + notch_width
                 + chord_length - padding, start_point[1])
    msp.add_line(start_point, end_point)

    # bottom horizontal. Head left
    start_point = end_point
    end_point = (start_point[0], start_point[1]+ corner_finger_length / 2 - chord_length)
    msp.add_line(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0] - chord_length, start_point[1] + chord_length)
    ccw_arc(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0]-notch_width+chord_length, start_point[1])
    msp.add_line(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0], start_point[1] + corner_finger_length)
    msp.add_line(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0] + notch_width - chord_length, start_point[1])
    msp.add_line(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0] + chord_length, start_point[1] + chord_length)
    ccw_arc(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0], start_point[1] + corner_finger_length / 2 - chord_length)
    msp.add_line(start_point, end_point)


def long_brace(start_point):
    x_spacing = (box_length - ((notch_length + 2 * padding) * (nbraces - 2))) / (nbraces - 1)
    # start bottom left, go CCW
    for i in range(nbraces-2):
        end_point = (start_point[0] + x_spacing + padding - chord_length, start_point[1])
        if i > 0:
            end_point = (end_point[0] -chord_length + padding, end_point[1])
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0] + chord_length, start_point[1] - chord_length)
        cw_arc(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0], end_point[1] - (notch_width - chord_length))
        msp.add_line(start_point, end_point)
        start_point = end_point
        end_point = (start_point[0]+notch_length, end_point[1])
        msp.add_line(start_point, end_point)
        start_point = end_point
        end_point = (start_point[0], end_point[1]+notch_width -chord_length)
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0] + chord_length, start_point[1] + chord_length)
        cw_arc(start_point, end_point)
        start_point = end_point

    end_point = (start_point[0]+x_spacing - chord_length + padding, end_point[1])
    msp.add_line(start_point, end_point)

    # right side vertical, always one finger
    start_point = end_point
    end_point = (start_point[0], end_point[1]+ corner_finger_length/2 - padding)
    msp.add_line(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0]-notch_width + chord_length, end_point[1])
    msp.add_line(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0] - chord_length, start_point[1] + chord_length)
    cw_arc(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0], end_point[1]+corner_finger_length - 2*chord_length + 2*padding)
    msp.add_line(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0] + chord_length, start_point[1] + chord_length)
    cw_arc(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0]+notch_width - chord_length, end_point[1])
    msp.add_line(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0], end_point[1]+corner_finger_length/2 - padding)
    msp.add_line(start_point, end_point)

    # top horizontal, head left
    start_point = end_point
    for i in range(nbraces-2):
        end_point = (start_point[0]-(x_spacing - chord_length + padding), start_point[1])
        if i > 0:
            end_point = (end_point[0] + chord_length - padding, end_point[1])
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0] - chord_length, start_point[1] + chord_length)
        cw_arc(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0], end_point[1] + notch_width - chord_length)
        msp.add_line(start_point, end_point)
        start_point = end_point
        end_point = (start_point[0]-notch_length, end_point[1])
        msp.add_line(start_point, end_point)
        start_point = end_point
        end_point = (start_point[0], end_point[1]-notch_width + chord_length)
        msp.add_line(start_point, end_point)

        start_point = end_point
        end_point = (start_point[0] - chord_length, start_point[1] - chord_length)
        cw_arc(start_point, end_point)

        start_point = end_point
    end_point = (start_point[0]- x_spacing+ chord_length - padding, end_point[1])
    msp.add_line(start_point, end_point)

    # left vertical, heading down
    start_point = end_point
    end_point = (start_point[0], end_point[1]-corner_finger_length/2 + padding)
    msp.add_line(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0]+notch_width-chord_length, end_point[1])
    msp.add_line(start_point, end_point)

    start_point = end_point
    end_point = (start_point[0] + chord_length, start_point[1] - chord_length)
    cw_arc(start_point, end_point)

    start_point = end_point
    end_point = (start_point[0], end_point[1]-corner_finger_length + 2*chord_length - 2*padding)
    msp.add_line(start_point, end_point)

    start_point = end_point
    end_point = (start_point[0] - chord_length, start_point[1] - chord_length)
    cw_arc(start_point, end_point)

    start_point = end_point
    end_point = (start_point[0]-notch_width+chord_length, end_point[1])
    msp.add_line(start_point, end_point)
    start_point = end_point
    end_point = (start_point[0], end_point[1]-corner_finger_length/2 + padding)
    msp.add_line(start_point, end_point)

    # pockets. Start bottom left, go CCW
    pocket_height = end_point[1]+ corner_finger_length/2 - padding
    for i in range(1,nbraces-1):
        start_point = (i* x_spacing
                       + (i-1) * 2 * padding
                       + notch_length / 2
                       + (i - 1) * notch_length
                       - ((notch_width - 2*chord_length) / 2), pocket_height)
        pocket(start_point, notch_width, corner_finger_length)


def plywood(sp):
    """
    Draw plywood sheet at the starting point given.
    """
    msp.add_line((sp[0],sp[1]), (sp[0]+96,sp[1]+0),
                 dxfattribs={"color": colors.YELLOW, "layer": "Plywood"})
    msp.add_line((sp[0]+96,sp[1]+0), (sp[0]+96, sp[1]+48),
                 dxfattribs={"color": colors.YELLOW, "layer": "Plywood"})
    msp.add_line((sp[0]+96,sp[1]+ 48), (sp[0]+0, sp[1]+48),
                 dxfattribs={"color": colors.YELLOW, "layer": "Plywood"})
    msp.add_line((sp[0]+0,sp[1]+48), (sp[0]+0, sp[1]+0),
                 dxfattribs={"color": colors.YELLOW, "layer": "Plywood"})

def leg_holes(sp):
    """
    Add holes for 4x4 legs.
    Start bottom left, go CW.
    """
    width = 3.5
    height = 3.5

    sp = (sp[0] + plywood_thickness + chord_length, sp[1] + plywood_thickness)
    pocket(sp, width, height)
    sp = (sp[0], sp[1] + box_width - height - 2*plywood_thickness - 2*padding)
    pocket(sp, width, height)
    sp = (sp[0] + box_length - width - 2*(plywood_thickness +padding), sp[1])
    pocket(sp, width, height)
    sp = (sp[0], sp[1] - box_width + height + 2*(plywood_thickness + padding))
    pocket(sp, width, height)



def main():
    # Top plate
    plywood((0,0))
    top_plate()

    # short braces
    plywood((0,48))
    for j in range(0,2):
        for i in range(1, int(nbraces / 2) + 1):
            start_point = (notch_width +
                           (box_width+ endmill_diameter + padding)*j ,
                           notch_width + i * (endmill_diameter+padding) +
                           i * box_height + 62
                           ) # 62 is fudge factor to get these in the right place
            short_brace(start_point)

    # long braces
    for i in range(2):
        sp = (0,
              48 + notch_width + i * (box_height + endmill_diameter + padding))
        long_brace(sp)

    # bottom plate
    plywood((0,-48))
    top_plate((0, -48))
    leg_holes((0,-48))

    # Add notes
    note = "Endmill Diameter: {}, \nPlywood Thickness: {}, Box Width: {}, Box Length: {}, Box Height: {}".format(str(endmill_diameter),str(plywood_thickness), str(box_width), str(box_length), str(box_height))
    msp.add_text(
        note,
        height=1,
        dxfattribs={"style": "LiberationSerif", "layer":"Notes"}
    ).set_placement((0, -50), align=TextEntityAlignment.LEFT)

    # Save the DXF document.
    doc.saveas("torsion_box.dxf")

main()
