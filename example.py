import json
import os
from contextlib import suppress
from steem.blockchain import Blockchain


def get_last_line(filename):
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            f.seek(-2, 2)
            while f.read(1) != b"\n":
                f.seek(-2, 1)
            return f.readline()


def get_previous_block_num(block):
    if not block:
        return -1
    
    if type(block) == bytes:
        block = block.decode('utf-8')
    
    if type(block) == str:
        block = json.loads(block)
    
    return int(block['previous'][:8], base=16)


def run(filename):
    b = Blockchain()
    # automatically resume from where we left off
    # previous + last + 1
    start_block = get_previous_block_num(get_last_line(filename)) + 2
    with open(filename, 'a+') as file:
        for block in b.stream_from(start_block=start_block, full_blocks=True):
            file.write(json.dumps(block, sort_keys=True) + '\n')


if __name__ == '__main__':
    output_file = '/home/user/Downloads/steem.blockchain.json'
    with suppress(KeyboardInterrupt):
        run(output_file)

