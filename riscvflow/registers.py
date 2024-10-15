from .utils import build_trie


def all_registers():
    """Return all registers from x0 to x31, and others"""
    x_registers = [f'x{i}' for i in range(32)]
    f_registers = [f'f{i}' for i in range(32)]
    a_registers = ['a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7']
    s_registers = [f's{i}' for i in range(12)]
    t_registers = [f't{i}' for i in range(7)]
    other_registers = ['zero', 'ra', 'sp', 'gp', 'tp', 't0', 't1', 't2', 'fp']
    all_registers = x_registers + f_registers + a_registers + s_registers + t_registers + other_registers
    return build_trie(all_registers)

