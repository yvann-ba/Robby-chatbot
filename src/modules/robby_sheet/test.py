import sys
from io import StringIO

# Save the original stdout
original_stdout = sys.stdout

# Create a StringIO object and redirect stdout to it
sys.stdout = captured_output = StringIO()

# Now any print statements will go to captured_output instead of the console
print("This will be captured")

# Reset stdout to its original value
sys.stdout = original_stdout

# Now print statements will go to the console again
print("This will go to the console")

# You can access the captured output with the .getvalue() method
# captured_text = captured_output.getvalue()

# print("Captured text:")
# print(captured_text)