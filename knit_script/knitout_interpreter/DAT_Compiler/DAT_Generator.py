from knit_script.knitout_interpreter.DAT_Compiler.DAT_Carriage_Pass import DAT_Carriage_Pass


def _null_line(total_width) -> list[int]:
    return [0 for _ in range(0, total_width)]


def _null_lines(total_width: int, lines: int) -> list[list[int]]:
    return [_null_line(total_width) for _ in range(0, lines)]


class DAT_Generator:
    """
        Class used to generate DAT image from carriage pass data
    """
    def __init__(self):
        self.dat_carriage_passes: list[DAT_Carriage_Pass] = []

    def dat_image(self, start_needle: int = 1,
                  bottom_spacing: int = 5, top_spacing: int = 5,
                  left_spacing: int = 8, right_spacing: int = 8, program_padding: int = 4) -> list[list[int]]:
        """
        :param top_spacing:
        :param start_needle:
        :param bottom_spacing:
        :param left_spacing: Spacing of empty information on the left side of whole program.
        :param right_spacing: Spacing of empty information on the right side of the whole program.
        :param program_padding: Spacing of empty information between operation lines and needle operations.
        :return: DAT program with given padding based on current carriage pass data.
        Data is represented as an array of integer arrays for each carriage pass
        """
        program_width = 0
        first_needle_pos = 0
        for cp in self.dat_carriage_passes:
            program_width = max(cp.needle_count, program_width)
            first_needle_pos = min(cp.sorted_needles()[0], first_needle_pos)
        image_lines = []
        body_start = 0
        right_start = 0
        for cp in self.dat_carriage_passes:
            cp_line, _ls, body_start, right_start = cp.dat_image_line(program_width, first_needle_pos, left_spacing, right_spacing, program_padding)
            image_lines.append(cp_line)
        total_width = len(image_lines[0])
        image_lines[:0] = _null_lines(total_width, bottom_spacing)  # add padding to bottom of program
        image_lines.append(_null_line(total_width))
        image_lines.extend(self._program_width_lines(total_width, body_start, right_start, start_needle))
        image_lines.extend(_null_lines(total_width, top_spacing))
        return image_lines

    @staticmethod
    def _program_width_lines(total_width: int, body_start: int, right_start: int, start_needle: int = 1) -> list[list[int]]:

        width_line = [1 if body_start <= i < right_start else 0 for i in range(0, total_width)]
        num_col: int = body_start - 2
        width_line[num_col] = start_needle % 100  # tenth and first place value
        ops = [width_line]
        remaining_start_needle_values: int = int(start_needle / 100)
        while remaining_start_needle_values > 0:
            place_line: list[int] = _null_line(total_width)
            place_line[num_col] = remaining_start_needle_values % 100
            ops.append(place_line)
            remaining_start_needle_values /= 100
        return ops
