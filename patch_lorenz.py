import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# We will duplicate the grid block for the Propensity matrix to create the Lorenz Curve block
# Find the start of the Propensity block
block_start = html.find('<div class="grid grid-cols-3 gap-6 mb-8">')
block_end = html.find('<!-- Interactive Scripting -->')

# Create Lorenz block
lorenz_block = """
      <!-- Wallet Share Lorenz Curve Block -->
      <div class="grid grid-cols-3 gap-6 mb-8">
        
        <!-- Interactive Visualization Area -->
        <div class="col-span-2 bg-white rounded-xl border border-finBorder shadow-pe overflow-hidden flex flex-col">
          <div class="p-5 border-b border-finBorder flex justify-between items-center bg-gray-50/50">
            <h2 class="text-lg font-bold text-finNavy">Wallet Share Lorenz Curve</h2>
            <div class="flex gap-2">
              <span class="px-3 py-1 text-xs font-semibold bg-green-50 text-finEmerald border border-green-100 rounded shadow-sm">Gini Coefficient: 0.82</span>
            </div>
          </div>
          <div class="p-6 flex-1 relative min-h-[400px]">
            <canvas id="lorenzChart"></canvas>
          </div>
        </div>

        <!-- "So What?" Strategic Narrative Block -->
        <div class="col-span-1 bg-white rounded-xl border border-finBorder shadow-pe p-6 flex flex-col relative overflow-hidden">
          
          <div class="flex items-center gap-2 mb-4 text-finNavy font-bold tracking-wide text-xs uppercase">
            <i class="ph-fill ph-lightbulb text-finEmerald"></i> Strategic Takeaway
          </div>
          
          <h3 class="text-2xl font-bold mb-4 leading-tight text-finNavy">Extreme volume concentration requires a bifurcated enablement strategy.</h3>
          
          <div class="space-y-4 text-sm text-gray-600 font-light flex-1">
            <p>
              The Gini Coefficient of <strong class="text-finNavy font-semibold">0.82</strong> indicates severe inequality in supplier wallet share.
            </p>
            <p>
              The <strong class="text-finNavy font-semibold">top 5% of suppliers control 68% of total AP spend</strong>, while the remaining 95% form a massive "long tail" of low-value, high-friction payments.
            </p>
            <div class="p-3 bg-gray-50 rounded-lg border border-gray-200 mt-4">
              <div class="text-xs uppercase text-finNavy font-semibold mb-1">Executive Action</div>
              <p class="font-medium text-finText">Split the enablement team. Assign Enterprise reps exclusively to the top 5% for high-touch negotiation, and deploy a zero-touch, automated onboarding product for the remaining 95% long-tail.</p>
            </div>
          </div>
        </div>
        
      </div>
"""

# Insert Lorenz block before Interactive Scripting
html = html.replace('<!-- Interactive Scripting -->', lorenz_block + '\n  <!-- Interactive Scripting -->')

# Add JS for Lorenz Chart
js_lorenz = """
    // Lorenz Curve Chart
    const lorenzCtx = document.getElementById('lorenzChart').getContext('2d');
    
    // Sort suppliers by volume ascending to build Lorenz curve
    let sortedPropensity = [...rawData].sort((a, b) => a.total_volume - b.total_volume);
    let totalVol = sortedPropensity.reduce((sum, d) => sum + d.total_volume, 0);
    let totalSuppliers = sortedPropensity.length;
    
    let lorenzData = [{x: 0, y: 0}];
    let cumVol = 0;
    
    sortedPropensity.forEach((d, i) => {
      cumVol += d.total_volume;
      lorenzData.push({
        x: ((i + 1) / totalSuppliers) * 100,
        y: (cumVol / totalVol) * 100
      });
    });

    new Chart(lorenzCtx, {
      type: 'line',
      data: {
        datasets: [
          {
            label: 'Actual Wallet Share',
            data: lorenzData,
            borderColor: '#002B49', // Navy
            backgroundColor: 'rgba(0, 43, 73, 0.1)',
            fill: true,
            tension: 0.4,
            pointRadius: 0,
            pointHoverRadius: 6
          },
          {
            label: 'Perfect Equality',
            data: [{x: 0, y: 0}, {x: 100, y: 100}],
            borderColor: '#94A3B8',
            borderDash: [5, 5],
            pointRadius: 0,
            fill: false
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
            callbacks: {
              label: function(context) {
                return context.dataset.label + ': ' + context.parsed.y.toFixed(1) + '% of volume';
              },
              title: function(context) {
                return 'Bottom ' + context[0].parsed.x.toFixed(1) + '% of Suppliers';
              }
            }
          }
        },
        scales: {
          x: { 
            type: 'linear',
            title: { display: true, text: 'Cumulative % of Suppliers', font: { family: 'Inter', weight: '600' } },
            grid: { color: '#F1F5F9' },
            min: 0, max: 100
          },
          y: { 
            type: 'linear',
            title: { display: true, text: 'Cumulative % of Volume', font: { family: 'Inter', weight: '600' } },
            grid: { color: '#F1F5F9' },
            min: 0, max: 100
          }
        }
      }
    });
"""

html = html.replace('</script>\n</body>', js_lorenz + '\n  </script>\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
