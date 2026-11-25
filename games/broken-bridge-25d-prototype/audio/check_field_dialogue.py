"""Check the additional v0.6 full-line captions and local voice waveforms."""
import re

import check_instruction_audio as checker
from generate_field_dialogue import generator, read_field_lines

checker.INSTRUCTIONS = generator.INSTRUCTIONS
checker.read_instructions = read_field_lines
base_normalize = checker.normalized


def normalize(text):
    value = base_normalize(text)
    replacements = {'26':'twenty six', '20':'twenty', 'cm':'centimeters'}
    return re.sub(r'\b(26|20|cm)\b',lambda match:replacements[match[0]],value)


if __name__ == '__main__':
    checker.normalized = normalize
    checker.main()
