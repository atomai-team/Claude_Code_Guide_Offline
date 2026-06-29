/* ════════════════════════════════════════════════════════════════════
   分级导航：header 高度测量 + scroll-spy + 移动抽屉
   ════════════════════════════════════════════════════════════════════ */
(function() {
  // 1. 实测 header 高度 → 注入 --header-h（避免硬编码，随主题/换行自适应）
  const header = document.querySelector('.header-strip');
  const setHeaderH = () => { if (header) document.documentElement.style.setProperty('--header-h', header.offsetHeight + 'px'); };
  setHeaderH();
  window.addEventListener('resize', setHeaderH, { passive: true });

  // 2. scroll-spy：位置法高亮"当前阅读"section（参考线 + 底部兜底，比纯 IO 稳）
  const links = [...document.querySelectorAll('.side-nav .nav-link')];
  const map = new Map();   // section 元素 → nav-link（保持 DOM 顺序）
  links.forEach(a => { const id = a.getAttribute('href').slice(1); const el = document.getElementById(id); if (el) map.set(el, a); });
  // 关键：按"物理位置"排序（导航分组顺序 ≠ 页面 DOM 顺序，如数据后台在导航里排末尾但物理在中部）
  const sections = [...map.keys()].sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);
  const setActive = (el) => {
    links.forEach(l => { l.classList.remove('active'); l.removeAttribute('aria-current'); });
    const a = map.get(el);
    if (a) { a.classList.add('active'); a.setAttribute('aria-current', 'location'); }
    const idx = sections.indexOf(el), total = sections.length;
    const fill = document.getElementById('navProgressFill');
    const count = document.getElementById('navProgressCount');
    if (fill && count && total > 0) {
      fill.style.width = Math.round((idx + 1) / total * 100) + '%';
      count.textContent = (idx + 1) + ' / ' + total;
    }
  };
  let ticking = false;
  const onSpy = () => {
    ticking = false;
    const ref = (header ? header.offsetHeight : 56) + 24;  // header 下方一点的参考线
    let current = sections[0];
    for (const sec of sections) { if (sec.getBoundingClientRect().top <= ref) current = sec; } // 取最后一个越过参考线的 section
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) current = sections[sections.length - 1]; // 底部兜底
    setActive(current);
  };
  window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onSpy); } }, { passive: true });
  onSpy();

  // 3. 移动端抽屉：汉堡开关 + 背景遮罩 + Esc/点链接关闭
  const nav = document.getElementById('sideNav');
  const toggle = document.getElementById('navToggle');
  const backdrop = document.getElementById('navBackdrop');
  if (nav && toggle && backdrop) {
    const openNav = () => { nav.classList.add('open'); backdrop.classList.add('show'); toggle.setAttribute('aria-expanded', 'true'); };
    const closeNav = () => { nav.classList.remove('open'); backdrop.classList.remove('show'); toggle.setAttribute('aria-expanded', 'false'); };
    toggle.addEventListener('click', () => nav.classList.contains('open') ? closeNav() : openNav());
    backdrop.addEventListener('click', closeNav);
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeNav(); });
    links.forEach(a => a.addEventListener('click', () => { if (window.matchMedia('(max-width: 1023px)').matches) closeNav(); }));
  }
})();

/* ════════════════════════════════════════════════════════════════════
   右侧悬浮按钮：滚动渐显 + 回顶/回底
   ════════════════════════════════════════════════════════════════════ */
