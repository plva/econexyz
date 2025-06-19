#!/usr/bin/env python3
import subprocess
import tempfile
import os
from typing import Tuple

HOOK_PATH = os.path.join('.git', 'hooks', 'commit-msg')

TEST_CASES = [
    # Valid cases
    {
        'name': 'valid_bugfix',
        'content': '[bugfix] fix something',
        'should_pass': True,
    },
    {
        'name': 'valid_feature',
        'content': '[feature] add new thing',
        'should_pass': True,
    },
    {
        'name': 'valid_workflow',
        'content': '[workflow] update docs',
        'should_pass': True,
    },
    # Invalid cases
    {
        'name': 'no_type',
        'content': 'fix something',
        'should_pass': False,
    },
    {
        'name': 'unknown_type',
        'content': '[unknown] foo',
        'should_pass': False,
    },
    {
        'name': 'header_too_long',
        'content': '[bugfix] ' + 'a' * 60,
        'should_pass': False,
    },
    {
        'name': 'body_line_too_long',
        'content': '[bugfix] short\n\n' + 'b' * 80,
        'should_pass': False,
    },
]

def run_hook_with_message(message: str) -> Tuple[int, str]:
    with tempfile.NamedTemporaryFile('w+', delete=False) as f:
        f.write(message)
        f.flush()
        temp_path = f.name
    try:
        result = subprocess.run([HOOK_PATH, temp_path], capture_output=True, text=True)
        return result.returncode, result.stdout + result.stderr
    finally:
        os.unlink(temp_path)

def main():
    print('Testing commit-msg hook...')
    passed = 0
    failed = 0
    for case in TEST_CASES:
        code, output = run_hook_with_message(case['content'])
        success = (code == 0) == case['should_pass']
        status = 'PASS' if success else 'FAIL'
        print(f"[{status}] {case['name']}")
        if not success:
            print('  Output:')
            print('  ' + output.replace('\n', '\n  '))
        if success:
            passed += 1
        else:
            failed += 1
    print(f"\nSummary: {passed} passed, {failed} failed, {len(TEST_CASES)} total.")
    if failed > 0:
        exit(1)

if __name__ == '__main__':
    main() 