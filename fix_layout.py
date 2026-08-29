import re

with open("templates/base.html", "r") as f:
    html = f.read()

# 1. Fix the Header to align with the main container
html = re.sub(
    r'<header class="glass-header sticky top-0 z-40 px-3.5 sm:px-6 lg:px-8 py-3 flex items-center justify-between gap-3">',
    r'<header class="glass-header sticky top-0 z-40 px-3.5 sm:px-6 lg:px-8 py-3 flex justify-center border-b border-slate-200 dark:border-slate-800/80 shadow-sm">\n  <div class="max-w-6xl w-full flex items-center justify-between gap-3">',
    html,
)
html = html.replace("</header>", "  </div>\n</header>")

# 2. Fix the Main App Wrapper and Feed Container
html = html.replace(
    '<div class="flex-1 flex flex-col lg:flex-row max-w-[1600px] w-full mx-auto p-3.5 sm:p-5 lg:p-6 gap-5 lg:gap-6">',
    '<div class="flex-1 flex flex-col lg:flex-row max-w-6xl w-full mx-auto p-3.5 sm:p-5 lg:p-6 gap-6 lg:gap-8 justify-center">',
)
html = html.replace(
    '<main id="feed-container" class="flex-1 flex flex-col min-w-0 max-w-3xl mx-auto w-full gap-5 lg:gap-6 pt-4">',
    '<main id="feed-container" class="flex-1 flex flex-col min-w-0 w-full gap-5 lg:gap-6 pt-0">',
)

# 3. Move the banner INTO the sidebar panel.
# We will match the end of the navigation div and insert the banner there.
banner_html = """
        <div class="mt-4 pt-4 border-t border-slate-200 dark:border-slate-800/80 flex flex-col gap-3">
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
          <p class="text-slate-600 dark:text-slate-400 text-[11px] leading-relaxed">
            Continuously filtering signals and executing workflows on the <code class="text-cyan-700 dark:text-[#00c2ff] font-mono">Technocore</code> protocol.
          </p>
        </div>
"""

# Remove the old appended banner
old_banner_pattern = re.compile(
    r"<!-- FLOP Banner & Info -->.*?</div>\s*</aside>", re.DOTALL
)
html = old_banner_pattern.sub("</aside>", html)

# Insert the new banner before the end of the glass-panel in the aside
html = html.replace(
    "      </div>\n    </aside>", banner_html + "      </div>\n    </aside>"
)

with open("templates/base.html", "w") as f:
    f.write(html)
