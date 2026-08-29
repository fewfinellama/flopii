import re

with open("templates/index.html", "r") as f:
    html = f.read()

new_js = """
    async function fetchState() {
        const res = await fetch('/api/state');
        const data = await res.json();
        
        document.getElementById('main-target-room').innerText = data.target_room || '/r/flopii';
        
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
        
        if (data.did) {
            document.getElementById('msg-did').innerText = data.did.substring(0, 16) + '...';
        }
        
        if (data.latest_payload) {
            document.getElementById('msg-content').innerText = data.latest_payload;
        }
        
        if (data.logs && data.logs.length > 0) {
            document.getElementById('msg-time').innerText = data.logs[0].timestamp;
            const v = (data.logs.length / 60).toFixed(2);
            document.getElementById('stat-velocity').innerText = v;
        }
    }
"""

html = re.sub(
    r"async function fetchState\(\) \{.*?(?=async function forceRun)",
    new_js,
    html,
    flags=re.DOTALL,
)

with open("templates/index.html", "w") as f:
    f.write(html)
