import nltk
import re


STD_FLAG_REGEX = b"[A-Za-z0-9]+{.*?}"


def log(string):
    print(f"LOG: {string}")


def output(string: str, output_file: str="stdout", end: str="\n", use_verbose: bool=False):
    if output_file == "stdout":
        if use_verbose:
            print(f"{string}, use verbose for more output", end=end)
        else:
            print(f"{string}", end=end)

    else:
        with open(output_file, "a") as f:
            if use_verbose:
                f.write(f"{string}, use verbose for more output {end}")
            else:
                f.write(f"{string}{end}")


def print_file(path: str, output_file: str="stdout", verbose: bool=False):
    with open(path, "r") as file:
        if verbose:
            output("-" * 30, output_file=output_file)
            output(f"{path}", output_file=output_file)
            output("-" * 30 + "\n", output_file=output_file)
        
        output(file.read(), output_file=output_file)


def get_file_contents(path: str, output_file: str="stdout", verbose: bool=False):
    with open(path, "rb") as file:
        if verbose:
            output("-" * 30, output_file=output_file)
            output(f"{path}", output_file=output_file)
            output("-" * 30 + "\n", output_file=output_file)
        
        return file.read()


def get_line(string: bytes, match: re.Match):
    line_number = string[:match.start()].count(10) + 1
    i = 0
    rows = string.split(bytes("\n", "utf-8"))
    return (line_number, rows[line_number - 1])


def find_in_file(path: str, pattern: bytes=STD_FLAG_REGEX, output_file: str="stdout", full_line: bool=False, verbose: bool=False):
    result = []

    with open(path, "rb") as file:
        if verbose:
            output("-" * 30, output_file=output_file)
            output(f"{path}", output_file=output_file)
            output("-" * 30 + "\n", output_file=output_file)
        
        content = file.read()
        matches = re.finditer(pattern, content)
        
        for match in matches:
            if full_line:
                result.append(get_line(content, match))
            else:
                result.append((get_line(content, match)[0], match.group()))
            
            if verbose:
                output(f"line {result[-1][0]}: {result[-1][1]}", output_file=output_file)

        
        return result


def find_in_binary(path: str, pattern: bytes=STD_FLAG_REGEX, output_file: str="stdout", verbose: bool=False):
    result = []

    with open(path, "rb") as file:
        if verbose:
            output("-" * 30, output_file=output_file)
            output(f"{path}", output_file=output_file)
            output("-" * 30 + "\n", output_file=output_file)

        content = file.read()
        matches = re.finditer(pattern, content)
        
        for match in matches:
            result.append((get_line(content, match)[0], match.group()))
            
            if verbose:
                output(f"line {result[-1][0]}: {result[-1][1]}", output_file=output_file)

        
        return result


def find_in_string(string: bytes, pattern: bytes=STD_FLAG_REGEX, output_file: str="stdout", full_line: bool=False, verbose: bool=False):
    result = [] 
    
    matches = re.finditer(pattern, string)
    for match in matches:
        if full_line:
            result.append(get_line(string, match))
        else:
            result.append((get_line(string, match)[0], match.group()))
        
        if verbose:
            output(f"line {result[-1][0]}: {result[-1][1]}", output_file=output_file)
        

    return result


def setup_nltk():
    nltk.download("brown")
    nltk.download("punkt")
