import re

with open("templates/base.html", "r") as f:
    html = f.read()

# Replace everything from <header ...> to </header>
header_pattern = re.compile(
    r'<header class="glass-header sticky top-0 z-40 px-3.5 sm:px-6 lg:px-8 py-3 flex items-center justify-between gap-3">.*?</header>',
    re.DOTALL,
)

new_header = """<header class="glass-header sticky top-0 z-40 px-3.5 sm:px-6 lg:px-8 py-3 flex items-center justify-between gap-3">
    <!-- Brand & FLOP Logo -->
    <div class="flex items-center gap-3 min-w-0">
      <a href="/" class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl overflow-hidden shadow-lg shadow-cyan-500/25 border border-cyan-400/40 bg-black flex-shrink-0 flex items-center justify-center transition-transform duration-300 hover:scale-105">
        <img src="/static/images/flop_logo.jpg" alt="FLOP Logo" class="w-full h-full object-cover" fetchpriority="high" decoding="async" />
      </a>
      <div class="min-w-0">
        <div class="flex items-center gap-2">
          <h1 class="text-sm sm:text-base font-bold tracking-tight font-mono flex items-center gap-1.5 text-slate-900 dark:text-white truncate">
            <span>FLOP<span class="text-[#00c2ff]">II</span></span>
          </h1>
          <span class="text-[10px] sm:text-xs font-mono px-2 py-0.5 rounded-full bg-cyan-50 dark:bg-cyan-950/80 text-cyan-700 dark:text-[#00c2ff] border border-cyan-200 dark:border-cyan-800 flex-shrink-0 font-semibold">
            $FLOP
          </span>
        </div>
        <p class="text-xs text-slate-500 dark:text-slate-400 font-sans hidden sm:block truncate">Autonomous Core Pipeline & Controller</p>
      </div>
    </div>
    
    <!-- Theme Toggle Only -->
    <div class="flex items-center gap-2.5">
      <button id="theme-toggle-btn" onclick="toggleTheme()" class="btn-interactive p-2 rounded-xl bg-slate-100 dark:bg-slate-900/80 hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 transition-colors shadow-sm" title="Toggle Theme">
        <svg id="theme-sun-icon" class="w-4 h-4 text-amber-400 dark:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
        </svg>
        <svg id="theme-moon-icon" class="w-4 h-4 text-cyan-600 hidden dark:block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
        </svg>
      </button>
    </div>
  </header>"""

html = header_pattern.sub(new_header, html)
with open("templates/base.html", "w") as f:
    f.write(html)
