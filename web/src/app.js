const API_BASE = window.__WEBUI_CONFIG__?.API_BASE_URL || 'http://localhost:8000';
const USE_MOCK = Boolean(window.__WEBUI_CONFIG__?.USE_MOCK);
document.querySelector('#mode-tag').textContent = `Mode: ${USE_MOCK ? 'Mock (Pages)' : 'Local API'}`;

const mock = {
  projects: [{ name: 'demo_project', meta: { name: 'demo_project', description: '演示项目' }, files: ['meta.json', 'sample_script.md'] }],
  templates: [{ name: 'outline_prompt', path: 'templates/drama/outline_prompt.md', category: 'drama' }],
  jobs: [{ job_name: 'generate_outline_demo', provider: 'mock', dry_run: true, run_dir: 'outputs/mock-run', outputs: ['outputs/mock-run/result.md'] }],
  reports: [{ run_dir: 'outputs/mock-run', json_content: { score: 92, passed: true, hits: [] }, md_content: '# 质检报告\n- score: 92' }],
};

async function api(path, init) {
  const res = await fetch(`${API_BASE}${path}`, { headers: { 'Content-Type': 'application/json' }, ...init });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

async function loadProjects() { return USE_MOCK ? mock.projects : (await api('/api/projects')).items; }
async function loadTemplates() { return USE_MOCK ? mock.templates : (await api('/api/templates')).items; }
async function loadJobs() { return USE_MOCK ? mock.jobs : (await api('/api/jobs')).items; }
async function loadReports() { return USE_MOCK ? mock.reports : (await api('/api/reports/qc')).items; }
async function loadConfigs() { return USE_MOCK ? ['configs/jobs/generate_outline.yaml'] : (await api('/api/jobs/configs')).items; }

function card(title, html) { return `<section class='card'><h2>${title}</h2>${html}</section>`; }

async function dashboard() {
  const jobs = await loadJobs();
  return card('最近任务', jobs.map((x) => `<div>${x.job_name} | ${x.run_dir}</div>`).join('')) +
    card('快捷入口', '<a href="#/templates">模板渲染</a> | <a href="#/jobs">发起任务</a>');
}

async function projects() {
  const items = await loadProjects();
  return card('项目列表', items.map((x) => `<div><b>${x.name}</b><pre>${JSON.stringify(x.meta, null, 2)}</pre><div>${x.files.join(', ')}</div></div>`).join(''));
}

async function templates() {
  const items = await loadTemplates();
  const selected = items[0]?.path || '';
  return card('模板渲染', `
    <label>Template<select id='tpl'>${items.map((x) => `<option value='${x.path}'>${x.path}</option>`).join('')}</select></label>
    <label>project_name<input id='project_name' value='逆光追凶'/></label>
    <label>genre<input id='genre' value='悬疑'/></label>
    <label>target_audience<input id='target_audience' value='18-35'/></label>
    <label>core_conflict<input id='core_conflict' value='真相与亲情冲突'/></label>
    <button id='renderBtn'>渲染预览</button>
    <pre id='preview'>点击渲染</pre>
  `);
}

async function jobsPage() {
  const cfgs = await loadConfigs();
  return card('Run Job', `
    <select id='jobCfg'>${cfgs.map((x) => `<option>${x}</option>`).join('')}</select>
    <button id='runJobBtn'>执行任务</button>
    <pre id='jobResult'>等待执行</pre>
  `);
}

async function reports() {
  const items = await loadReports();
  return card('QC Reports', items.map((x) => `<div><b>${x.run_dir}</b><pre>${JSON.stringify(x.json_content || x.md_content, null, 2)}</pre></div>`).join(''));
}

const routes = { '/': dashboard, '/projects': projects, '/templates': templates, '/jobs': jobsPage, '/reports': reports };

async function renderRoute() {
  const hash = location.hash.replace('#', '') || '/';
  const view = routes[hash] || routes['/'];
  document.getElementById('app').innerHTML = await view();
  bindEvents();
}

function bindEvents() {
  const renderBtn = document.getElementById('renderBtn');
  if (renderBtn) {
    renderBtn.onclick = async () => {
      const payload = {
        template: document.getElementById('tpl').value,
        variables: {
          project_name: document.getElementById('project_name').value,
          genre: document.getElementById('genre').value,
          target_audience: document.getElementById('target_audience').value,
          core_conflict: document.getElementById('core_conflict').value,
        },
      };
      const out = USE_MOCK ? `Mock Render\n${JSON.stringify(payload, null, 2)}` : (await api('/api/templates/render', { method: 'POST', body: JSON.stringify(payload) })).rendered;
      document.getElementById('preview').textContent = out;
    };
  }

  const runBtn = document.getElementById('runJobBtn');
  if (runBtn) {
    runBtn.onclick = async () => {
      const job_config = document.getElementById('jobCfg').value;
      const result = USE_MOCK ? mock.jobs[0] : await api('/api/jobs/run', { method: 'POST', body: JSON.stringify({ job_config, dry_run: true }) });
      document.getElementById('jobResult').textContent = JSON.stringify(result, null, 2);
    };
  }
}

window.addEventListener('hashchange', renderRoute);
renderRoute();
