import math
import nltk
from nltk.corpus import brown
from std_functions import log, output

wordlist = set(brown.words())


def calculate_similarity_to_english(input_text: bytes) -> float:
    """
    Used for evaluation of strings, not recommended for use outside this library
    """
    input_words = nltk.word_tokenize(str(input_text).lower())
    total_words = len(input_words)
    english_words = 0
    for word in input_words:
        if word in wordlist:
            k = 3
            weight = 1 / (1 + math.exp(-k * (len(word) - 3)))
            english_words += weight

    similarity = english_words / total_words
    return similarity


def caesar(string: bytes, n: int = None, known_strings: list[bytes] = None, possible_strings: list[bytes] = None,
        verbose: bool = False, output_file: str = "stdout") -> list[bytes]:
    """
    Decrypt Caesar-ciphers.
    Returns a list of all possibilities. Ranks them by likelihood of english
    Arguments:
        string: input string
        n (int): Rotation amount
        known_strings (list[bytes]): Any known strings in the final string, used for automatic decryption
        possible_strings (list[bytes]): Any possible strings in the final string, used for automatic decryption
        verbose (bool): True/False
        output_file: output file path
    """
    upper = lambda x: 65 <= x <= 90
    lower = lambda x: 97 <= x <= 122
    result = []

    if n is not None:
        current_result = b""
        for char in string:
            if upper(char):
                current_result += ((((char - 65) + n) % 26) + 65).to_bytes()
            elif lower(char):
                current_result += ((((char - 97) + n) % 26) + 97).to_bytes()
            else:
                current_result += char.to_bytes()
        result.append(current_result)

    elif known_strings is not None or possible_strings is not None:
        for i in range(1, 25):
            current_result = b""
            for char in string:
                if upper(char):
                    current_result += ((((char - 65) + i) % 26) + 65).to_bytes()
                elif lower(char):
                    current_result += ((((char - 97) + i) % 26) + 97).to_bytes()
                else:
                    current_result += char.to_bytes()

            if known_strings is not None:
                for s in known_strings:
                    if s.lower() not in current_result.lower():
                        break
                else:
                    if verbose:
                        output(f"Found \"n\" = {i} such that it satisfies all known_strings ({known_strings})",
                               output_file=output_file)
                        output(current_result, output_file=output_file)
                    else:
                        output(f"Possible candidate \"n\" = {i}", use_verbose=True, output_file=output_file)
                    result.append(current_result)
                    continue

            if possible_strings is not None:
                found = []
                for s in possible_strings:
                    if s.lower() in current_result.lower():
                        found.append(s.lower())

                if len(found) > 0:
                    if verbose:
                        output("--------------------------------")
                        output(f"Possible candidate n = \"{i}\", contains \"{found}\"", output_file=output_file)
                        output(current_result, end="\n\n", output_file=output_file)
                    else:
                        output(f"Possible candidate n = \"{i}\"", use_verbose=True, output_file=output_file)
                    result.append(current_result)

        if verbose and known_strings is not None:
            print(f"Could not find any \"n\" that satisfies {known_strings}")

    else:
        if verbose:
            log("Outputting all possibilities of Caesar-cipher")
        for i in range(1, 26):
            if verbose:
                output("-----------------------------------------------", output_file=output_file)
                output(f"Current n: {i}\n", output_file=output_file)

            current_result = b""
            for char in string:
                if upper(char):
                    current_result += ((((char - 65) + i) % 26) + 65).to_bytes()
                elif lower(char):
                    current_result += ((((char - 97) + i) % 26) + 97).to_bytes()
                else:
                    current_result += char.to_bytes()
            if verbose:
                output(current_result, output_file=output_file)
            result.append(current_result)

    result.sort(key=calculate_similarity_to_english, reverse=True)
    return result


print(caesar(b"TRVJRI TZGYVIJ RIV HLZKV VRJP KF TIRTB", known_strings=None, possible_strings=None, verbose=True))
