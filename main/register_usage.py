# main/register_usage.py

import argparse
import sys
import os

# Add the parent directory (where riscvflow is) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from riscvflow import RISCVControlFlowBuilder, getFunctions, registerUsageInFunction, dfsFunction


def main():
    # Set up argparse for input arguments
    parser = argparse.ArgumentParser(description="Check register usage in a RISCV assembly file.")
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

    # Check register usage for each function
    for func in functions:
        func_start = cfg[func]
        function_nodes = dfsFunction(cfg, func_start.label)

        # Check and print register usage
        labels = [f.label for f in function_nodes]
        registerUsageInFunction(cfg, labels)


if __name__ == '__main__':
    main()
