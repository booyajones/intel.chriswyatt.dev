#!/usr/bin/env python3
"""
Dashboard Review Gauntlet
Automated layout and quality review of the dashboard index.html
"""

import re
import os
import sys
import json
import argparse
import io
from pathlib import Path

# Force UTF-8 output on Windows so box-drawing and unicode symbols render correctly
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ─── ANSI Colors ──────────────────────────────────────────────────────────────

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"

# ─── Result Accumulator ───────────────────────────────────────────────────────

results = []  # list of dicts: {status, category, message, fix_hint}

def record(status, category, message, fix_hint=""):
    results.append({
        "status": status,
        "category": category,
        "message": message,
        "fix_hint": fix_hint,
    })

def PASS(category, message):
    record("PASS", category, message)

def FAIL(category, message, fix_hint=""):
    record("FAIL", category, message, fix_hint)

def WARN(category, message, fix_hint=""):
    record("WARN", category, message, fix_hint)

# ─── File Loading ─────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent.resolve()

def load_file(filename):
    """Load a file from the script directory. Returns (content_str, error_str)."""
    path = SCRIPT_DIR / filename
    try:
        return path.read_text(encoding="utf-8"), None
    except FileNotFoundError:
        return None, f"File not found: {path}"
    except Exception as e:
        return None, f"Error reading {path}: {e}"

def file_exists(filename):
    return (SCRIPT_DIR / filename).exists()

def file_size(filename):
    path = SCRIPT_DIR / filename
    try:
        return path.stat().st_size
    except Exception:
        return 0

# ─── JS Data File Parser ──────────────────────────────────────────────────────

def parse_js_data(js_content, var_name):
    """
    Strip  var VAR_NAME = { ... };  and parse the JSON body.
    Returns (dict_or_list, error_str).
    """
    # Match: (const|let|var) VAR_NAME = <json>;
    pattern = rf'(?:var|let|const)\s+{re.escape(var_name)}\s*=\s*'
    match = re.search(pattern, js_content)
    if not match:
        return None, f"Could not find variable '{var_name}' in JS file"
    body = js_content[match.end():].strip()
    # Remove trailing semicolon(s)
    body = re.sub(r';\s*$', '', body.rstrip())
    # Strip JS line comments (// ...) that are not valid JSON
    body = re.sub(r'//[^\n]*', '', body)
    try:
        return json.loads(body), None
    except json.JSONDecodeError as e:
        return None, f"JSON parse error for '{var_name}': {e}"

# ─── 1. Structure Checks ──────────────────────────────────────────────────────

