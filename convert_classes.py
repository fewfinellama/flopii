import glob

replacements = {
    "flop-card": "glass-panel p-5 rounded-2xl mb-6 shadow-sm",
    "flop-heading": "text-lg font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2 tracking-tight",
    "flop-label": "block text-xs font-mono uppercase font-semibold text-slate-500 dark:text-slate-400 tracking-wider mb-2",
    "flop-input": "w-full px-3 py-2 bg-slate-50 dark:bg-slate-950/80 border border-slate-200 dark:border-slate-800 rounded-xl text-sm font-mono text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-600 focus:outline-none focus:border-[#00c2ff] focus:ring-2 focus:ring-[#00c2ff]/20 transition",
    "flop-btn-primary": "btn-interactive flex items-center justify-center gap-2 px-4 py-2 bg-[#00c2ff] hover:bg-[#00b4d8] text-slate-950 font-bold rounded-xl text-xs sm:text-sm font-mono shadow-sm transition",
    "flop-btn-secondary": "btn-interactive flex items-center justify-center gap-2 px-3 py-2 bg-slate-100 dark:bg-slate-900/80 hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 rounded-xl text-xs sm:text-sm font-mono font-medium shadow-sm",
}

for file in glob.glob("templates/*.html"):
    if file == "templates/base.html":
        continue
    with open(file, "r") as f:
        content = f.read()

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(file, "w") as f:
        f.write(content)
