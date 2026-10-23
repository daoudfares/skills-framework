#!/usr/bin/env python3
"""Regenerate references/ from MuleSoft's published documentation.

The files under references/ are derived artifacts. Do not hand-edit them; run
this against newer sources instead, then update the pins in ATTRIBUTION.md and
the versions stated in SKILL.md.

    git clone --depth 1 --branch v4.12 \\
        https://github.com/mulesoft/docs-mule-runtime.git /tmp/mule-runtime
    git clone --depth 1 --branch v3.7 \\
        https://github.com/mulesoft/docs-munit.git /tmp/munit
    python3 scripts/build_references.py \\
        --runtime /tmp/mule-runtime --munit /tmp/munit --fetch-acb /tmp/acb

Anypoint Code Builder has no public documentation repository, so its pages are
fetched from the rendered site using its llms.txt manifest. --fetch-acb
downloads them into the given directory; --acb reuses an existing download.

Mule runtime documentation is BSD 3-Clause, Copyright (c) 2021 Salesforce.com,
Inc. MUnit documentation is Apache 2.0. See ATTRIBUTION.md and licenses/.
"""

import argparse
import hashlib
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adoc2md import convert as adoc_convert
from html2md import convert as html_convert

ACB_INDEX = 'https://docs.mulesoft.com/anypoint-code-builder/llms.txt'

# Release notes churn on every release and would swamp the digest that stands
# in for a commit on this source. They are not reference material either.
ACB_EXCLUDE = ('acb-release-notes.md',)

# ---------------------------------------------------------------------------
# What goes in each reference file. Order within a list is reading order, not
# alphabetical -- these are concatenated into one document.
# ---------------------------------------------------------------------------

RUNTIME = {
    'flows.md': (
        'Flows, events and the things that travel through them', [
            'about-mule-event', 'about-mule-message', 'about-mule-variables',
            'target-variables', 'about-flows', 'flow-component', 'flowref-about',
            'mule-components', 'scheduler-concept', 'correlation-id',
        ]),
    'routers.md': (
        'Routers and scopes', [
            'choice-router-concept', 'scatter-gather-concept', 'round-robin',
            'first-successful', 'for-each-scope-concept', 'parallel-foreach-scope',
            'until-successful-scope', 'async-scope-reference', 'try-scope-concept',
            'cache-scope', 'cache-scope-strategy', 'idempotent-message-validator',
        ]),
    'errors.md': (
        'Errors and error handling', [
            'mule-error-concept', 'error-handling', 'on-error-scope-concept',
            'raise-error-component-reference',
        ]),
    'configuration.md': (
        'Application structure, descriptors and properties', [
            'about-mule-configuration', 'mule-artifact-json',
            'package-a-mule-application', 'configuring-properties',
            'mule-app-properties-to-configure', 'secure-configuration-properties',
            'global-elements', 'shared-resources',
            'modularizing-your-configuration-files-for-team-development',
        ]),
    'streaming.md': (
        'Streaming', ['streaming-about', 'streaming-strategies-reference']),
    'batch.md': (
        'Batch processing', [
            'batch-processing-concept', 'batch-phases', 'batch-reference',
            'batch-filters-and-batch-aggregator', 'batch-error-concept',
            'batch-error-handling-faq', 'batch-job-instance-id',
        ]),
    'reliability.md': (
        'Transactions, retries and reliability', [
            'transaction-management', 'single-resource-transaction', 'xa-transactions',
            'reconnection-strategy-about', 'redelivery-policy', 'reliability-patterns',
            'mule-object-stores',
        ]),
    'deployment.md': (
        'Packaging, Maven and deployment targets', [
            'using-maven-with-mule', 'mmp-concept', 'maven-reference', 'deploying',
            'deploy-to-cloudhub-2', 'deploy-to-rtf', 'deploy-on-premises',
            'deploying-to-multiple-environments',
        ]),
    'performance.md': (
        'Performance tuning', [
            'tuning-guide', 'tuning-recommendations', 'tuning-repeatable-nonrepeatable',
            'tuning-backpressure-maxconcurrency', 'tuning-caching',
            'tuning-pooling-profiles', 'tuning-batch-processing', 'tuning-app-design',
            'tuning-logging', 'execution-engine',
        ]),
    'security.md': (
        'Security', [
            'securing', 'tls-configuration', 'authorization-grant-types',
            'component-authorization-using-spring-security',
            'setting-up-ldap-provider-for-spring-security',
        ]),
    'logging.md': (
        'Logging and debugging', [
            'logging-in-mule', 'logging-and-debugging', 'logging-mdc',
            'enable-verbose-logging', 'configuring-mule-stacktraces',
            'debugging-outside-studio', 'mule-server-notifications',
        ]),
}

