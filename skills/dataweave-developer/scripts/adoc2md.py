"""AsciiDoc (Antora) to Markdown conversion for MuleSoft's DataWeave docs.

Handles the subset of AsciiDoc those docs use: headings, source and listing
blocks, tables (including per-line cells and style specifiers), lists, block
titles, admonitions and inline cross-references. Tolerates the malformed
blocks that appear upstream, such as a [source] with no opening delimiter.

Used by build_references.py; also runnable on a single file:

    python3 adoc2md.py <page.adoc>
"""

import re, html, os, sys

LANG = {'dataweave':'dataweave','json':'json','xml':'xml','java':'java','csv':'text',
        'yaml':'yaml','text':'text','scala':'scala','sql':'sql','shell':'sh','bash':'sh',
        'console':'text','xquery':'text','properties':'ini','avro':'json','none':'text'}

def humanize(ref):
    ref = re.sub(r'\.adoc.*$', '', ref).split('/')[-1]
    ref = ref.replace('dataweave-', '').replace('dw-', '')
    return re.sub(r'[_-]+', ' ', ref).strip()

def _xref(m):
    label = m.group(2).strip()
    return label if label else humanize(m.group(1))

def inline(s):
    s = re.sub(r'xref:([^\[]+)\[([^\]]*)\]', _xref, s)
    s = re.sub(r'link:([^\[]+)\[([^\]]*)\]', _xref, s)
    s = re.sub(r'https?://(\S+?)\[([^\]]*)\]', _xref, s)
    s = re.sub(r'<<[^,>]+,\s*([^>]+)>>', r'\1', s)
    s = re.sub(r'<<([^>]+)>>', lambda m: humanize(m.group(1)), s)
    s = re.sub(r'image::?[^\[]*\[[^\]]*\]', '', s)
    s = re.sub(r'`\+([^+]*)\+`', r'`\1`', s)      # `+literal+`
    s = re.sub(r'\*\*(.+?)\*\*', r'**\1**', s)
    s = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'**\1**', s)
    s = re.sub(r'\{dw-version\}', '2.12', s)
    s = re.sub(r'\{[a-z-]+\}', '', s)
    return s.rstrip()

def convert(text):
    text = html.unescape(text)
    lines = text.split('\n')
    out, i, n = [], 0, len(lines)
    pending_attr = ''
    while i < n:
        ln = lines[i]
        if ln.startswith(('ifndef::','ifdef::','endif::','include::','//',
                          'image::','video::')) or re.match(r'^:[\w-]+:', ln):
            i += 1; continue
        if re.match(r'^\[\[[^\]]+\]\]$', ln):
            i += 1; continue
        # source block
        m = re.match(r'^\[source,\s*([A-Za-z]+)', ln)
        if m or ln.startswith('[source]'):
            lang = LANG.get((m.group(1).lower() if m else 'text'), 'text')
            j = i + 1
            while j < n and (re.match(r'^\[[^\]]*\]$', lines[j])
                             or re.match(r'^\.\S', lines[j])
                             or not lines[j].strip()):
                j += 1              # attribute lines, block titles, blank lines
            fenced = j < n and lines[j].startswith('----')
            if fenced:
                j += 1                      # well-formed: opening delimiter
            # else: upstream omitted the opening delimiter; content starts here
            buf = []
            while j < n and not lines[j].startswith('----'):
                # a heading only terminates an unfenced block; inside a real
                # one, a leading '=' is DataWeave code ("= aString match {")
                if not fenced and (lines[j].startswith('=')
                                   or lines[j].startswith('[[')
                                   or lines[j].startswith('[source')):
                    break
                buf.append(lines[j]); j += 1
            if j < n and lines[j].startswith('----'):
                j += 1
            while buf and not buf[-1].strip():
                buf.pop()
            if buf:
                out.append('```' + lang); out.extend(buf); out.append('```'); out.append('')
            i = j; continue
        # bare listing block
        if ln.startswith('----'):
            j = i + 1; buf = []
            while j < n and not lines[j].startswith('----'):
                buf.append(lines[j]); j += 1
            out.append('```text'); out.extend(buf); out.append('```'); out.append('')
            i = j + 1; continue
        # table — triggered by the |=== delimiter itself, since the
        # [%header]/[cols] attribute line is optional in these docs
        if ln.startswith('|==='):
            j = i + 1; rows, cur = [], []
            while j < n and not lines[j].startswith('|==='):
                # a cell may open with a style specifier at line start: "a| ..."
                l2 = re.sub(r'^[adsmhlev]\|', '|', lines[j])
                if l2.startswith('|'):
                    if cur: rows.append(cur)
                    # drop AsciiDoc cell-style specifiers ("a|", "h|", "m|" ...)
                    l2 = re.sub(r'(?<=\s)[adsmhlev]\|', '|', l2)
                    cur = [c.strip() for c in l2.split('|')[1:]]
                elif l2.strip() and cur:
                    frag = l2.strip()
                    # nested list markers inside a cell become bullet separators
                    frag = re.sub(r'^\*+\s+', '\u00b7 ', frag)
                    cur[-1] += ' ' + frag
                j += 1
            if cur: rows.append(cur)
            m2 = re.search(r'cols="([^"]+)"', pending_attr)
            ncols = len(m2.group(1).split(',')) if m2 else 0
            pending_attr = ''
            if ncols > 1:
                flat = [c for r in rows for c in r]
                rows = [flat[k:k+ncols] for k in range(0, len(flat), ncols)]
            rows = [[inline(c) for c in r] for r in rows if any(c.strip() for c in r)]
            if rows:
                w = max(len(r) for r in rows)
                rows = [r + ['']*(w-len(r)) for r in rows]
                out.append('| ' + ' | '.join(rows[0]) + ' |')
                out.append('|' + '---|'*w)
                for r in rows[1:]:
                    out.append('| ' + ' | '.join(x.replace('|','\\|') for x in r) + ' |')
                out.append('')
            i = j + 1; continue
        # headings
        m = re.match(r'^(=+)\s+(.*)$', ln)
        if m:
            out.append('#'*len(m.group(1)) + ' ' + inline(m.group(2))); out.append('')
            i += 1; continue
        # admonitions
        m = re.match(r'^(NOTE|TIP|IMPORTANT|WARNING|CAUTION):\s*(.*)$', ln)
        if m:
            out.append('> **%s:** %s' % (m.group(1).title(), inline(m.group(2))))
            out.append(''); i += 1; continue
        # block title: a leading dot with no following space
        m = re.match(r'^\.(\S.*)$', ln)
        if m and not ln.startswith('..'):
            out.append('**' + inline(m.group(1)) + '**'); out.append('')
            i += 1; continue
        # lists
        m = re.match(r'^(\*+)\s+(.*)$', ln)
        if m:
            out.append('  '*(len(m.group(1))-1) + '- ' + inline(m.group(2))); i += 1; continue
        m = re.match(r'^(\.+)\s+(\S.*)$', ln)
        if m and not ln.startswith('...'):
            out.append('  '*(len(m.group(1))-1) + '1. ' + inline(m.group(2))); i += 1; continue
        if ln.strip() in ('====','****','--','+'):
            i += 1; continue
        if ln.startswith('[') and ln.endswith(']'):
            pending_attr = ln
            i += 1; continue
        out.append(inline(ln)); i += 1
    txt = '\n'.join(out)
    txt = re.sub(r'\n{3,}', '\n\n', txt)
    return txt.strip() + '\n'

if __name__ == '__main__':
    print(convert(open(sys.argv[1], encoding='utf-8').read()))
