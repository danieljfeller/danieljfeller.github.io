#!/usr/bin/env python3
"""Convert demo.ipynb to demo_notebook/index.html."""

import json
import re
import html as html_lib
import base64
from pathlib import Path

import mistune

NOTEBOOK_PATH = Path("/Users/daniel/Code/solutions/demos/standard/federated_data_science/demo.ipynb")
NOTEBOOK_IMAGES_DIR = Path("/Users/daniel/Code/solutions/demos/standard/federated_data_science/images")
OUTPUT_PATH = Path("/Users/daniel/Code/danieljfeller.github.io/demo_notebook/index.html")

with open(NOTEBOOK_PATH) as f:
    nb = json.load(f)

md = mistune.create_markdown(plugins=["table", "strikethrough"])


def embed_local_images(html_str):
    """Replace src="images/..." with inline base64 data URIs."""
    def replace_src(m):
        src = m.group(1)
        img_path = NOTEBOOK_IMAGES_DIR / Path(src).name
        if img_path.exists():
            mime = "image/png" if img_path.suffix.lower() == ".png" else "image/jpeg"
            b64 = base64.b64encode(img_path.read_bytes()).decode()
            return f'src="data:{mime};base64,{b64}"'
        return m.group(0)
    return re.sub(r'src="images/([^"]+)"', replace_src, html_str)


def strip_ansi(text):
    return re.sub(r'\x1b\[[0-9;]*[mGKH]', '', text)


def render_outputs(outputs):
    parts = []
    for output in outputs:
        output_type = output.get("output_type", "")
        data = output.get("data", {})

        if "application/vnd.plotly.v1+json" in data:
            fig_json = json.dumps(data["application/vnd.plotly.v1+json"])
            div_id = f"plotly-{abs(hash(fig_json)) % 10**9}"
            # Encode as base64 to avoid any Jekyll/HTML escaping issues
            fig_b64 = base64.b64encode(fig_json.encode()).decode()
            parts.append(f'''<div class="output-plotly">
  <div id="{div_id}"></div>
  <script>
    (function(){{
      var d = atob("{fig_b64}");
      var fig = JSON.parse(d);
      var layout = Object.assign({{autosize:true, margin:{{l:50,r:30,t:50,b:50}}}}, fig.layout||{{}});
      Plotly.newPlot("{div_id}", fig.data, layout, {{responsive:true}});
    }})();
  </script>
</div>''')

        elif "image/png" in data:
            img = data["image/png"].strip()
            parts.append(f'<div class="output-image"><img src="data:image/png;base64,{img}"></div>')

        elif "text/html" in data:
            html_content = "".join(data["text/html"])
            parts.append(f'<div class="output-html">{html_content}</div>')

        elif "text/plain" in data:
            text = html_lib.escape("".join(data["text/plain"]))
            parts.append(f'<div class="output-text"><pre>{text}</pre></div>')

        if output_type == "stream":
            text = html_lib.escape("".join(output.get("text", [])))
            cls = "output-stderr" if output.get("name") == "stderr" else "output-stream"
            parts.append(f'<div class="{cls}"><pre>{text}</pre></div>')

        if output_type == "error":
            ename = html_lib.escape(output.get("ename", ""))
            evalue = html_lib.escape(output.get("evalue", ""))
            tb = strip_ansi("\n".join(output.get("traceback", [])))
            tb = html_lib.escape(tb)
            parts.append(f'<div class="output-error"><pre>{ename}: {evalue}\n{tb}</pre></div>')

    return "\n".join(parts)


cells_html = []
for i, cell in enumerate(nb["cells"]):
    cell_type = cell["cell_type"]
    source = "".join(cell.get("source", []))
    outputs = cell.get("outputs", [])

    if not source.strip() and not outputs:
        continue

    if cell_type == "markdown":
        rendered = embed_local_images(md(source))
        cells_html.append(f'<div class="cell cell-markdown">{rendered}</div>')

    elif cell_type == "code":
        escaped = html_lib.escape(source)
        output_html = render_outputs(outputs)
        output_block = f'<div class="cell-output">{output_html}</div>' if output_html.strip() else ""
        cells_html.append(f'''<div class="cell cell-code">
  <div class="cell-input"><pre><code class="language-python">{escaped}</code></pre></div>
  {output_block}
</div>''')

