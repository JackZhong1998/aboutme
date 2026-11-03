"""Rebuild resume.html body and resume.pdf from resume.md.

Usage: python3 scripts/build_resume.py
"""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent.parent
MD = (ROOT / "resume.md").read_text(encoding="utf-8")


def inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)

    def link(m):
        url = m[1]
        if "originalPosts" in url:
            label = "即刻原文"
        elif "mp.weixin" in url:
            label = "微信文章"
        else:
            label = url.replace("https://", "").rstrip("/")
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>'

    return re.sub(r"(https?://[^\s<｜]+)", link, s)


def render(md: str) -> str:
    out, in_list = [], False
    for line in md.splitlines():
        if not line.strip():
            if in_list:
                out.append("</ul>")
                in_list = False
            continue
        if line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(line[2:])}</li>")
            continue
        if in_list:
            out.append("</ul>")
            in_list = False
        if line.startswith("#"):
            n = len(line) - len(line.lstrip("#"))
            out.append(f"<h{n}>{inline(line[n:].strip())}</h{n}>")
        else:
            out.append(f"<p>{inline(line)}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def build_html():
    path = ROOT / "resume.html"
    page = path.read_text(encoding="utf-8")
    start = page.index('<main class="document">') + len('<main class="document">')
    end = page.index("</main>", start)
    page = page[:start] + render(MD) + page[end:]
    path.write_text(page, encoding="utf-8")


def build_pdf():
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Paragraph, SimpleDocTemplate, PageBreak

    font_candidates = [
        ("/System/Library/Fonts/STHeiti Light.ttc", 0),
        ("/System/Library/Fonts/Supplemental/Songti.ttc", 0),
        ("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 0),
        ("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", 0),
    ]
    for font_path, idx in font_candidates:
        if not Path(font_path).exists():
            continue
        try:
            pdfmetrics.registerFont(TTFont("CJK", font_path, subfontIndex=idx))
            break
        except Exception:
            continue
    else:
        raise SystemExit("No embeddable CJK TrueType font found")
    ink, body_c = colors.HexColor("#1d1d1f"), colors.HexColor("#43434a")
    base = dict(fontName="CJK", wordWrap="CJK")
    st = {
        "body": ParagraphStyle("b", fontSize=8.5, leading=11.8, textColor=body_c, spaceAfter=1.5, **base),
        "bullet": ParagraphStyle("l", fontSize=8.5, leading=11.8, textColor=body_c, spaceAfter=1.5,
                                 leftIndent=10, firstLineIndent=-8, **base),
        "h1": ParagraphStyle("h1", fontSize=22, leading=29, textColor=ink, spaceAfter=4, **base),
        "h2": ParagraphStyle("h2", fontSize=12, leading=16, textColor=ink, spaceBefore=6, spaceAfter=3,
                             keepWithNext=True, **base),
        "h3": ParagraphStyle("h3", fontSize=10.5, leading=15, textColor=ink, spaceBefore=6, spaceAfter=2,
                             keepWithNext=True, **base),
        "h4": ParagraphStyle("h4", fontSize=9.5, leading=14, textColor=ink, spaceBefore=5, spaceAfter=2,
                             keepWithNext=True, **base),
    }

    def markup(s: str) -> str:
        s = html.escape(s)
        s = re.sub(r"\*\*(.+?)\*\*", r'<font color="#1d1d1f">\1</font>', s)

        def link(m):
            url = m[0]
            if "originalPosts" in url:
                label = "即刻原文"
            elif "mp.weixin" in url:
                label = "文章链接"
            else:
                label = url.replace("https://", "").rstrip("/")
            return f'<a href="{url}" color="#0066cc">{label}</a>'

        return re.sub(r"https?://[^\s<｜]+", link, s)

    story = []
    for line in MD.splitlines():
        if not line.strip():
            continue
        if line == "## 独立 Agent 产品实践":
            story.append(PageBreak())
        if line.startswith("#"):
            n = len(line) - len(line.lstrip("#"))
            story.append(Paragraph(markup(line[n:].strip()), st[f"h{n}"]))
        elif line.startswith("- "):
            story.append(Paragraph("• " + markup(line[2:]), st["bullet"]))
        else:
            story.append(Paragraph(markup(line), st["body"]))

    def footer(c, doc):
        c.setFont("CJK", 7.5)
        c.setFillColor(colors.HexColor("#808087"))
        c.drawString(40, 24, "钟镇杰 | AI 产品经理")
        c.drawRightString(555, 24, str(doc.page))

    SimpleDocTemplate(str(ROOT / "resume.pdf"), pagesize=(595.28, 841.89), leftMargin=40, rightMargin=40,
                      topMargin=28, bottomMargin=36, title="钟镇杰｜AI产品经理｜简历",
                      author="钟镇杰").build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build_html()
    build_pdf()
    print("resume.html and resume.pdf rebuilt")
