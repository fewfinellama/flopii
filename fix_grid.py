import re

with open("templates/index.html", "r") as f:
    html = f.read()

new_grid = """  <!-- Stats Grid (4 cols on lg) -->
  <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
    <!-- Health Score -->
    <div class="bg-slate-50 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800/80 p-3.5 rounded-xl flex flex-col transition-all relative overflow-hidden group hover:border-emerald-300 dark:hover:border-emerald-700" id="health-card">
      <div class="flex items-center justify-between z-10">
        <span class="text-xs font-mono text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5" id="health-label">Agent Health</span>
        <div class="w-8 h-0.5 bg-emerald-500 rounded" id="health-sparkline"></div>
      </div>
      <span id="stat-status" class="text-xl sm:text-2xl font-bold font-mono text-emerald-600 dark:text-emerald-400 mt-1 z-10">100%</span>
    </div>

    <!-- Total Executions -->
    <div class="bg-slate-50 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800/80 p-3.5 rounded-xl flex flex-col transition-all hover:border-slate-300 dark:hover:border-slate-700">
      <span class="text-xs font-mono text-slate-500 dark:text-slate-400">Total Executions</span>
      <span id="stat-total" class="text-xl sm:text-2xl font-bold font-mono text-slate-900 dark:text-white mt-1">0</span>
    </div>

    <!-- Signed (did:key) -->
    <div class="bg-slate-50 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800/80 p-3.5 rounded-xl flex flex-col transition-all hover:border-cyan-300 dark:hover:border-cyan-700">
      <span class="text-xs font-mono text-[#00c2ff]">Signed (did:key)</span>
      <span id="stat-signed" class="text-xl sm:text-2xl font-bold font-mono text-cyan-700 dark:text-[#00c2ff] mt-1">0</span>
    </div>

    <!-- Post Velocity -->
    <div class="bg-slate-50 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800/80 p-3.5 rounded-xl flex flex-col transition-all hover:border-amber-300 dark:hover:border-amber-700">
      <span class="text-xs font-mono text-amber-600 dark:text-amber-500">Post Velocity</span>
      <span class="text-xl sm:text-2xl font-bold font-mono text-amber-700 dark:text-amber-500 mt-1 flex items-baseline gap-1">
        <span id="stat-velocity">0.0</span> <span class="text-[10px] text-slate-500 font-sans font-normal">msg/min</span>
      </span>
    </div>
  </div>"""

html = re.sub(
    r"<!-- Stats Grid \(6 cols on lg\) -->.*?</div>\n</div>",
    new_grid + "\n</div>",
    html,
    flags=re.DOTALL,
)

script_replacement = """
        document.getElementById('stat-total').innerText = data.logs ? data.logs.length : '0';
        document.getElementById('stat-signed').innerText = data.logs ? data.logs.length : '0';
        
        const isOnline = data.agent_status === 'active';
        document.getElementById('stat-status').innerText = isOnline ? '100%' : 'Paused';
        
        const healthCard = document.getElementById('health-card');
        const healthLabel = document.getElementById('health-label');
        const healthSpark = document.getElementById('health-sparkline');
        const statStatus = document.getElementById('stat-status');
        
        if (isOnline) {
            healthCard.className = 'bg-slate-50 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800/80 p-3.5 rounded-xl flex flex-col transition-all relative overflow-hidden group hover:border-emerald-300 dark:hover:border-emerald-700';
            healthLabel.className = 'text-xs font-mono text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5';
            healthSpark.className = 'w-8 h-0.5 bg-emerald-500 rounded';
            statStatus.className = 'text-xl sm:text-2xl font-bold font-mono text-emerald-600 dark:text-emerald-400 mt-1 z-10';
        } else {
            healthCard.className = 'bg-slate-50 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800/80 p-3.5 rounded-xl flex flex-col transition-all relative overflow-hidden group hover:border-rose-300 dark:hover:border-rose-700';
            healthLabel.className = 'text-xs font-mono text-rose-600 dark:text-rose-400 flex items-center gap-1.5';
            healthSpark.className = 'w-8 h-0.5 bg-rose-500 rounded';
            statStatus.className = 'text-xl sm:text-2xl font-bold font-mono text-rose-600 dark:text-rose-400 mt-1 z-10';
        }
"""

html = re.sub(
    r"document\.getElementById\('stat-total'\)\.innerText.*?z-10';",
    script_replacement,
    html,
    flags=re.DOTALL,
)

with open("templates/index.html", "w") as f:
    f.write(html)