def check_structure(html):
    cat = "Structure"

    # DOCTYPE
    if re.search(r'<!DOCTYPE\s+html', html, re.IGNORECASE):
        PASS(cat, "DOCTYPE declaration present")
    else:
        FAIL(cat, "Missing <!DOCTYPE html> declaration",
             "Add <!DOCTYPE html> as the very first line of index.html")

    # <html lang="en">
    if re.search(r'<html[^>]+lang\s*=\s*["\']en["\']', html, re.IGNORECASE):
        PASS(cat, '<html lang="en"> present')
    else:
        FAIL(cat, 'Missing <html lang="en">',
             'Change <html> to <html lang="en">')

    # meta charset
    if re.search(r'<meta[^>]+charset\s*=\s*["\']?UTF-8["\']?', html, re.IGNORECASE):
        PASS(cat, '<meta charset="UTF-8"> present')
    else:
        FAIL(cat, 'Missing <meta charset="UTF-8">',
             'Add <meta charset="UTF-8"> inside <head>')

    # meta viewport
    if re.search(r'<meta[^>]+name\s*=\s*["\']viewport["\']', html, re.IGNORECASE):
        PASS(cat, '<meta name="viewport"> present')
    else:
        FAIL(cat, 'Missing <meta name="viewport">',
             'Add <meta name="viewport" content="width=device-width, initial-scale=1.0"> inside <head>')

    # title
    if re.search(r'<title[^>]*>.+?</title>', html, re.IGNORECASE | re.DOTALL):
        PASS(cat, '<title> tag present and non-empty')
    else:
        FAIL(cat, 'Missing or empty <title> tag',
             'Add a descriptive <title> inside <head>')

    # structural landmarks
    for tag in ("header", "nav", "main"):
        if re.search(rf'<{tag}[\s>]', html, re.IGNORECASE):
            PASS(cat, f'<{tag}> element present')
        else:
            FAIL(cat, f'Missing <{tag}> element',
                 f'Add a <{tag}> landmark element for semantics and accessibility')

    # exactly 3 tab buttons
    tab_btns = re.findall(r'class\s*=\s*["\'][^"\']*\btab-btn\b[^"\']*["\']', html)
    n_btns = len(tab_btns)
    if n_btns == 3:
        PASS(cat, f'Exactly 3 tab buttons (class="tab-btn") found')
    else:
        FAIL(cat, f'Expected 3 tab buttons, found {n_btns}',
             'Ensure exactly 3 elements have class="tab-btn" (one per tab)')

    # exactly 3 tab panels
    tab_panels = re.findall(r'class\s*=\s*["\'][^"\']*\btab-panel\b[^"\']*["\']', html)
    n_panels = len(tab_panels)
    if n_panels == 3:
        PASS(cat, f'Exactly 3 tab panels (class="tab-panel") found')
    else:
        FAIL(cat, f'Expected 3 tab panels, found {n_panels}',
             'Ensure exactly 3 elements have class="tab-panel" (one per tab)')

    # tab buttons have data-tab attributes
    btn_with_data_tab = re.findall(
        r'<button[^>]+class\s*=\s*["\'][^"\']*\btab-btn\b[^"\']*["\'][^>]*data-tab\s*=',
        html, re.IGNORECASE)
    # also check reversed attribute order
    btn_with_data_tab2 = re.findall(
        r'<button[^>]+data-tab\s*=[^>]+class\s*=\s*["\'][^"\']*\btab-btn\b',
        html, re.IGNORECASE)
    total_data_tab = len(btn_with_data_tab) + len(btn_with_data_tab2)
    if total_data_tab >= 3:
        PASS(cat, 'Tab buttons have data-tab attributes')
    else:
        FAIL(cat, f'Tab buttons missing data-tab attributes (found {total_data_tab}/3)',
             'Add data-tab="<tab-id>" to each tab button')

    # tab panels have id attributes
    panels_with_id = re.findall(
        r'<[^>]+class\s*=\s*["\'][^"\']*\btab-panel\b[^"\']*["\'][^>]+id\s*=',
        html, re.IGNORECASE)
    panels_with_id2 = re.findall(
        r'<[^>]+id\s*=[^>]+class\s*=\s*["\'][^"\']*\btab-panel\b',
        html, re.IGNORECASE)
    total_panel_ids = len(panels_with_id) + len(panels_with_id2)
    if total_panel_ids >= 3:
        PASS(cat, 'Tab panels have id attributes')
    else:
        FAIL(cat, f'Tab panels missing id attributes (found {total_panel_ids}/3)',
             'Add a unique id="<tab-id>" to each tab panel div')

    # one tab-btn active by default
    active_btns = re.findall(
        r'class\s*=\s*["\'][^"\']*\btab-btn\b[^"\']*\bactive\b[^"\']*["\']', html)
    if len(active_btns) == 1:
        PASS(cat, 'Exactly one tab button has class="tab-btn active" by default')
    elif len(active_btns) == 0:
        FAIL(cat, 'No tab button has class="tab-btn active" by default',
             'Add "active" class to the first tab button so a tab is visible on load')
    else:
        WARN(cat, f'{len(active_btns)} tab buttons have "active" class (expected 1)',
             'Only the default/first tab button should have the "active" class on page load')

    # one tab-panel active by default
    active_panels = re.findall(
        r'class\s*=\s*["\'][^"\']*\btab-panel\b[^"\']*\bactive\b[^"\']*["\']', html)
    if len(active_panels) == 1:
        PASS(cat, 'Exactly one tab panel has class="tab-panel active" by default')
    elif len(active_panels) == 0:
        FAIL(cat, 'No tab panel has class="tab-panel active" by default',
             'Add "active" class to the first tab panel so its content is visible on load')
    else:
        WARN(cat, f'{len(active_panels)} tab panels have "active" class (expected 1)',
             'Only the default/first tab panel should have the "active" class on page load')


# ─── 2. CDN / Script Checks ───────────────────────────────────────────────────