(function() {
  const stack = document.getElementById('fabStack');
  if (!stack) return;
  const onScroll = () => {
    const show = window.scrollY > 400;
    stack.classList.toggle('show', show);
    stack.setAttribute('aria-hidden', show ? 'false' : 'true');
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();

/* ════════════════════════════════════════════════════════════════════
   主题：localStorage + data-theme
   ════════════════════════════════════════════════════════════════════ */
(function() {
  const saved = localStorage.getItem('mycc_theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
  const btn = document.getElementById('themeToggle');
  function update() {
    const cur = document.documentElement.getAttribute('data-theme') || 'light';
    btn.textContent = cur === 'dark' ? '☀️' : '🌙';
    btn.setAttribute('aria-label', cur === 'dark' ? '切换到亮色主题' : '切换到暗色主题');
  }
  window.__toggleTheme = function() {
    const cur = document.documentElement.getAttribute('data-theme') || 'light';
    const next = cur === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('mycc_theme', next);
    update();
  };
  btn?.addEventListener('click', window.__toggleTheme);
  update();
})();

/* ════════════════════════════════════════════════════════════════════
   Fetch mycc-stats.json (SSoT) · 失败降级内联
   ════════════════════════════════════════════════════════════════════ */

let STATS = { counts: FALLBACK_COUNTS, lists: {}, version: FALLBACK_VERSION, generated_at: new Date().toISOString() };
let DETAILS = null;
let BOARD = null;
let KANBAN_VIEW = (function() { try { return localStorage.getItem('kanbanView') || 'card'; } catch(e) { return 'card'; } })();

async function loadStats() {
  try {
    const r = await fetch('mycc-stats.json', { cache: 'no-store' });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    STATS = await r.json();
    console.log('[stats] mycc-stats.json loaded', STATS.counts);
  } catch (e) {
    console.warn('[stats] fetch failed, fallback:', e.message);
  }
  renderStats();
}

function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }

function renderStats() {
  const c = STATS.counts || FALLBACK_COUNTS;
  const v = STATS.version || FALLBACK_VERSION;
  const l = STATS.lists || {};
  const h = STATS.hooks || {};

  // Hero stats
  const hs = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
  hs('hs-skills', c.skills || '?');
  hs('hs-agents', c.agents_total || '?');
  hs('hs-hooks', c.hooks_registered || '?');
  hs('hs-mcp', c.mcp_servers || '?');
  hs('hs-routes', c.intent_words_routes || '?');
  hs('hs-plugins', c.enabled_plugins || '?');

  // Header meta
  const genAt = STATS.generated_at || new Date().toISOString();
  const dateStr = new Date(genAt).toLocaleString('zh-CN');
  const metaEl = document.getElementById('headerMeta');
  if (metaEl) metaEl.textContent = `CLI ${v.claude_code || '?'} · OMC ${v.omc || '?'} · CC Switch ${v.cc_switch || '?'} · ${dateStr}`;
  const genTimeEl = document.getElementById('genTime');
  if (genTimeEl) genTimeEl.textContent = dateStr;
  if (genTimeEl) genTimeEl.setAttribute('datetime', genAt);

  // Hero eyebrow
  const eb = document.getElementById('heroEyebrow');
  if (eb) eb.textContent = `📘 MYCC ${v.stats_engine || 'V53'} · Claude Code ${v.claude_code || '?'} · ${dateStr.split(' ')[0]}`;

  // Metric grid (动态)
  const mg = document.getElementById('metricGrid');
  if (mg) {
    const items = [
      ['本地 Skills', c.skills, '核心能力', 'accent'],
      ['Agents', c.agents_total, `${c.agents_core||0} 核心 + ${c.agents_ceo_roles||0} CEO + ${c.agents_industry||0} 行业 + ${c.agents_teams||0} 团队`, 'orange'],
      ['Hooks', c.hooks_registered, `已注册 / ${c.hook_events||'?'} 事件`, 'blue'],
      ['Workflows', c.workflows, '编排器', 'purple'],
      ['MCPs', c.mcp_servers, '模型上下文协议', 'green'],
      ['路由', c.intent_words_routes, '意图词表', 'red'],
      ['插件 Skills', c.plugin_skills, '市场', 'accent'],
      ['插件 Agents', c.plugin_agents, '市场', 'orange'],
    ];
    mg.innerHTML = items.map(([label, val, trend, color]) =>
      `<div class="card metric-card"><div class="metric"><span class="metric-value" style="color:var(--${color})">${esc(val)}</span><span class="metric-label">${esc(label)}</span></div><div class="metric-trend">${esc(trend)}</div></div>`
    ).join('');
  }

  // Entry table
  const tblEntry = document.getElementById('tblEntry');
  if (tblEntry) {
    const rows = l.priority_routes || l.orchestration?.entry_points || [
      {say:'队长 / leader / boss / 老大', engine:'smart-flow-all', priority: 95},
      {say:'活力全开 / 火力全开 / yolo_l4', engine:'yolo-all', priority: 95},
      {say:'ceo 决策 / 战略分析 / 顾问委员会', engine:'ceo_decision_council', priority: 88},
      {say:'系统级升级 / 全栈升级 / comprehensive upgrade', engine:'comprehensive_upgrade_workflow', priority: 86},
      {say:'smart / flow / 自动化 / 智能', engine:'smart_captain', priority: 85},
      {say:'调研 / 对比 / 选型 / 横评', engine:'team-research', priority: 80},
      {say:'代码 review / 审查 / CR', engine:'code-reviewer', priority: 75},
      {say:'安全审查 / 找漏洞 / 渗透 / OWASP', engine:'team-security', priority: 72},
      {say:'做个网站 / 全栈开发 / 上线一个功能', engine:'team-fullstack', priority: 70},
      {say:'深度调研 / 多源 / 异构 / 报告', engine:'deep-research', priority: 68},
    ];
    tblEntry.querySelector('tbody').innerHTML = rows.slice(0, 12).map(e =>
      `<tr><td style="padding-left:var(--sp-4)"><span class="kw">${esc(e.say || e.keywords?.join(' / ') || e.name || '')}</span></td><td>${esc(e.engine || e.target || '—')}</td><td><span class="badge badge-accent">P${esc(e.priority ?? '?')}</span></td></tr>`
    ).join('');
  }

  // Workflow list
  const wfList = document.getElementById('wfList');
  if (wfList) {
    const wfArr = l.workflows || ['autopilot','ultrawork','ralph','team','ralplan','start-work','comprehensive-upgrade','dev-pipeline','n-step-pipeline','harness-audit','ceo-pipeline','mycc-audit-pipeline','fundraising','self-evolve-loop'];
    const wfMap = l.workflow_map || {};
    wfList.innerHTML = wfArr.slice(0, 14).map(w =>
      `<div class="card wf-item"><span class="wf-name">/${esc(w)}</span><span class="wf-desc">${esc(wfMap[w] || '—')}</span></div>`
    ).join('');
  }

  // CLI 表格
  const tblCLI = document.getElementById('tblCLI');
  if (tblCLI) {
    const cliRows = [
      {n:'kimi', d:'Moonshot/MiniMax-M3 · 256K context · 长文档 + agentic 多文件读取'},
      {n:'mmx', d:'MiniMax · 中文内容/创作优化'},
      {n:'opencode', d:'Kimi K2.7 Code · 代码专长/写代码外包'},
      {n:'qwen', d:'通义千问 · 阿里系生态/中文异构视角'},
      {n:'mavis', d:'OpenCode+MiniMax · 多 agent 编排/独立对抗审查'},
      {n:'codex', d:'OpenAI Codex · 仅手动交互 TUI'},
    ];
    tblCLI.querySelector('tbody').innerHTML = cliRows.map(x =>
      `<tr><td style="padding-left:var(--sp-4)"><code style="color:var(--accent);font-family:var(--font-mono)">${esc(x.n)}</code></td><td>${esc(x.d)}</td></tr>`
    ).join('');
  }

  // Hook bars
  const hookBars = document.getElementById('hookBars');
  if (hookBars) {
    const byEvent = h.by_event || {};
    const HOOK_CN = {
      PreToolUse:'工具调用前', PostToolUse:'工具调用后', UserPromptSubmit:'用户消息提交',
      SessionStart:'会话开始', SessionEnd:'会话结束', Stop:'通用停止', SubagentStop:'子代理停止',
      Notification:'系统通知', PreCompact:'上下文压缩前', PermissionRequest:'权限请求',
      PermissionDenied:'权限被拒', SessionStart:'会话开始'
    };
    const entries = Object.entries(byEvent).sort((a,b) => b[1]-a[1]);
    const max = Math.max(1, ...entries.map(e => e[1]));
    hookBars.innerHTML = entries.slice(0, 12).map(([ev, n]) => {
      const cn = HOOK_CN[ev] || ev;
      const pct = ((n/max)*100).toFixed(0);
      return `<div class="hook-row">
        <span class="hook-label">${esc(cn)} <small>${esc(ev)}</small></span>
        <div class="hook-bar-track"><div class="hook-bar-fill" style="width:${pct}%"></div></div>
        <span class="hook-bar-num">${n}</span>
      </div>`;
    }).join('') || '<p class="muted" style="font-size:var(--fs-sm)">暂无 hook 数据</p>';
  }

  // Agent tags
  const AGENT_DESC = {
    'captain':'队长 — 极限档全权统筹调度',
    'evolution-scout':'进化侦察兵 — 扫官方新版/GitHub/社区',
    'needs-analyst':'需求分析师 — 把模糊口语转精确任务蓝图',
    'product-manager':'产品经理 — JTBD + BDD + RICE',
    'architect':'架构师 — C4 + ADR + 技术选型',
    'ceo-orchestrator':'CEO 总编排 — 战略拆解/团队调度/质量验收',
    'cfo-advisor':'CFO — runway/现金流/融资/估值',
    'cmo-advisor':'CMO — GTM/品牌/增长',
    'coo-advisor':'COO — 执行落地/SOP/OKR',
    'cto-advisor':'CTO — 工程化战略/技术债务',
    'ciso-advisor':'CISO — 安全 ALE/合规/零信任',
    'caio-advisor':'CAIO — AI Build-vs-Buy/EU AI Act',
    'cro-advisor':'CRO — 收入模型/销售预测/NRR',
    'chief-of-staff':'参谋长 — 跨部门决策路由',
    'designer':'设计师 — UX/线框→高保真',
    'engineer':'工程师 — TDD 三阶段/变更闭环',
    'qa-validator':'QA 验证 — 独立验证/BDD 逐条核实',
    'code-reviewer':'代码审查 — 安全/性能/规范',
    'test-engineer':'测试工程师 — BDD→Gherkin/测试金字塔',
    'security-analyst':'安全分析师 — OWASP/威胁建模',
    'devops-engineer':'DevOps — CI/CD/容器/部署',
    'researcher':'调研员 — ≥5 渠道深度调研',
    'explore':'代码库搜索专家',
    'executor':'专注任务执行与代码实现',
    'general-purpose':'通用 agent — 复杂多步任务',
    'capital-ir':'投融资 — BP/财务建模/估值',
    'chain-expansion':'连锁扩张 — 加盟/直营/选址',
    'consumer-trend':'新消费 — 品类机会/爆品方法论',
    'overseas-entry':'海外准入 — 市场/法务/本地化',
    'supply-chain':'供应链 — 采购/仓配/成本',
    'unit-economics':'单店模型 — 收入成本/盈亏平衡',
    'market-analyst':'市场分析师 — TAM/SAM/SOM/竞品',
    'team-data-ai':'数据/AI 团队',
    'team-fullstack':'全栈团队 — 一条龙',
    'team-infra':'基础设施团队',
    'team-research':'调研团队',
    'team-security':'安全团队',
    'team-testing':'测试团队',
    'team-perf':'性能团队',
    'team-docs':'文档团队',
    'team-evolution':'进化团队',
    'team-deploy':'部署团队',
  };
  function aTag(prefix, a, cls) {
    const d = AGENT_DESC[a];
    const desc = d ? ` — ${d.split(' — ').slice(1).join(' — ') || d}` : '';
    return `<span class="tag ${cls||''}" title="${esc(d || a)}">${prefix}<b>${esc(a)}</b>${desc ? `<span style="opacity:.6;font-weight:400">${esc(desc)}</span>` : ''}</span>`;
  }
  const core = l.core_agents || ['captain','evolution-scout','needs-analyst','product-manager','architect'];
  const ceo = l.ceo_roles || ['ceo-orchestrator','cfo-advisor','cmo-advisor','coo-advisor','ciso-advisor','caio-advisor','cro-advisor','chief-of-staff','cto-advisor','general-counsel-advisor','pricing-strategist','partnerships-architect'];
  const industry = l.industry_agents || ['capital-ir','chain-expansion','consumer-trend','overseas-entry','supply-chain','unit-economics','market-analyst'];
  const teams = l.teams || ['team-data-ai','team-fullstack','team-infra','team-research','team-security','team-testing'];
  const top = document.getElementById('agentTagsTop');
  if (top) top.innerHTML = core.map(a => aTag('⭐ ', a, 'agent')).join('');
  const teamsEl = document.getElementById('agentTagsTeams');
  if (teamsEl) teamsEl.innerHTML = ceo.map(a => aTag('👔 ', a, 'agent')).join('');
  const indEl = document.getElementById('industryAgents');
  if (indEl) indEl.innerHTML = industry.map(a => aTag('🏭 ', a, 'agent')).join('');
  const teamEl = document.getElementById('teamAgents');
  if (teamEl) teamEl.innerHTML = teams.map(a => aTag('👥 ', a, 'agent')).join('');

  // 全能力检索
  (function() {
    const sd = l.skill_desc || {};
    const routes = l.all_routes || l.priority_routes || [];
    const skills = [...new Set(Object.values(l.skill_categories || {}).flat())];
    const idx = [
      ...skills.map(s => ({t:'skill', n:s, d:sd[s]||'', e:'说 /'+s+' 或描述需求自动触发'})),
      ...routes.map(r => ({t:'route', n:r.name, d:'引擎: '+(r.target||'—')+' · P'+(r.priority||0), e:'说: '+((r.keywords||[]).slice(0,4).join(' / ')||r.name)})),
      ...Object.keys(AGENT_DESC).map(a => ({t:'agent', n:a, d:AGENT_DESC[a]||'', e:'说"用 '+a+' 做X" 或 队长自动派'})),
    ];
    const col = {skill:'var(--accent)', route:'var(--green)', agent:'var(--orange)'};
    const capCount = document.getElementById('capCount');
    if (capCount) capCount.textContent = `${idx.length} 项`;

    function highlight(text, q) {
      if (!q || !text) return esc(text || '');
      const lower = text.toLowerCase();
      const ql = q.toLowerCase();
      let out = '', i = 0, idx2 = lower.indexOf(ql);
      while (idx2 !== -1) {
        out += esc(text.slice(i, idx2)) + '<mark style="background:var(--accent-soft);color:var(--accent);padding:0 2px;border-radius:2px">' + esc(text.slice(idx2, idx2 + q.length)) + '</mark>';
        i = idx2 + q.length;
        idx2 = lower.indexOf(ql, i);
      }
      out += esc(text.slice(i));
      return out;
    }
    function render(q) {
      q = (q||'').trim().toLowerCase();
      const hit = q ? idx.filter(x => (x.n+x.d+x.e).toLowerCase().includes(q)) : idx;
      const box = document.getElementById('capResults');
      if (!box) return;
      box.innerHTML = `<div style="color:var(--text-muted);font-size:var(--fs-xs);padding:var(--sp-1) 0">${q?`匹配 "${esc(q)}" → ${hit.length} / ${idx.length}`:`共 ${idx.length} 项 · 输入关键词过滤`}</div>` +
        hit.slice(0, 200).map(x => `<div class="cap-item">
          <span class="cap-item-type tag" style="color:${col[x.t]||'var(--text)'};background:var(--bg-subtle)">${x.t}</span>
          <span class="cap-item-name">${highlight(x.n, q)}</span>
          <div class="cap-item-meta">${highlight(x.d, q)}</div>
          <div class="cap-item-trigger">▶ ${highlight(x.e, q)}</div>
        </div>`).join('') +
        (hit.length > 200 ? '<div style="color:var(--text-muted);font-size:var(--fs-xs);padding:var(--sp-2)">…仅显示前 200</div>' : '');
    }
    const inp = document.getElementById('capSearch');
    if (inp) { inp.addEventListener('input', e => render(e.target.value)); render(''); }
  })();

  // expert types
  const et = document.getElementById('expertTypes');
  if (et) et.textContent = `${c.agents_total||'?'} agent / ${c.hooks_registered||'?'} hook / ${c.skills||'?'} skill`;

  // skills link
  const skl = document.getElementById('skillsDetailLink');
  if (skl) skl.textContent = `查看全部 ${c.skills||'?'} →`;

  // stale
  if (STATS.generated_at) {
    const ageMs = Date.now() - new Date(STATS.generated_at).getTime();
    const ageDays = ageMs / (1000*60*60*24);
    const warn = document.getElementById('staleWarn');
    if (warn && ageDays > 1) {
      const label = ageDays > 7 ? `数据已 ${Math.floor(ageDays)} 天前生成，强烈建议刷新` : `数据已 ${(Math.round(ageDays*10)/10)} 天前生成，建议刷新`;
      warn.textContent = `⚠️ ${label}`;
      warn.classList.add('show');
    }
  }
}

/* ════════════════════════════════════════════════════════════════════
   Auto refresh 5 min + countdown
   ════════════════════════════════════════════════════════════════════ */
const REFRESH_SECS = 5 * 60;
let refreshTimer = null;
function startAutoRefresh() {
  const el = document.getElementById('autoRefreshCountdown');
  if (!el) return;
  if (refreshTimer) clearInterval(refreshTimer);
  let remain = REFRESH_SECS;
  function tick() {
    const m = Math.floor(remain/60), s = remain%60;
    el.textContent = `⏱ ${m}:${s.toString().padStart(2,'0')} 后自动刷新`;
    if (remain <= 0) { location.reload(); return; }
    remain--;
  }
  tick();
  refreshTimer = setInterval(tick, 1000);
}
function refreshData() {
  const cmd = 'python3 ~/.claude/lib/mycc-stats.py';
  if (navigator.clipboard?.writeText) {
    navigator.clipboard.writeText(cmd).then(() => showToast('✅ 命令已复制！粘贴到终端运行后 ⌘R 刷新本页')).catch(() => showToast('📋 终端运行: ' + cmd));
  } else {
    showToast('📋 终端运行: ' + cmd);
  }
}
function showToast(msg) {
  const t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.remove('show'), 4000);
}

/* ════════════════════════════════════════════════════════════════════
   全量目录 + 详情 Modal (fetch dashboard-details.json)
   ════════════════════════════════════════════════════════════════════ */
async function loadDetails() {
  try {
    const r = await fetch('dashboard-details.json', { cache: 'no-cache' });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    DETAILS = await r.json();
    console.log('[details] loaded', DETAILS.counts);
  } catch (e) {
    console.warn('[details] fetch failed:', e.message);
    const status = document.getElementById('catalogStatus');
    if (status) status.textContent = '❌ 数据加载失败 (需 http.server)';
    return;
  }
  initModal();
  initCatalog();
}

function initModal() {
  if (!DETAILS) return;
  const idx = { skills: {}, hooks: {}, agents: {} };
  DETAILS.skills.forEach(s => { idx.skills[s.id] = s; });
  DETAILS.hooks.forEach(h => { idx.hooks[h.id] = h; });
  DETAILS.agents.forEach(a => { idx.agents[a.id] = a; });

  function row(label, val, mono) {
    if (!val) return '';
    return `<div class="row"><div class="row-label">${label}</div><div class="row-val ${mono?'mono':''}">${esc(val)}</div></div>`;
  }

  window.openDetail = function(type, id) {
    const item = idx[type]?.[id];
    if (!item) { showToast('⚠️ 未找到详情: ' + type + '/' + id); return; }
    const overlay = document.getElementById('detailOverlay');
    if (!overlay) return;
    // P2-1 a11y: 焦点陷阱 — Modal 开时主内容(<main>)加 inert, 背景不可 Tab,
    // Modal 自身在 <body> 内但不在 <main> 内, 仍可访问.
    const mainEl = document.getElementById('main') || document.querySelector('main');
    if (mainEl) mainEl.setAttribute('inert', '');
    document.getElementById('detailTitle').textContent = item.name_en || item.name_zh || item.id || id;
    let html = '';
    if (type === 'skills') {
      html += row('📦 名称', item.name_en, true);
      html += row('📝 描述', item.description);
      if (item.trigger_words?.length) html += row('🗣️ 触发词', item.trigger_words.join('、'));
      if (item.what_for) html += row('💡 何时用', item.what_for);
      if (item.example) html += row('📖 示例', item.example, true);
      if (item.body_short) html += row('📄 概要', item.body_short, true);
    } else if (type === 'hooks') {
      html += row('📦 文件名', item.id, true);
      html += row('🛡️ 类型', item.hook_type);
      html += row('⚡ 事件', (item.events || []).join(' / '));
      html += row('✓ 已注册', item.registered ? '是' : '否');
      html += row('🎯 守护什么', item.what_protects);
      if (item.kill_switch) html += row('🚪 Kill Switch', item.kill_switch, true);
      html += row('📏 行数', item.size_lines);
    } else if (type === 'agents') {
      html += row('📦 名称', item.id, true);
      html += row('🗂️ 分类', item.category);
      html += row('🤖 模型', item.model);
      if (item.level) html += row('📊 Level', item.level);
      html += row('📝 描述', item.description);
      if (item.trigger_words?.length) html += row('🗣️ 触发词', item.trigger_words.join('、'));
      if (item.body_short) html += row('📄 概要', item.body_short, true);
    }
    document.getElementById('detailBody').innerHTML = html;
    const total = DETAILS.counts[type + '_total'] || DETAILS.counts[type.replace(/s$/,'') + '_total'] || '?';
    const typeLabel = type === 'skills' ? 'skill' : type === 'hooks' ? 'hook' : 'agent';
    document.getElementById('detailMeta').textContent = `${total} 个${typeLabel} · id=${id}`;
    overlay.style.display = 'flex';
  };

  window.closeDetail = function() {
    const o = document.getElementById('detailOverlay');
    if (o) o.style.display = 'none';
    // P2-1 a11y: 焦点陷阱解除
    const mainEl = document.getElementById('main') || document.querySelector('main');
    if (mainEl) mainEl.removeAttribute('inert');
  };
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      const task = document.getElementById('taskOverlay');
      if (task && task.style.display === 'flex') { closeTaskDetail(); return; }
      closeDetail();
    }
  });
}

