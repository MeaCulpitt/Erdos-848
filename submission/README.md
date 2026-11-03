# Submission sources

The LaTeX masters are the math-marked Markdown files (`*_src.md`, inline maths as `$...$`). `build2.py` (with `build.py` for the Unicode fallbacks) turns each into a pdflatex-compatible `.tex` and a PDF:

    python3 build2.py erdos848_src.md "Stability, rigidity and exact extremisers for Erd\H{o}s Problem 848" "Luke Culpitt (AI assisted)" erdos848.tex
    python3 build2.py witness_game_beyond_848_src.md "The witness game beyond Erd\H{o}s Problem 848: higher powers, \$ab+c\$, and the third density" "Luke Culpitt (AI assisted)" witness_game_beyond_848.tex

The `.tex` files compile with plain pdflatex (no XeLaTeX), as arXiv requires. The Markdown in `paper/` is the plain-Unicode working version; edits made there must be carried over to the `_src.md` files.
