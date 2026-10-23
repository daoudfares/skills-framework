#!/usr/bin/env python3
"""Regenerate references/ from a checkout of mulesoft/docs-dataweave.

The files under references/ are derived artifacts. Do not hand-edit them; run
this against a newer upstream checkout instead, then update the pinned commit
in ATTRIBUTION.md and the version stated in SKILL.md.

    git clone --depth 1 --branch v2.12 \\
        https://github.com/mulesoft/docs-dataweave.git /tmp/dwdocs
    python3 scripts/build_references.py --source /tmp/dwdocs

Upstream is versioned per DataWeave release (v2.3 ... v2.12). Pin the branch
matching the Mule runtime the scripts actually run on -- the function set
differs between versions.

Source documentation is BSD 3-Clause, Copyright (c) 2021 Salesforce.com, Inc.
See ATTRIBUTION.md and LICENSE.txt.
"""

import argparse
import collections
import glob
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adoc2md import convert


def decode(s):
    return html.unescape(s)


def fn_strip_inline(s):
    s = re.sub(r'xref:[^\[]+\[([^\]]*)\]', r'\1', s)
    s = re.sub(r'link:[^\[]+\[([^\]]*)\]', r'\1', s)
    s = re.sub(r'<<[^,>]+,\s*([^>]+)>>', r'\1', s)
    s = re.sub(r'<<([^>]+)>>', r'\1', s)
    s = re.sub(r'image::?[^\[]+\[[^\]]*\]', '', s)
    s = s.replace('{dw-version}', DW_VERSION)
    return s.strip()


def clean_lines(text):
    out = []
    for ln in text.split('\n'):
        if ln.startswith(('ifndef::', 'ifdef::', 'endif::', 'include::', ':toc', '//')):
            continue
        out.append(ln)
    return out


LANGMAP = {'dataweave': 'dataweave', 'json': 'json', 'xml': 'xml', 'csv': 'text',
           'java': 'java', 'text': 'text', 'yaml': 'yaml'}

DW_VERSION = '2.12'

def parse_table(lines, i):
    """Parse a 2-col asciidoc table starting at/after i. Returns (rows, next_i)."""
    rows, n = [], len(lines)
    while i < n and not lines[i].startswith('|==='):
        if lines[i].strip() and not lines[i].startswith('['):
            pass
        i += 1
    if i >= n: return rows, i
    i += 1  # past opening |===
    cur = []
    while i < n and not lines[i].startswith('|==='):
        ln = lines[i]
        if ln.startswith('|'):
            parts = [p.strip() for p in ln.split('|')[1:]]
            cur.extend(parts)
        elif ln.strip() and cur:
            cur[-1] += ' ' + ln.strip()
        i += 1
    i += 1
    # first two cells are the header
    cells = cur[2:] if len(cur) > 2 else []
    for j in range(0, len(cells) - 1, 2):
        name, desc = cells[j], cells[j+1]
        if name:
            rows.append((fn_strip_inline(name), fn_strip_inline(desc)))
    return rows, i

def parse_block(lines, i):
    """Parse the delimited source block following heading line i.
    Always returns an index strictly greater than i."""
    n, lang = len(lines), ''
    j = i + 1                      # step past the '==== Source' heading
    while j < n and not lines[j].startswith('----'):
        m = re.match(r'\[source,\s*([A-Za-z]+)', lines[j])
        if m:
            lang = m.group(1)
        elif lines[j].startswith('='):   # ran into the next heading: no block
            return '', '', j
        j += 1
    if j >= n:
        return '', '', n
    j += 1
    buf = []
    while j < n and not lines[j].startswith('----'):
        buf.append(lines[j]); j += 1
    return lang, '\n'.join(buf).strip(), j + 1

LANGMAP = {'dataweave':'dataweave','json':'json','xml':'xml','csv':'text','java':'java','text':'text','yaml':'yaml'}

