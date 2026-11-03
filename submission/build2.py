"""Math-marked Markdown ($...$) -> LaTeX (pdflatex, arXiv-compatible) -> PDF.  Leftover Unicode handled by newunicodechar."""
import re, sys, subprocess, pathlib
from build import HEADER
EXTRA = r"""\usepackage{amsmath,amssymb,amsthm}
\allowdisplaybreaks
\renewcommand{\arraystretch}{1.15}
"""
def convert(md, title, author, out):
    lines = md.split('\n'); i = 0
    while i < len(lines) and not lines[i].startswith('## '): i += 1
    body = '\n'.join(lines[i:])
    body = re.sub(r'```latex\n(.*?)\n```', lambda m: '$$' + ' '.join(m.group(1).split('\n')) + '$$', body, flags=re.S)
    meta = f"---\ntitle: |\n  {title}\nauthor: {author}\ndate: November 2026\n---\n\n"
    p = pathlib.Path(out); p.with_suffix('.md').write_text(meta + body)
    hdr = p.parent / 'header2.tex'; hdr.write_text(EXTRA + HEADER)
    subprocess.run(['pandoc', str(p.with_suffix('.md')), '-s', '-o', str(p.with_suffix('.tex')),
                    '--from', 'markdown+tex_math_dollars+pipe_tables-auto_identifiers-subscript-superscript',
                    '-H', str(hdr), '-V', 'geometry:margin=2.4cm', '-V', 'fontsize=11pt', '-V', 'colorlinks=true'], check=True)
    for _ in range(2):
        subprocess.run(['pdflatex', '-interaction=nonstopmode', p.with_suffix('.tex').name], cwd=p.parent, capture_output=True, text=True)
    log = (p.parent / (p.stem + '.log')).read_text(errors='ignore')
    print(out, 'pdf ok' if p.with_suffix('.pdf').exists() else 'NO PDF', '| errors:', log.count('\n! '), '| missing chars:', log.count('Missing character'))
    for m in re.findall(r'\n! .*\n(?:.*\n){0,3}', log)[:10]: print('   ', m.strip().replace('\n', ' | ')[:300])
if __name__ == "__main__":
    src, title, author, out = sys.argv[1:5]
    convert(open(src).read(), title, author, out)