function initCatalog() {
  if (!DETAILS) return;
  const status = document.getElementById('catalogStatus');
  const chips = document.getElementById('catalogChips');
  const search = document.getElementById('catalogSearch');
  const tabs = document.querySelectorAll('#s-catalog .catalog-tab');

  const all = [
    ...DETAILS.skills.map(s => ({type:'skills', id:s.id, label:s.name_en || s.id, desc:s.description || ''})),
    ...DETAILS.hooks.map(h => ({type:'hooks', id:h.id, label:h.id, desc:h.what_protects || h.name_zh || ''})),
    ...DETAILS.agents.map(a => ({type:'agents', id:a.id, label:a.id, desc:a.description || ''})),
  ];
  if (status) status.textContent = `✓ ${all.length} 条 · 点击 chip 查详情`;

  let curTab = 'all', curQuery = '';
  function render() {
    const filtered = all.filter(item => {
      if (curTab !== 'all' && item.type !== curTab) return false;
      if (curQuery) return (item.id + ' ' + item.label + ' ' + item.desc).toLowerCase().includes(curQuery.toLowerCase());
      return true;
    });
    const typeIcon = {skills:'🛠', hooks:'🪝', agents:'🤖'};
    if (chips) chips.innerHTML = filtered.slice(0, 500).map(item =>
      `<span class="catalog-chip" data-type="${item.type}" data-id="${esc(item.id)}" title="${esc(item.desc.slice(0,200))}"><span class="chip-type">${typeIcon[item.type]}</span>${esc(item.label)}</span>`
    ).join('');
    if (chips) chips.querySelectorAll('.catalog-chip').forEach(el => {
      el.addEventListener('click', () => openDetail(el.dataset.type, el.dataset.id));
    });
    if (status) status.textContent = `✓ ${filtered.length} / ${all.length} 条`;
  }
  tabs.forEach(btn => btn.addEventListener('click', () => {
    tabs.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    curTab = btn.dataset.tab;
    render();
  }));
  if (search) search.addEventListener('input', () => { curQuery = search.value.trim(); render(); });
  render();
}

