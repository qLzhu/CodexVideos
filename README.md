# CodexVideos

本项目是一个面向内容生产（短剧 / 网文 / AIGC 提示词）的 **本地脚本管理与自动化生成平台 MVP**：

- 主线：`CLI + FastAPI + GitHub Actions`
- 可视化入口：`WebUI（MVP）`
- 配置驱动：模板、任务、质检规则、导出归档

## WebUI 可视化界面

`web/` 已提供可运行 MVP 页面：

- **Dashboard**：最近任务、快捷入口
- **Projects**：项目列表与详情
- **Templates**：模板列表、变量输入、渲染预览
- **Run Job**：选择 job config 并执行（真实 API 或 mock）
- **QC Reports**：报告列表与详情（JSON/Markdown）

> 功能截图占位：后续可补充真实截图到本节。

## 本地联调方式（前后端）

### 1）启动后端（FastAPI）

```bash
python -m pip install --upgrade pip
pip install -e .[dev]
uvicorn app.api.main:app --reload --port 8000
```

### 2）启动前端（WebUI）

```bash
cd web
npm install
npm run dev
```

前端默认地址：`http://localhost:5173`。

### 3）API 地址配置

编辑 `web/src/config.js`：

```js
window.__WEBUI_CONFIG__ = {
  API_BASE_URL: 'http://localhost:8000',
  USE_MOCK: false,
};
```

- `USE_MOCK=false`：本地联调真实 API
- `USE_MOCK=true`：静态演示模式（无需后端）

## WebUI 预览地址

优先方案：**GitHub Pages**（`deploy-webui.yml` 自动部署）。

- 预览地址规则：`https://<OWNER>.github.io/CodexVideos/`
- 示例占位：`https://YOUR_GITHUB_ID.github.io/CodexVideos/`

说明：

- GitHub Pages 仅托管静态资源，因此默认走 **mock 模式**。
- 完整流程演示请使用本地联调模式（FastAPI + WebUI）。

## 仓库 Description 推荐文案

- `本地AIGC脚本管理与自动化生成平台（CLI + WebUI + GitHub Actions）｜预览：https://<OWNER>.github.io/CodexVideos/`

## 如何更新仓库 Description（含命令）

### 1）GitHub CLI（推荐）

```bash
gh repo edit <OWNER>/CodexVideos \
  --description "本地AIGC脚本管理与自动化生成平台｜WebUI预览: https://<OWNER>.github.io/CodexVideos/"
```

### 2）GitHub API（curl）

```bash
curl -X PATCH \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/<OWNER>/CodexVideos \
  -d '{"description":"本地AIGC脚本管理与自动化生成平台｜WebUI预览: https://<OWNER>.github.io/CodexVideos/"}'
```

## API（WebUI 对接 MVP）

- `GET /health`
- `GET /version`
- `GET /api/projects`
- `GET /api/templates`
- `POST /api/templates/render`
- `POST /api/jobs/run`
- `GET /api/jobs`
- `GET /api/reports/qc`
- `GET /api/jobs/configs`

## GitHub Actions

现有 workflows：

1. `ci.yml`
2. `manual-generate.yml`
3. `scheduled-qc.yml`
4. `export-release.yml`
5. `deploy-webui.yml`（新增，部署 WebUI 到 GitHub Pages）

## 目录结构

```text
CodexVideos/
├─ app/
├─ web/
├─ configs/
├─ templates/
├─ projects/
├─ outputs/
├─ data/
├─ tests/
└─ .github/workflows/
```