def check_cdn(html):
    cat = "CDN/Scripts"

    # Chart.js
    if re.search(r'<script[^>]+src\s*=\s*["\'][^"\']*chart\.js[^"\']*["\']', html, re.IGNORECASE):
        PASS(cat, 'Chart.js loaded from CDN')
    else:
        FAIL(cat, 'Chart.js CDN script not found',
             'Add <script src="https://cdn.jsdelivr.net/npm/chart.js"></script> before closing </body>')

    # Tailwind
    if re.search(r'<script[^>]+src\s*=\s*["\'][^"\']*tailwindcss[^"\']*["\']', html, re.IGNORECASE):
        PASS(cat, 'Tailwind CSS loaded from CDN')
    else:
        FAIL(cat, 'Tailwind CSS CDN script not found',
             'Add <script src="https://cdn.tailwindcss.com"></script> inside <head>')

    # Google Fonts / Inter
    has_gfonts = bool(re.search(r'fonts\.googleapis\.com', html, re.IGNORECASE))
    has_inter  = bool(re.search(r'\bInter\b', html))
    if has_gfonts and has_inter:
        PASS(cat, 'Inter font loaded from Google Fonts')
    elif has_gfonts:
        WARN(cat, 'Google Fonts link found but Inter not referenced',
             'Ensure the Google Fonts URL includes "Inter" as a font family')
    else:
        FAIL(cat, 'Inter font from Google Fonts not found',
             'Add <link href="https://fonts.googleapis.com/css2?family=Inter:wght@...&display=swap" rel="stylesheet"> in <head>')

    # Data JS files referenced in HTML
    data_files = {
        "customer_value_data.js": r'customer_value_data\.js',
        "cbm_insights_data.js":   r'cbm_insights_data\.js',
        "ops_data.js":            r'ops_data\.js',
    }
    for filename, pattern in data_files.items():
        if re.search(pattern, html, re.IGNORECASE):
            PASS(cat, f'{filename} referenced in HTML')
        else:
            FAIL(cat, f'{filename} not referenced in HTML',
                 f'Add <script src="{filename}"></script> before your main inline script')

        # Also check disk existence
        if file_exists(filename):
            PASS(cat, f'{filename} exists on disk')
        else:
            FAIL(cat, f'{filename} does not exist on disk',
                 f'Create the file {SCRIPT_DIR / filename} with the required data object')

    # fetch_bq_data.py
    if file_exists("fetch_bq_data.py"):
        PASS(cat, 'fetch_bq_data.py exists on disk')
    else:
        FAIL(cat, 'fetch_bq_data.py does not exist on disk',
             f'Create {SCRIPT_DIR / "fetch_bq_data.py"} — the BigQuery data fetch script')


# ─── 3. Tab Content Checks ────────────────────────────────────────────────────

def _count_kpi_cards(section_html):
    """Count card/kpi-card elements in a section of HTML."""
    return len(re.findall(r'class\s*=\s*["\'][^"\']*\b(?:card|kpi-card)\b[^"\']*["\']', section_html))

def _extract_tab_section(html, tab_id):
    """
    Try to extract the HTML block for a specific tab panel by id.
    Returns the slice of html between the opening tag and a heuristic closing </div>.
    Falls back to full html if not found.
    """
    # Look for <div id="<tab_id>" ...> or <section id="<tab_id>" ...>
    start_pat = r'<(?:div|section)[^>]+id\s*=\s*["\']' + re.escape(tab_id) + r'["\'][^>]*>'
    m = re.search(start_pat, html, re.IGNORECASE)
    if not m:
        return html  # can't isolate, search full document
    return html[m.start():]

