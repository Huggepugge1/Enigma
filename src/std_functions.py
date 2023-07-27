import nltk


def log(string):
    print(f"LOG: {string}")


def output(string, output_file="stdout", end="\n", use_verbose=False):
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


def setup_nltk():
    nltk.download("brown")
    nltk.download("punkt")