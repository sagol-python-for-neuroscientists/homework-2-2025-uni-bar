MORSE_CODE = {'A': '.-',     'B': '-...',   'C': '-.-.',
              'D': '-..',    'E': '.',      'F': '..-.',
              'G': '--.',    'H': '....',   'I': '..',
              'J': '.---',   'K': '-.-',    'L': '.-..',
              'M': '--',     'N': '-.',     'O': '---',
              'P': '.--.',   'Q': '--.-',   'R': '.-.',
              'S': '...',    'T': '-',      'U': '..-',
              'V': '...-',   'W': '.--',    'X': '-..-',
              'Y': '-.--',   'Z': '--..',

              '0': '-----',  '1': '.----',  '2': '..---',
              '3': '...--',  '4': '....-',  '5': '.....',
              '6': '-....',  '7': '--...',  '8': '---..',
              '9': '----.',

              '.': '.-.-.-', ',': '--..--', ':': '---...',
              "'": '.----.', '-': '-....-',
              }


def english_to_morse(
    input_file: str = "lorem.txt",
    output_file: str = "lorem_morse.txt"
):
    """Convert an input text file to an output Morse code file.

    Notes
    -----
    This function assumes the existence of a MORSE_CODE dictionary, containing a
    mapping between English letters and their corresponding Morse code.

    Parameters
    ----------
    input_file : str
        Path to file containing the text file to convert.
    output_file : str
        Name of output file containing the translated Morse code. Please don't change
        it since it's also hard-coded in the tests file.
    """
    # Read the text and convert to uppercase
    with open(input_file, 'r') as f:
        text = f.read().upper()

    # Convert each character to Morse code using the MORSE_CODE dictionary
    table = str.maketrans(MORSE_CODE) # Create a translation table

    # splitting the text to lines and mapping each word in this line and join by ""
    # and then join by new line
    morse_code = "\n".join(
        "\n".join(word.translate(table) for word in line.split()) if line.split() else ""
        for line in text.splitlines()
    )

    # Write the Morse code to the output file
    with open(output_file, 'w') as f:
        f.write(morse_code)


if __name__ == "__main__":
    english_to_morse()
    print("Conversion completed successfully.")