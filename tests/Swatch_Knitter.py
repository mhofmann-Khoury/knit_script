from knit_script.interpret import knit_script_to_knitout_to_dat
from knit_script.knit_graphs.Knit_Graph import Knit_Graph
from knit_script.knit_graphs.Pull_Direction import Pull_Direction
from knit_script.knit_graphs.Yarn import Yarn


def cast_on(width: int = 10) -> tuple[Knit_Graph, Yarn, list[int]]:
    knit_graph = Knit_Graph()
    yarn = Yarn("yarn")
    knit_graph.add_yarn(yarn)

    for _ in range(0, width):
        yarn.add_loop_to_end(knit_graph=knit_graph)
    return knit_graph, yarn, [*yarn]


def jersey_knit(width: int = 10, height: int = 10) -> Knit_Graph:
    """
    :param width: number of stitches.
    :param height: Number of courses.
    :return: A knit graph structure of width loop and height course with all knit stitches.
    """

    knit_graph, yarn, last_course = cast_on(width)
    for r in range(1, height):
        new_course: list[int] = []
        for parent_loop_id in reversed(last_course):
            loop_id, loop = yarn.add_loop_to_end(knit_graph=knit_graph)
            new_course.append(loop_id)
            knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF)
        last_course = new_course
    return knit_graph


def seed_stitch(width: int = 10, height: int = 10) -> Knit_Graph:
    """
    :param width: number of stitches.
    :param height: number of courses.
    :return: A knit graph structure of width loop and height course with alternating knit and purl stitches in a checkered pattern.
    """
    knit_graph, yarn, last_course = cast_on(width)
    direction = Pull_Direction.BtF
    for r in range(1, height):
        new_course: list[int] = []
        for parent_loop_id in reversed(last_course):
            loop_id, loop = yarn.add_loop_to_end(knit_graph=knit_graph)
            new_course.append(loop_id)
            knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=direction)
            direction = direction.opposite()
        last_course = new_course
    return knit_graph


def kp_rib(width: int = 10, height: int = 10) -> Knit_Graph:
    """
    :param width: number of stitches.
    :param height: number of courses.
    :return: A knit graph structure of width loop and height course with alternating columns of knits and purls.
    """
    knit_graph, yarn, last_course = cast_on(width)
    end_of_course_direction = Pull_Direction.BtF
    for r in range(1, height):
        new_course: list[int] = []
        direction = end_of_course_direction
        for parent_loop_id in reversed(last_course):
            loop_id, loop = yarn.add_loop_to_end(knit_graph=knit_graph)
            new_course.append(loop_id)
            knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=direction)
            end_of_course_direction = direction
            direction = direction.opposite()
        last_course = new_course
    return knit_graph


def lace(width: int = 12, height: int = 10) -> Knit_Graph:
    """
    :param width: Number of stitches. Must be increments of 6
    :param height: Number of courses.
    :return: A knit graph structure of width loop and height course with a | |\ o o /| | structure on odd rows.
    """
    assert width % 6 == 0, "Lace must be a repeat of 6 stitches"
    knit_graph, yarn, last_course = cast_on(width)
    for r in range(1, height):
        new_course: list[int] = []
        reversed_course = [*reversed(last_course)]
        for i, parent_loop_id in enumerate(reversed_course):
            loop_id, loop = yarn.add_loop_to_end(knit_graph=knit_graph)
            new_course.append(loop_id)
            if r % 2 == 0:  # even rows knit across
                knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF)
            else:
                if i % 6 in [0, 5]:  # knits
                    knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF)
                elif i % 6 == 1:
                    knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF, stack_position=1)
                    knit_graph.connect_loops(parent_loop_id=reversed_course[i + 1], child_loop_id=loop_id, pull_direction=Pull_Direction.BtF, stack_position=0, parent_offset=1)
                elif i % 6 == 4:
                    knit_graph.connect_loops(parent_loop_id=reversed_course[i - 1], child_loop_id=loop_id, pull_direction=Pull_Direction.BtF, stack_position=0, parent_offset=-1)
                    knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF, stack_position=1)
        last_course = new_course
    return knit_graph


def cable(width: int = 10, height: int = 10) -> Knit_Graph:
    """
    :param width: Number of stitches. Must be increments of 5
    :param height: Number of courses.
    :return: A knit graph structure of width loop and height course with a 2-to-left cable surrounded by knits on odd rows.
    """
    assert width % 5 == 0, "Cable must be a repeat of 5 stitches"
    knit_graph, yarn, last_course = cast_on(width)
    for r in range(1, height):
        new_course: list[int] = []
        cable_course: list[int] = []
        reserved_course = [*reversed(last_course)]
        for l, parent_loop_id in enumerate(reserved_course):
            loop_id, loop = yarn.add_loop_to_end(knit_graph=knit_graph)
            new_course.append(loop_id)
            if r % 2 == 0:  # even rows knit across
                knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF)
            else:
                if l % 5 in [0, 4]:
                    knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF)
                    cable_course.append(loop_id)
                elif l % 5 in [3, 2]:
                    cable_course.insert(-1, loop_id)
                    knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF, depth=-1, parent_offset=1)
                elif l % 5 == 1:
                    cable_course.append(loop_id)
                    knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF, depth=1, parent_offset=-2)
        if len(cable_course) > 0:
            new_course = cable_course
        last_course = new_course
    return knit_graph


def knit_swatch(knit_graph: Knit_Graph, out_put_name: str = "swatch_instructions"):
    courses = knit_graph.get_courses()
    knit_graph_built = knit_script_to_knitout_to_dat("Swatch_Knitter.ks", f"{out_put_name}.k", dat_name=f"{out_put_name}.dat", pattern_is_filename=True,
                                                     python_variables={"swatch": knit_graph, "courses": courses}, visualize_instruction_graph=False)
    return knit_graph_built
