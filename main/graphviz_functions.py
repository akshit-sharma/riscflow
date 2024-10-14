# main/print_functions.py

import argparse
import sys
import os
from pathlib import Path

# Add the parent directory (where riscvflow is) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from riscvflow import RISCVControlFlowBuilder, getFunctions, dfsFunction


def main():
    parser = argparse.ArgumentParser(description="Print functions from the RISCV assembly file.")
    parser.add_argument('filename', help="Path to the RISCV assembly file")
    parser.add_argument('--start', default='[default]', help="Label to start function discovery from")
    parser.add_argument('output_dir', help="Output directory for the functions", type=Path)
    args = parser.parse_args()

    builder = RISCVControlFlowBuilder(args.filename)
    builder.parse_and_build_cfg()

    cfg = builder.get_cfg()

    functions = []
    getFunctions(cfg, args.start, functions)

    for func in functions:
        func_start = cfg[func]
        function_nodes = dfsFunction(cfg, func_start.label)
        fileNoExt = args.output_dir / f"{args.filename.stem}_{func_start.label}"
        cfg.save_svg(function_nodes, fileNoExt)


if __name__ == '__main__':
    main()

