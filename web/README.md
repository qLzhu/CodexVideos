# CodexVideos WebUI (MVP)

本目录提供可运行的可视化界面（MVP），覆盖：

- Dashboard：最近任务 + 快捷入口
- Projects：项目列表/详情
- Templates：模板列表、变量输入、渲染预览
- Run Job：选择配置并触发任务
- QC Reports：查看质检报告（JSON/Markdown）

## 运行模式

1. **本地联调模式（真实 API）**
   - 修改 `src/config.js`：`USE_MOCK=false`，`API_BASE_URL='http://localhost:8000'`
2. **静态演示模式（GitHub Pages）**
   - `USE_MOCK=true`，所有页面使用内置 mock 数据

## 本地启动

```bash
cd web
npm install
npm run dev
```

默认地址：`http://localhost:5173`。

## 构建

```bash
cd web
npm run build
npm run preview
```

构建产物位于 `web/dist/`，可直接用于静态托管。
