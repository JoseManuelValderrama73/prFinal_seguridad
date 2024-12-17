import sys
import tty
import termios
import time


def get_char():
    """Get a single character without pressing Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return char


def secure_input(prompt):
    """Input that replaces characters with '*' after 1 second."""
    print(prompt, end="", flush=True)
    input_chars = []
    try:
        while True:
            char = get_char()
            if char == "\n" or char == "\r":  # Enter key pressed
                break
            print(char, end="", flush=True)  # Print character immediately
            input_chars.append(char)
            time.sleep(1)
            print("\b*", end="", flush=True)  # Replace character with '*'
    except KeyboardInterrupt:
        print("\nInput interrupted.")
    print()  # Move to the next line
    return "".join(input_chars)


# Example usage
if __name__ == "__main__":
    password = secure_input("Enter your password: ")
    print(f"Your input was: {password}")
