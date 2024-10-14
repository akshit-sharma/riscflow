import re
from riscvflow.node import InstructionNode


def registerUsageInFunction(cfg, labels):
    # Regular expressions for different types of instructions
    arithmetic_re = re.compile(r'(\w+)\s+(\w+),\s*(\w+),\s*(\w+)')  # Arithmetic: add a0, a1, a2
    arithmetic_immediate_re = re.compile(r'(\w+)\s+(\w+),\s*(\w+),\s*(-?\d+)')  # addi a0, a1, immediate
    load_store_re = re.compile(r'(lw|sw)\s+(\w+),\s*(-?\d+)\((\w+)\)')  # Load/Store: lw a0, offset(sp)
    jump_re = re.compile(r'jal\s+(\w+),\s*(\w+)')  # jal ra, function_name
    branch_re = re.compile(r'(beq|bne|blt|bge)\s+(\w+),\s*(\w+),\s*(\w+)')  # Branch: beq a0, zero, label

    # Loop through each label in the CFG to analyze the register usage
    for label in labels:
        node = cfg[label]
        for ast_node in node.ast_nodes:
            print(ast_node)
            if isinstance(ast_node, InstructionNode):
                code = ast_node.code

                # Match arithmetic instructions (e.g., add, sub, mul)
                match = arithmetic_re.search(code)
                if match:
                    instr = match.group(1)
                    dest_reg = match.group(2)
                    src_reg1 = match.group(3)
                    src_reg2 = match.group(4)
                    print(f"Instruction: {instr}, Dest: {dest_reg}, Src1: {src_reg1}, Src2: {src_reg2}")
                    continue

                # Match arithmetic with immediate (e.g., addi a0, a1, 10)
                match = arithmetic_immediate_re.search(code)
                if match:
                    instr = match.group(1)
                    dest_reg = match.group(2)
                    src_reg = match.group(3)
                    immediate_value = match.group(4)
                    print(f"Instruction: {instr}, Dest: {dest_reg}, Src: {src_reg}, Immediate: {immediate_value}")
                    continue

                # Match load/store instructions (e.g., lw a0, 0(sp))
                match = load_store_re.search(code)
                if match:
                    instr = match.group(1)
                    reg = match.group(2)
                    offset = match.group(3)
                    base_reg = match.group(4)
                    print(f"Instruction: {instr}, Reg: {reg}, Offset: {offset}, Base: {base_reg}")
                    continue

                # Match jump instructions (e.g., jal ra, function_name)
                match = jump_re.search(code)
                if match:
                    instr = 'jal'
                    return_reg = match.group(1)
                    target_label = match.group(2)
                    print(f"Instruction: {instr}, Return Reg: {return_reg}, Target: {target_label}")
                    continue

                # Match branch instructions (e.g., beq a0, zero, label)
                match = branch_re.search(code)
                if match:
                    instr = match.group(1)
                    reg1 = match.group(2)
                    reg2 = match.group(3)
                    target_label = match.group(4)
                    print(f"Instruction: {instr}, Reg1: {reg1}, Reg2: {reg2}, Target: {target_label}")
                    continue

                # If no match is found, print an unrecognized instruction
                print(f"Unrecognized instruction: {code}")
