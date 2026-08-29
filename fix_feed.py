import re

with open("templates/index.html", "r") as f:
    html = f.read()

# Replace the single card HTML with a container
feed_container = """
<!-- Execution Feed Container -->
<div id="execution-feed" class="flex flex-col gap-4">
  <!-- Filled dynamically by JS -->
  <div class="glass-panel rounded-2xl p-4 sm:p-5 text-center text-sm font-mono text-slate-500">
    No executions logged yet. Click "Force Run Now" to execute the agent.
  </div>
</div>
"""
html = re.sub(
    r"<!-- Flopscope Style Message Card -->.*?</div>\s*</div>\s*</div>",
    feed_container,
    html,
    flags=re.DOTALL,
)


# Update the fetchState JS to loop over data.logs
js_update = """
        if (data.logs && data.logs.length > 0) {
            const feed = document.getElementById('execution-feed');
            feed.innerHTML = '';
            
            data.logs.forEach(log => {
                const isSuccess = log.status === 'Success';
                const badgeHtml = isSuccess 
                    ? `<div class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-mono font-semibold bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-700 shadow-sm"><svg class="w-3.5 h-3.5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg><span>Verified Proof</span></div>`
                    : `<div class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-mono font-semibold bg-rose-100 dark:bg-rose-950/80 text-rose-800 dark:text-rose-300 border border-rose-300 dark:border-rose-700 shadow-sm"><svg class="w-3.5 h-3.5 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/></svg><span>Failed</span></div>`;
                
                const card = document.createElement('div');
                card.className = "glass-panel rounded-2xl p-4 sm:p-5 gap-3 flex flex-col";
                card.innerHTML = `
                  <div class="flex items-start justify-between gap-3 flex-wrap">
                    <div class="flex items-center gap-3 min-w-0">
                      <div class="w-9 h-9 rounded-xl bg-slate-200 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 flex items-center justify-center font-mono font-bold text-slate-600 dark:text-slate-300 shadow-sm flex-shrink-0">
                        <svg class="w-5 h-5 text-cyan-600 dark:text-[#00c2ff]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                      </div>
                      <div class="min-w-0">
                        <div class="flex items-center gap-2">
                          <span class="font-mono text-xs sm:text-sm font-semibold text-cyan-600 dark:text-[#00c2ff] truncate">${data.did ? data.did.substring(0, 16) + '...' : 'Unknown DID'}</span>
                        </div>
                        <div class="flex items-center gap-2 text-[11px] font-mono text-slate-400 dark:text-slate-500 pt-0.5">
                          <span>${log.timestamp}</span>
                        </div>
                      </div>
                    </div>
                    <div class="flex items-center gap-2 flex-wrap">
                      ${badgeHtml}
                    </div>
                  </div>
                  <div class="relative group mt-2">
                    <div class="text-slate-800 dark:text-slate-200 text-sm sm:text-base leading-relaxed break-words font-sans selection:bg-cyan-500/30 whitespace-pre-wrap">${log.payload}</div>
                  </div>
                `;
                feed.appendChild(card);
            });
            
            const v = (data.logs.length / 60).toFixed(2);
            document.getElementById('stat-velocity').innerText = v;
        }
"""

html = re.sub(
    r"if \(data\.did\) \{.*?document\.getElementById\(\'stat-velocity\'\)\.innerText = v;\n\s*\}",
    js_update.strip(),
    html,
    flags=re.DOTALL,
)
html = html.replace("Latest Agent Execution", "Recent Agent Executions")

with open("templates/index.html", "w") as f:
    f.write(html)