MUNIT = {
    'munit.md': (
        'MUnit: suites, tests and lifecycle', [
            'index', 'munit-test-concept', 'before-after-scopes-reference',
            'enable-flow-sources-concept', 'parameterized', 'munit-showing-results',
            'munit-coverage-report', 'coverage-maven-concept', 'munit-maven-plugin',
        ]),
    'munit-processors.md': (
        'MUnit: processors', [
            'event-processors', 'set-event-processor', 'mock-event-processor',
            'verify-event-processor', 'spy-event-processor',
            'assertion-event-processor', 'assertion-equals-processor',
            'assertion-expression-processor', 'fail-event-processor',
            'run-custom-event-processor', 'storage-event-processors',
            'queue-processors', 'sleep-processor', 'dynamic-ports',
            'dynamic-directories', 'munit-utils', 'db-util', 'ftp-util',
        ]),
    'munit-matchers.md': (
        'MUnit: matchers', [
            'munit-matchers', 'core-matchers-reference', 'string-matchers-reference',
            'comparable-matchers-reference', 'iterable-map-matchers-reference',
            'resource-matchers-reference', 'dataweave-assertions-library',
        ]),
    'munit-cookbook.md': (
        'MUnit: worked examples', [
            'munit-cookbook', 'test-mock-errors-cookbook',
            'mock-before-after-foreach-cookbook', 'mock-file-cookbook',
            'use-environment-properties-on-tests-cookbook', 'utility-classes-cookbook',
            'test-flow-with-scheduler-cookbook', 'test-processor-that-uses-target-variable',
            'db-server-cookbook', 'ftp-server-cookbook',
        ]),
}

ACB = {
    # Anypoint Code Builder is a GUI product and most of its documentation is
    # click-through walkthroughs. Only the pages that answer a question an
    # agent editing XML actually has are worth shipping.
    'acb.md': (
        'Anypoint Code Builder: local workflow', [
            'index', 'int-versions', 'int-trigger-flows', 'int-debug-mule-apps',
            'int-run-mule-apps-with-properties', 'int-run-multiple-mule-apps',
            'ref-acb-commands', 'ref-connectors', 'ref-launch-json-properties',
            'ref-acb-maven',
        ]),
    'troubleshooting.md': (
        'Troubleshooting', [
            'troubleshooting', 'troubleshoot-mule-runtime-errors',
            'troubleshoot-implementation-errors', 'troubleshoot-dataweave',
            'troubleshoot-loading-errors', 'troubleshoot-deploy-errors',
            'troubleshoot-authentication-errors', 'troubleshoot-missing-features',
        ]),
}

# The component pages get their own builder: they share one rigid shape and are
# the reference an agent reaches for most often.
ACB_COMPONENTS = 'components.md'

SOURCE_NOTE = {
    'runtime': 'Derived from mulesoft/docs-mule-runtime (BSD 3-Clause).',
    'munit': 'Derived from mulesoft/docs-munit (Apache 2.0).',
    'acb': 'Derived from the Anypoint Code Builder documentation at '
           'docs.mulesoft.com.',
}


# "1. In the canvas, click the (Add component) icon." -- a step an agent can
# neither perform nor learn from. Whole procedures of these dominate the
# Anypoint Code Builder pages.
UI_STEP = re.compile(
    r'^(\s*)(?:\d+\.|[-*])\s+(?:Click|Select|In the|From the|Choose|Navigate|'
    r'Open the|Enter|Type|Press|Go to|Hover|Right-click|Double-click|Drag|'
    r'Notice|Scroll|Expand|Collapse|Toggle)\b')


def strip_ui_steps(text):
    return outside_code(_strip_ui_steps, text)


def _strip_ui_steps(text):
    """Drop GUI walkthrough steps and everything nested under them."""
    lines, out, i, n = text.split('\n'), [], 0, len(text.split('\n'))
    while i < n:
        m = UI_STEP.match(lines[i])
        if not m:
            out.append(lines[i]); i += 1; continue
        indent = len(m.group(1))
        i += 1
        while i < n:                       # swallow the step's continuation
            nxt = lines[i]
            if not nxt.strip():
                i += 1; continue
            if len(nxt) - len(nxt.lstrip()) > indent:
                i += 1; continue
            break
    return '\n'.join(out)


