from abaqus import *
from abaqusConstants import *

def generate_model(config, rectangle_data):
    """
    Build an Abaqus model with a box and merged flat rectangles (plates) inside.

    Parameters:
        config : dict
            Configuration dictionary containing box/rectangle dimensions
            and model specifications.
        rectangle_data : list of tuples (center, angles, vertices)
            Information about rectangles: center coordinates, Euler angles, vertices.
    """
    # Extract parameters from the config dictionary
    BOX_W, BOX_H, BOX_D = config["BOX_DIMS"]
    RECT_W, RECT_H = config["RECT_DIMS"]
    
    model_name = 'GeneratedModel'

    # Delete existing model if it exists
    if model_name in mdb.models:
        del mdb.models[model_name]

    model = mdb.Model(name=model_name)
    assembly = model.rootAssembly

    # Create the main box part
    sketch_box = model.ConstrainedSketch(name='__box__', sheetSize=200.0)
    sketch_box.rectangle((0.0, 0.0), (BOX_W, BOX_H))
    box_part = model.Part(name='Box', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    box_part.BaseSolidExtrude(sketch=sketch_box, depth=BOX_D)

    # Add box instance to the assembly
    assembly.Instance(name='Box-1', part=box_part, dependent=ON)

    # Create base rectangle part (flat shell)
    sketch_rect = model.ConstrainedSketch(name='__rect__', sheetSize=200.0)
    sketch_rect.rectangle((-RECT_W/2.0, -RECT_H/2.0), (RECT_W/2.0, RECT_H/2.0))
    base_rectangle = model.Part(name='BaseRectangle', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    base_rectangle.BaseShell(sketch=sketch_rect)

    # Create rectangle instances
    inst_list = []
    for i, (center, angles, _) in enumerate(rectangle_data):
        alpha, beta, gamma = angles
        inst_name = f'Rectangle_{i+1:06d}'

        assembly.Instance(name=inst_name, part=base_rectangle, dependent=ON)
        assembly.rotate(instanceList=(inst_name,), axisPoint=(0,0,0), axisDirection=(0,0,1), angle=alpha)
        assembly.rotate(instanceList=(inst_name,), axisPoint=(0,0,0), axisDirection=(1,0,0), angle=beta)
        assembly.rotate(instanceList=(inst_name,), axisPoint=(0,0,0), axisDirection=(0,0,1), angle=gamma)
        assembly.translate(instanceList=(inst_name,), vector=center)
        inst_list.append(assembly.instances[inst_name])

    # Merge all rectangle instances into a single part
    assembly.InstanceFromBooleanMerge(
        name='MergedRectangles',
        instances=tuple(inst_list),
        originalInstances=DELETE,
        domain=GEOMETRY
    )
