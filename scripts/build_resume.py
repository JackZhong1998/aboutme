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

    # Use WenQuanYi Zen Hei (TTF, reportlab-compatible) for CJK.
    # No separate bold TTF available; create hierarchy via color + size contrast.
    pdfmetrics.registerFont(TTFont("CJK", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", subfontIndex=0))
    pdfmetrics.registerFontFamily("CJK", normal="CJK", bold="CJK", italic="CJK", boldItalic="CJK")

    ink = colors.HexColor("#111114")
    body_c = colors.HexColor("#4a4a52")
    muted_c = colors.HexColor("#8e8e96")
    base = dict(fontName="CJK", wordWrap="CJK")

    st = {
        "body": ParagraphStyle("b", fontSize=9, leading=14, textColor=body_c, spaceAfter=4, **base),
        "bullet": ParagraphStyle("l", fontSize=9, leading=14, textColor=body_c, spaceAfter=4,
                                leftIndent=18, firstLineIndent=0, bulletIndent=4,
                                bulletColor=colors.HexColor("#0066cc"), bulletFontSize=11, **base),
        "h1": ParagraphStyle("h1", fontSize=22, leading=28, textColor=ink, spaceAfter=2, **base),
        "h2": ParagraphStyle("h2", fontSize=13, leading=18, textColor=ink,
                             spaceBefore=12, spaceAfter=6, keepWithNext=True, **base),
        "h3": ParagraphStyle("h3", fontSize=11, leading=15, textColor=ink,
                             spaceBefore=9, spaceAfter=4, keepWithNext=True, **base),
        "h4": ParagraphStyle("h4", fontSize=9.5, leading=13.5, textColor=ink,
                             spaceBefore=6, spaceAfter=2, keepWithNext=True, **base),
    }

    def markup(s: str) -> str:
        s = html.escape(s)
        # Bold lead labels: dark ink color (visual hierarchy without bold TTF).
        s = re.sub(r"\*\*(.+?)\*\*", r'<font color="#111114">\1</font>', s)

        def link(m):
            url = m[0]
            if "github.com" in url:
                label = "代码"
            elif "mp.weixin" in url or "okjike" in url:
                label = "文章"
            else:
                label = "官网"
            return f'<a href="{url}" color="#0066cc">{label}</a>'

        return re.sub(r"https?://[^\s<｜]+", link, s)

    story = []
    for line in MD.splitlines():
        if not line.strip():
            continue
        if line.startswith("#"):
            n = len(line) - len(line.lstrip("#"))
            story.append(Paragraph(markup(line[n:].strip()), st[f"h{n}"]))
        elif line.startswith("- "):
            story.append(Paragraph(markup(line[2:]), st["bullet"], bulletText="·"))
        else:
            story.append(Paragraph(markup(line), st["body"]))

    def footer(c, doc):
        c.setFont("CJK", 7.5)
        c.setFillColor(colors.HexColor("#86868e"))
        c.drawString(48, 24, "钟镇杰 | AI 产品经理")
        c.drawRightString(547, 24, str(doc.page))

    def first_page(c, doc):
        # Draw headshot in top-right corner.
        img_path = str(ROOT / "assets" / "img" / "avatar.jpg")
        if Path(img_path).exists():
            c.drawImage(img_path, 480, 715, width=68, height=88, mask='auto')
        footer(c, doc)

    SimpleDocTemplate(str(ROOT / "resume.pdf"), pagesize=(595.28, 841.89), leftMargin=48, rightMargin=48,
                      topMargin=36, bottomMargin=44, title="钟镇杰｜AI产品经理｜简历",
                      author="钟镇杰").build(story, onFirstPage=first_page, onLaterPages=footer)


if __name__ == "__main__":
    build_html()
    build_pdf()
    print("resume.html and resume.pdf rebuilt")
