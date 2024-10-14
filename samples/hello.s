    .data           # Data section
str:                # Label pointing to the string
    .string "Hello World!\n"  # Define the string in memory

    .text           # Code section
main:               # Main program label

    # System call to write "Hello World!" to stdout
    addi a0, zero, 1        # Load immediate 1 into a0 (file descriptor for stdout)
    la a1, str      # Load address of the string into a1
    addi a2, zero, 13       # Load immediate 13 into a2 (length of the string)
    addi a7, zero, 64       # Load immediate 64 into a7 (system call number for write)
    ecall           # Make the system call

    # System call to exit the program
    addi a0, zero, 0        # Load immediate 0 into a0 (exit code)
    addi a7, zero, 10       # Load immediate 10 into a7 (system call number for exit)
    ecall           # Make the system call

# Example of a function that increments a0 by 1
add_one:            # Function label
    addi a0, a0, 1  # Add 1 to a0 (argument is in a0)
    jalr zero, ra, 0  # Jump back to the return address (ra), equivalent to ret

# Main function that calls the add_one function
demo_function_calls:

    addi a0, zero, 2        # Load immediate 2 into a0 (function argument)
    jal ra, add_one # Jump to add_one function, return address stored in ra
    jal ra, add_one # Call add_one again (a0 will now be 4)

    # Now you can perform additional operations or exit the program
