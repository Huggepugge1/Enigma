def base32_encode(string: bytes) -> bytes:
    """
    Encode base32 string
    """
    base32_chars = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    result = b""
    padding = b""

    padding_dict = {
        0: 0,
        1: 6,
        2: 4,
        3: 3,
        4: 1
    }

    padding_len = padding_dict[len(string) % 5]
        
    if padding_len != 0:
        string += b"\0" * padding_len
        padding += b"=" * padding_len

    for index, substring in enumerate([string[i:i+5] for i in range(0, len(string), 5)]):
        if index > 0 and (index / 5 * 8) % 76 == 0:
            result += b"\n"

        n = sum(((char << (4 - i) * 8) for i, char in enumerate(substring)))
        result += b"".join((base32_chars[(n >> (7 - i) * 5) & 31].to_bytes() for i in range(8)))

    return result.rstrip(b"A") + padding


def base32_decode(string: bytes) -> bytes:
    """
    Decode base32 string
    """
    base32_chars = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    result = b""
    string = string.replace(b"=", b"\0")
    string = string.replace(b"\n", b"")

    for substring in [string[i:i+8] for i in range(0, len(string), 8)]:
        n = sum(((0 if char == 0 else base32_chars.index(char.to_bytes()) << (7 - i) * 5) for i, char in enumerate(substring)))
        result += b"".join((((n >> (4 - i) * 8) & 255).to_bytes() for i in range(5)))

    return result.rstrip(b"\0")


def base64_encode(string: bytes) -> bytes:
    """
    Encode base64 string
    """
    base64_chars = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    result = b""
    padding = b""

    padding_len = 3 - len(string) % 3

    if padding_len != 0:
        string += b"\0" * padding_len
        padding += b"=" * padding_len

    for index, substring in enumerate([string[i:i+3] for i in range(0, len(string), 3)]):
        if index > 0 and (index / 3 * 4) % 76 == 0:
            result += b"\n"

        n = sum(((char << (2 - i) * 8) for i, char in enumerate(substring)))
        result += b"".join((base64_chars[(n >> (3 - i) * 6) & 63].to_bytes() for i in range(4)))
        
    return result[0:-padding_len] + padding


def base64_decode(string: bytes) -> bytes:
    """
    Decode base64 string
    """
    base64_chars = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    result = b""
    string = string.replace(b"=", b"\0")
    string = string.replace(b"\n", b"")

    for substring in [string[i:i+4] for i in range(0, len(string), 4)]:
        n = sum(((0 if char == 0 else base64_chars.index(char.to_bytes()) << (3 - i) * 6) for i, char in enumerate(substring)))
        result += b"".join((((n >> (2 - i) * 8) & 255).to_bytes() for i in range(3)))
        
    return result.rstrip(b"\0")


def to_base85(num: int) -> list[int]:
    result = []
    while num > 0:
        result.insert(0, num % 85)
        num //= 85
    return result


def from_base85(num: list[int]) -> int:
    result = 0
    for index, i in enumerate(num[::-1]):
        result += i * (85 ** index)

    return result


def base85_encode(string: bytes) -> bytes:
    result = b""
    for index, substring in enumerate([string[i:i+4] for i in range(0, len(string), 4)]):
        n = sum(((char << (3 - i) * 8) for i, char in enumerate(substring)))
        result += b"".join([(x + 33).to_bytes() for x in to_base85(n)])
    return result


def base85_decode(string: bytes) -> bytes:
    result = b""
    string += b"\0" * (len(string) % 5)
    for index, substring in enumerate([string[i: i+5] for i in range(0, len(string), 5)]):
        n = [char - 33 for char in substring]
        m = from_base85(n)
        result += b"".join(((m >> (8 * (3 - i))) & 255).to_bytes() for i in range(4))
    return result.rstrip(b"\0")


print(base32_encode(b"Hello World"))
print(base32_decode(b"JBSWY3DPEBLW64TMMQ======"))

print(base64_encode(b"Hello World"))
print(base64_decode(b"SGVsbG8gV29ybGQ="))

print(f"{from_base85([21, 79, 73, 64, 27]):b}")

print(base85_encode(b"Hello World"))
print(base85_decode(b"87cURD]i,\"Ebo7d"))