def check_tab_content(html):
    cat_cv  = "Tab:CustomerValue"
    cat_cbm = "Tab:CBMInsights"
    cat_ops = "Tab:Ops"

    # ── Customer Value Tab ──
    cv_html = _extract_tab_section(html, "customer-value")

    kpi_count = _count_kpi_cards(cv_html)
    if kpi_count >= 4:
        PASS(cat_cv, f'At least 4 KPI cards found ({kpi_count})')
    else:
        FAIL(cat_cv, f'Expected ≥4 KPI cards, found {kpi_count}',
             'Add KPI card elements (class="card" or class="kpi-card") to the Customer Value tab')

    if re.search(r'<canvas[^>]+id\s*=\s*["\'][^"\']*(?:payment(?:Method)?|donut|doughnut)[^"\']*["\']',
                 cv_html, re.IGNORECASE):
        PASS(cat_cv, 'Donut/doughnut chart canvas found (payment method mix)')
    else:
        FAIL(cat_cv, 'Missing donut/doughnut chart canvas for payment method mix',
             'Add <canvas id="paymentMethodChart"></canvas> in the Customer Value tab')

    if re.search(r'<canvas[^>]+id\s*=\s*["\'][^"\']*(?:monthly|volume|stacked)[^"\']*["\']',
                 cv_html, re.IGNORECASE):
        PASS(cat_cv, 'Stacked bar chart canvas for monthly volume found')
    else:
        FAIL(cat_cv, 'Missing stacked bar chart canvas for monthly volume',
             'Add <canvas id="monthlyVolumeChart"></canvas> in the Customer Value tab')

    if re.search(r'<canvas[^>]+id\s*=\s*["\'][^"\']*(?:top|buyer|horizontal|buyer)[^"\']*["\']',
                 cv_html, re.IGNORECASE):
        PASS(cat_cv, 'Horizontal bar chart canvas for top buyers found')
    else:
        FAIL(cat_cv, 'Missing horizontal bar chart canvas for top buyers',
             'Add <canvas id="chart-top-buyers"></canvas> in the Customer Value tab')

    if re.search(r'supplier', cv_html, re.IGNORECASE):
        PASS(cat_cv, 'Supplier stats section present')
    else:
        FAIL(cat_cv, 'Missing supplier stats section',
             'Add a section referencing supplierStats data from CUSTOMER_VALUE_DATA in the Customer Value tab')

    # ── CBM Insights Tab ──
    cbm_html = _extract_tab_section(html, "cbm-insights")

    kpi_count = _count_kpi_cards(cbm_html)
    if kpi_count >= 4:
        PASS(cat_cbm, f'At least 4 KPI cards found ({kpi_count})')
    else:
        FAIL(cat_cbm, f'Expected ≥4 KPI cards, found {kpi_count}',
             'Add KPI card elements to the CBM Insights tab')

    if re.search(r'(?:<canvas[^>]+id\s*=\s*["\'][^"\']*(?:funnel|stage|event)[^"\']*["\']|funnel|ple_event_stage|eventStageFunnel)',
                 cbm_html, re.IGNORECASE):
        PASS(cat_cbm, 'Funnel/stage chart or HTML funnel found')
    else:
        FAIL(cat_cbm, 'Missing funnel/stage chart or HTML funnel',
             'Add a stage funnel visualization (canvas or HTML) referencing CBM_INSIGHTS_DATA.eventStageFunnel')

    if re.search(r'<canvas[^>]+id\s*=\s*["\'][^"\']*(?:age|Age)[^"\']*["\']',
                 cbm_html, re.IGNORECASE):
        PASS(cat_cbm, 'Age distribution chart canvas found')
    else:
        FAIL(cat_cbm, 'Missing age distribution chart canvas',
             'Add <canvas id="ageDistributionChart"></canvas> in the CBM Insights tab')

    if re.search(r'<canvas[^>]+id\s*=\s*["\'][^"\']*(?:exc|exception|trend)[^"\']*["\']',
                 cbm_html, re.IGNORECASE):
        PASS(cat_cbm, 'Exception trend chart canvas found')
    else:
        FAIL(cat_cbm, 'Missing exception trend chart canvas',
             'Add <canvas id="chart-exc-trend"></canvas> in the CBM Insights tab')

    if re.search(r'refund', cbm_html, re.IGNORECASE):
        PASS(cat_cbm, 'Refund analysis section present')
    else:
        FAIL(cat_cbm, 'Missing refund analysis section',
             'Add a refund analysis section referencing CBM_INSIGHTS_DATA.refundAnalysis')

    # ── Ops Tab ──
    ops_html = _extract_tab_section(html, "ops")

    kpi_count = _count_kpi_cards(ops_html)
    if kpi_count >= 4:
        PASS(cat_ops, f'At least 4 KPI cards found ({kpi_count})')
    else:
        FAIL(cat_ops, f'Expected ≥4 KPI cards, found {kpi_count}',
             'Add KPI card elements to the Ops tab')

    if re.search(r'<canvas[^>]+id\s*=\s*["\'][^"\']*(?:payment(?:Status|status)|status)[^"\']*["\']',
                 ops_html, re.IGNORECASE):
        PASS(cat_ops, 'Payment status chart canvas found')
    else:
        FAIL(cat_ops, 'Missing payment status chart canvas',
             'Add <canvas id="paymentStatusChart"></canvas> in the Ops tab')

    if re.search(r'<canvas[^>]+id\s*=\s*["\'][^"\']*(?:delivery|Delivery)[^"\']*["\']',
                 ops_html, re.IGNORECASE):
        PASS(cat_ops, 'Delivery method trend chart canvas found')
    else:
        FAIL(cat_ops, 'Missing delivery method trend chart canvas',
             'Add <canvas id="deliveryMethodChart"></canvas> in the Ops tab')

    if re.search(r'class\s*=\s*["\'][^"\']*\blb-table\b[^"\']*["\']', ops_html, re.IGNORECASE):
        PASS(cat_ops, 'Table with class="lb-table" found (refund details)')
    else:
        FAIL(cat_ops, 'Missing table with class="lb-table" for refund details',
             'Add a <table class="lb-table"> for refund details in the Ops tab')

    if re.search(r'(?:case|Case)\s*(?:breakdown|Breakdown)', ops_html, re.IGNORECASE) or \
       re.search(r'caseBreakdown', ops_html):
        PASS(cat_ops, 'Case breakdown section present')
    else:
        FAIL(cat_ops, 'Missing case breakdown section',
             'Add a section referencing OPS_DATA.caseBreakdown in the Ops tab')


