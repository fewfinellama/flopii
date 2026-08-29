import re

with open("templates/base.html", "r") as f:
    html = f.read()

# Make sure feed container is centered and constrained
html = html.replace(
    '<main id="feed-container" class="flex-1 flex flex-col min-w-0 max-w-full gap-5 lg:gap-6">',
    '<main id="feed-container" class="flex-1 flex flex-col min-w-0 max-w-3xl mx-auto w-full gap-5 lg:gap-6 pt-4">',
)

banner_html = """
      <!-- FLOP Banner & Info -->
      <div class="glass-panel rounded-2xl p-4 flex flex-col gap-3 mt-4">
        <div class="rounded-xl overflow-hidden border border-slate-200 dark:border-slate-700/60 shadow-sm relative group">
          <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent z-10 pointer-events-none"></div>
          <img src="/static/images/flop-banner.jpeg" alt="Flopii Agent" class="w-full h-auto object-cover" />
        </div>
        <div class="flex items-center gap-1.5 text-[#00c2ff] font-mono font-semibold text-xs">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
          </svg>
          <span>Flopii Autonomous Core</span>
        </div>
        <p class="text-slate-600 dark:text-slate-400 text-xs leading-relaxed">
          Continuously filtering signals and executing workflows on the <code class="text-cyan-700 dark:text-[#00c2ff] font-mono">Technocore</code> protocol.
        </p>
      </div>
"""

# Insert banner_html right before the end of the aside tag
html = re.sub(r"(</aside>)", banner_html + r"\1", html)

with open("templates/base.html", "w") as f:
    f.write(html)
