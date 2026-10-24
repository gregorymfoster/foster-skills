#!/usr/bin/env python3
"""Write each platform's marketplace file from the root plugin.json, or check that they match."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = 'foster-skills'


def outputs(plugin):
    entry = {'name': plugin['name'], 'description': plugin['description'], 'version': plugin['version']}
    return {
        # Claude Code. The plugin is the repository root.
        '.claude-plugin/marketplace.json': {
            'name': MARKETPLACE,
            'owner': plugin['author'],
            'metadata': {'description': plugin['description']},
            'plugins': [dict(entry, source='.')],
        },
        # Codex and ChatGPT.
        '.agents/plugins/marketplace.json': {
            'name': MARKETPLACE,
            'interface': {'displayName': plugin['displayName']},
            'plugins': [{
                'name': plugin['name'],
                'source': {'source': 'local', 'path': './'},
                'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'},
                'category': 'Productivity',
            }],
        },
    }


def render(data):
    return json.dumps(data, indent=2, ensure_ascii=False) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if a generated file is out of date; write nothing.')
    args = parser.parse_args()
    plugin = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))
    stale = []
    for path, data in outputs(plugin).items():
        target = ROOT / path
        if target.exists() and target.read_text(encoding='utf-8') == render(data):
            continue
        stale.append(path)
        if not args.check:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render(data), encoding='utf-8')
    if args.check and stale:
        sys.exit('Out of date, run scripts/sync_plugin.py: ' + ', '.join(stale))
    print('\n'.join(stale) if stale else 'Plugin files are up to date.')


if __name__ == '__main__':
    main()