# ─── 4. CSS Checks ────────────────────────────────────────────────────────────

def check_css(html):
    cat = "CSS"

    css_checks = [
        (r'\.tab-nav\s*\{',                   '.tab-nav style defined'),
        (r'\.tab-btn\s*\{',                    '.tab-btn style defined'),
        (r'\.tab-btn\.active',                 '.tab-btn.active style defined'),
        (r'\.tab-btn[^}]*::after',             '.tab-btn ::after pseudo-element style defined'),
        (r'\.card\s*\{',                       '.card style defined'),
        (r'\.card-sm\s*\{',                    '.card-sm style defined'),
        (r'\.card-title\s*\{',                 '.card-title style defined'),
        (r'\.kpi-value\s*\{',                  '.kpi-value style defined'),
        (r'\.tab-panel\s*\{[^}]*display\s*:\s*none', '.tab-panel display:none defined'),
        (r'\.tab-panel\.active\s*\{[^}]*display\s*:\s*block', '.tab-panel.active display:block defined'),
        (r'\.section-rule\s*\{',               '.section-rule style defined'),
        (r'\.insight\s*\{',                    '.insight style defined'),
        (r'\.lb-table\s*\{',                   '.lb-table style defined'),
        (r'\.bar-track\s*\{',                  '.bar-track style defined'),
        (r'\.bar-fill\s*\{',                   '.bar-fill style defined'),
        (r'#F8FAFC',                           'Background color #F8FAFC present'),
        (r'#4F46E5',                           'Primary accent #4F46E5 present'),
    ]

    fix_hints = {
        '.tab-nav style defined':
            'Add .tab-nav { ... } inside a <style> block in <head>',
        '.tab-btn style defined':
            'Add .tab-btn { ... } inside a <style> block',
        '.tab-btn.active style defined':
            'Add .tab-btn.active { ... } to highlight the selected tab',
        '.tab-btn ::after pseudo-element style defined':
            'Add .tab-btn.active::after { content:""; ... } for the active indicator underline',
        '.card style defined':
            'Add .card { background: white; border-radius: ...; padding: ...; } in <style>',
        '.card-sm style defined':
            'Add .card-sm { } as a smaller card variant in <style>',
        '.card-title style defined':
            'Add .card-title { font-size: ...; font-weight: ...; } in <style>',
        '.kpi-value style defined':
            'Add .kpi-value { font-size: 2rem; font-weight: 700; } in <style>',
        '.tab-panel display:none defined':
            'Add .tab-panel { display: none; } so inactive tabs are hidden',
        '.tab-panel.active display:block defined':
            'Add .tab-panel.active { display: block; } so the active tab is shown',
        '.section-rule style defined':
            'Add .section-rule { border-top: 1px solid ...; margin: ...; } in <style>',
        '.insight style defined':
            'Add .insight { ... } for insight callout boxes in <style>',
        '.lb-table style defined':
            'Add .lb-table { width: 100%; border-collapse: collapse; ... } in <style>',
        '.bar-track style defined':
            'Add .bar-track { background: #E5E7EB; border-radius: ...; height: ...; } in <style>',
        '.bar-fill style defined':
            'Add .bar-fill { background: #4F46E5; height: 100%; border-radius: ...; } in <style>',
        'Background color #F8FAFC present':
            'Add background-color: #F8FAFC to the body or a wrapper element style',
        'Primary accent #4F46E5 present':
            'Use #4F46E5 as the primary accent color (active tab, bar fills, etc.)',
    }

    for pattern, label in css_checks:
        if re.search(pattern, html, re.DOTALL):
            PASS(cat, label)
        else:
            FAIL(cat, label, fix_hints.get(label, ""))


# ─── 5. JavaScript Checks ─────────────────────────────────────────────────────