cells_content = "\n".join(cells_html)

HTML = f"""---
render_with_liquid: false
---
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Federated Data Science Demo — Rhino Health</title>
  <script src="https://cdn.plot.ly/plotly-2.34.0.min.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 14px;
      line-height: 1.6;
      color: #1f2328;
      background: #f6f8fa;
      margin: 0;
      padding: 24px 16px 80px;
    }}
    .notebook {{
      max-width: 900px;
      margin: 0 auto;
    }}
    /* Cells */
    .cell {{
      margin-bottom: 8px;
      border-radius: 6px;
    }}
    /* Markdown */
    .cell-markdown {{
      background: #fff;
      border: 1px solid #d0d7de;
      padding: 16px 20px;
    }}
    .cell-markdown h1 {{ font-size: 1.6em; border-bottom: 1px solid #d0d7de; padding-bottom: 8px; margin-top: 0; }}
    .cell-markdown h2 {{ font-size: 1.3em; border-bottom: 1px solid #d0d7de; padding-bottom: 6px; margin-top: 1em; }}
    .cell-markdown h3 {{ font-size: 1.1em; margin-top: 1em; }}
    .cell-markdown p {{ margin: 0.5em 0; }}
    .cell-markdown code {{
      background: #f6f8fa;
      border: 1px solid #d0d7de;
      border-radius: 3px;
      padding: 1px 5px;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 0.875em;
    }}
    .cell-markdown pre {{
      background: #f6f8fa;
      border: 1px solid #d0d7de;
      border-radius: 6px;
      padding: 12px 16px;
      overflow-x: auto;
    }}
    .cell-markdown pre code {{ background: none; border: none; padding: 0; font-size: 0.85em; }}
    .cell-markdown ul, .cell-markdown ol {{ padding-left: 1.5em; margin: 0.4em 0 0.6em; }}
    .cell-markdown li {{ margin-bottom: 3px; }}
    .cell-markdown table {{ border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 0.9em; }}
    .cell-markdown th, .cell-markdown td {{ border: 1px solid #d0d7de; padding: 6px 12px; }}
    .cell-markdown th {{ background: #f6f8fa; font-weight: 600; }}
    .cell-markdown blockquote {{
      border-left: 4px solid #0969da;
      margin: 0; padding: 4px 16px;
      color: #57606a; background: #f6f8fa;
    }}
    /* Code cells */
    .cell-code {{
      border: 1px solid #d0d7de;
      border-radius: 6px;
      overflow: hidden;
    }}
    .cell-input {{
      background: #fff;
    }}
    .cell-input pre {{
      margin: 0;
      padding: 12px 16px;
      overflow-x: auto;
      background: #fff;
    }}
    .cell-input code {{
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
      font-size: 13px;
      line-height: 1.5;
    }}
    /* Outputs */
    .cell-output {{
      border-top: 1px solid #d0d7de;
      background: #fff;
    }}
    .output-plotly {{ padding: 8px 0; }}
    .output-plotly > div:first-child {{ min-height: 400px; }}
    .output-image {{ padding: 12px 16px; }}
    .output-image img {{ max-width: 100%; display: block; }}
    .output-html {{ padding: 8px 16px; overflow-x: auto; font-size: 0.9em; }}
    .output-html table {{ border-collapse: collapse; }}
    .output-html th, .output-html td {{ border: 1px solid #d0d7de; padding: 5px 10px; font-size: 0.9em; }}
    .output-html th {{ background: #f6f8fa; }}
    .output-text pre, .output-stream pre {{
      margin: 0; padding: 10px 16px;
      font-family: "SFMono-Regular", Consolas, monospace;
      font-size: 12px;
      white-space: pre-wrap;
      word-break: break-word;
      color: #1f2328;
    }}
    .output-stderr pre {{ color: #cf222e; }}
    .output-error pre {{ color: #cf222e; background: #fff5f5; padding: 10px 16px; margin: 0; font-size: 12px; }}
  </style>
</head>
<body>
<div class="notebook">
{cells_content}
</div>
<script>hljs.highlightAll();</script>
</body>
</html>"""

OUTPUT_PATH.write_text(HTML)
print(f"Written {OUTPUT_PATH} ({OUTPUT_PATH.stat().st_size // 1024} KB)")