def outside_code(fn, text):
    """Apply fn only to the parts of text that are not fenced code blocks.

    Upstream ships shell and gitignore snippets whose `#` comments would
    otherwise be demoted into Markdown headings.
    """
    out, buf, in_code = [], [], False
    for ln in text.split('\n'):
        if ln.lstrip().startswith('```'):
            if not in_code:
                out.append(fn('\n'.join(buf))); buf = []
            in_code = not in_code
            out.append(ln)
        elif in_code:
            out.append(ln)
        else:
            buf.append(ln)
    out.append(fn('\n'.join(buf)))
    return '\n'.join(out)


def strip_see_also(text):
    """Drop trailing cross-reference lists; they point at pages we do not ship."""
    return re.sub(r'\n#+ See Also\n.*?(?=\n#|\Z)', '\n', text, flags=re.S)


def demote(text, levels=1):
    """Push every heading down so pages concatenate under one file title."""
    bump = lambda t: re.sub(r'^(#+)(?= )',
                            lambda m: '#' * min(len(m.group(1)) + levels, 6),
                            t, flags=re.M)
    return outside_code(bump, text)


def tidy(text):
    text = strip_see_also(text)
    text = re.sub(r'^\s*\n', '', text)
    return re.sub(r'\n{3,}', '\n\n', text).rstrip() + '\n'


INCLUDE = re.compile(r'^include::([^\[]+)\[([^\]]*)\]\s*$', re.M)


def extract_tag(text, tag):
    """Antora tagged region: // tag::name[] ... // end::name[]."""
    m = re.search(r'//\s*tag::%s\[\]\n(.*?)//\s*end::%s\[\]'
                  % (re.escape(tag), re.escape(tag)), text, re.S)
    return m.group(1) if m else ''


def resolve_includes(text, root, depth=0):
    """Inline Antora partials and example files.

    `partial$mmp-concept.adoc` alone is included 65 times across the runtime
    pages; dropping those leaves the Maven and deployment references full of
    holes. Includes that name another Antora component live in a repository we
    do not have, and are dropped.
    """
    if depth > 3:
        return text
    pages = os.path.join(root, 'modules', 'ROOT', 'pages')
    examples = os.path.join(root, 'modules', 'ROOT', 'examples')

    def repl(m):
        target, attrs = m.group(1).strip(), m.group(2)
        if '::' in target:
            return ''
        if target.startswith('partial$'):
            path = os.path.join(pages, '_partials', target[8:])
        elif target.startswith('example$'):
            path = os.path.join(examples, target[8:])
        elif target.startswith('{examplesdir}/'):
            path = os.path.join(examples, target[14:])
        else:
            return ''
        if not os.path.exists(path):
            return ''
        body = open(path, encoding='utf-8').read()
        tag = re.search(r'tags?=([\w-]+)', attrs)
        if tag:
            body = extract_tag(body, tag.group(1))
        if not body.strip():
            return ''
        if path.endswith(('.xml', '.json', '.yaml')):
            lang = {'xml': 'xml', 'json': 'json', 'yaml': 'yaml'}[path.rsplit('.', 1)[1]]
            return '[source,%s]\n----\n%s\n----' % (lang, body.strip())
        return resolve_includes(body, root, depth + 1)

    return INCLUDE.sub(repl, text)


def read_adoc(root, slug):
    path = os.path.join(root, 'modules', 'ROOT', 'pages', slug + '.adoc')
    if not os.path.exists(path):
        return None
    raw = resolve_includes(open(path, encoding='utf-8').read(), root)
    return adoc_convert(raw)


def read_acb(root, slug):
    path = os.path.join(root, slug + '.md')
    if not os.path.exists(path):
        return None
    return strip_ui_steps(html_convert(open(path, encoding='utf-8').read()))


def build_group(spec, reader, root, note, out_dir, missing):
    for name, (title, slugs) in sorted(spec.items()):
        parts = ['# ' + title, '', '> ' + note, '']
        for slug in slugs:
            body = reader(root, slug)
            if body is None:
                missing.append('%s: %s' % (name, slug))
                continue
            parts.append(demote(tidy(body)))
            parts.append('')
        write(os.path.join(out_dir, name), '\n'.join(parts))