def check_javascript(html):
    cat = "JavaScript"

    js_checks = [
        (r'DOMContentLoaded',
         'DOMContentLoaded event listener present',
         "Add document.addEventListener('DOMContentLoaded', () => { ... }) to initialize the dashboard"),

        (r'\.tab-btn',
         'Tab switching logic references .tab-btn',
         "Add a click handler: document.querySelectorAll('.tab-btn').forEach(btn => btn.addEventListener('click', ...))"),

        (r'\bfmt[Mm]\b',
         'Currency formatter function (fmtM or similar) defined',
         "Add a helper like: const fmtM = v => '$' + (v/1e6).toFixed(2) + 'M'"),

        (r'CUSTOMER_VALUE_DATA',
         'CUSTOMER_VALUE_DATA referenced in script',
         "Reference CUSTOMER_VALUE_DATA (loaded from customer_value_data.js) to populate Customer Value tab"),

        (r'CBM_INSIGHTS_DATA',
         'CBM_INSIGHTS_DATA referenced in script',
         "Reference CBM_INSIGHTS_DATA (loaded from cbm_insights_data.js) to populate CBM Insights tab"),

        (r'OPS_DATA',
         'OPS_DATA referenced in script',
         "Reference OPS_DATA (loaded from ops_data.js) to populate Ops tab"),

        (r'Chart\.defaults',
         'Chart.defaults configuration present',
         "Add Chart.defaults.font.family = 'Inter'; and similar global Chart.js defaults after the CDN loads"),

        (r'responsive\s*:\s*true',
         'responsive: true in chart configs',
         "Add responsive: true to the options object of each new Chart(...)"),

        (r'maintainAspectRatio\s*:\s*false',
         'maintainAspectRatio: false in chart configs',
         "Add maintainAspectRatio: false to each chart's options so it respects the container height"),

        (r'#last-updated|last-updated',
         '#last-updated element populated',
         "Add document.getElementById('last-updated').textContent = data.lastUpdated; when initializing each tab"),
    ]

    for pattern, label, fix in js_checks:
        if re.search(pattern, html):
            PASS(cat, label)
        else:
            FAIL(cat, label, fix)


# ─── 6. Accessibility Checks ──────────────────────────────────────────────────

def check_accessibility(html):
    cat = "Accessibility"

    # Images missing alt
    all_imgs = re.findall(r'<img\b[^>]*>', html, re.IGNORECASE)
    imgs_without_alt = [img for img in all_imgs
                        if not re.search(r'\balt\s*=', img, re.IGNORECASE)]
    if not all_imgs:
        PASS(cat, 'No <img> tags present (nothing to check for alt)')
    elif not imgs_without_alt:
        PASS(cat, f'All {len(all_imgs)} <img> tag(s) have alt attributes')
    else:
        WARN(cat, f'{len(imgs_without_alt)} image(s) missing alt attributes',
             'Add descriptive alt="..." to each <img> tag; use alt="" for decorative images')

    # Canvas elements have id
    canvases = re.findall(r'<canvas\b[^>]*>', html, re.IGNORECASE)
    canvases_without_id = [c for c in canvases if not re.search(r'\bid\s*=', c, re.IGNORECASE)]
    if not canvases:
        WARN(cat, 'No <canvas> elements found at all',
             'Add canvas elements for each chart (Chart.js requires a canvas target)')
    elif not canvases_without_id:
        PASS(cat, f'All {len(canvases)} <canvas> element(s) have id attributes')
    else:
        FAIL(cat, f'{len(canvases_without_id)} canvas element(s) missing id attribute',
             'Add a unique id="..." to every <canvas> so Chart.js can target them')

    # Button elements have non-empty text content
    buttons = re.findall(r'<button\b[^>]*>(.*?)</button>', html, re.IGNORECASE | re.DOTALL)
    empty_buttons = [b for b in buttons if not re.sub(r'<[^>]+>', '', b).strip()]
    if not buttons:
        WARN(cat, 'No <button> elements found',
             'Ensure tab controls are <button> elements for keyboard accessibility')
    elif not empty_buttons:
        PASS(cat, f'All {len(buttons)} <button>(s) have descriptive text content')
    else:
        WARN(cat, f'{len(empty_buttons)} button(s) appear to have no visible text content',
             'Add descriptive text inside each <button>, or use aria-label for icon-only buttons')

    # Basic color palette check — ensure dark text colors from approved set are used
    approved_text_colors = [
        '#0F172A', '#1E293B', '#475569', '#64748B', '#94A3B8',
        '#4F46E5', '#0D9488', '#D97706', '#059669', '#E11D48',
        '#047857', '#111827', '#1F2937', '#374151', '#6B7280',
        '#ffffff', '#fff', '#F8FAFC', '#E2E8F0', '#F1F5F9',
        '#EEF2FF', '#C7D2FE', '#CCFBF1', '#F0FDFA',
    ]
    inline_colors = re.findall(r'color\s*:\s*(#[0-9a-fA-F]{3,6})', html)
    suspicious = [c for c in inline_colors
                  if c.lower() not in [a.lower() for a in approved_text_colors]]
    if not suspicious:
        PASS(cat, 'All inline text colors are from the approved palette')
    else:
        unique_suspicious = list(set(suspicious))
        WARN(cat, f'Unapproved text color(s) found: {", ".join(unique_suspicious[:5])}',
             'Stick to the approved text color palette: #111827, #1F2937, #374151, #6B7280, #4F46E5')


