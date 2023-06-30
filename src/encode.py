def base32_encode(string: str) -> str:
    """
    Encode base32 string
    """
    base32_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    result = ""
    padding = ""

    padding_dict = {
        0: 0,
        1: 6,
        2: 4,
        3: 3,
        4: 1
    }

    padding_len = padding_dict[len(string) % 5]
        
    if padding_len != 0:
        string += "\x00" * padding_len
        padding += "=" * padding_len

    for index, substring in enumerate([string[i:i+5] for i in range(0, len(string), 5)]):
        if index > 0 and (index / 5 * 8) % 76 == 0:
            result += "\n"

        n = sum(((ord(char) << (4 - i) * 8) for i, char in enumerate(substring)))
        result += "".join((base32_chars[(n >> (7 - i) * 5) & 31] for i in range(8)))

    return result.rstrip("A") + padding


def base32_decode(string: str) -> str:
    """
    Decode base32 string
    """
    base32_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    result = ""
    string = string.replace("=", "\0")
    string = string.replace("\n", "")

    for substring in [string[i:i+8] for i in range(0, len(string), 8)]:
        n = sum(((0 if substring[i] == "\0" else base32_chars.index(substring[i]) << (7 - i) * 5) for i in range(8)))
        result += "".join((chr((n >> (4 - i) * 8) & 255) for i in range(5)))
        
    return result


def base64_encode(string: str) -> str:
    """
    Encode base64 string
    """
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    result = ""
    padding = ""

    padding_len = 3 - len(string) % 3

    if padding_len != 0:
        string += "\0" * padding_len
        padding += "=" * padding_len

    for index, substring in enumerate([string[i:i+3] for i in range(0, len(string), 3)]):
        if index > 0 and (index / 3 * 4) % 76 == 0:
            result += "\n"

        n = sum(((ord(substring[i]) << (2 - i) * 8) for i in range(3)))
        result += "".join((base64_chars[(n >> (3 - i) * 6) & 63] for i in range(4)))
        
    return result[0:-padding_len] + padding


def base64_decode(string: str) -> str:
    """
    Decode base64 string
    """
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    result = ""
    string = string.replace("=", "\0")
    string = string.replace("\n", "")

    for substring in [string[i:i+4] for i in range(0, len(string), 4)]:
        n = sum(((0 if substring[i] == "\0" else base64_chars.index(substring[i]) << (3 - i) * 6) for i in range(4)))
        result += "".join((chr((n >> (2 - i) * 8) & 255) for i in range(3)))
        
    return result


print(base64_encode("Hello World"))
print(base64_decode("SGVsbG8gV29ybGQ="))

print(base32_encode("5QltpwtYIHFzPW8X0Zq3lCDirT9ViOBk"))
print(base32_decode("JBSWY3DPEBLW64TMMQ======"))
