import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Header
html = html.replace('Macro Payment Flow', 'Virtual Card Propensity (Monetization Matrix)')
html = html.replace('Operations</span>', 'Customer Value</span>')

# Update "So What?" section
html = html.replace(
    'Physical checks are driving 72% of all payment friction.',
    'High-Frequency, High-Value ACH/Check suppliers present immediate monetization ROI.'
)

html = html.replace(
    'While Virtual Cards represent the largest volume share ($820M), <strong class="text-white font-semibold">Check-By-Mail ($450M) accounts for the vast majority of exceptions and SLA breaches.</strong>',
    'The upper-right quadrant contains suppliers receiving over $5M in combined annual volume via zero-margin legacy rails (Check/ACH) with high transaction frequency.'
)

html = html.replace(
    'The float drag on checks currently averages 12.4 days from issue to clear, locking up approximately <strong class="text-white font-semibold">$15M in unoptimized capital</strong> daily.',
    "Converting just the top 10 'Whale' suppliers in this cluster to Virtual Card (assuming standard 1.5% rebate) yields approximately <strong class=\"text-white font-semibold\">$425k in net new annual revenue</strong>."
)

html = html.replace(
    'Target the top 200 suppliers currently receiving Checks > $50k for an immediate Virtual Card enablement sprint.',
    'Launch targeted Tier 1 enablement campaigns at the upper-right quadrant. Prioritize Check-receivers over ACH for dual operational & revenue wins.'
)

html = html.replace(
    'Capital Routing Architecture',
    'Monetization Propensity (Frequency vs Avg Size)'
)

# Replace the Chart.js mock with real data logic
# First, insert the data file in head
if '<script src="customer_value_data.js"></script>' not in html:
    html = html.replace('</head>', '  <script src="customer_value_data.js"></script>\n</head>')

# Now replace the entire JS block
js_old_start = "// Initialize a sophisticated looking chart"
js_old = html[html.find(js_old_start):html.find("</body>")]

js_new = """// Load Data from customer_value_data.js
    const ctx = document.getElementById('mainChart').getContext('2d');
    
    // Finexio PE Palette
    const colors = {
      vcard: '#00D382', // Emerald
      ach: '#002B49',   // Navy
      check: '#94A3B8', // Slate
      wire: '#F59E0B'   // Gold
    };

    // Prepare Bubble Data
    const rawData = typeof CUSTOMER_VALUE_DATA !== 'undefined' ? (CUSTOMER_VALUE_DATA.supplierPropensity || []) : [];
    
    const achData = [];
    const checkData = [];
    
    // Process top 100 for visual clarity
    rawData.slice(0, 100).forEach(d => {
      const bubble = {
        x: d.frequency,
        y: d.avg_size,
        r: Math.max(5, Math.min(30, Math.sqrt(d.total_volume) / 500)), // Volume scales radius
        supplier_name: d.supplier_name,
        total_volume: d.total_volume,
        method: d.method
      };
      if (d.method === 'ACH') achData.push(bubble);
      if (d.method === 'Check') checkData.push(bubble);
    });

    new Chart(ctx, {
      type: 'bubble',
      data: {
        datasets: [
          {
            label: 'ACH Suppliers',
            data: achData,
            backgroundColor: 'rgba(0, 43, 73, 0.7)', // Navy
            borderColor: colors.ach,
            borderWidth: 1
          },
          {
            label: 'Check Suppliers',
            data: checkData,
            backgroundColor: 'rgba(148, 163, 184, 0.7)', // Slate
            borderColor: colors.check,
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { usePointStyle: true, boxWidth: 8, font: { family: 'Inter', weight: '500' } } },
          tooltip: {
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            titleColor: '#002B49',
            bodyColor: '#334155',
            borderColor: '#E2E8F0',
            borderWidth: 1,
            padding: 12,
            boxPadding: 6,
            titleFont: { family: 'Inter', size: 14, weight: 'bold' },
            bodyFont: { family: 'Inter', size: 13 },
            callbacks: {
              title: function(context) {
                return context[0].raw.supplier_name;
              },
              label: function(context) {
                const d = context.raw;
                return [
                  `Method: ${d.method}`,
                  `Total Volume: $${(d.total_volume / 1000000).toFixed(2)}M`,
                  `Avg Size: $${d.y.toLocaleString(undefined, {maximumFractionDigits:0})}`,
                  `Frequency: ${d.x}`
                ];
              }
            }
          }
        },
        scales: {
          x: { 
            type: 'logarithmic',
            title: { display: true, text: 'Transaction Frequency (Log)', font: { family: 'Inter', weight: '600' } },
            grid: { color: '#F1F5F9', drawTicks: false }
          },
          y: { 
            type: 'logarithmic',
            title: { display: true, text: 'Average Transaction Size (Log)', font: { family: 'Inter', weight: '600' } },
            grid: { color: '#F1F5F9', drawTicks: false },
            ticks: { callback: function(value) { return '$' + value; } }
          }
        }
      }
    });
  </script>
"""

html = html.replace(js_old, js_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