def parse_function(path):
    raw = decode(open(path, encoding='utf-8').read())
    lines = clean_lines(raw)
    title = ''
    for ln in lines:
        if ln.startswith('= '):
            title = ln[2:].strip(); break
    sigs, i, n = [], 0, len(lines)
    while i < n:
        if lines[i].startswith('== '):
            sig = lines[i][3:].strip()
            i += 1
            desc, params, ex = [], [], None
            in_desc = True
            while i < n and not lines[i].startswith('== '):
                ln = lines[i]
                if ln.startswith('==='):
                    in_desc = False
                if ln.startswith('=== Parameters'):
                    params, i = parse_table(lines, i)
                    continue
                if ln.startswith('=== Example') and ex is None:
                    src = out = None
                    j = i + 1
                    while j < n and not lines[j].startswith(('== ', '=== ')):
                        if lines[j].startswith('==== Source'):
                            lg, code, j = parse_block(lines, j); src = (lg, code); continue
                        if lines[j].startswith('==== Output'):
                            lg, code, j = parse_block(lines, j); out = (lg, code); continue
                        j += 1
                    if src: ex = (src, out)
                    i = j
                    continue
                if ln.startswith(('=== ', '==== ')):
                    i += 1; continue
                if in_desc and ln.strip() and not ln.startswith(('[', '|', '----')):
                    desc.append(fn_strip_inline(ln))
                i += 1
            sigs.append({'sig': sig, 'desc': ' '.join(desc).strip(),
                         'params': params, 'example': ex})
            continue
        i += 1
    return title, sigs

def render_function(title, sigs):
    o = ['## %s\n' % title]
    for s in sigs:
        o.append('```')
        o.append(s['sig'])
        o.append('```\n')
        if s['desc']:
            o.append(s['desc'] + '\n')
        if s['params']:
            for nm, d in s['params']:
                o.append('- `%s` \u2014 %s' % (nm.strip('`'), d))
            o.append('')
        if s['example']:
            (slang, scode), out = s['example']
            o.append('```%s' % LANGMAP.get(slang.lower(), 'dataweave'))
            o.append(scode)
            o.append('```')
            if out and out[1]:
                olang, ocode = out
                o.append('')
                o.append('```%s' % LANGMAP.get(olang.lower(), 'text'))
                o.append(ocode)
                o.append('```')
            o.append('')
    return '\n'.join(o)


TITLE = {'core': 'Core', 'strings': 'Strings', 'arrays': 'Arrays', 'objects': 'Objects',
         'types': 'Types', 'dates': 'Dates', 'periods': 'Periods', 'math': 'Math',
         'numbers': 'Numbers', 'runtime': 'Runtime', 'coercions': 'Coercions',
         'binaries': 'Binaries', 'crypto': 'Crypto', 'url': 'URL', 'tree': 'Tree',
         'values': 'Values', 'timer': 'Timer', 'system': 'System', 'mime': 'MIME',
         'multipart': 'Multipart', 'mule': 'Mule', 'diff': 'Diff', 'dtd': 'DTD'}

# modules whose example scripts never import them (Mule-implicit, or doc gaps)
NS_OVERRIDE = {'crypto': 'dw::Crypto', 'mule': 'dw::Mule',
               'multipart': 'dw::module::Multipart'}

# modules available without an explicit import
NO_IMPORT = ('core', 'mule')


def namespace(mod, paths):
    if mod in NS_OVERRIDE:
        return NS_OVERRIDE[mod]
    c = collections.Counter()
    for p in paths:
        for ns in re.findall(r'from\s+(dw::[A-Za-z:]+)', open(p, encoding='utf-8').read()):
            c[ns] += 1
    return c.most_common(1)[0][0] if c else 'dw::core'


def build_modules(pages, out):
    mods = collections.defaultdict(list)
    for p in sorted(glob.glob(os.path.join(pages, 'dw-*-functions-*.adoc'))):
        m = re.match(r'dw-(.+?)-functions-(.+)\.adoc$', os.path.basename(p))
        if m:
            mods[m.group(1)].append(p)
    results = []
    for mod, paths in sorted(mods.items()):
        ns = namespace(mod, paths)
        fns = sorted((parse_function(p) for p in paths), key=lambda x: x[0].lower())
        body = ['# dw::%s \u2014 %s functions\n' % (mod, TITLE.get(mod, mod)),
                'Namespace `%s`.' % ns,
                '' if mod in NO_IMPORT else
                'Requires an explicit import: `import * from %s`.' % ns,
                '',
                'Functions: ' + ', '.join('`%s`' % t for t, _ in fns) + '\n',
                '---\n']
        for t, s in fns:
            body.append(render_function(t, s))
        txt = re.sub(r'\n{4,}', '\n\n\n', '\n'.join(body).rstrip() + '\n')
        open(os.path.join(out, mod + '.md'), 'w', encoding='utf-8').write(txt)
        results.append((mod + '.md', len(fns), len(txt)))
    return results


