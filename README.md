# CodexVideos

本项目是一个面向内容生产（短剧 / 网文 / AIGC 提示词）的 **本地脚本管理与自动化生成平台 MVP**，核心定位是：

- 本地开发调试：`CLI + FastAPI`
- 自动化批处理：`GitHub Actions`
- 配置驱动：模板、任务、质检规则、导出归档
- 可追溯：输出目录、日志、报告统一管理

> 当前版本优先保证 CLI 与自动化链路可跑通，WebUI 目录为占位。

## 核心能力

- 配置系统（优先级：CLI 参数 > 环境变量 > YAML > 默认值）
- Prompt 模板变量识别 / 校验 / 渲染
- 批量任务执行（支持 Mock/Echo 模型适配器）
- 基础规则质检（总结腔、重复、段落长度）
- 导出（`md/json/csv/zip`）
- FastAPI 基础服务（`/health`、`/version`）
- GitHub Actions（CI、手动生成、定时质检、导出）

## 架构说明

- 主线：`Python Core + CLI + GitHub Actions`
- API：FastAPI 提供基础可用能力
- WebUI：`web/README.md` 先占位，后续扩展

## 目录结构

```text
CodexVideos/
├─ app/
│  ├─ api/
│  ├─ cli/
│  ├─ core/
│  ├─ adapters/
│  ├─ schemas/
│  ├─ services/
│  └─ utils/
├─ web/
├─ configs/
│  ├─ app.yaml
│  ├─ models.yaml
│  ├─ qc_rules.yaml
│  └─ jobs/
├─ templates/
├─ projects/
├─ outputs/
├─ data/
├─ tests/
├─ .github/workflows/
├─ .env.example
├─ .gitignore
├─ pyproject.toml
└─ README.md
```

## 快速开始

### 1）安装

```bash
python -m pip install --upgrade pip
pip install -e .[dev]
```

### 2）配置

```bash
cp .env.example .env
```

并根据需要修改环境变量（默认可直接使用 mock）。

### 3）运行 CLI

```bash
python -m app.cli --help
python -m app.cli project list
```

### 4）运行 FastAPI

```bash
uvicorn app.api.main:app --reload --port 8000
```

访问：
- `GET /health`
- `GET /version`

## CLI 使用示例

### 项目管理

```bash
python -m app.cli project init demo2
python -m app.cli project list
```

### 模板管理

```bash
python -m app.cli template validate --template templates/drama/outline_prompt.md --vars '{"project_name":"逆光追凶","genre":"悬疑","target_audience":"18-35","core_conflict":"真相与亲情冲突"}'
python -m app.cli template render --template templates/drama/outline_prompt.md --vars '{"project_name":"逆光追凶","genre":"悬疑","target_audience":"18-35","core_conflict":"真相与亲情冲突"}'
```

### 生成任务

```bash
python -m app.cli run generate --config configs/jobs/generate_outline.yaml --dry-run
python -m app.cli run generate --config configs/jobs/generate_outline.yaml
```

### 质检任务

```bash
python -m app.cli qc run --config configs/jobs/qc_project.yaml
```

### 导出

```bash
python -m app.cli export results --run-dir outputs/run-YYYYmmdd-HHMMSS
```

## GitHub Actions 使用

### 1）CI（`.github/workflows/ci.yml`）

触发：`push` / `pull_request`

执行：安装依赖、测试、模板校验 smoke。

### 2）手动生成（`manual-generate.yml`）

触发：`workflow_dispatch`

输入：
- `job_config`
- `dry_run`
- `model_provider`

执行后上传 `outputs/` artifact。

### 3）定时质检（`scheduled-qc.yml`）

触发：
- 定时（每日 UTC 02:00）
- 手动触发

执行后上传 `outputs/` artifact。

### 4）导出（`export-release.yml`）

手动传入 `run_dir` 后执行导出并上传 artifact。

## GitHub Secrets（可选）

当前 MVP 默认 mock，无需真实密钥。
如接入真实模型，建议配置：

- `OPENAI_API_KEY`
- `MODEL_PROVIDER`

并通过环境变量注入，不要写入仓库。

## 输出目录与 artifact 说明

每次运行创建：

- `outputs/run-YYYYmmdd-HHMMSS/`
  - `logs/`：运行日志
  - `exports/`：导出文件
  - `summary.json` / `qc_report.json` / `qc_report.md`

Actions 中会上传 `outputs/` 作为 artifact。

## 常见问题（FAQ）

1. **Actions 无法访问本地 Ollama？**
   - GitHub Hosted Runner 不能访问你本地网络服务；请改为云端模型 API，或使用自托管 Runner。

2. **模板校验失败提示缺失变量？**
   - 检查 `--vars` JSON 是否包含模板中的全部 `{{变量}}`。

3. **输出目录未生成？**
   - 确认命令执行成功，并检查是否传入了正确的配置路径。

## 路线图

### V1（当前）

- CLI 可用
- Mock 全流程可跑通
- 基础规则质检
- GitHub Actions 4 条工作流

### V1.1（下一步）

- 真实模型适配器（OpenAI/Ollama 等）
- WebUI（任务配置与报告看板）
- 更丰富 QC（LLM 语义评分）
- 数据库存储与历史检索
