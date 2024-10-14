# main/print_functions.py

import argparse
import sys
import os

# Add the parent directory (where riscvflow is) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from riscvflow import RISCVControlFlowBuilder, getFunctions


def main():
    # Set up argparse for input arguments
    parser = argparse.ArgumentParser(description="Print functions from the RISCV assembly file.")
    parser.add_argument('filename', help="Path to the RISCV assembly file")
    parser.add_argument('--start', default='[default]', help="Label to start function discovery from")
    args = parser.parse_args()

    # Build the control flow graph from the assembly file
    builder = RISCVControlFlowBuilder(args.filename)
    builder.parse_and_build_cfg()

    cfg = builder.get_cfg()

    # Discover functions starting from the provided label
    functions = []
    getFunctions(cfg, args.start, functions)

    # Print the discovered functions
    print('Possible functions:', functions)


if __name__ == '__main__':
    main()