/* ════════════════════════════════════════════════════════════════════
   CmdK 全局搜索 (懒加载 MiniSearch)
   ════════════════════════════════════════════════════════════════════ */
const GS_DOCS = [
  '00-速查表.html','01-小白使用手册.html','02-商城项目实战手册.html',
  '03-全能力清单-Skills+MCP+插件.html','04-CMMI配置文档-PM专业版.html',
  '05-创业分析专家系统.html','06-CEO能力速用手册.html',
  'dashboard.html','mycc-stats.html','MYCC-能力全景总册.html',
  'external-intel-prompt-v7.html','external-investigator-prompt.html',
  'requirements-summary-for-external-ai.html'
];
let gsReady = false, gsMinisearch = null, gsDocs = [];

function gsStripHtml(html) {
  const d = document.createElement('div'); d.innerHTML = html;
  return (d.textContent || '').replace(/\s+/g, ' ').trim();
}
function gsExcerpt(text, q, max = 180) {
  const i = text.toLowerCase().indexOf(q.toLowerCase());
  if (i < 0) return text.slice(0, max) + (text.length > max ? '...' : '');
  const start = Math.max(0, i-60), end = Math.min(text.length, i+max-60);
  let s = text.slice(start, end);
  if (start > 0) s = '...' + s; if (end < text.length) s += '...';
  return s.replace(new RegExp('(' + q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi'), '【$1】');
}
async function initGlobalSearch() {
  if (gsReady || !window.MiniSearch) return;
  if (!('IntersectionObserver' in window)) return;
  const card = document.getElementById('s-catalog');
  if (!card) return;
  const obs = new IntersectionObserver(async (es) => {
    if (!es.some(e => e.isIntersecting)) return;
    obs.disconnect();
    if (gsReady) return;
    try {
      gsMinisearch = new MiniSearch({ fields: ['title','body'], storeFields: ['title'], searchOptions: { boost: {title:2}, prefix: true, fuzzy: 0.2 } });
      const docs = [];
      for (const url of GS_DOCS) {
        try {
          const r = await fetch(url, { cache: 'no-store' });
          if (!r.ok) continue;
          const html = await r.text();
          const titleMatch = html.match(/<title>(.*?)<\/title>/);
          const title = titleMatch ? titleMatch[1] : url;
          const body = gsStripHtml(html);
          if (body.length < 30) continue;
          docs.push({ id: url, title, body: body.slice(0, 50000) });
        } catch(e) {}
      }
      gsDocs = docs;
      gsMinisearch.addAll(docs);
      gsReady = true;
      console.log('[cmdk] indexed', docs.length, 'docs');
    } catch (e) {
      console.warn('[cmdk] init failed:', e.message);
    }
  }, { rootMargin: '200px' });
  obs.observe(card);
}

let cmdkActiveIdx = 0, cmdkHits = [], cmdkCategory = 'all';
const CMDK_CATS = [['all','🌐 全部'],['doc','📚 文档'],['manual','📖 手册'],['config','⚙️ 配置']];

function openCmdK() {
  const o = document.getElementById('cmdkOverlay');
  if (!o) return;
  // P2-1 a11y: 焦点陷阱 — CmdK 开时 <main> 加 inert (Modal 自身在 body 内但不在 main, 仍可访问)
  const mainEl = document.getElementById('main') || document.querySelector('main');
  if (mainEl) mainEl.setAttribute('inert', '');
  o.style.display = 'flex';
  const i = document.getElementById('cmdkInput');
  if (i) { i.value = ''; setTimeout(() => i.focus(), 30); }
  renderCmdKTabs();
  runCmdK('');
}
function closeCmdK() {
  const o = document.getElementById('cmdkOverlay');
  if (o) o.style.display = 'none';
  // P2-1 a11y: 焦点陷阱解除
  const mainEl = document.getElementById('main') || document.querySelector('main');
  if (mainEl) mainEl.removeAttribute('inert');
}
function renderCmdKTabs() {
  const t = document.getElementById('cmdkTabs');
  if (!t) return;
  t.innerHTML = CMDK_CATS.map(([k,n]) => `<button class="cmdk-tab${k===cmdkCategory?' active':''}" data-cat="${k}">${n}</button>`).join('');
  t.querySelectorAll('.cmdk-tab').forEach(b => b.addEventListener('click', () => {
    cmdkCategory = b.dataset.cat;
    renderCmdKTabs();
    runCmdK(document.getElementById('cmdkInput').value);
  }));
}
function classifyDoc(id) {
  if (id.includes('小白')||id.includes('商城')||id.includes('CEO')||id.includes('CMMI')||id.includes('能力')) return 'manual';
  if (id.includes('mycc-config')||id.includes('guardrail')||id.includes('capability')) return 'config';
  return 'doc';
}
function runCmdK(q) {
  if (!gsReady) {
    document.getElementById('cmdkResults').innerHTML = '<div class="cmdk-hint">⏳ 索引懒加载中… 滚到下方触发；或 1-2s 后重试</div>';
    document.getElementById('cmdkCount').textContent = '0';
    return;
  }
  q = (q || '').trim();
  if (!q) {
    cmdkHits = gsDocs.slice(0, 8).map(d => ({id: d.id, title: d.title, snippet: d.body.slice(0,200).replace(/\s+/g,' ').trim()}));
    document.getElementById('cmdkResults').innerHTML = cmdkHits.map((h,i) => cmdkRowHTML(h, i)).join('');
    document.getElementById('cmdkCount').textContent = cmdkHits.length + ' (推荐)';
    cmdkActiveIdx = 0; cmdkUpdateActive();
    return;
  }
  let hits = gsMinisearch.search(q, { prefix: true, fuzzy: 0.2, combineWith: 'AND' }).slice(0, 40);
  if (cmdkCategory !== 'all') hits = hits.filter(h => classifyDoc(h.id) === cmdkCategory);
  cmdkHits = hits.slice(0, 20);
  if (!cmdkHits.length) {
    document.getElementById('cmdkResults').innerHTML = '<div class="cmdk-hint">无匹配 · 试试更短关键词</div>';
    document.getElementById('cmdkCount').textContent = '0';
    return;
  }
  document.getElementById('cmdkResults').innerHTML = cmdkHits.map((h,i) => {
    const d = gsDocs.find(x => x.id === h.id);
    return { id: h.id, title: h.title, snippet: gsExcerpt(d?.body || '', q), score: h.score };
  }).map((h,i) => cmdkRowHTML(h, i)).join('');
  document.getElementById('cmdkCount').textContent = cmdkHits.length;
  cmdkActiveIdx = 0; cmdkUpdateActive();
}
function cmdkRowHTML(h, i) {
  return `<a class="cmdk-result${i===cmdkActiveIdx?' active':''}" href="${esc(h.id)}" target="_blank" data-i="${i}">
    <div class="cmdk-result-title">📄 ${esc(h.title)}</div>
    <div class="cmdk-result-snippet">${esc((h.snippet || '').slice(0,220))}</div>
    <div class="cmdk-result-path">${esc(h.id)}</div>
  </a>`;
}
function cmdkUpdateActive() {
  const rs = document.querySelectorAll('#cmdkResults .cmdk-result');
  rs.forEach((r,i) => r.classList.toggle('active', i === cmdkActiveIdx));
  const cur = rs[cmdkActiveIdx]; if (cur) cur.scrollIntoView({ block: 'nearest' });
}
function cmdkOpen(idx) {
  const h = cmdkHits[idx]; if (h) window.open(h.id, '_blank');
}
document.addEventListener('keydown', e => {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') { e.preventDefault(); openCmdK(); return; }
  if (document.getElementById('cmdkOverlay')?.style.display === 'flex') {
    if (e.key === 'Escape') { e.preventDefault(); closeCmdK(); return; }
    if (e.key === 'ArrowDown') { e.preventDefault(); cmdkActiveIdx = Math.min(cmdkHits.length-1, cmdkActiveIdx+1); cmdkUpdateActive(); return; }
    if (e.key === 'ArrowUp') { e.preventDefault(); cmdkActiveIdx = Math.max(0, cmdkActiveIdx-1); cmdkUpdateActive(); return; }
    if (e.key === 'Enter') { e.preventDefault(); cmdkOpen(cmdkActiveIdx); closeCmdK(); return; }
  }
});
document.addEventListener('input', e => {
  if (e.target && e.target.id === 'cmdkInput') runCmdK(e.target.value);
});

// Lazy-load MiniSearch from CDN
(function() {
  if (window.MiniSearch) { initGlobalSearch(); return; }
  const s = document.createElement('script');
  s.src = 'https://cdn.jsdelivr.net/npm/minisearch@7.1.0/dist/umd/index.min.js';
  s.onload = initGlobalSearch;
  s.onerror = () => console.warn('[cmdk] MiniSearch CDN load failed');
  document.head.appendChild(s);
})();

/* ════════════════════════════════════════════════════════════════════
   Board Tasks · board-tasks.json 看板数据
   ════════════════════════════════════════════════════════════════════ */

async function loadBoardTasks() {
  try {
    const r = await fetch('board-tasks.json', { cache: 'no-store' });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    BOARD = await r.json();
    console.log('[board] board-tasks.json loaded');
  } catch (e) {
    console.warn('[board] fetch failed:', e.message);
  }
  renderBoardTasks();
}

window.reloadTasks = async function() {
  const btn = document.getElementById('btn-reload-tasks');
  if (btn) { btn.disabled = true; btn.textContent = '⟳ 加载中…'; }
  await loadBoardTasks();
  if (btn) { btn.disabled = false; btn.textContent = '⟳ 重载数据'; }
  showToast('✅ 看板数据已重载');
};

// ─── 状态色板 & 工具函数 ───
const STATUS_CLR = { done: '#10b981', partial: '#f59e0b', doing: 'var(--accent)', todo: '#9ca3af', blocked: '#ef4444' };

function groupBy(arr, key) {
  return arr.reduce((acc, x) => { (acc[x[key]] = acc[x[key]] || []).push(x); return acc; }, {});
}

function renderGroupedList(elId, countId, items) {
  const el = document.getElementById(elId);
  if (!el || !items || !items.length) return;
  const todo = items.filter(x => x.status === 'todo' || x.status === 'doing').length;
  const countEl = document.getElementById(countId);
  if (countEl) countEl.textContent = `${items.length} 条${todo ? ` · ⚡ ${todo} 待做` : ' · 全部完成'}`;
  const groups = groupBy(items, 'group');
  el.innerHTML = Object.entries(groups).map(([g, gItems]) => {
    const gt = gItems.filter(x => x.status === 'todo' || x.status === 'doing').length;
    return `<details style="margin-top:var(--sp-2)">
      <summary style="cursor:pointer;list-style:none;display:flex;gap:var(--sp-2);align-items:center;padding:var(--sp-2) 0;font-size:var(--fs-xs);font-weight:600">
        ${esc(g)} <span style="color:var(--text-dim);font-weight:400">(${gItems.length}${gt ? ` · ⚡${gt}` : ''})</span>
      </summary>
      <div style="padding-left:var(--sp-4);border-left:2px solid var(--border);margin-bottom:var(--sp-2)">
        ${gItems.map(c => `<div style="display:flex;align-items:flex-start;gap:var(--sp-2);padding:2px 0;font-size:var(--fs-xs)">
          <span class="bt-status" style="background:${STATUS_CLR[c.status] || '#9ca3af'};margin-top:4px"></span>
          <span${c.status === 'todo' ? ' style="font-weight:600"' : ''}>
            <span style="color:var(--text-dim)">${esc(c.id)}</span> ${esc(c.title)}${c.evidence ? ` <code class="bt-ev">${esc(c.evidence)}</code>` : ''}${c.blocker ? ` <span style="color:#ef4444"> ⚠${esc(c.blocker)}</span>` : ''}
          </span>
        </div>`).join('')}
      </div>
    </details>`;
  }).join('');
}

function renderBoardTasks() {
  if (!BOARD) return;
  const { kanban, milestones, blockers, notes, closure, requirements, subplans, memory_system } = BOARD;

  const set = (id, v) => { const el = document.getElementById(id); if (el) el.textContent = v; };
  const subDoing = (subplans || []).filter(s => s.status === 'doing').length;
  set('bt-doing',   (kanban?.['进行中'] || []).length + subDoing);
  set('bt-blocked', (blockers || []).length);
  set('bt-done',    (kanban?.['审核中'] || []).length);
  set('bt-evidence', closure?.with_evidence ?? '—');

  // 看板渲染（提取为独立函数，支持卡片/列表切换）
  const kanbanEl = document.getElementById('bt-kanban');
  if (kanbanEl) renderKanbanInto(kanbanEl, kanban, subplans);
  syncViewButtons();

  // 里程碑
  const milestonesEl = document.getElementById('bt-milestones');
  if (milestonesEl && milestones) {
    const icon = { done: '✅', doing: '🔄', todo: '⬜', blocked: '🚫' };
    milestonesEl.innerHTML = `<div style="display:flex;flex-direction:column;gap:var(--sp-2)">
      ${milestones.map(m => `<div style="display:flex;gap:var(--sp-3);align-items:flex-start;padding:var(--sp-2) var(--sp-3);border:1px solid var(--border);border-radius:var(--radius-sm);background:var(--surface)">
        <span style="flex-shrink:0">${icon[m.status] || '⬜'}</span>
        <div><span style="font-weight:600;font-size:var(--fs-sm)">${esc(m.id)} · ${esc(m.title)}</span>${m.evidence ? `<code class="bt-ev" style="margin-left:var(--sp-2)">${esc(m.evidence)}</code>` : ''}</div>
      </div>`).join('')}
    </div>`;
  }

  // 需求清单 & 子计划 (按 group 折叠)
  renderGroupedList('bt-requirements', 'bt-req-count', requirements);
  renderGroupedList('bt-subplans',     'bt-sub-count', subplans);

  // 记忆体系
  const memEl = document.getElementById('bt-memory');
  if (memEl && memory_system) {
    const countEl = document.getElementById('bt-mem-count');
    if (countEl) countEl.textContent = `${memory_system.total_files} 文件 · ${(memory_system.categories || []).length} 类`;
    memEl.innerHTML = `<div style="display:flex;flex-wrap:wrap;gap:var(--sp-2);padding-top:var(--sp-3)">
      ${(memory_system.categories || []).map(c => `<span style="font-size:var(--fs-xs);padding:2px var(--sp-3);border:1px solid var(--border);border-radius:var(--radius-pill);background:var(--surface)">${esc(c.name)} <strong>${c.count}</strong></span>`).join('')}
    </div>`;
  }

  // 卡点
  const blockersEl = document.getElementById('bt-blockers');
  if (blockersEl && blockers && blockers.length) {
    blockersEl.innerHTML = `<h4 style="font-weight:700;font-size:var(--fs-sm);margin-bottom:var(--sp-2)">卡点 (${blockers.length})</h4>
      <div style="display:flex;flex-direction:column;gap:var(--sp-2)">
      ${blockers.map(b => `<div style="display:flex;gap:var(--sp-2);padding:var(--sp-2) var(--sp-3);border-left:3px solid #ef4444;background:var(--surface);border-radius:0 var(--radius-sm) var(--radius-sm) 0">
        <span style="font-size:var(--fs-xs);font-weight:600;color:var(--text-dim);flex-shrink:0">${esc(b.id)}</span>
        <span style="font-size:var(--fs-xs)">${esc(b.title)}</span>
        ${b.ref ? `<code class="bt-ev" style="margin-left:auto;flex-shrink:0">${esc(b.ref)}</code>` : ''}
      </div>`).join('')}
    </div>`;
  }

  // 决策笔记
  const notesEl = document.getElementById('bt-notes');
  if (notesEl && notes && notes.length) {
    notesEl.innerHTML = `<h4 style="font-weight:700;font-size:var(--fs-sm);margin-bottom:var(--sp-2);margin-top:var(--sp-4)">最近决策笔记 (${notes.length})</h4>
      <div style="display:flex;flex-direction:column;gap:var(--sp-2)">
      ${notes.map(n => `<div style="font-size:var(--fs-xs);padding:var(--sp-2) var(--sp-3);border:1px solid var(--border);border-radius:var(--radius-sm);background:var(--surface)">
        <span style="color:var(--text-dim);margin-right:var(--sp-2)">${esc(n.date)}</span>${esc(n.note)}
      </div>`).join('')}
    </div>`;
  }

  // 闭环统计
  const closureEl = document.getElementById('bt-closure');
  if (closureEl && closure) {
    const pct = closure.total ? Math.round(closure.with_evidence / closure.total * 100) : 0;
    closureEl.innerHTML = `<h4 style="font-weight:700;font-size:var(--fs-sm);margin-bottom:var(--sp-2);margin-top:var(--sp-4)">闭环统计</h4>
      <div style="display:flex;gap:var(--sp-5);font-size:var(--fs-xs)">
        <span>有证据 <strong>${closure.with_evidence}</strong></span>
        <span>无证据 <strong>${closure.without_evidence}</strong></span>
        <span>总计 <strong>${closure.total}</strong></span>
        <span>闭环率 <strong>${pct}%</strong></span>
      </div>`;
  }
}

/* ════════════════════════════════════════════════════════════════════
   Kanban 渲染（卡片 / 列表双模式）
   ════════════════════════════════════════════════════════════════════ */

function kanbanCardHtml(c, dotClr) {
  const cardData = encodeURIComponent(JSON.stringify(c));
  const evHash   = c.evidence ? c.evidence.split(':').pop().slice(-7) : null;
  return `<div style="font-size:var(--fs-xs);padding:var(--sp-2);border:1px solid var(--border);border-radius:var(--radius-sm);margin-bottom:var(--sp-2);background:var(--surface);cursor:pointer;transition:border-color .15s;position:relative" onmouseenter="this.style.borderColor='var(--accent)'" onmouseleave="this.style.borderColor='var(--border)'" onclick="openTaskDetail(JSON.parse(decodeURIComponent('${cardData}')),'kanban')">
    ${c.closure_badge ? `<span style="position:absolute;top:4px;right:4px;font-size:9px;background:#10b981;color:#fff;border-radius:3px;padding:0 4px;font-weight:700">✓ done</span>` : ''}
    ${c.blocker ? `<span title="${esc(c.blocker)}" style="position:absolute;top:4px;right:${c.closure_badge ? '44' : '4'}px;width:14px;height:14px;border-radius:50%;background:#ef4444;color:#fff;font-size:9px;font-weight:700;display:inline-flex;align-items:center;justify-content:center;line-height:1">!</span>` : ''}
    <div style="font-weight:600;line-height:1.4;padding-right:${c.blocker || c.closure_badge ? '18px' : '0'}">${esc(c.id)} · ${esc(c.title)}</div>
    <div style="display:flex;align-items:center;gap:var(--sp-2);margin-top:4px">
      <span style="color:var(--text-dim)">${esc(c.group)}</span>
      ${evHash ? `<code class="bt-ev" style="margin-left:auto;flex-shrink:0">${evHash}</code>` : ''}
    </div>
  </div>`;
}

function kanbanListRow(c, dotClr) {
  const cardData = encodeURIComponent(JSON.stringify(c));
  const evHash   = c.evidence ? c.evidence.split(':').pop().slice(-7) : null;
  return `<div style="display:grid;grid-template-columns:60px 80px 1fr 80px 80px 24px;align-items:center;gap:4px;padding:5px var(--sp-2);border-radius:var(--radius-sm);cursor:pointer;font-size:var(--fs-xs);height:36px" onmouseenter="this.style.background='var(--bg-subtle)'" onmouseleave="this.style.background=''" onclick="openTaskDetail(JSON.parse(decodeURIComponent('${cardData}')),'kanban')">
    <span style="display:inline-flex;align-items:center;justify-content:center;gap:3px;background:${dotClr}22;border:1px solid ${dotClr};border-radius:3px;padding:0 4px;font-size:9px;color:${dotClr};font-weight:700;white-space:nowrap;overflow:hidden">${esc(c.status)}</span>
    <span style="font-weight:600;color:var(--text-muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${esc(c.id)}</span>
    <span style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${esc(c.title)}</span>
    <span style="color:var(--text-dim);font-size:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${esc(c.group)}</span>
    <span style="text-align:right">${evHash ? `<code class="bt-ev">${evHash}</code>` : ''}</span>
    <span style="text-align:center">${c.blocker ? `<span title="${esc(c.blocker)}" style="width:14px;height:14px;border-radius:50%;background:#ef4444;color:#fff;font-size:9px;font-weight:700;display:inline-flex;align-items:center;justify-content:center">!</span>` : ''}</span>
  </div>`;
}

function renderKanbanInto(kanbanEl, kanban, subplans) {
  if (!kanbanEl) return;
  const cols   = ['待规划', '待办', '进行中', '审核中'];
  const dotClr = { '待规划': '#6b7280', '待办': '#f59e0b', '进行中': 'var(--accent)', '审核中': '#10b981' };
  const subPending = (subplans || []).filter(s => s.status === 'todo' || s.status === 'doing');

  if (KANBAN_VIEW === 'list') {
    kanbanEl.style.gridTemplateColumns = '1fr';
    kanbanEl.innerHTML = [...cols, kanban ? null : null].filter(Boolean).map(col => {
      const cards = (kanban || {})[col] || [];
      if (!cards.length) return '';
      return `<div class="card" style="padding:var(--sp-3) var(--sp-4)">
        <div style="display:flex;align-items:center;gap:var(--sp-2);margin-bottom:var(--sp-2)">
          <span style="width:8px;height:8px;border-radius:50%;background:${dotClr[col]};flex-shrink:0"></span>
          <span style="font-weight:700;font-size:var(--fs-sm)">${esc(col)}</span>
          <span style="color:var(--text-dim);font-size:var(--fs-xs)">(${cards.length})</span>
        </div>
        ${cards.map(c => kanbanListRow(c, dotClr[col])).join('')}
      </div>`;
    }).join('');
    if (subPending.length) {
      kanbanEl.innerHTML += `<div class="card" style="padding:var(--sp-3) var(--sp-4);border-left:3px solid #8b5cf6">
        <div style="display:flex;align-items:center;gap:var(--sp-2);margin-bottom:var(--sp-2)">
          <span style="width:8px;height:8px;border-radius:50%;background:#8b5cf6;flex-shrink:0"></span>
          <span style="font-weight:700;font-size:var(--fs-sm)">待优化</span>
          <span style="color:var(--text-dim);font-size:var(--fs-xs)">(${subPending.length})</span>
          <span style="margin-left:auto;font-size:9px;color:#8b5cf6;font-weight:600">subplans</span>
        </div>
        ${subPending.map(c => kanbanListRow(c, '#8b5cf6')).join('')}
      </div>`;
    }
  } else {
    kanbanEl.style.gridTemplateColumns = 'repeat(auto-fill,minmax(200px,1fr))';
    kanbanEl.innerHTML = cols.map(col => {
      const cards   = (kanban || {})[col] || [];
      const visible = cards.slice(0, col === '审核中' ? 5 : 30);
      const rest    = cards.length - visible.length;
      return `<div class="card" style="min-height:80px">
        <div style="display:flex;align-items:center;gap:var(--sp-2);margin-bottom:var(--sp-3)">
          <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${dotClr[col]};flex-shrink:0"></span>
          <span style="font-weight:700;font-size:var(--fs-sm)">${esc(col)}</span>
          <span style="color:var(--text-dim);font-size:var(--fs-xs)">(${cards.length})</span>
        </div>
        ${cards.length === 0 ? `<p style="color:var(--text-dim);font-size:var(--fs-xs);text-align:center">— 暂无 —</p>` : ''}
        ${visible.map(c => kanbanCardHtml(c, dotClr[col])).join('')}
        ${rest > 0 ? `<p style="color:var(--text-dim);font-size:var(--fs-xs);text-align:center">… 还有 ${rest} 项</p>` : ''}
      </div>`;
    }).join('');
    if (subPending.length) {
      kanbanEl.innerHTML += `<div class="card" style="min-height:80px;border-left:3px solid #8b5cf6">
        <div style="display:flex;align-items:center;gap:var(--sp-2);margin-bottom:var(--sp-3)">
          <span style="width:8px;height:8px;border-radius:50%;background:#8b5cf6;flex-shrink:0"></span>
          <span style="font-weight:700;font-size:var(--fs-sm)">待优化</span>
          <span style="color:var(--text-dim);font-size:var(--fs-xs)">(${subPending.length})</span>
          <span style="margin-left:auto;font-size:9px;color:#8b5cf6;font-weight:600">subplans</span>
        </div>
        ${subPending.map(c => kanbanCardHtml(c, '#8b5cf6')).join('')}
      </div>`;
    }
  }
}

function syncViewButtons() {
  const btnCard = document.getElementById('btn-view-card');
  const btnList = document.getElementById('btn-view-list');
  if (!btnCard || !btnList) return;
  const isCard = KANBAN_VIEW !== 'list';
  btnCard.style.background = isCard ? 'var(--accent)' : 'var(--surface)';
  btnCard.style.color = isCard ? '#fff' : 'var(--text)';
  btnList.style.background = !isCard ? 'var(--accent)' : 'var(--surface)';
  btnList.style.color = !isCard ? '#fff' : 'var(--text)';
}

window.setKanbanView = function(v) {
  KANBAN_VIEW = v;
  try { localStorage.setItem('kanbanView', v); } catch(e) {}
  if (BOARD) {
    const el = document.getElementById('bt-kanban');
    if (el) renderKanbanInto(el, BOARD.kanban, BOARD.subplans);
  }
  syncViewButtons();
};

/* ════════════════════════════════════════════════════════════════════
   Task 详情 Modal
   ════════════════════════════════════════════════════════════════════ */

// 不可折叠区块
function tdSection(title, content) {
  return `<div style="margin-bottom:var(--sp-4)">
    <div style="font-size:10px;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:.06em;padding-bottom:var(--sp-1);border-bottom:1px solid var(--border);margin-bottom:var(--sp-2)">${title}</div>
    <div style="padding-top:2px">${content}</div>
  </div>`;
}

// 可折叠区块 (Section 3/4/5)
function tdCollapsible(title, content, isOpen) {
  return `<details ${isOpen ? 'open' : ''} style="margin-bottom:var(--sp-3);border:1px solid var(--border);border-radius:var(--radius-sm);overflow:hidden">
    <summary style="cursor:pointer;list-style:none;display:flex;align-items:center;gap:var(--sp-2);padding:var(--sp-2) var(--sp-3);font-size:10px;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:.06em;background:var(--surface);user-select:none">
      <span style="font-size:9px">${isOpen ? '▾' : '▸'}</span> ${title}
    </summary>
    <div style="padding:var(--sp-2) var(--sp-3) var(--sp-3)">${content}</div>
  </details>`;
}

function tdReqItem(r) {
  const evHash = r.evidence ? r.evidence.split(':').pop().slice(-7) : null;
  return `<div style="display:flex;align-items:center;gap:var(--sp-2);padding:4px 0;font-size:var(--fs-xs);border-bottom:1px solid var(--border-faint,var(--border))">
    <span class="bt-status" style="background:${STATUS_CLR[r.status] || '#9ca3af'};flex-shrink:0"></span>
    <span style="color:var(--text-muted);min-width:36px;flex-shrink:0;font-size:10px">${esc(r.id)}</span>
    <span style="flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${esc(r.title)}</span>
    ${evHash ? `<code class="bt-ev" style="flex-shrink:0;margin-left:auto">${evHash}</code>` : ''}
  </div>`;
}

window.openTaskDetail = function(card, source) {
  if (!BOARD || !card) return;
  const overlay = document.getElementById('taskOverlay');
  if (!overlay) return;
  const mainEl = document.getElementById('main') || document.querySelector('main');
  if (mainEl) mainEl.setAttribute('inert', '');

  const { requirements, subplans, milestones, blockers } = BOARD;
  const statusClr   = STATUS_CLR[card.status] || '#9ca3af';
  const statusLabel = { done: '已完成', doing: '进行中', todo: '待办', partial: '部分完成', blocked: '卡点' };

  // ── Section 1: 任务标头 ──────────────────────────────────
  document.getElementById('td-status-bar').innerHTML =
    `<div style="display:flex;align-items:center;gap:var(--sp-2);flex-wrap:wrap">
       <span style="display:inline-flex;align-items:center;gap:5px;padding:2px 10px;border-radius:var(--radius-pill);background:${statusClr}22;border:1px solid ${statusClr};font-size:var(--fs-xs);font-weight:600;color:${statusClr}">
         <span style="width:6px;height:6px;border-radius:50%;background:${statusClr}"></span>
         ${esc(statusLabel[card.status] || card.status)}
       </span>
       ${source === 'subplans' ? `<span style="font-size:9px;color:#8b5cf6;font-weight:700;border:1px solid #8b5cf6;border-radius:3px;padding:0 5px">subplan</span>` : ''}
       ${card.closure_badge ? `<span style="font-size:9px;background:#10b981;color:#fff;border-radius:3px;padding:0 6px;font-weight:700;margin-left:auto">✓ ${esc(card.closure_badge)}</span>` : ''}
     </div>`;

  document.getElementById('td-title').textContent = card.id + ' · ' + card.title;
  document.getElementById('td-group').textContent  = '分组: ' + card.group + (source ? '  ·  来源: ' + source : '');

  const relReqs = (requirements || []).filter(r => (r.group || '').trim() === (card.group || '').trim());
  const relSubs = (subplans || []).filter(s => (s.group || '').trim() === (card.group || '').trim());
  const relBlks = (blockers || []).filter(b => String(b.ref) === String(card.id));
  const milArr  = milestones || [];

  let body = '';

  // blocker 警告条 — 行动信息，紧接 header
  if (card.blocker) {
    body += `<div style="display:flex;align-items:flex-start;gap:var(--sp-2);padding:var(--sp-2) var(--sp-3);border-left:3px solid #ef4444;background:#ef444411;border-radius:0 var(--radius-sm) var(--radius-sm) 0;margin-bottom:var(--sp-4);font-size:var(--fs-xs);color:#ef4444">
      <span style="font-weight:700;flex-shrink:0">⚠ 卡点</span>
      <span>${esc(card.blocker)}</span>
    </div>`;
  }

  // ── Section 2: 执行凭证 (不可折叠) ──────────────────────
  const evFull = card.evidence || '';
  const evHash = evFull ? evFull.split(':').pop() : null;
  const GITHUB_REPO = 'atomai-team/Claude_Code_Guide_Offline';
  const ghLink = evHash ? `https://github.com/${GITHUB_REPO}/commit/${evHash}` : null;
  body += tdSection('📎 执行凭证 / Commit',
    evFull
      ? `<div style="display:flex;align-items:center;gap:var(--sp-2)">
           <code class="bt-ev" style="font-size:var(--fs-xs)">${esc(evFull)}</code>
           <button onclick="navigator.clipboard.writeText('${esc(evHash || evFull)}').catch(()=>{})" title="复制 hash" style="border:none;background:none;cursor:pointer;color:var(--text-dim);font-size:12px;padding:2px 4px;border-radius:3px" onmouseenter="this.style.color='var(--accent)'" onmouseleave="this.style.color='var(--text-dim)'">⎘</button>
           ${ghLink ? `<a href="${ghLink}" target="_blank" rel="noopener" title="在 GitHub 查看此 commit" onclick="event.stopPropagation()" style="display:inline-flex;align-items:center;gap:3px;color:var(--accent);font-size:var(--fs-xs);text-decoration:none;border:1px solid var(--accent);border-radius:3px;padding:1px 6px;font-weight:600" onmouseenter="this.style.background='var(--accent)';this.style.color='#fff'" onmouseleave="this.style.background='';this.style.color='var(--accent)'"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg> GitHub</a>` : ''}
         </div>`
      : `<span style="color:var(--text-dim);font-size:var(--fs-xs)">—— 暂无执行证据</span>`);

  // ── Section 3: 关联需求 WHAT (可折叠) ───────────────────
  body += tdCollapsible('🎯 关联需求 (WHAT)',
    relReqs.length
      ? relReqs.map(tdReqItem).join('')
      : `<span style="color:var(--text-dim);font-size:var(--fs-xs)">此分组暂无关联需求文档</span>`,
    relReqs.length > 0);

  // ── Section 4: 子计划 HOW (可折叠) ──────────────────────
  body += tdCollapsible('🔧 子计划 (HOW)',
    relSubs.length
      ? relSubs.map(tdReqItem).join('')
      : `<span style="color:var(--text-dim);font-size:var(--fs-xs)">此分组暂无子计划</span>`,
    relSubs.length > 0);

  // ── Section 5: 里程碑 & 关联阻塞 (可折叠，默认关闭，两者均空则不渲染) ──
  if (milArr.length || relBlks.length) {
    const icon = { done: '✅', doing: '🔄', todo: '⬜', blocked: '🚫' };
    const milHtml = milArr.length
      ? milArr.map(m => {
          const mHash = m.evidence ? m.evidence.split(':').pop().slice(-7) : null;
          return `<div style="display:flex;align-items:center;gap:var(--sp-2);padding:4px 0;font-size:var(--fs-xs)">
            ${icon[m.status] || '⬜'}
            <span style="font-weight:600;min-width:36px;flex-shrink:0">${esc(m.id)}</span>
            <span style="flex:1">${esc(m.title)}</span>
            ${mHash ? `<code class="bt-ev">${mHash}</code>` : ''}
          </div>`;
        }).join('')
      : `<span style="color:var(--text-dim);font-size:var(--fs-xs)">暂无里程碑数据</span>`;
    const blkHtml = relBlks.length
      ? relBlks.map(b => `<div style="display:flex;align-items:center;gap:var(--sp-2);padding:3px 0;font-size:var(--fs-xs)">
          <code class="bt-ev">${esc(b.id)}</code>
          <span style="flex:1">${esc(b.title || '')}</span>
          <span style="color:var(--text-dim);font-size:10px">→ ref:${esc(String(b.ref))}</span>
        </div>`).join('')
      : `<span style="color:var(--text-dim);font-size:var(--fs-xs)">无关联阻塞记录</span>`;
    const s5content = tdSection('⛳ 里程碑', milHtml) + tdSection('🚧 关联阻塞', blkHtml);
    body += tdCollapsible('⛳ 里程碑 & 关联阻塞', s5content, false);
  }

  document.getElementById('td-body').innerHTML = body;
  overlay.style.display = 'flex';
};

window.closeTaskDetail = function() {
  const o = document.getElementById('taskOverlay');
  if (o) o.style.display = 'none';
  const mainEl = document.getElementById('main') || document.querySelector('main');
  if (mainEl) mainEl.removeAttribute('inert');
};

/* ════════════════════════════════════════════════════════════════════
   Init
   ════════════════════════════════════════════════════════════════════ */
(async function() {
  await Promise.all([loadStats(), loadDetails(), loadBoardTasks()]);
  startAutoRefresh();
})();
