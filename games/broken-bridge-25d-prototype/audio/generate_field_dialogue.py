"""Generate only v0.6 dialogue with the existing Ranger Lin Kokoro voice."""
import json
import subprocess

import generate_instructions as generator

generator.INSTRUCTIONS = generator.AUDIO / 'field-dialogue'


def read_field_lines():
    return json.loads(subprocess.check_output([
        'node', '--input-type=module', '-e',
        "import {fieldLines} from './src/field-dialogue.mjs'; "
        "console.log(JSON.stringify(fieldLines));",
    ], cwd=generator.AUDIO.parent))


if __name__ == '__main__':
    generator.read_instructions = read_field_lines
    generator.main()
