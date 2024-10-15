import re
from riscvflow.node import CFGNode, InstructionNode, MacroNode
from riscvflow.cfg import ControlFlowGraph
from riscvflow.utils import set_numLines
from riscvflow.logger import logger


class RISCVControlFlowBuilder:
    def __init__(self, filepath):
        self.filepath = filepath
        self.cfg = ControlFlowGraph()
        self.in_text_section = False
        self.in_data_section = False
        self.in_macro = False
        self.current_block = None  # Current block we are building
        self.current_function = None  # Current function node being built
        self.return_stack = []  # Stack to keep track of return addresses


    def parse_and_build_cfg(self):
        # Regular expressions to match labels, instructions, branches, and ecall (program exit)
        label_re = re.compile(r'(\w+):')
        instruction_re = re.compile(r'\b\w+\b')
        branch_re = re.compile(r'(beq|bne|blt|bge)\s+(\w+)\s*,?\s*(\w+)\s*,?\s*(\w+)')
        jump_re = re.compile(r'j\s+(\w+)')  # Match unconditional jumps
        jal_re = re.compile(r'jal\s+(\w+),\s*(\w+)')  # Match jal instructions
        jalr_re = re.compile(r'jalr\s+\w+,\s*\w+,\s*\w+')  # Match jalr instructions
        end_program_re = re.compile(r'addi\s+a7,\s+zero,\s+10')  # Exit program code
        ecall_re = re.compile(r'ecall')
        macro_start_re = re.compile(r'\.macro\s+(\w+)')
        macro_end_re = re.compile(r'\.end_macro')

        before_macro_node = None

        file = open(self.filepath, 'r')

        for no, line in enumerate(file):
            line = line.strip()

            if line.startswith('#') or not line:
                continue  # Skip comments and empty lines

            if line.startswith('.global'):
                continue

            # Detect section changes between .data and .text
            if line.startswith('.data'):
                self.in_data_section = True
                self.in_text_section = False
                continue

            if line.startswith('.text'):
                self.in_text_section = True
                self.in_data_section = False

                # Initialize a default block for instructions if no label is encountered yet
                if self.current_block is None:
                    self.current_block = CFGNode(label="[default]")
                    self.cfg[self.current_block.label] = self.current_block
                continue

            # Detect the start of a macro
            if line.startswith('.macro'):
                before_macro_node = self.current_block
                self.in_macro = True
                macro_name = macro_start_re.search(line).group(1)
                logger.info(f"Detected macro start: {macro_name} at line {no + 1}")

                # Create a new MacroNode
                macro_node = MacroNode(no + 1, macro_name)
                self.current_block = macro_node  # Set current block to the macro node
                self.cfg[macro_name] = macro_node  # Add the macro node to the CFG
                continue

            # If we are inside a macro, handle its instructions
            if self.in_macro:
                # Detect the end of the macro
                if macro_end_re.search(line):
                    self.in_macro = False
                    self.current_block.set_end_line(no + 1)
                    logger.info(f"Detected macro end at line {no + 1}")
                    self.current_block = None  # Reset current block after the macro ends
                    self.current_block = before_macro_node  # Set current block to the block before the macro
                else:
                    # Add AST nodes (instructions) to the macro block
                    instr_node = InstructionNode(no + 1, line)
                    self.current_block.add_ast_node(instr_node)
                    logger.info(f"Adding instruction to macro: {line} at line {no + 1}")
                continue

            # Detect labels
            label_match = label_re.match(line)
            if label_match:
                label = label_match.group(1)
                if self.in_text_section:
                    # Check if the label already exists (forward reference from a jal instruction)
                    if label in self.cfg:
                        new_block = self.cfg[label]  # Use the existing block
                    else:
                        # Create a new block for the label if not found
                        new_block = CFGNode(label=label)
                        self.cfg[label] = new_block  # Add to CFG

                    # Link the previous block to the new label block (fall-through)
                    if self.current_block:
                        self.cfg.add_edge(self.current_block, new_block)
                        logger.info(f"Edge created from {self.current_block.label} to {label}")

                    self.current_block = new_block  # Set current_block to new label block
                continue

            # Skip if inside the .data section
            if self.in_data_section:
                continue

            # Detect branch instructions (conditional branch)
            # Detect branch instructions (conditional branch)
            branch_match = branch_re.search(line)
            if branch_match:
                instr_node = InstructionNode(no + 1, line)
                self.current_block.add_ast_node(instr_node)

                branch_instr = branch_match.group(1)  # e.g., beq, bne
                reg1 = branch_match.group(2)  # The first register (e.g., 'a1')
                reg2 = branch_match.group(3)  # The second operand (e.g., 'zero')
                target_label = branch_match.group(4)  # The target label (e.g., 'valid')

                # Define the condition based on the branch instruction
                if branch_instr == 'beq':
                    condition = f"{reg1} == {reg2}"
                elif branch_instr == 'bne':
                    condition = f"{reg1} != {reg2}"
                elif branch_instr == 'blt':
                    condition = f"{reg1} < {reg2}"
                elif branch_instr == 'bge':
                    condition = f"{reg1} >= {reg2}"
                else:
                    condition = None

                # Create an edge to the branch target (true case, jump to 'valid' if a1 == 0)
                target_block = self.cfg[target_label]
                if not target_block:
                    target_block = CFGNode(label=target_label)
                    self.cfg[target_label] = target_block
                #self.cfg.add_edge(self.current_block, target_block)  # Create edge from 'main' to 'valid'
                self.current_block.add_successor(target_block, condition)
                logger.info(f'Adding branch edge from {self.current_block.label} to {target_block.label} with condition: {condition}')
                logger.info(f"Branch edge created from {self.current_block.label} to {target_label}")

                opposite_condition = f"not ({condition})"
                if branch_instr == 'beq':
                    opposite_condition = f"{reg1} != {reg2}"
                elif branch_instr == 'bne':
                    opposite_condition = f"{reg1} == {reg2}"
                elif branch_instr == 'blt':
                    opposite_condition = f"{reg1} >= {reg2}"
                elif branch_instr == 'bge':
                    opposite_condition = f"{reg1} < {reg2}"

                # Create a new block for the fall-through case (next instruction after 'beq')
                fall_through_block = CFGNode(label=f'[fallthrough(#{no+1})]')
                self.cfg[fall_through_block.label] = fall_through_block
                self.cfg.add_edge(self.current_block, fall_through_block, opposite_condition)
                logger.info(f"Fall-through edge created from {self.current_block.label} to fall-through block")

                self.current_block = fall_through_block  # Set the current block to the fall-through block
                continue

            # Detect jump instructions (j, jal)
            jump_match = jump_re.search(line)
            if jump_match:
                instr_node = InstructionNode(no + 1, line)
                self.current_block.add_ast_node(instr_node)

                target_label = jump_match.group(1)

                # Create an edge to the jump target
                target_block = self.cfg[target_label]
                if not target_block:
                    target_block = CFGNode(label=target_label)
                    self.cfg[target_label] = target_block
                self.cfg.add_edge(self.current_block, target_block)
                logger.info(f"Jump edge created from {self.current_block.label} to {target_label}")

                # Set current_block to None after the jump
                self.current_block = None
                continue

            # Detect jal (jump and link)
            jal_match = jal_re.search(line)
            if jal_match:
                instr_node = InstructionNode(no + 1, line)
                self.current_block.add_ast_node(instr_node)

                return_reg = jal_match.group(1)  # e.g., ra
                target_label = jal_match.group(2)  # The target label (function)

                if return_reg == 'ra':
                    self.return_stack.append(self.current_block)

                # Create an edge to the jal target (function)
                target_block = self.cfg[target_label]
                if not target_block:
                    target_block = CFGNode(label=target_label)
                    self.cfg[target_label] = target_block
                if return_reg == 'ra':
                    target_block.is_function_start = True  # Mark the target block as a function
                self.cfg.add_edge(self.current_block, target_block)
                logger.info(f"Function call edge created from {self.current_block.label} to {target_label}")

                # No need to set current block to None, as execution continues after the function call
                continue

            # Detect jalr (jump and link return)
            if jalr_re.search(line):
                instr_node = InstructionNode(no + 1, line)
                self.current_block.add_ast_node(instr_node)

                # After jalr, return to the caller, so we link back to the caller's next block.
                if self.return_stack:
                    return_block = self.return_stack.pop()
                    self.cfg.add_edge(self.current_block, return_block)
                    logger.info(f"Return edge created from {self.current_block.label} to return block {return_block.label}")

                # Set current_block to None after return to avoid further execution
                self.current_block = None
                continue

            # Detect program termination (addi a7, zero, 10 followed by ecall)
            if end_program_re.search(line):
                instr_node = InstructionNode(no + 1, line)
                self.current_block.add_ast_node(instr_node)

                # Check if the next line is the ecall instruction (exit)
                next_line = file.readline().strip()
                if ecall_re.search(next_line):
                    ecall_node = InstructionNode(no + 2, next_line)
                    self.current_block.add_ast_node(ecall_node)

                    # Mark the block as an exit block (no further edges should be added)
                    self.current_block.is_exit = True
                    logger.info(f"Exit block: {self.current_block.label}")

                # No need to add any further edges after this block
                self.current_block = None
                continue

            # Regular instruction
            instr_node = InstructionNode(no + 1, line)
            self.current_block.add_ast_node(instr_node)

        set_numLines(no + 1)

        file.close()

    def get_cfg(self):
        return self.cfg
