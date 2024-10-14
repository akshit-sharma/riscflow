.data
prompt_1: .asciz "Enter first number: "
prompt_2: .asciz "Enter second number: "
result_msg: .asciz "The result of the addition is: "
newline: .asciz "\n"

.text

# A macro for printing a string (overwrites a0 and a7)
.macro print_string(%label)
la a0, %label
addi a7, zero, 4
ecall
.end_macro

# A macro for printing a number (overwrites a0 and a7)
.macro print_number(%reg)
add a0, zero, %reg
addi a7, zero, 1
ecall
.end_macro

# A macro for taking a number as input and saving it in the specified register (overwrites a0 and a7)
.macro read_number(%reg)
addi a7, zero, 5
ecall
add %reg, a0, zero

    la a0, newline       # Load the newline character
    addi a7, zero, 4     # System call for print string
    ecall                # Print newline
.end_macro

main:
    print_string(prompt_1)  # Print prompt for first number
    read_number(s0)         # Read the first number into s0

    print_string(prompt_2)  # Print prompt for second number
    read_number(s1)         # Read the second number into s1

    add a0, s0, s1          # Add the two numbers (s0 + s1), result stored in a0

    print_string(result_msg)  # Print the result message
    print_number(a0)          # Print the result of the addition (a0)

    # Exit the program
    addi a7, zero, 10        # System call for exit
    ecall

