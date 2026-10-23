"""Markdown clean-up for the pages served by docs.mulesoft.com.

The `<page>.md` endpoints that `llms.txt` points at are mostly Markdown, but
every table is emitted as one unwrapped HTML blob on a single line. Those
tables carry the payload of the component reference pages -- the attribute
names, their XML spelling and what they do -- so they have to be recovered
rather than stripped.

Used by build_references.py; also runnable on a single file:

    python3 html2md.py <page.md>
"""

import html
import re
import sys
from html.parser import HTMLParser

# Cells that every component page repeats. They document the canvas label and
# the generated id, which are the same on all 29 components and say nothing
# about the component itself; SKILL.md states the rule once instead.
BOILERPLATE_ATTRS = ('doc:name', 'doc:id')


class TableParser(HTMLParser):
    """Collect <table> contents as rows of plain-text cells."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self._row = None
        self._cell = None
        self._header = False
        self.has_header = False

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self._row = []
        elif tag in ('td', 'th'):
            self._cell = []
            if tag == 'th':
                self._header = True
        elif tag in ('br', 'p', 'div', 'li') and self._cell is not None:
            self._cell.append(' ')

    def handle_endtag(self, tag):
        if tag == 'tr' and self._row is not None:
            if any(c.strip() for c in self._row):
                self.rows.append(self._row)
                if self._header and len(self.rows) == 1:
                    self.has_header = True
            self._row = None
        elif tag in ('td', 'th') and self._cell is not None:
            text = re.sub(r'\s+', ' ', ''.join(self._cell)).strip()
            if self._row is not None:
                self._row.append(text)
            self._cell = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)


def _emphasis(tag_text):
    """Re-apply the inline markup the parser flattened away."""
    tag_text = re.sub(r'<code>(.*?)</code>', r'`\1`', tag_text, flags=re.S)
    tag_text = re.sub(r'<strong>(.*?)</strong>', r'**\1**', tag_text, flags=re.S)
    tag_text = re.sub(r'<em>(.*?)</em>', r'*\1*', tag_text, flags=re.S)
    tag_text = re.sub(r'<a [^>]*>(.*?)</a>', r'\1', tag_text, flags=re.S)
    return tag_text


def table_to_md(raw, drop_boilerplate=True):
    p = TableParser()
    p.feed(_emphasis(raw))
    rows = [[c.replace('|', r'\|') for c in r] for r in p.rows]
    if drop_boilerplate:
        rows = [r for r in rows
                if not any(f'`{a}`' in c for a in BOILERPLATE_ATTRS for c in r)]
    if not rows:
        return ''
    width = max(len(r) for r in rows)
    rows = [r + [''] * (width - len(r)) for r in rows]
    if p.has_header:
        head, body = rows[0], rows[1:]
    else:
        head, body = [''] * width, rows
    if not body:
        return ''
    out = ['| ' + ' | '.join(head) + ' |', '|' + '---|' * width]
    out += ['| ' + ' | '.join(r) + ' |' for r in body]
    return '\n'.join(out)


# Only these are stripped as markup. Anything else inside angle brackets is a
# Mule XML element -- `<set-variable/>`, `<ee:transform/>` -- and those appear
# in headings and inline code, where they are the whole point of the page.
HTML_TAGS = ('a|b|br|col|colgroup|div|em|h[1-6]|i|img|li|nobr|ol|p|small|span|'
             'strong|sub|sup|table|tbody|td|th|thead|tr|ul|code')


def _protect_code(text):
    """Lift fenced code blocks out so no later rule can rewrite Mule XML."""
    blocks = []

    def stash(m):
        blocks.append(m.group(0))
        return '\x00CODE%d\x00' % (len(blocks) - 1)

    return re.sub(r'```.*?```', stash, text, flags=re.S), blocks


def convert(text, drop_boilerplate=True):
    text = re.sub(r'\A---\n.*?\n---\n', '', text, flags=re.S)     # frontmatter
    text = re.sub(r'^> For the full documentation index.*$\n?', '', text,
                  flags=re.M)
    text, blocks = _protect_code(text)
    text = re.sub(r'<table.*?</table>',
                  lambda m: '\n' + table_to_md(m.group(0), drop_boilerplate) + '\n',
                  text, flags=re.S)
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', text)              # images
    # Relative links point at the docs site, not at anything the skill ships.
    text = re.sub(r'\[([^\]]+)\]\((?!https?://)[^)]*\)', r'\1', text)
    text = re.sub(r'</?(?:%s)(?:\s[^>]*)?/?>' % HTML_TAGS, '', text)
    text = html.unescape(text)
    text = re.sub(r'[ \t]+$', '', text, flags=re.M)
    text = re.sub(r'\n{3,}', '\n\n', text).strip() + '\n'
    return re.sub(r'\x00CODE(\d+)\x00', lambda m: blocks[int(m.group(1))], text)


if __name__ == '__main__':
    print(convert(open(sys.argv[1], encoding='utf-8').read()))
