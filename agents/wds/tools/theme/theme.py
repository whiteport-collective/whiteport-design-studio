"""
theme.py: the look of every artefact WDS renders. Part of WDS (agents/wds/tools/theme.md).

neutral.css is the default. The client's brand overrides it with tokens.css, found by walking up
from the folder being rendered, stopping at the repo root. At each level it looks for
brand/design-system/tokens.css, then brand/visual-identity/tokens.css, then visual-identity/tokens.css
(older repos). The nearest one wins.
"""

import re
from pathlib import Path

HERE = Path(__file__).parent
IMPORT = r"""@import\s+(?:url\([^)]*\)|"[^"]*"|'[^']*')[^;]*;"""  # a font URL may itself contain ";"
CANDIDATES = ("brand/design-system/tokens.css", "brand/visual-identity/tokens.css", "visual-identity/tokens.css")


def find_tokens(folder):
    folder = Path(folder).resolve()
    for level in [folder, *folder.parents]:
        for c in CANDIDATES:
            if (level / c).exists():
                return level / c
        if (level / ".git").exists():
            return None
    return None


class Theme:
    """values: the --wds-* roles resolved to plain values (for SVG). imports and css: for HTML pages."""

    def __init__(self, folder, override=None):
        self.tokens = Path(override) if override else find_tokens(folder)
        files = [HERE / "neutral.css"] + ([self.tokens] if self.tokens else [])
        css = "\n".join(f.read_text(encoding="utf-8") for f in files)
        props = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", css))

        def resolve(v, depth=0):
            if depth > 10:
                return v
            return re.sub(r"var\((--[\w-]+)(?:\s*,\s*([^)]+))?\)",
                          lambda m: resolve(props.get(m.group(1), m.group(2) or ""), depth + 1), v).strip()

        self.values = {k: resolve(v) for k, v in props.items() if k.startswith("--wds-")}
        self.imports = "\n".join(re.findall(IMPORT, css))
        self.css = re.sub(IMPORT, "", css)

    def get(self, key, default=""):
        return self.values.get(key, default)

    def describe(self):
        return f"neutral + {self.tokens}" if self.tokens else "neutral (no brand tokens.css found)"

    def style(self, page_css=""):
        """A <style> block for an HTML page: the font imports first, then the theme, then the page's own CSS."""
        return f"<style>{self.imports}\n{self.css}\n{page_css}</style>"


# ── VS Code: markdown in the brand's look ───────────────────────────────

VSCODE_CSS = """{imports}
.vditor{{border:0!important}}
.vditor-toolbar{{background:{surface}!important;border-bottom:1px solid {line}!important;padding-left:max(16px,calc(50% - 400px))!important}}
.vditor-content,.vditor-wysiwyg,.vditor-ir,.vditor-sv{{background:{paper}!important}}
.vditor-reset{{font-family:{body}!important;font-size:16px!important;line-height:1.75!important;color:{ink}!important;max-width:820px!important;margin:0 auto!important;padding:56px 32px 160px!important}}
.vditor-reset h1,.vditor-reset h2,.vditor-reset h3,.vditor-reset h4{{font-family:{display}!important;font-weight:{heading_weight}!important;color:{ink}!important}}
.vditor-reset h1{{font-size:2.3em!important;letter-spacing:-.02em;line-height:1.15!important;margin:0 0 .7em!important;border:0!important;padding:0!important}}
.vditor-reset h2{{font-size:1.55em!important;letter-spacing:-.01em;margin:2.2em 0 .7em!important;padding:0 0 .35em!important;border-bottom:1px solid {line}!important}}
.vditor-reset h3{{font-size:1.2em!important;margin:1.8em 0 .5em!important}}
.vditor-reset h4,.vditor-reset h5{{font-size:1em!important;margin:1.4em 0 .4em!important}}
.vditor-reset p{{margin:0 0 1em!important}}
.vditor-reset ul,.vditor-reset ol{{padding-left:1.4em!important;margin:0 0 1em!important}}
.vditor-reset li{{margin:.25em 0!important}}
.vditor-reset blockquote{{border-left:3px solid {accent}!important;background:{surface}!important;color:{ink2}!important;padding:.6em 1.1em!important;margin:1.2em 0!important;border-radius:0 {radius} {radius} 0}}
.vditor-reset table{{display:table!important;border-collapse:collapse!important;width:100%!important;font-size:.94em!important;margin:1.2em 0!important}}
.vditor-reset table tr{{background:transparent!important;border:0!important}}
.vditor-reset table th,.vditor-reset table td{{border:0!important;border-bottom:1px solid {line}!important;padding:9px 12px!important;text-align:left!important;vertical-align:top}}
.vditor-reset table th{{background:transparent!important;color:{ink3}!important;font-size:.78em!important;font-weight:600!important;letter-spacing:.05em;text-transform:uppercase}}
.vditor-reset code:not(.hljs){{font-family:{mono}!important;background:{surface}!important;padding:.12em .38em!important;border-radius:4px;font-size:.86em!important}}
.vditor-reset a{{color:{accent_ink}!important;text-decoration:underline!important;text-underline-offset:2px}}
.vditor-reset hr{{border:0!important;height:1px!important;background:{line}!important;margin:2em 0!important}}
.vditor-reset strong{{font-weight:600!important}}
"""


def vscode_css(th):
    v = th.get
    # Only fonts from the web reach VS Code's editor view; a relative @import cannot be resolved there.
    imports = "\n".join(i for i in th.imports.splitlines() if "http" in i)
    css = VSCODE_CSS.format(
        imports=imports, paper=v("--wds-paper"), surface=v("--wds-surface"), ink=v("--wds-ink"), ink2=v("--wds-ink-2"),
        ink3=v("--wds-ink-3"), line=v("--wds-line"), accent=v("--wds-accent"), accent_ink=v("--wds-accent-ink"),
        body=v("--wds-font-body"), display=v("--wds-font-display"), mono=v("--wds-font-mono"),
        radius=v("--wds-radius", "0"), heading_weight=v("--wds-heading-weight", "600"))
    return " ".join(css.split())


def write_vscode(repo, theme_path=None):
    """Writes the brand's look for markdown into <repo>/.vscode/settings.json, keeping every other setting."""
    import json
    repo = Path(repo)
    th = Theme(repo, theme_path)
    path = repo / ".vscode" / "settings.json"
    settings = {}
    if path.exists():
        text = re.sub(r"^\s*//.*$", "", path.read_text(encoding="utf-8"), flags=re.M)  # settings.json may have comments
        settings = json.loads(text or "{}")
    settings["markdown-editor.customCss"] = vscode_css(th)
    settings["markdown-editor.showLineNumbers"] = False
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(settings, indent=4, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"{path}  (tema: {th.describe()})")


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if len(args) >= 2 and args[0] == "vscode":
        write_vscode(args[1], args[args.index("--theme") + 1] if "--theme" in args else None)
    else:
        print("python theme.py vscode <repo> [--theme <css>]   # markdown in VS Code in the brand's look")