# Language-level pages, concatenated and re-levelled into one file each.
GUIDES = [
    ('language', 'DataWeave language reference',
     'Script structure, variables, functions, flow control, pattern matching, '
     'scoping and operators.',
     ['dataweave-language-guide', 'dataweave-variables', 'dataweave-functions',
      'dataweave-flow-control', 'dataweave-flow-control-precedence',
      'dataweave-pattern-matching', 'dataweave-scope-visibility', 'dw-operators']),
    ('selectors', 'DataWeave selectors',
     'Traversing objects and arrays: single-value, multi-value, descendants, '
     'index, range, attribute, namespace, filter and metadata selectors.',
     ['dataweave-selectors', 'dataweave-selecting-types']),
    ('type-system', 'DataWeave type system',
     'Built-in types, the type system, and coercion rules.',
     ['dataweave-types', 'dataweave-type-system', 'dataweave-types-coercion']),
    ('formats', 'DataWeave data formats',
     'Supported MIME types with their reader and writer properties.',
     ['dataweave-formats', 'dataweave-formats-json', 'dataweave-formats-xml',
      'dataweave-formats-csv', 'dataweave-formats-flatfile',
      'dataweave-formats-fixedwidth', 'dataweave-formats-excel',
      'dataweave-formats-java', 'dataweave-formats-yaml', 'dataweave-formats-text',
      'dataweave-formats-urlencoded', 'dataweave-formats-ndjson',
      'dataweave-formats-multipart', 'dataweave-formats-binary']),
    ('troubleshooting', 'DataWeave troubleshooting',
     'Common errors, their causes and fixes.',
     ['dataweave-troubleshoot', 'dataweave-versioning-behavior']),
]


def build_guides(pages, out):
    results = []
    for name, title, intro, srcs in GUIDES:
        parts = ['# %s\n' % title, intro.strip() + '\n']
        for pg in srcs:
            path = os.path.join(pages, pg + '.adoc')
            if not os.path.exists(path):
                print('  warning: missing upstream page %s' % pg, file=sys.stderr)
                continue
            md = convert(open(path, encoding='utf-8').read())
            md = re.sub(r'^#\s+(.*)$', r'## \1', md, count=1, flags=re.M)
            md = re.sub(r'^(#{2,})\s', lambda m: '#' * (len(m.group(1)) + 1) + ' ',
                        md, flags=re.M)
            md = re.sub(r'^###\s+(.*)$', r'## \1', md, count=1, flags=re.M)
            parts.append(md.strip())
            parts.append('\n---\n')
        txt = re.sub(r'\n{3,}', '\n\n', '\n'.join(parts[:-1]).rstrip() + '\n')
        open(os.path.join(out, name + '.md'), 'w', encoding='utf-8').write(txt)
        results.append((name + '.md', len(srcs), len(txt)))
    return results


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--source', required=True,
                    help='checkout of github.com/mulesoft/docs-dataweave')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(here), 'references'),
                    help='output directory (default: ../references)')
    a = ap.parse_args()

    pages = os.path.join(a.source, 'modules', 'ROOT', 'pages')
    if not os.path.isdir(pages):
        ap.error('no modules/ROOT/pages under %s -- is that a docs-dataweave '
                 'checkout?' % a.source)
    os.makedirs(a.out, exist_ok=True)

    rows = build_modules(pages, a.out) + build_guides(pages, a.out)
    total = 0
    for name, n, size in rows:
        print('  %-20s %3d  %7.1f KB' % (name, n, size / 1024.0))
        total += size
    print('  %-20s %3s  %7.1f KB in %d files' % ('TOTAL', '', total / 1024.0, len(rows)))


if __name__ == '__main__':
    main()
