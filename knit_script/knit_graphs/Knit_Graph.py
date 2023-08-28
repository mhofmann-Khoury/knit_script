"""The graph structure used to represent knitted objects"""
import networkx

from knit_script.knit_graphs.Loop import Loop
from knit_script.knit_graphs.Pull_Direction import Pull_Direction
from knit_script.knit_graphs.Yarn import Yarn


class Course:
    """
    Course object for organizing loops into knitting rows
    """

    def __init__(self):
        self.loops_by_id_in_order: list[int] = []
        self.loops_by_id: dict[int, Loop] = {}

    def add_loop(self, loop: Loop, index: int | None = None):
        """
        Add the loop at the given index or to the end of the course
        :param loop: loop to add
        :param index: index to insert at or None if adding to end
        """
        for parent_loop in loop.parent_loops:
            assert parent_loop not in self, f"{loop} has parent {parent_loop}, cannot be added to same course"
        self.loops_by_id[loop.loop_id] = loop
        if index is None:
            self.loops_by_id_in_order.append(loop.loop_id)
        else:
            self.loops_by_id_in_order.insert(index, loop.loop_id)

    def __getitem__(self, index: int) -> int:
        return self.loops_by_id_in_order[index]

    def index(self, loop_id: int | Loop) -> int:
        """
        Searches for index of given loop_id
        :param loop_id: loop_id or loop to find
        :return: index of the loop_id
        """
        if isinstance(loop_id, Loop):
            loop_id = loop_id.loop_id
        return self.loops_by_id_in_order.index(loop_id)

    def __contains__(self, loop_id: int | Loop) -> bool:
        if isinstance(loop_id, Loop):
            loop_id = loop_id.loop_id
        return loop_id in self.loops_by_id

    def __iter__(self):
        return self.loops_by_id_in_order.__iter__()

    def __len__(self):
        return len(self.loops_by_id_in_order)

    def __str__(self):
        return str(self.loops_by_id_in_order)

    def __repr__(self):
        return str(self)


class Knit_Graph:
    """
    A representation of knitted structures as connections between loops on yarns
    ...

    Attributes
    ----------
    graph : networkx.DiGraph
        the directed-graph structure of loops pulled through other loops.
    loops: Dict[int, Loop]
        A map of each unique loop id to its loop
    yarns: Dict[str, Yarn]
         A list of Yarns used in the graph
    """

    def __init__(self):
        self.graph: networkx.DiGraph = networkx.DiGraph()
        self.loops: dict[int, Loop] = {}
        self.last_loop_id: int = -1
        self.yarns: dict[str, Yarn] = {}

    def add_loop(self, loop: Loop):
        """
        Adds a loop to the graph
        :param loop: the loop to be added in as a node in the graph
        """
        self.graph.add_node(loop.loop_id, loop=loop)
        if loop.yarn not in self.yarns:
            self.add_yarn(loop.yarn)
        if loop not in self.yarns[loop.yarn.yarn_id]:  # make sure the loop is on the yarn specified
            self.yarns[loop.yarn].add_loop_to_end(loop_id=None, loop=loop, knit_graph=self)
        if loop.loop_id > self.last_loop_id:
            self.last_loop_id = loop.loop_id
        self.loops[loop.loop_id] = loop

    def add_yarn(self, yarn: Yarn):
        """
        Adds a yarn to the graph. Assumes that loops do not need to be added
        :param yarn: the yarn to be added to the graph structure
        """
        self.yarns[yarn.yarn_id] = yarn

    def connect_loops(self, parent_loop_id: int, child_loop_id: int,
                      pull_direction: Pull_Direction = Pull_Direction.BtF,
                      stack_position: int | None = None, depth: int = 0, parent_offset: int = 0):
        """
        Creates a stitch-edge by connecting a parent and child loop
        :param parent_offset: The direction and distance, oriented from the front, to the parent_loop
        :param depth: -1, 0, 1: The crossing depth in a cable over other stitches. 0 if Not crossing other stitches
        :param parent_loop_id: the id of the parent loop to connect to this child
        :param child_loop_id:  the id of the child loop to connect to the parent
        :param pull_direction: the direction the child is pulled through the parent
        :param stack_position: The position to insert the parent into, by default add on top of the stack
        """
        assert parent_loop_id in self, f"parent loop {parent_loop_id} is not in this graph"
        assert child_loop_id in self, f"child loop {child_loop_id} is not in this graph"
        self.graph.add_edge(parent_loop_id, child_loop_id, pull_direction=pull_direction, depth=depth, parent_offset=parent_offset)
        child_loop = self[child_loop_id]
        parent_loop = self[parent_loop_id]
        child_loop.add_parent_loop(parent_loop, stack_position)

    def get_courses(self) -> list[Course]:
        """
        :return: A dictionary of loop_ids to the course they are on,
        a dictionary or course ids to the loops on that course in the order of creation.
        The first set of loops in the graph is on course 0.
        A course change occurs when a loop has a parent loop that is in the last course.
        """
        courses = []
        course = Course()
        for loop_id in sorted([*self.graph.nodes]):
            loop = self[loop_id]
            for parent_id in self.graph.predecessors(loop_id):
                if parent_id in course:
                    courses.append(course)
                    course = Course()
                    break
            course.add_loop(loop)
        courses.append(course)
        return courses

    def __contains__(self, item):
        """
        Returns true if the item is in the graph
        :param item: the loop being checked for in the graph
        :return: true if the loop_id of item or the loop is in the graph
        """
        if type(item) is int:
            return self.graph.has_node(item)
        elif isinstance(item, Loop):
            return self.graph.has_node(item.loop_id)
        else:
            return False

    def __getitem__(self, item: int) -> Loop:
        """
        Gets the loop by an id
        :param item: the loop_id being checked for in the graph
        :return: the Loop in the graph with the matching id
        """
        if item not in self:
            raise AttributeError
        else:
            return self.graph.nodes[item]["loop"]

    def get_stitch_edge(self, parent: Loop | int, child: Loop | int, stitch_property: str | None = None):
        """
        Shortcut to get stitch-edge data from loops or ids
        :param stitch_property: property of edge to return
        :param parent: parent loop or id of parent loop
        :param child: child loop or id of child loop
        :return: the edge data for this stitch edge
        """
        parent_id = parent
        if isinstance(parent, Loop):
            parent_id = parent.loop_id
        child_id = child
        if isinstance(child, Loop):
            child_id = child.loop_id
        if self.graph.has_edge(parent_id, child_id):
            if stitch_property is not None:
                return self.graph[parent_id][child_id][stitch_property]
            else:
                return self.graph[parent_id][child_id]
        else:
            return None

    def get_child_loop(self, loop_id: Loop | int) -> int | None:
        """
        :param loop_id: loop_id to look for child from.
        :return: child loop_id or None if no child loop
        """
        if isinstance(loop_id, Loop):
            loop_id = loop_id.loop_id
        successors = [*self.graph.successors(loop_id)]
        if len(successors) == 0:
            return None
        return successors[0]
