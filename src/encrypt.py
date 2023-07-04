import math
import nltk
from nltk.corpus import brown

wordlist = set(brown.words())


def calculate_similarity_to_english(input_text: bytes) -> float:
    """
    Used for evaluation of strings, not recommended for use outside of this library
    """
    input_words = nltk.word_tokenize(input_text.lower())
    total_words = len(input_words)
    english_words = 0
    for word in input_words:
        if word in wordlist:
            k = 3
            weight = 1/(1+math.exp(-k * (len(word) - 3)))
            english_words += weight

    similarity = english_words / total_words
    return similarity


def rot(string: bytes, n: int = None, known_strings: list[bytes] = None, possible_strings: list[bytes] = None, verbose: bool = False) -> list[bytes]:
    """
    Decrypt ROT-ciphers.
    Returns a list of all possibilities. Ranks them by likelyhood of english
    Arguments:
        n (int): Rotation amount
        known_strings (list[bytes]): Any known strings in the final string, used for automatic decryption
        possible_strings (list[bytes]): Any possible strings in the final string, used for automatic decryption
        verbose (bool): True/False
    """
    upper = lambda x: 65 <= x <= 90
    lower = lambda x: 97 <= x <= 122
    result = []

    if n is not None:
        result.append(b"")
        for char in string:
            if upper(char):
                result[0] += ((((char - 65) + n) % 26) + 65).to_bytes()
            elif lower(char):
                result[0] += ((((char - 97) + n) % 26) + 97).to_bytes()
            else:
                result[0] += char.to_bytes()

    elif known_strings is not None or possible_strings is not None:
        for i in range(1, 25):
            for char in string:
                if upper(char):
                    result += ((((char - 65) + i) % 26) + 65).to_bytes()
                elif lower(char):
                    result += ((((char - 97) + i) % 26) + 97).to_bytes()
                else:
                    result += char.to_bytes()

            if known_strings is not None:
                for s in known_strings:
                    if s.lower() not in result.lower():
                        break
                else:
                    if verbose:
                        print(f"Found \"n\" = {i} such that it satisfies all known_strings ({known_strings})")
                    return result

            if possible_strings is not None:
                found = []
                for s in possible_strings:
                    if s.lower() in result.lower():
                        found.append(s.lower())

                if len(found) > 0:
                    if verbose:
                        print("--------------------------------")
                        print(f"Possible candidate n = \"{i}\", contains \"{found}\"")
                        print(result, end="\n\n")
                    else:
                        print(f"Possible candidate n = \"{i}\", use verbose to see the string")

            result = b""

        if verbose and known_strings is not None:
            print(f"Could not find any \"n\" that satisfies {known_strings}")
        
    else:
        if verbose == True:
            print("Printing all possibilities of ROT-cipher")
        for i in range(1, 26):
            if verbose:
                print("-----------------------------------------------")
                print(f"Current n: {i}\n")

                result = b""
            for char in string:
                if upper(char):
                    result += ((((char - 65) + i) % 25) + 65).to_bytes()
                elif lower(char):
                    result += ((((char - 97) + i) % 25) + 97).to_bytes()
                else:
                    result += char.to_bytes()

            print(result, end="\n\n\n")

    return result


print(rot(b"""Riihuhg vdb ylvlwhg hoghuob dqg. Zdlwhg shulrg duh sodbhg idplob pdq iruphg. Kh bh ergb ru pdgh rq sdlq sduw phhw. Brx rqh ghodb qru ehjlq rxu iroob dergh. Eb glvsrvhg uhsoblqj pu ph xqsdfnhg qr. Dv prrqoljkw ri pb uhvroylqj xqzloolqj.

Dsduwphqwv vlpsolflwb ru xqghuvwrrg gr lw zh. Vrqj vxfk hbhv kdg dqg rii. Uhpryhg zlqglqj dvn hasodlq gholjkw rxw ihz ehkdyhg odvwlqj. Ohwwhuv rog kdvwlob kdp vhqglqj qrw vha fkdpehu ehfdxvh suhvhqw. Rk lv lqghhg wzhqwb hqwluh iljxuh. Rffdvlrqdo glplqxwlrq dqqrxqflqj qhz qrz olwhudwxuh whuplqdwhg. Uhdoob uhjdug hafxvh rii whq sxoohg. Odgb dp urrp khdg vr odgb irxu ru hbhv dq. Kh gr ri frqvxowhg vrphwlphv frqfoxghg pu. Dq krxvhkrog ehkdylrxu li suhwhqghg. Brx fdq xvh wklvmxolxv dv iodj exw grqw irujhw wr irupdw.

Qrz lqgxojhqfh glvvlplodu iru klv wkrurxjkob kdv whuplqdwhg. Djuhhphqw riihqglqj frppdqghg pb dq. Fkdqjh zkroob vdb zkb hoghvw shulrg. Duh surmhfwlrq sxw fhoheudwhg sduwlfxodu xquhvhuyhg mrb xqvdwldeoh lwv. Lq wkhq gduh jrrg dp urvh euhg ru. Rq dp lq qhduhu vtxduh zdqwhg.""", known_strings=None, possible_strings=[b"you", b"flag", b"thisjulius"], verbose=True))
