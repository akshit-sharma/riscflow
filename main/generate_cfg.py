# main/generate_cfg.py

import argparse

import os
import sys
from pathlib import Path

# Add the parent directory (where riscvflow is) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from riscvflow import RISCVControlFlowBuilder, dfsVisited, listMacros
from riscvflow.logger import logger, console_handler


def main():
    # Set up argparse for input arguments
    parser = argparse.ArgumentParser(description="Generate SVG CFG for a function.")
    parser.add_argument('filename', help="Path to the RISCV assembly file")
    parser.add_argument('output', help="Output file name for the SVG", type=Path)
    parser.add_argument('--start-label', help="The start label of the function (default: function_name)", type=str, default='[default]')
    parser.add_argument('--macros', help="Include macros in the CFG", action='store_true')
    args = parser.parse_args()

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    # Build the control flow graph from the assembly file
    builder = RISCVControlFlowBuilder(args.filename)
    builder.parse_and_build_cfg()

    cfg = builder.get_cfg()

    nodes = dfsVisited(cfg, args.start_label)

    if args.macros:
        macroNodes = listMacros(cfg)
        nodes = nodes.union(macroNodes)

    fileNoExt = args.output.parent / args.output.stem

    cfg.save_svg(nodes, fileNoExt)
    print(f"CFG for '{args.start_label}' saved as {fileNoExt}.svg")


if __name__ == '__main__':
    main()

