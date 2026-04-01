"""Reads logo, outputs final index.html with logo embedded"""
import base64, os

logo_path = r'C:\Users\Administrator\.openclaw\workspace\assets\finexio-logo-color.png'
with open(logo_path, 'rb') as f:
    logo_b64 = base64.b64encode(f.read()).decode()
logo_uri = f'data:image/png;base64,{logo_b64}'

html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Finexio Operations Intelligence</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --bg: #F6F9FC; --surface: #FFFFFF; --surface-2: #F8FAFC;
      --navy: #043886; --navy-mid: #0A52C4; --blue: #169ee3; --pale-blue: #adddf5;
      --blue-light: #E8F4FD; --emerald: #00C48C; --emerald-bg: #EDFAF5;
      --amber: #F59E0B; --amber-bg: #FFFBEB; --rose: #E53E3E; --rose-bg: #FFF5F5;
      --text-primary: #0A2540; --text-secondary: #425466; --text-muted: #8898AA;
      --border: #E3E8EF; --border-2: #CBD5E1;
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.06); --shadow-md: 0 4px 12px rgba(10,37,64,0.08);
      --font: 'Inter', -apple-system, sans-serif; --radius: 10px; --radius-lg: 14px;
    }
    body { font-family: var(--font); background: var(--bg); color: var(--text-primary); min-height: 100vh; }

    /* HEADER */
    .header {
      position: sticky; top: 0; z-index: 100; background: var(--surface);
      border-bottom: 1px solid var(--border); padding: 0 32px; height: 60px;
      display: flex; align-items: center; justify-content: space-between;
      box-shadow: var(--shadow-sm);
    }
    .header-left { display: flex; align-items: center; gap: 12px; }
    .logo-img { height: 28px; width: auto; }
    .header-divider { width: 1px; height: 24px; background: var(--border); }
    .header-title { font-size: 14px; font-weight: 700; color: var(--text-primary); }
    .header-subtitle { font-size: 11px; color: var(--text-muted); margin-top: 1px; }
    .updated-badge {
      font-size: 11px; font-weight: 500; color: var(--text-secondary);
      background: var(--surface-2); border: 1px solid var(--border);
      border-radius: 20px; padding: 4px 12px;
    }
    .stale-badge {
      font-size: 11px; font-weight: 600; color: #C53030;
      background: var(--rose-bg); border: 1px solid #FEB2B2;
      border-radius: 20px; padding: 4px 12px;
    }

    /* FILTER BAR */
    .filter-bar {
      background: var(--surface); border-bottom: 1px solid var(--border);
      padding: 8px 32px; display: flex; align-items: center; gap: 12px;
      position: sticky; top: 60px; z-index: 99; flex-wrap: wrap;
    }
    .filter-group { display: flex; align-items: center; gap: 8px; }
    .filter-label {
      font-size: 11px; font-weight: 600; color: var(--text-muted);
      text-transform: uppercase; letter-spacing: 0.05em; white-space: nowrap;
    }
    .filter-select {
      font-family: var(--font); font-size: 13px; font-weight: 500;
      color: var(--text-primary); background: var(--surface);
      border: 1px solid var(--border-2); border-radius: 7px;
      padding: 5px 28px 5px 10px; cursor: pointer; appearance: none; -webkit-appearance: none;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='7' viewBox='0 0 10 7'%3E%3Cpath d='M1 1l4 4 4-4' stroke='%238898AA' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
      background-repeat: no-repeat; background-position: right 9px center;
      min-width: 180px; max-width: 280px; transition: border-color 0.15s;
    }
    .filter-select:focus { outline: none; border-color: var(--navy); }
    .filter-sep { width: 1px; height: 20px; background: var(--border); margin: 0 4px; }

    /* DATE RANGE BUTTONS */
    .date-group { display: flex; gap: 4px; }
    .date-btn {
      font-family: var(--font); font-size: 12px; font-weight: 500;
      color: var(--text-secondary); background: var(--surface-2);
      border: 1px solid var(--border); border-radius: 6px;
      padding: 4px 10px; cursor: pointer; transition: all 0.15s; white-space: nowrap;
    }
    .date-btn:hover { border-color: var(--navy); color: var(--navy); }
    .date-btn.active {
      background: var(--navy); color: #fff; border-color: var(--navy);
    }

    /* MAIN */
    .main { padding: 24px 32px; max-width: 1600px; margin: 0 auto; }

    /* KPI CARDS */
    .kpi-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin-bottom: 22px; }
    .kpi-card {
      background: var(--surface); border-radius: var(--radius-lg);
      padding: 18px 20px 16px; box-shadow: var(--shadow-sm); border: 1px solid var(--border);
    }
    .kpi-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
    .kpi-label-top { font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.04em; }
    .kpi-badge { font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 20px; }
    .kpi-badge.emerald { background: var(--emerald-bg); color: #00875F; }
    .kpi-badge.amber   { background: var(--amber-bg);   color: #B45309; }
    .kpi-badge.rose    { background: var(--rose-bg);    color: #C53030; }
    .kpi-badge.neutral { background: var(--blue-light); color: var(--navy-mid); }
    .kpi-value { font-size: 26px; font-weight: 800; color: var(--text-primary); line-height: 1.1; letter-spacing: -0.03em; }
    .kpi-delta { font-size: 12px; font-weight: 600; margin-top: 3px; }
    .kpi-delta.up   { color: #00875F; }
    .kpi-delta.down { color: #C53030; }
    .kpi-delta.flat { color: var(--text-muted); }
    .kpi-sublabel { font-size: 12px; color: var(--text-secondary); margin-top: 2px; }

    /* CHART GRID */
    .chart-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 18px; margin-bottom: 18px; }
    .chart-card {
      background: var(--surface); border-radius: var(--radius-lg);
      padding: 22px; box-shadow: var(--shadow-md); border: 1px solid var(--border);
    }
    .chart-card.full { grid-column: 1 / -1; }
    .chart-title { font-size: 13px; font-weight: 700; color: var(--text-primary); margin-bottom: 2px; }
    .chart-subtitle { font-size: 11px; color: var(--text-muted); margin-bottom: 18px; }
    .chart-wrap { position: relative; }

    /* TABLES */
    .table-card {
      background: var(--surface); border-radius: var(--radius-lg);
      padding: 22px; box-shadow: var(--shadow-md); border: 1px solid var(--border);
      margin-bottom: 18px;
    }
    .table-card-title { font-size: 13px; font-weight: 700; color: var(--text-primary); margin-bottom: 2px; }
    .table-card-sub { font-size: 11px; color: var(--text-muted); margin-bottom: 16px; }
    .data-table { width: 100%; border-collapse: collapse; font-size: 12px; }
    .data-table thead th {
      text-align: left; font-weight: 600; color: var(--text-muted);
      text-transform: uppercase; font-size: 10px; letter-spacing: 0.06em;
      padding: 7px 10px; border-bottom: 2px solid var(--border);
    }
    .data-table thead th.r { text-align: right; }
    .data-table tbody td {
      padding: 9px 10px; color: var(--text-secondary);
      border-bottom: 1px solid var(--surface-2); vertical-align: middle;
    }
    .data-table tbody td.r { text-align: right; font-variant-numeric: tabular-nums; }
    .data-table tbody td.bold { font-weight: 600; color: var(--text-primary); }
    .data-table tbody tr:hover td { background: var(--surface-2); }
    .data-table tbody tr:last-child td { border-bottom: none; }
    .data-table tbody tr.clickable { cursor: pointer; }
    .data-table tbody tr.selected td { background: #EEF3FF; }

    /* INLINE DELTA */
    .delta { font-size: 10px; font-weight: 600; margin-left: 4px; }
    .delta.up   { color: #00875F; }
    .delta.down { color: #C53030; }

    /* PROGRESS BAR */
    .prog-wrap { display: flex; align-items: center; gap: 6px; }
    .prog-bar { flex: 1; height: 5px; background: #E3E8EF; border-radius: 3px; overflow: hidden; min-width: 60px; }
    .prog-fill { height: 100%; border-radius: 3px; }

    /* METHOD PILL */
    .pill { display: inline-flex; align-items: center; font-size: 10px; font-weight: 600; padding: 2px 7px; border-radius: 20px; }
    .pill.check { background: var(--amber-bg); color: #B45309; }
    .pill.ach   { background: var(--blue-light); color: var(--navy-mid); }
    .pill.vcard { background: var(--emerald-bg); color: #00875F; }

    @media (max-width: 900px) {
      .header { padding: 0 16px; } .filter-bar { padding: 8px 16px; } .main { padding: 16px; }
      .chart-grid { grid-template-columns: 1fr; } .kpi-value { font-size: 22px; }
    }
  </style>
</head>
<body>

<header class="header">
  <div class="header-left">
    <img class="logo-img" src="LOGO_URI_PLACEHOLDER" alt="Finexio">
    <div class="header-divider"></div>
    <div>
      <div class="header-title">Operations Intelligence</div>
      <div class="header-subtitle">Channel Partner &amp; Customer View</div>
    </div>
  </div>
  <span id="updated-badge" class="updated-badge">Loading...</span>
</header>

<div class="filter-bar">
  <div class="filter-group">
    <span class="filter-label">Channel Partner</span>
    <select class="filter-select" id="filter-partner" onchange="onPartnerChange()">
      <option value="__all__">All Partners</option>
    </select>
  </div>
  <div class="filter-sep"></div>
  <div class="filter-group">
    <span class="filter-label">Customer</span>
    <select class="filter-select" id="filter-customer" onchange="onCustomerChange()">
      <option value="__all__">All Customers</option>
    </select>
  </div>
  <div class="filter-sep"></div>
  <div class="filter-group">
    <span class="filter-label">Period</span>
    <div class="date-group">
      <button class="date-btn" data-months="1" onclick="onDateRange(1)">30D</button>
      <button class="date-btn" data-months="3" onclick="onDateRange(3)">QTD</button>
      <button class="date-btn active" data-months="13" onclick="onDateRange(13)">YTD</button>
      <button class="date-btn" data-months="0" onclick="onDateRange(0)">All</button>
    </div>
  </div>
</div>

<main class="main">

  <!-- KPI ROW -->
  <div class="kpi-row">
    <div class="kpi-card">
      <div class="kpi-top"><span class="kpi-label-top">Payment Volume</span><span class="kpi-badge neutral" id="kpi-vol-badge">Period</span></div>
      <div class="kpi-value" id="kpi-vol">--</div>
      <div class="kpi-delta flat" id="kpi-vol-delta"></div>
      <div class="kpi-sublabel">Payments processed</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-top"><span class="kpi-label-top">Net Interchange</span><span class="kpi-badge emerald">Revenue</span></div>
      <div class="kpi-value" id="kpi-ic">--</div>
      <div class="kpi-delta flat" id="kpi-ic-delta"></div>
      <div class="kpi-sublabel">Finexio earnings</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-top"><span class="kpi-label-top">Virtual Card Rate</span><span class="kpi-badge" id="kpi-vcard-badge">Rate</span></div>
      <div class="kpi-value" id="kpi-vcard">--</div>
      <div class="kpi-delta flat" id="kpi-vcard-delta"></div>
      <div class="kpi-sublabel">Card adoption share</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-top"><span class="kpi-label-top">Check Volume</span><span class="kpi-badge amber">At Risk</span></div>
      <div class="kpi-value" id="kpi-check">--</div>
      <div class="kpi-delta flat" id="kpi-check-delta"></div>
      <div class="kpi-sublabel">Conversion opportunity</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-top"><span class="kpi-label-top">Customers</span><span class="kpi-badge neutral">Active</span></div>
      <div class="kpi-value" id="kpi-cust">--</div>
      <div class="kpi-delta flat" id="kpi-cust-delta"></div>
      <div class="kpi-sublabel">Accounts in period</div>
    </div>
  </div>

  <!-- TREND CHART -->
  <div class="chart-grid">
    <div class="chart-card full">
      <div class="chart-title" id="trend-title">Monthly Payment Volume by Method</div>
      <div class="chart-subtitle" id="trend-subtitle">ACH &middot; Virtual Card &middot; Check</div>
      <div class="chart-wrap" style="height:260px"><canvas id="chart-trend"></canvas></div>
    </div>
  </div>

  <!-- METHOD MIX + PARTNER BAR -->
  <div class="chart-grid">
    <div class="chart-card">
      <div class="chart-title">Payment Method Mix</div>
      <div class="chart-subtitle">Volume share by payment type</div>
      <div class="chart-wrap" style="height:280px"><canvas id="chart-mix"></canvas></div>
    </div>
    <div class="chart-card">
      <div class="chart-title">Volume by Channel Partner</div>
      <div class="chart-subtitle">All-time totals &mdash; click to filter</div>
      <div class="chart-wrap" style="height:280px"><canvas id="chart-partners"></canvas></div>
    </div>
  </div>

  <!-- CUSTOMER TABLE -->
  <div class="table-card">
    <div class="table-card-title" id="cust-table-title">Top Customers</div>
    <div class="table-card-sub" id="cust-table-sub">Select a channel partner to drill down</div>
    <table class="data-table">
      <thead>
        <tr>
          <th>Customer Account</th>
          <th class="r">Total Volume</th>
          <th class="r">MoM</th>
          <th class="r">Payments</th>
          <th class="r">Buyers</th>
          <th style="min-width:160px">Virtual Card Rate</th>
          <th class="r">Check Volume</th>
          <th class="r">ACH Volume</th>
        </tr>
      </thead>
      <tbody id="cust-tbody"></tbody>
    </table>
  </div>

  <!-- PARTNER COMPARISON TABLE -->
  <div class="table-card">
    <div class="table-card-title">Channel Partner Comparison</div>
    <div class="table-card-sub">All partners &mdash; click a row to filter</div>
    <table class="data-table">
      <thead>
        <tr>
          <th>Partner</th>
          <th class="r">Total Volume</th>
          <th class="r">MoM</th>
          <th class="r">Net Interchange</th>
          <th class="r">Payments</th>
          <th class="r">Customers</th>
          <th class="r">Buyers</th>
          <th class="r">VCard %</th>
          <th class="r">Check Volume</th>
          <th class="r">Refund Volume</th>
        </tr>
      </thead>
      <tbody id="partner-tbody"></tbody>
    </table>
  </div>

</main>

<script src="tab1_data.js"></script>
<script>
  // ── Formatters ────────────────────────────────────────────────
  function fc(n) {
    if (!n && n !== 0) return '--';
    var a = Math.abs(n);
    if (a >= 1e9) return (n < 0 ? '-' : '') + '$' + (a/1e9).toFixed(1) + 'B';
    if (a >= 1e6) return (n < 0 ? '-' : '') + '$' + (a/1e6).toFixed(1) + 'M';
    if (a >= 1e3) return (n < 0 ? '-' : '') + '$' + (a/1e3).toFixed(1) + 'K';
    return (n < 0 ? '-$' : '$') + Math.round(a).toLocaleString();
  }
  function fn(n) { return (n||0).toLocaleString('en-US'); }
  function fp(n) { return (n||0).toFixed(1) + '%'; }
  function fdelta(pct) {
    if (!pct && pct !== 0) return '';
    var sign = pct > 0 ? '+' : '';
    return sign + pct.toFixed(1) + '% MoM';
  }
  function deltaClass(pct) { return pct > 0 ? 'up' : pct < 0 ? 'down' : 'flat'; }

  // ── Chart defaults ────────────────────────────────────────────
  Chart.defaults.font.family = "'Inter', sans-serif";
  Chart.defaults.font.size = 11;
  Chart.defaults.color = '#8898AA';
  var charts = {};
  function gc() { return { color: '#E3E8EF' }; }
  function tt() {
    return {
      backgroundColor: '#0A2540', titleColor: '#fff', bodyColor: '#CBD5E1',
      borderColor: 'rgba(255,255,255,0.1)', borderWidth: 1, padding: 9, cornerRadius: 7,
      titleFont: { size: 12, weight: '600' }, bodyFont: { size: 11 }
    };
  }
  function destroyChart(k) { if (charts[k]) { charts[k].destroy(); delete charts[k]; } }

  // ── State ─────────────────────────────────────────────────────
  var selPartner  = '__all__';
  var selCustomer = '__all__';
  var selMonths   = 13;  // YTD default

  // ── Date range filter ─────────────────────────────────────────
  function onDateRange(months) {
    selMonths = months;
    document.querySelectorAll('.date-btn').forEach(function(b) {
      b.classList.toggle('active', parseInt(b.dataset.months) === months);
    });
    render();
  }

  function filterMonths(data) {
    if (selMonths === 0) return data;
    if (!data || !data.length) return data;
    var cutoff;
    var now = new Date();
    if (selMonths === 1) {
      cutoff = new Date(now.getFullYear(), now.getMonth() - 1, now.getDate());
    } else {
      cutoff = new Date(now.getFullYear(), now.getMonth() - selMonths, 1);
    }
    var cutoffStr = cutoff.toISOString().slice(0, 7);
    return data.filter(function(d) { return d.month >= cutoffStr; });
  }

  // ── Filter dropdowns ──────────────────────────────────────────
  function populatePartners() {
    var sel = document.getElementById('filter-partner');
    TAB1_DATA.channelPartners.forEach(function(cp) {
      var o = document.createElement('option');
      o.value = cp.channel_partner; o.textContent = cp.channel_partner;
      sel.appendChild(o);
    });
  }

  function populateCustomers(partner) {
    var sel = document.getElementById('filter-customer');
    sel.innerHTML = '<option value="__all__">All Customers</option>';
    if (partner === '__all__') return;
    var list = TAB1_DATA.customersByPartner[partner] || [];
    list.forEach(function(c) {
      var o = document.createElement('option');
      o.value = c.customer; o.textContent = c.customer;
      sel.appendChild(o);
    });
  }

  function onPartnerChange() {
    selPartner = document.getElementById('filter-partner').value;
    selCustomer = '__all__';
    document.getElementById('filter-customer').value = '__all__';
    populateCustomers(selPartner);
    render();
  }
  function onCustomerChange() {
    selCustomer = document.getElementById('filter-customer').value;
    render();
  }

  // ── Get monthly series for current selection ───────────────────
  function getMonthly() {
    var raw;
    if (selPartner === '__all__') {
      raw = TAB1_DATA.monthlyByPartner['__all__'] || [];
    } else {
      raw = TAB1_DATA.monthlyByPartner[selPartner] || [];
    }
    return filterMonths(raw);
  }

  // ── Compute aggregates from monthly series ─────────────────────
  function sumMonthly(data) {
    return data.reduce(function(acc, m) {
      acc.total_volume += m.total_volume;
      acc.vcard_volume += m.vcard_volume;
      acc.ach_volume   += m.ach_volume;
      acc.check_volume += m.check_volume;
      return acc;
    }, { total_volume: 0, vcard_volume: 0, ach_volume: 0, check_volume: 0 });
  }

  // ── Render KPIs ───────────────────────────────────────────────
  function renderKPIs() {
    var monthly = getMonthly();
    var sums = sumMonthly(monthly);
    var total = sums.total_volume;
    var vcardRate = total ? 100 * sums.vcard_volume / total : 0;

    // Interchange: from partner data (all-time for now)
    var ic = 0;
    if (selPartner === '__all__') {
      TAB1_DATA.channelPartners.forEach(function(cp) { ic += cp.net_interchange; });
    } else {
      var cp = TAB1_DATA.channelPartners.find(function(x) { return x.channel_partner === selPartner; });
      if (cp) ic = cp.net_interchange;
    }

    // MoM for the selected partner
    var mom = 0;
    if (selPartner !== '__all__') {
      var cp2 = TAB1_DATA.channelPartners.find(function(x) { return x.channel_partner === selPartner; });
      if (cp2) mom = cp2.mom_pct;
    }

    // Customer count
    var custCount = 0;
    if (selPartner === '__all__') {
      TAB1_DATA.channelPartners.forEach(function(cp) { custCount += cp.customer_count; });
    } else {
      var cp3 = TAB1_DATA.channelPartners.find(function(x) { return x.channel_partner === selPartner; });
      if (cp3) custCount = cp3.customer_count;
    }

    document.getElementById('kpi-vol').textContent   = fc(total);
    document.getElementById('kpi-ic').textContent    = fc(ic);
    document.getElementById('kpi-vcard').textContent = fp(vcardRate);
    document.getElementById('kpi-check').textContent = fc(sums.check_volume);
    document.getElementById('kpi-cust').textContent  = fn(custCount);

    var vcardBadge = document.getElementById('kpi-vcard-badge');
    if (vcardRate >= 20)      { vcardBadge.className = 'kpi-badge emerald'; vcardBadge.textContent = 'Strong'; }
    else if (vcardRate >= 10) { vcardBadge.className = 'kpi-badge amber';   vcardBadge.textContent = 'Growing'; }
    else                      { vcardBadge.className = 'kpi-badge rose';    vcardBadge.textContent = 'Low'; }

    // Deltas — only meaningful for non-all selection
    function setDelta(id, pct) {
      var el = document.getElementById(id);
      if (!pct) { el.textContent = ''; el.className = 'kpi-delta flat'; return; }
      el.textContent = fdelta(pct);
      el.className = 'kpi-delta ' + deltaClass(pct);
    }
    if (selPartner !== '__all__' && mom !== 0) {
      setDelta('kpi-vol-delta', mom);
    } else {
      setDelta('kpi-vol-delta', null);
    }
    setDelta('kpi-ic-delta', null);
    setDelta('kpi-vcard-delta', null);
    setDelta('kpi-check-delta', null);
    setDelta('kpi-cust-delta', null);
  }

  // ── Render Trend ──────────────────────────────────────────────
  function renderTrend() {
    destroyChart('trend');
    var data = getMonthly();
    var label = selPartner === '__all__' ? 'All Partners' : selPartner;
    document.getElementById('trend-title').textContent = 'Monthly Payment Volume — ' + label;
    charts.trend = new Chart(document.getElementById('chart-trend'), {
      type: 'bar',
      data: {
        labels: data.map(function(m) { return m.month; }),
        datasets: [
          { label: 'ACH',          data: data.map(function(m){return m.ach_volume;}),   backgroundColor: '#043886', stack: 'v' },
          { label: 'Virtual Card', data: data.map(function(m){return m.vcard_volume;}), backgroundColor: '#00C48C', stack: 'v' },
          { label: 'Check',        data: data.map(function(m){return m.check_volume;}), backgroundColor: '#F59E0B', stack: 'v' }
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { font: { size: 11 }, padding: 14, usePointStyle: true, pointStyleWidth: 8 } },
          tooltip: Object.assign({}, tt(), {
            callbacks: { label: function(ctx) { return '  ' + ctx.dataset.label + ': ' + fc(ctx.parsed.y); } }
          })
        },
        scales: {
          x: { stacked: true, grid: { display: false }, ticks: { font: { size: 10 } } },
          y: { stacked: true, grid: gc(), ticks: { font: { size: 10 }, callback: function(v){ return fc(v); } } }
        }
      }
    });
  }

  // ── Render Method Mix ─────────────────────────────────────────
  function renderMix() {
    destroyChart('mix');
    var monthly = getMonthly();
    var sums = sumMonthly(monthly);
    var total = sums.total_volume;
    var other = Math.max(0, total - sums.ach_volume - sums.vcard_volume - sums.check_volume);
    var entries = [
      { l: 'ACH',          v: sums.ach_volume,   c: '#043886' },
      { l: 'Virtual Card', v: sums.vcard_volume,  c: '#00C48C' },
      { l: 'Check',        v: sums.check_volume,  c: '#F59E0B' },
      { l: 'Other',        v: other,              c: '#8898AA' }
    ].filter(function(e) { return e.v > 0; });

    charts.mix = new Chart(document.getElementById('chart-mix'), {
      type: 'doughnut',
      data: {
        labels: entries.map(function(e){return e.l;}),
        datasets: [{ data: entries.map(function(e){return e.v;}), backgroundColor: entries.map(function(e){return e.c;}), borderWidth: 3, borderColor: '#fff', hoverOffset: 8 }]
      },
      options: {
        responsive: true, maintainAspectRatio: false, cutout: '60%',
        plugins: {
          legend: {
            position: 'right',
            labels: {
              font: { size: 11 }, padding: 10, usePointStyle: true, pointStyleWidth: 8,
              generateLabels: function(chart) {
                var d = chart.data.datasets[0].data;
                var tot = d.reduce(function(a,b){return a+b;},0);
                return chart.data.labels.map(function(lbl,i){
                  return { text: lbl + '  ' + ((d[i]/tot)*100).toFixed(1)+'%', fillStyle: chart.data.datasets[0].backgroundColor[i], strokeStyle: chart.data.datasets[0].backgroundColor[i], pointStyle:'circle', index:i };
                });
              }
            }
          },
          tooltip: Object.assign({}, tt(), { callbacks: { label: function(ctx){ return '  '+ctx.label+': '+fc(ctx.parsed); } } })
        }
      }
    });
  }

  // ── Render Partner Bar ────────────────────────────────────────
  function renderPartnerBar() {
    destroyChart('pbar');
    var partners = TAB1_DATA.channelPartners.slice(0, 12);
    charts.pbar = new Chart(document.getElementById('chart-partners'), {
      type: 'bar',
      data: {
        labels: partners.map(function(p){return p.channel_partner;}),
        datasets: [{
          label: 'Volume',
          data: partners.map(function(p){return p.total_volume;}),
          backgroundColor: partners.map(function(p){ return p.channel_partner === selPartner ? '#043886' : 'rgba(4,56,134,0.45)'; }),
          borderRadius: 3
        }]
      },
      options: {
        indexAxis: 'y', responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: Object.assign({}, tt(), { callbacks: { label: function(ctx){ return '  '+fc(ctx.parsed.x); } } })
        },
        scales: {
          x: { grid: gc(), ticks: { font: { size: 10 }, callback: function(v){ return fc(v); } } },
          y: { grid: { display: false }, ticks: { font: { size: 10 } } }
        },
        onClick: function(evt, items) {
          if (items.length) {
            var name = partners[items[0].index].channel_partner;
            document.getElementById('filter-partner').value = name;
            selPartner = name; selCustomer = '__all__';
            document.getElementById('filter-customer').value = '__all__';
            populateCustomers(selPartner);
            render();
          }
        }
      }
    });
  }

  // ── Render Customer Table ─────────────────────────────────────
  function renderCustTable() {
    var tbody = document.getElementById('cust-tbody');
    tbody.innerHTML = '';
    var list = [];
    if (selPartner !== '__all__') {
      list = TAB1_DATA.customersByPartner[selPartner] || [];
      document.getElementById('cust-table-title').textContent = 'Customers — ' + selPartner;
      document.getElementById('cust-table-sub').textContent   = list.length + ' accounts ranked by payment volume';
    } else {
      var map = {};
      Object.keys(TAB1_DATA.customersByPartner).forEach(function(p) {
        (TAB1_DATA.customersByPartner[p] || []).forEach(function(c) {
          if (!map[c.customer]) map[c.customer] = { customer: c.customer, buyer_count: 0, total_volume: 0, payment_count: 0, vcard_volume: 0, ach_volume: 0, check_volume: 0, vol_this_month: 0, vol_last_month: 0 };
          map[c.customer].total_volume   += c.total_volume;
          map[c.customer].payment_count  += c.payment_count;
          map[c.customer].buyer_count    += c.buyer_count;
          map[c.customer].vcard_volume   += c.vcard_volume;
          map[c.customer].ach_volume     += c.ach_volume;
          map[c.customer].check_volume   += c.check_volume;
          map[c.customer].vol_this_month += c.vol_this_month;
          map[c.customer].vol_last_month += c.vol_last_month;
        });
      });
      list = Object.values(map).sort(function(a,b){ return b.total_volume - a.total_volume; }).slice(0, 20);
      list.forEach(function(c) {
        c.mom_pct = c.vol_last_month ? (c.vol_this_month - c.vol_last_month) / c.vol_last_month * 100 : 0;
      });
      document.getElementById('cust-table-title').textContent = 'Top Customers — All Partners';
      document.getElementById('cust-table-sub').textContent   = 'Top 20 accounts across all channel partners';
    }

    list.forEach(function(c) {
      var vcr = c.total_volume ? (100 * c.vcard_volume / c.total_volume) : 0;
      var barC = vcr >= 20 ? '#00C48C' : vcr >= 10 ? '#F59E0B' : '#E53E3E';
      var mom = c.mom_pct || 0;
      var momHtml = mom !== 0
        ? '<span class="delta ' + deltaClass(mom) + '">' + (mom > 0 ? '+' : '') + mom.toFixed(1) + '%</span>'
        : '<span style="color:var(--text-muted)">--</span>';
      var tr = document.createElement('tr');
      tr.innerHTML =
        '<td class="bold">' + c.customer + '</td>' +
        '<td class="r">' + fc(c.total_volume) + '</td>' +
        '<td class="r">' + momHtml + '</td>' +
        '<td class="r">' + fn(c.payment_count) + '</td>' +
        '<td class="r">' + fn(c.buyer_count) + '</td>' +
        '<td><div class="prog-wrap"><div class="prog-bar"><div class="prog-fill" style="width:' + Math.min(vcr,100).toFixed(0) + '%;background:' + barC + '"></div></div><span style="font-size:11px;color:var(--text-secondary);min-width:34px">' + fp(vcr) + '</span></div></td>' +
        '<td class="r"><span class="pill check">' + fc(c.check_volume) + '</span></td>' +
        '<td class="r">' + fc(c.ach_volume) + '</td>';
      tbody.appendChild(tr);
    });
  }

  // ── Render Partner Table ──────────────────────────────────────
  function renderPartnerTable() {
    var tbody = document.getElementById('partner-tbody');
    tbody.innerHTML = '';
    TAB1_DATA.channelPartners.forEach(function(cp) {
      var tr = document.createElement('tr');
      tr.className = 'clickable' + (cp.channel_partner === selPartner ? ' selected' : '');
      var mom = cp.mom_pct || 0;
      var momHtml = '<span class="delta ' + deltaClass(mom) + '">' + (mom > 0 ? '+' : '') + mom.toFixed(1) + '%</span>';
      tr.innerHTML =
        '<td class="bold">' + cp.channel_partner + '</td>' +
        '<td class="r">' + fc(cp.total_volume) + '</td>' +
        '<td class="r">' + momHtml + '</td>' +
        '<td class="r">' + fc(cp.net_interchange) + '</td>' +
        '<td class="r">' + fn(cp.payment_count) + '</td>' +
        '<td class="r">' + fn(cp.customer_count) + '</td>' +
        '<td class="r">' + fn(cp.buyer_count) + '</td>' +
        '<td class="r">' + fp(cp.vcard_rate) + '</td>' +
        '<td class="r"><span class="pill check">' + fc(cp.check_volume) + '</span></td>' +
        '<td class="r">' + fc(cp.refund_volume) + '</td>';
      tr.addEventListener('click', function() {
        selPartner = cp.channel_partner;
        selCustomer = '__all__';
        document.getElementById('filter-partner').value = selPartner;
        document.getElementById('filter-customer').value = '__all__';
        populateCustomers(selPartner);
        render();
      });
      tbody.appendChild(tr);
    });
  }

  // ── Master render ─────────────────────────────────────────────
  function render() {
    renderKPIs();
    renderTrend();
    renderMix();
    renderPartnerBar();
    renderCustTable();
    renderPartnerTable();
  }

  // ── Bootstrap ─────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function() {
    populatePartners();

    var ts = new Date(TAB1_DATA.lastUpdated);
    var now = new Date();
    var ageHours = (now - ts) / 3600000;
    var badge = document.getElementById('updated-badge');
    var label = 'Updated ' +
      ts.toLocaleDateString('en-US', { month:'short', day:'numeric', year:'numeric' }) +
      ' \u00b7 ' +
      ts.toLocaleTimeString('en-US', { hour:'2-digit', minute:'2-digit', timeZoneName:'short' });
    if (ageHours > 25) {
      badge.className = 'stale-badge';
      label = 'Data may be stale \u00b7 ' + label;
    }
    badge.textContent = label;

    render();
  });
</script>
</body>
</html>"""

html = html.replace('LOGO_URI_PLACEHOLDER', logo_uri)

out = r'C:\Users\Administrator\.openclaw\workspace\intel-dashboard\index.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Wrote {out} ({len(html)//1024}KB)")
