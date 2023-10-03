import subprocess
import encode
from std_functions import *
import auto_solve


def get_metadata_from_img(path: str, output_file="stdout", verbose=True):
    log(f"Running exiftool on \"{path}\"")
    result = subprocess.run(["exiftool", path], capture_output=True)
    if result.returncode != 0:
        if verbose:
            output(f"exiftool returned with a non 0 exitcode ({result.returncode})", output_file=output_file)
            output(f"{result.stderr}", output_file=output_file)
        return None
    
    tags = {tag.split(b": ")[0].rstrip(): tag.split(b": ")[1].rstrip() for tag in result.stdout[:-1].split(b"\n")}

    if verbose:
        for tag in tags:
            output(f"{tag} = {tags[tag]}", output_file)

    for tag in tags:
        decrypted = auto_solve.auto_solve(tags[tag])
        # print(decrypted)
        if decrypted[0][0] is not None:
            log(f"Possible point of interest: {decrypted[0][0]} of {tags[tag]} gives {decrypted[0][1]}")


    return tags


get_metadata_from_img("src/cat.jpg", verbose=False)
