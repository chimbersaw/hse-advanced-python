import os

from ast_visualizer_demo import main as ast_builder

sample_table = [
    [1, "alksjdfbanlm", 4, "293999"],
    [1, 2, 3, 4],
    [None, "pepepep", "0", 123]
]


def latex_header():
    return (
        "\\documentclass{article}\n"
        "\\usepackage{graphicx}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\begin{document}\n"
    )


def latex_footer():
    return "\\end{document}\n"


def table_to_latex(table):
    return table_header(table) + table_body(table) + table_footer()


def gen_columns(n):
    return "|" + " c |" * n


def gen_table_row(row):
    return " & ".join(map(str, row)) + "\\\\"


def table_header(table):
    return f"\\begin{{tabular}}{{{gen_columns(len(table[0]))}}}\n"


def table_body(table):
    return "\\hline\n" + "\n\\hline\n".join(map(gen_table_row, table)) + "\n\\hline\n"


def table_footer():
    return "\\end{tabular}\\\\\n"


def image_to_latex(path, scale=0.25):
    return f"\\includegraphics[scale={scale}]{{{path}}}\n"


def gen_latex(table, image_path):
    return latex_header() + table_to_latex(table) + image_to_latex(image_path) + latex_footer()


def main():
    if not os.path.exists("artifacts"):
        os.mkdir("artifacts")
    with open("artifacts/sample.tex", "w") as f:
        ast_builder()
        f.write(gen_latex(sample_table, "fib.png"))


if __name__ == "__main__":
    main()
