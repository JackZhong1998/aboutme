# Zhong Zhenjie — Personal Site

钟镇杰的个人网站：在人与 Agent 的接触面上做产品。

在线地址：**https://jackzhong1998.github.io/aboutme/**

纯静态单页（原生 HTML / CSS / JS，无构建步骤），通过 GitHub Actions 自动部署到 GitHub Pages。

## 本地预览

```bash
# 任选其一
python3 -m http.server 8080
npx serve .
```

浏览器打开 `http://localhost:8080`。

## 目录结构

```
.
├── index.html        # 网站主页面（自包含，内联 CSS/JS）
├── resume.md         # 结构化简历（Markdown，GitHub 可直接阅读）
├── assets/img/       # 头像与项目配图
└── .github/workflows/deploy.yml  # push 到 main 自动部署
```

网站右下角「简历 · MD」支持：在线阅读格式化简历、一键复制 Markdown、下载 `.md`、打印 / 存为 PDF。
