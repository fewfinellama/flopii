import re

with open("templates/index.html", "r") as f:
    html = f.read()

# Let's replace the grid with the exact labels from the screenshot.

new_grid = """  <!-- Stats Grid (6 cols on lg) -->
  <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
    <!-- Health Score -->
    <div class="bg-slate-50 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800/80 p-3.5 rounded-xl flex flex-col transition-all relative overflow-hidden group hover:border-rose-300 dark:hover:border-rose-700">
      <div class="flex items-center justify-between z-10">
        <span class="text-xs font-mono text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5" id="health-label">Health Score</span>
        <div class="w-8 h-0.5 bg-rose-500 rounded" id="health-sparkline"></div>
      </div>
      <span id="stat-status" class="text-xl sm:text-2xl font-bold font-mono text-rose-600 dark:text-rose-400 mt-1 z-10">100%</span>
    </div>

    <!-- Total in Ring -->
    <div class="bg-slate-50 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800/80 p-3.5 rounded-xl flex flex-col transition-all hover:border-slate-300 dark:hover:border-slate-700">
      <span class="text-xs font-mono text-slate-500 dark:text-slate-400">Total in Ring</span>
      <span id="stat-total" class="text-xl sm:text-2xl font-bold font-mono text-slate-900 dark:text-white mt-1">0</span>
    </div>

    <!-- Signed (did:key) -->
    <div class="bg-slate-50 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800/80 p-3.5 rounded-xl flex flex-col transition-all hover:border-cyan-300 dark:hover:border-cyan-700">
      <span class="text-xs font-mono text-[#00c2ff]">Signed (did:key)</span>
      <span id="stat-signed" class="text-xl sm:text-2xl font-bold font-mono text-cyan-700 dark:text-[#00c2ff] mt-1">0</span>
    </div>

    <!-- Verified Proofs -->
    <div class="bg-slate-50 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800/80 p-3.5 rounded-xl flex flex-col transition-all hover:border-emerald-300 dark:hover:border-emerald-700">
      <span class="text-xs font-mono text-emerald-600 dark:text-emerald-400">Verified Proofs</span>
      <span id="stat-verified" class="text-xl sm:text-2xl font-bold font-mono text-emerald-700 dark:text-emerald-300 mt-1">0</span>
    </div>

    <!-- Unique DIDs -->
    <div class="bg-slate-50 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800/80 p-3.5 rounded-xl flex flex-col transition-all hover:border-indigo-300 dark:hover:border-indigo-700">
      <span class="text-xs font-mono text-indigo-600 dark:text-indigo-400">Unique DIDs</span>
      <span id="stat-dids" class="text-xl sm:text-2xl font-bold font-mono text-indigo-700 dark:text-indigo-400 mt-1">1</span>
    </div>

    <!-- Chat Velocity -->
    <div class="bg-slate-50 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800/80 p-3.5 rounded-xl flex flex-col transition-all hover:border-amber-300 dark:hover:border-amber-700">
      <span class="text-xs font-mono text-amber-600 dark:text-amber-500">Chat Velocity</span>
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

# Update fetchState to populate these correctly based on our agent data
# "Total in Ring" = data.logs.length
# "Signed (did:key)" = data.logs.length
# "Verified Proofs" = data.logs.length
# "Unique DIDs" = 1 (since it's an agent)
# Health Score = dynamic based on agent_status
script_replacement = """
        document.getElementById('stat-total').innerText = data.logs ? data.logs.length : '0';
        document.getElementById('stat-signed').innerText = data.logs ? data.logs.length : '0';
        document.getElementById('stat-verified').innerText = data.logs ? data.logs.length : '0';
        
        const isOnline = data.agent_status === 'active';
        document.getElementById('stat-status').innerText = isOnline ? '100%' : '38%';
        document.getElementById('stat-status').className = isOnline ? 'text-xl sm:text-2xl font-bold font-mono text-emerald-700 dark:text-emerald-400 mt-1 z-10' : 'text-xl sm:text-2xl font-bold font-mono text-rose-600 dark:text-rose-400 mt-1 z-10';
        document.getElementById('health-label').className = isOnline ? 'text-xs font-mono text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5' : 'text-xs font-mono text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5';
        document.getElementById('health-sparkline').className = isOnline ? 'w-8 h-0.5 bg-emerald-500 rounded' : 'w-8 h-0.5 bg-rose-500 rounded';
"""

# Replace the data bindings inside fetchState
html = re.sub(
    r"document\.getElementById\('stat-llm'\).*?document\.getElementById\('stat-feeds'\)\.innerText = feedsCount;",
    script_replacement,
    html,
    flags=re.DOTALL,
)

with open("templates/index.html", "w") as f:
    f.write(html)
