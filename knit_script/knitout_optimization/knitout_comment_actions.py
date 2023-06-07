import re
from typing import Optional

from parglare import get_collector
from parglare.parser import LRStackNode

from knit_script.knitout_optimization.knitout_structures.Knitout_Line import Comment_Line

comment_action = get_collector()


@comment_action
def comment_line(stack_node: LRStackNode, nodes) -> Optional[Comment_Line]:
    """

    :param stack_node:
    :param nodes:
    :return:
    """
    content = nodes[0]
    if not re.match(r'^\s*$', content):  # comment, not whitespace
        parser = stack_node.parser.knitout_parser
        comment = Comment_Line(content)
        parser.add_code_line(comment)
        return comment
    else:
        return None


@comment_action
def commented_line(stack_node: LRStackNode, _, code: Optional[str], comment: str) -> Optional[Comment_Line]:
    """

    :param code:
    :param stack_node:
    :param _:
    :param comment:
    :return:
    """
    if not re.match(r'^\s*$', comment):  # comment is just whitespace
        parser = stack_node.parser.knitout_parser
        comment = Comment_Line(comment[1:])
        if code is None:  # code isn't yet processed
            parser.held_comments.append(comment)
        else:  # code processed
            start_pos = stack_node.start_position
            parser.in_line_comments_start_position = start_pos, comment
        return comment
    else:
        return None

# @comment_action
# def Comment(stack_node: LRStackNode, node: str) -> str:
#     """
#
#     :param stack_node:
#     :param node:
#     :return:
#     """
#     # Todo isolate solo comments
#     comment = node[1:].strip()
#     parser = stack_node.parser.knitout_parser
#     line_str = parser.get_stack_node_string(stack_node)
#     prior_char = stack_node.input_str[parser.last_position+1]
#     last_char = stack_node.input_str[stack_node.end_position]
#     if parser.last_position < stack_node.start_position: # line of code between this and last parsed code
#         parser.held_comment = comment
#         parser.held_comment_end = stack_node.end_position
#     else:
#         line_number, code = parser.last_line_of_code
#         parser.comments_by_line[line_number] = comment
#         parser.last_position = stack_node.position
#     return comment
