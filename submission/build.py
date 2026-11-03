"""Markdown (Claude Doc export) -> pdflatex-compatible LaTeX (arXiv-friendly) -> PDF."""
import re, sys, subprocess, pathlib
MAP = {'±':r'\ensuremath{\pm}','²':r'\ensuremath{^{2}}','³':r'\ensuremath{^{3}}','·':r'\ensuremath{\cdot}','¹':r'\ensuremath{^{1}}',
 '×':r'\ensuremath{\times}','ő':r'\H{o}','Σ':r'\ensuremath{\Sigma}','α':r'\ensuremath{\alpha}','β':r'\ensuremath{\beta}','δ':r'\ensuremath{\delta}',
 'η':r'\ensuremath{\eta}','θ':r'\ensuremath{\theta}','ι':r'\ensuremath{\iota}','κ':r'\ensuremath{\kappa}','λ':r'\ensuremath{\lambda}','μ':r'\ensuremath{\mu}',
 'ν':r'\ensuremath{\nu}','π':r'\ensuremath{\pi}','ρ':r'\ensuremath{\rho}','σ':r'\ensuremath{\sigma}','τ':r'\ensuremath{\tau}','ψ':r'\ensuremath{\psi}',
 'ω':r'\ensuremath{\omega}','…':r'\ldots{}','′':r'\ensuremath{'+"'"+'}','″':r'\ensuremath{'+"''"+'}',
 '⁰':r'\ensuremath{^{0}}','⁴':r'\ensuremath{^{4}}','⁵':r'\ensuremath{^{5}}','⁶':r'\ensuremath{^{6}}','⁷':r'\ensuremath{^{7}}','⁸':r'\ensuremath{^{8}}',
 '⁹':r'\ensuremath{^{9}}','⁺':r'\ensuremath{^{+}}','⁻':r'\ensuremath{^{-}}','₀':r'\ensuremath{_{0}}','₁':r'\ensuremath{_{1}}','₂':r'\ensuremath{_{2}}',
 '₃':r'\ensuremath{_{3}}','₄':r'\ensuremath{_{4}}','₅':r'\ensuremath{_{5}}','₆':r'\ensuremath{_{6}}','₇':r'\ensuremath{_{7}}','₈':r'\ensuremath{_{8}}',
 'ℓ':r'\ensuremath{\ell}','ℛ':r'\ensuremath{\mathcal{R}}','→':r'\ensuremath{\to}','↦':r'\ensuremath{\mapsto}','∅':r'\ensuremath{\emptyset}',
 '∈':r'\ensuremath{\in}','∉':r'\ensuremath{\notin}','∎':r'\ensuremath{\blacksquare}','∏':r'\ensuremath{\prod}','−':r'\ensuremath{-}',
 '∖':r'\ensuremath{\setminus}','√':r'\ensuremath{\surd}','∞':r'\ensuremath{\infty}','∤':r'\ensuremath{\nmid}','∥':r'\ensuremath{\parallel}',
 '∩':r'\ensuremath{\cap}','∪':r'\ensuremath{\cup}','≈':r'\ensuremath{\approx}','≠':r'\ensuremath{\neq}','≡':r'\ensuremath{\equiv}',
 '≢':r'\ensuremath{\not\equiv}','≤':r'\ensuremath{\le}','≥':r'\ensuremath{\ge}','⊄':r'\ensuremath{\not\subseteq}','⊆':r'\ensuremath{\subseteq}',
 '⊔':r'\ensuremath{\sqcup}','⌊':r'\ensuremath{\lfloor}','⌋':r'\ensuremath{\rfloor}','𝒞':r'\ensuremath{\mathcal{C}}','𝒫':r'\ensuremath{\mathcal{P}}',
 '∣':r'\ensuremath{\mid}','∗':r'\ensuremath{\ast}','⋯':r'\ensuremath{\cdots}','≪':r'\ensuremath{\ll}','∼':r'\ensuremath{\sim}'}
HEADER = r"""\usepackage{newunicodechar}
\usepackage{amssymb}
""" + "\n".join(r"\newunicodechar{%s}{%s}" % (k, v) for k, v in MAP.items() if k not in 'áèéö–') + "\n"

def sup_sub(line):
    # x^{...} -> ^...^ ; x^tok -> ^tok^ ; \_{...} -> ~...~ ; \_tok -> ~tok~   (pandoc super/subscript; spaces escaped)
    esc = lambda s: s.replace('\\_', '').replace('_', '').replace(' ', '\\ ')
    def sup(m):
        g = m.group(1)
        return '^' + (esc(g[1:-1]) if g.startswith('{') else g) + '^'
    line = re.sub(r'\^(\{[^{}]*\}|[0-9][0-9.]*[0-9]|[0-9]|[A-Za-z][A-Za-z0-9]*)', sup, line)
    def sub(m):
        g = m.group(1)
        return '~' + (esc(g[1:-1]) if g.startswith('{') else g) + '~'
    line = re.sub(r'(?<=[^\s\\~^])\\?_(\{[^{}]*\}|[A-Za-z0-9∞]+)', sub, line)
    return line

def convert(md, title, author, out):
    lines = md.split('\n')
    # drop title line and byline/author lines at the top
    body = []; i = 0
    while i < len(lines) and not lines[i].startswith('## '): i += 1
    in_code = False; code_lang = None; buf = []
    for l in lines[i:]:
        if l.startswith('```'):
            if not in_code:
                in_code = True; code_lang = l[3:].strip(); buf = []
            else:
                in_code = False
                if code_lang == 'latex': body.append('$$' + ' '.join(buf) + '$$')
                else: body += ['```'] + buf + ['```']
            continue
        if in_code: buf.append(l); continue
        if l.startswith('|') or l.startswith('- ') or l.startswith('  -') or re.match(r'\s*\d+[.)] ', l) or l.strip() == '' or True:
            # keep inline code spans intact
            parts = re.split(r'(`[^`]*`)', l)
            l = ''.join(p if p.startswith('`') else sup_sub(p) for p in parts)
        body.append(l)
    text = '\n'.join(body)
    meta = f"---\ntitle: |\n  {title}\nauthor: {author}\ndate: November 2026\n---\n\n"
    p = pathlib.Path(out); p.with_suffix('.md').write_text(meta + text)
    hdr = p.parent / 'header.tex'; hdr.write_text(HEADER)
    subprocess.run(['pandoc', str(p.with_suffix('.md')), '-s', '-o', str(p.with_suffix('.tex')),
                    '--from', 'markdown+superscript+subscript+pipe_tables+tex_math_dollars-auto_identifiers',
                    '-H', str(hdr), '-V', 'geometry:margin=2.4cm', '-V', 'fontsize=11pt', '-V', 'linkcolor=blue',
                    '-V', 'colorlinks=true'], check=True)
    for _ in range(2):
        r = subprocess.run(['pdflatex', '-interaction=nonstopmode', p.with_suffix('.tex').name], cwd=p.parent, capture_output=True, text=True)
    log = (p.parent / (p.stem + '.log')).read_text(errors='ignore')
    print(out, 'pdf ok' if p.with_suffix('.pdf').exists() else 'NO PDF', '| errors:', log.count('\n! '), '| missing chars:', log.count('Missing character'))
    for m in re.findall(r'\n! .*\n.*\n', log)[:8]: print('   ', m.strip()[:200])

if __name__ == "__main__":
    src, title, author, out = sys.argv[1:5]
    convert(open(src).read(), title, author, out)