def build_components(root, out_dir, missing):
    """One entry per Core component: what it does, its XML, its attributes."""
    slugs = sorted(f[:-3] for f in os.listdir(root)
                   if f.startswith('acb-component-') and f.endswith('.md'))
    parts = ['# Core component XML reference', '',
             '> ' + SOURCE_NOTE['acb'], '',
             'Every component also accepts `doc:name` (the canvas label) and',
             '`doc:id` (a generated identifier). Both are omitted below.', '']
    for slug in slugs:
        body = read_acb(root, slug)
        if body is None:
            missing.append('%s: %s' % (ACB_COMPONENTS, slug))
            continue
        body = tidy(body)
        # Keep everything up to the worked examples: the description, the XML
        # skeleton and the attribute and child-element tables.
        body = re.split(r'\n## (?:Examples?|Adding |Configure |Create |Use )',
                        body, maxsplit=1)[0]
        parts.append(demote(body.rstrip()))
        parts.append('')
    write(os.path.join(out_dir, ACB_COMPONENTS), '\n'.join(parts))


def fetch_acb(dest):
    os.makedirs(dest, exist_ok=True)
    with urllib.request.urlopen(ACB_INDEX) as r:
        index = r.read().decode('utf-8')
    urls = sorted(set(re.findall(
        r'https://docs\.mulesoft\.com/anypoint-code-builder/[\w.-]+\.md', index)))
    for url in urls:
        name = url.rsplit('/', 1)[1]
        with urllib.request.urlopen(url) as r:
            data = r.read()
        with open(os.path.join(dest, name), 'wb') as fh:
            fh.write(data)
    print('fetched %d Anypoint Code Builder pages' % len(urls), file=sys.stderr)
    return dest


def acb_digest(root):
    """Stand-in for a commit: a digest over the fetched page set.

    Deliberately reproducible with coreutils, so the value can be checked
    without running this script:

        ls | grep -v '^acb-release-notes.md$' | LC_ALL=C sort \\
          | xargs sha256sum | sha256sum | cut -c1-40

    LC_ALL=C matters: the default locale collates punctuation differently from
    the byte order this function sorts by, and the digests then disagree.
    """
    lines = []
    for name in sorted(os.listdir(root)):
        if not name.endswith('.md') or name in ACB_EXCLUDE:
            continue
        digest = hashlib.sha256(open(os.path.join(root, name), 'rb').read()).hexdigest()
        lines.append('%s  %s\n' % (digest, name))
    return hashlib.sha256(''.join(lines).encode()).hexdigest()[:40]


def write(path, text):
    text = re.sub(r'\n{3,}', '\n\n', text).rstrip() + '\n'
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--runtime', required=True, help='docs-mule-runtime checkout')
    ap.add_argument('--munit', required=True, help='docs-munit checkout')
    ap.add_argument('--acb', help='directory of already-fetched ACB .md pages')
    ap.add_argument('--fetch-acb', metavar='DIR',
                    help='download ACB pages into DIR, then use them')
    ap.add_argument('--out', default=None, help='output directory')
    args = ap.parse_args()

    if not (args.acb or args.fetch_acb):
        ap.error('one of --acb or --fetch-acb is required')
    acb_dir = fetch_acb(args.fetch_acb) if args.fetch_acb else args.acb

    out_dir = args.out or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'references')
    os.makedirs(out_dir, exist_ok=True)

    missing = []
    build_group(RUNTIME, read_adoc, args.runtime, SOURCE_NOTE['runtime'], out_dir, missing)
    build_group(MUNIT, read_adoc, args.munit, SOURCE_NOTE['munit'], out_dir, missing)
    build_group(ACB, read_acb, acb_dir, SOURCE_NOTE['acb'], out_dir, missing)
    build_components(acb_dir, out_dir, missing)

    files = sorted(os.listdir(out_dir))
    total = sum(os.path.getsize(os.path.join(out_dir, f)) for f in files)
    print('wrote %d files, %d KB' % (len(files), total // 1024), file=sys.stderr)
    print('acb digest: %s' % acb_digest(acb_dir), file=sys.stderr)
    if missing:
        print('MISSING PAGES (upstream renamed or removed):', file=sys.stderr)
        for m in missing:
            print('  ' + m, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
