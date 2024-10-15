import argparse
import sys
import os
from pathlib import Path

# Add the parent directory (where riscvflow is) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from riscvflow import RISCVControlFlowBuilder, getFunctions, dfsFunction, nestedFunctions


def main():
    parser = argparse.ArgumentParser(description="Print functions from the RISCV assembly file.")
    parser.add_argument('filename', help="Path to the RISCV assembly file", type=Path)
    parser.add_argument('--start', default='[default]', help="Label to start function discovery from")
    args = parser.parse_args()

    builder = RISCVControlFlowBuilder(args.filename)
    builder.parse_and_build_cfg()

    cfg = builder.get_cfg()

    functions = []
    getFunctions(cfg, args.start, functions)

    print("Functions found in the file:", functions)

    nested_functions = []
    for func in functions:
        func_start = cfg[func]
        nested_funcs = nestedFunctions(cfg, func)
        nested_funcs = list(set(nested_funcs) & set(functions))
        print("Nested functions found in the file:", nested_funcs)
        nested_functions.append(nested_funcs)
        print(f"Function {func} has {len(nested_functions[-1])} nodes {nested_functions[-1]}")


if __name__ == '__main__':
    main()

