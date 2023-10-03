import encrypt
import encode

encryption_functions = [
    "caesar"
]

encoding_functions = [
    "decimal_decode",
    "base32_encode",
    "base32_decode",
    "base64_encode",
    "base64_decode",
    "base85_encode",
    "base85_decode"
]


def auto_solve(string: bytes):
    if string == b"":
        return None

    result = []

    result.append((None, string))

    for function_name in dir(encrypt):
        if function_name in encryption_functions:
            function = getattr(encrypt, function_name)
            result.append((function_name, function(string)[0]))

    for function_name in dir(encode):
        if function_name in encoding_functions:
            function = getattr(encode, function_name)
            result.append((function_name, function(string)))
    
    result.sort(key=lambda x: 0 if x[1] == None else encrypt.calculate_similarity_to_english(x[1]), reverse=True)
    return result
