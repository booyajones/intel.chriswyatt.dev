with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the bubbleData section
old_bubble = """      const bubbleData = data.paymentMethodMix.filter(m => m.count > 0).map(m => {
        return {
          x: m.count,
          y: m.amount,
          r: Math.max(8, Math.min(50, Math.sqrt(m.count) / 15)), // Scaled radius
          method: m.method,
          rawAvg: m.amount / m.count
        };
      });"""

new_bubble = """      // Bubble Chart: Virtual Card Propensity 2x2
      const propensity = data.supplierPropensity || [];
      const bubbleData = propensity.map(p => {
        return {
          x: p.frequency,
          y: p.avg_size,
          r: Math.max(5, Math.min(30, Math.sqrt(p.total_volume) / 500)), // Bubble size = total volume
          method: p.method,
          supplier: p.supplier_name,
          total_volume: p.total_volume
        };
      });"""

html = html.replace(old_bubble, new_bubble)

# Replace the Chart configuration for the bubble chart
old_bubble_cfg = """        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: { 
              type: 'logarithmic',
              title: { display: true, text: 'Log Frequency (Count)', color: colors.slate },
              grid: { color: colors.slateBorder, drawTicks: false }
            },
            y: { 
              type: 'logarithmic',
              title: { display: true, text: 'Log Total Volume ($)', color: colors.slate },
              grid: { color: colors.slateBorder, drawTicks: false },
              ticks: { callback: val => formatCurrency(val) }
            }
          },
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: function(ctx) {
                  const d = ctx.raw;
                  return [
                    `${d.method}`,
                    `Volume: ${formatCurrency(d.y)}`,
                    `Freq: ${formatNumber(d.x)}`,
                    `Avg Size: ${formatCurrency(d.rawAvg)}`
                  ];
                }
              }
            }
          }
        }"""

new_bubble_cfg = """        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: { 
              type: 'logarithmic',
              title: { display: true, text: 'Payment Frequency (Count)', color: colors.slate },
              grid: { color: colors.slateBorder, drawTicks: false },
              ticks: { callback: val => formatNumber(val) }
            },
            y: { 
              type: 'logarithmic',
              title: { display: true, text: 'Avg Transaction Size ($)', color: colors.slate },
              grid: { color: colors.slateBorder, drawTicks: false },
              ticks: { callback: val => formatCurrency(val) }
            }
          },
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: function(ctx) {
                  const d = ctx.raw;
                  return [
                    `Supplier: ${d.supplier}`,
                    `Method: ${d.method}`,
                    `Total Vol: ${formatCurrency(d.total_volume)}`,
                    `Avg Size: ${formatCurrency(d.y)}`,
                    `Freq: ${formatNumber(d.x)}`
                  ];
                }
              }
            }
          }
        }"""

html = html.replace(old_bubble_cfg, new_bubble_cfg)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html")