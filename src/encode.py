def base64_encode(string: str) -> str:
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    result = ""
    padding = ""

    padding_len = len(string) % 3

    if padding_len != 0:
        string += "\0" * (3 - padding_len)
        padding += "=" * (3 - padding_len)

    for index, substring in enumerate([string[i:i+3] for i in range(0, len(string), 3)]):
        if index > 0 and (index / 3 * 4) % 76 == 0:
            result += "\n"

        n = sum(((ord(substring[i]) << (2 - i) * 8) for i in range(3)))
        result += "".join((base64_chars[(n >> (3 - i) * 6) & 63] for i in range(4)))
        
    return result[0:-len(padding)] + padding


def base64_decode(string: str) -> str:
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