# ─── 7. Data Wiring Checks ────────────────────────────────────────────────────

def check_data_wiring(html):
    cat = "DataWiring"

    data_file_specs = [
        ("customer_value_data.js", "CUSTOMER_VALUE_DATA",
         ["kpis", "paymentMethodMix", "monthlyVolume", "topBuyers", "supplierStats", "lastUpdated"]),
        ("cbm_insights_data.js", "CBM_INSIGHTS_DATA",
         ["kpis", "ageDistribution", "eventStageFunnel", "exceptionTrend", "refundAnalysis", "lastUpdated"]),
        ("ops_data.js", "OPS_DATA",
         ["kpis", "paymentStatus", "deliveryMethodTrend", "paymentEventTimeline",
          "caseBreakdown", "refundDetails", "checkProcessing", "lastUpdated"]),
    ]

    for filename, var_name, required_keys in data_file_specs:
        content, err = load_file(filename)
        if err:
            FAIL(cat, f'{filename}: {err}',
                 f'Create {filename} with a {var_name} = {{ ... }} object containing the required keys')
            continue

        data, err = parse_js_data(content, var_name)
        if err:
            FAIL(cat, f'{filename}: {err}',
                 f'Ensure {filename} exports exactly: var {var_name} = {{ ... }};')
            continue

        PASS(cat, f'{filename}: {var_name} parsed successfully')

        if not isinstance(data, dict):
            FAIL(cat, f'{var_name} is not a JSON object (got {type(data).__name__})',
                 f'The top-level value of {var_name} must be a plain object {{ ... }}')
            continue

        for key in required_keys:
            if key in data:
                PASS(cat, f'{var_name}.{key} key present')
            else:
                FAIL(cat, f'{var_name} missing required key: "{key}"',
                     f'Add a "{key}" property to the {var_name} object in {filename}')

    # Cross-reference: check that .paymentMethodMix etc. are referenced in HTML
    property_refs = [
        ("paymentMethodMix",   "CUSTOMER_VALUE_DATA"),
        ("monthlyVolume",      "CUSTOMER_VALUE_DATA"),
        ("topBuyers",          "CUSTOMER_VALUE_DATA"),
        ("supplierStats",      "CUSTOMER_VALUE_DATA"),
        ("ageDistribution",    "CBM_INSIGHTS_DATA"),
        ("eventStageFunnel",   "CBM_INSIGHTS_DATA"),
        ("exceptionTrend",     "CBM_INSIGHTS_DATA"),
        ("refundAnalysis",     "CBM_INSIGHTS_DATA"),
        ("paymentStatus",      "OPS_DATA"),
        ("deliveryMethodTrend","OPS_DATA"),
        ("caseBreakdown",      "OPS_DATA"),
        ("refundDetails",      "OPS_DATA"),
    ]
    for prop, source in property_refs:
        if re.search(rf'\.{re.escape(prop)}\b', html):
            PASS(cat, f'{source}.{prop} referenced in index.html')
        else:
            FAIL(cat, f'{source}.{prop} not referenced in index.html',
                 f'Use {source}.{prop} in your inline script to populate the corresponding UI section')


# ─── 8. File Size Checks ──────────────────────────────────────────────────────

