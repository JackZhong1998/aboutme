# Zhong Zhenjie — Personal Site

钟镇杰的个人主页：AI Builder，在人与 Agent 的接触面上做产品。

在线地址：**https://jackzhong1998.github.io/aboutme/**

纯静态单页（原生 HTML/CSS/JS，无构建），push 到 `main` 后 GitHub Actions 自动部署。

## 本地预览

```bash
python3 -m http.server 8080
```

## 目录

- `index.html` — 主页（内联 CSS/JS）
- `resume.md` — 结构化简历（重点版）
- `assets/img/jike-avatar.jpg` — 头像
- `.github/workflows/deploy.yml` — Pages 自动部署

主页中「简历」入口支持阅读格式化简历、复制 Markdown、下载 `.md`、打印为 PDF。