def check_file_sizes():
    cat = "FileSize"

    html_size = file_size("index.html")
    if html_size == 0 and not file_exists("index.html"):
        FAIL(cat, 'index.html not found — cannot check file size',
             'Create index.html in the dashboard directory')
    elif html_size < 20 * 1024:
        FAIL(cat, f'index.html is too small ({html_size:,} bytes < 20 KB) — likely incomplete',
             'index.html should be at least 20 KB; ensure all tabs, charts, and styles are included')
    elif html_size > 2 * 1024 * 1024:
        FAIL(cat, f'index.html is too large ({html_size:,} bytes > 2 MB) — possible accidental bloat',
             'Consider moving large inline data to external JS files')
    else:
        PASS(cat, f'index.html size is {html_size:,} bytes (within 20 KB–2 MB range)')

    for filename in ("customer_value_data.js", "cbm_insights_data.js", "ops_data.js"):
        size = file_size(filename)
        if size == 0 and not file_exists(filename):
            FAIL(cat, f'{filename} not found — cannot check file size',
                 f'Create {filename} in the dashboard directory')
        elif size < 2 * 1024:
            FAIL(cat, f'{filename} is too small ({size:,} bytes < 2 KB) — likely empty or stub',
                 f'Populate {filename} with real data; it should exceed 2 KB')
        else:
            PASS(cat, f'{filename} size is {size:,} bytes (> 2 KB)')


# ─── Report Output ────────────────────────────────────────────────────────────

def print_human_report(show_fix_hints):
    print()
    print(BOLD + "╔══════════════════════════════════════════════════════╗" + RESET)
    print(BOLD + "║        Dashboard Review Gauntlet — Run Report        ║" + RESET)
    print(BOLD + "╚══════════════════════════════════════════════════════╝" + RESET)
    print()

    for r in results:
        status = r["status"]
        if status == "PASS":
            icon  = GREEN  + "[PASS] ✓" + RESET
        elif status == "FAIL":
            icon  = RED    + "[FAIL] ✗" + RESET
        else:
            icon  = YELLOW + "[WARN] ⚠" + RESET

        print(f"{icon} {r['category']}: {r['message']}")
        if show_fix_hints and r["fix_hint"] and status != "PASS":
            print(DIM + f"       → {r['fix_hint']}" + RESET)

    total   = len(results)
    passed  = sum(1 for r in results if r["status"] == "PASS")
    failed  = sum(1 for r in results if r["status"] == "FAIL")
    warned  = sum(1 for r in results if r["status"] == "WARN")
    score   = max(0.0, 100.0 - (failed * 3) - (warned * 1))

    print()
    print(DIM + "───────────────────────────────────────────────────────" + RESET)
    summary = (f"Summary: {total} checks | "
               f"{GREEN}{passed} passed{RESET} | "
               f"{RED}{failed} failed{RESET} | "
               f"{YELLOW}{warned} warning{'s' if warned != 1 else ''}{RESET}")
    print(summary)
    score_color = GREEN if failed == 0 else (YELLOW if score >= 70 else RED)
    print(f"Score: {score_color}{score:.1f}/100{RESET}")
    print(DIM + "───────────────────────────────────────────────────────" + RESET)
    print()


def print_json_report():
    total   = len(results)
    passed  = sum(1 for r in results if r["status"] == "PASS")
    failed  = sum(1 for r in results if r["status"] == "FAIL")
    warned  = sum(1 for r in results if r["status"] == "WARN")
    score   = max(0.0, 100.0 - (failed * 3) - (warned * 1))

    output = {
        "summary": {
            "total":   total,
            "passed":  passed,
            "failed":  failed,
            "warned":  warned,
            "score":   round(score, 1),
        },
        "results": results,
    }
    print(json.dumps(output, indent=2))


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Dashboard Review Gauntlet — automated layout and quality review of index.html"
    )
    parser.add_argument(
        "--fix-hints",
        action="store_true",
        help="Print specific fix suggestions for each failure/warning",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output results as JSON instead of human-readable text",
    )
    args = parser.parse_args()

    # Load index.html
    html, html_err = load_file("index.html")
    if html_err:
        if not args.json_output:
            print(RED + f"\n[FATAL] {html_err}" + RESET)
            print(RED + "Cannot continue — index.html is required for most checks.\n" + RESET)
        FAIL("FileLoad", f"index.html could not be loaded: {html_err}",
             "Create index.html in the same directory as review_gauntlet.py")
        # Still run file-size checks (they handle missing file gracefully)
        check_file_sizes()
        if args.json_output:
            print_json_report()
        else:
            print_human_report(args.fix_hints)
        sys.exit(1)

    # Run all check categories
    check_structure(html)
    check_cdn(html)
    check_tab_content(html)
    check_css(html)
    check_javascript(html)
    check_accessibility(html)
    check_data_wiring(html)
    check_file_sizes()

    # Output
    if args.json_output:
        print_json_report()
    else:
        print_human_report(args.fix_hints)

    # Exit code
    has_failures = any(r["status"] == "FAIL" for r in results)
    sys.exit(1 if has_failures else 0)


if __name__ == "__main__":
    main()
