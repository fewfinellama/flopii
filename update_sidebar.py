import re

with open("templates/base.html", "r") as f:
    html = f.read()

# We need to replace the entire <aside> block up to </aside>
aside_start = html.find("<!-- DESKTOP LEFT SIDEBAR -->")
aside_end = html.find("</aside>") + len("</aside>")

aside_content = html[aside_start:aside_end]

# We want to keep the links but restructure the panels.
# Let's extract the links block
links_match = re.search(
    r'(<a href="/".*?</a>\s*<a href="/identity".*?</a>\s*<a href="/settings".*?</a>\s*<a href="/logs".*?</a>)',
    aside_content,
    re.DOTALL,
)
if links_match:
    links = links_match.group(1)
else:
    # Fallback to extracting everything between <div class="space-y-2..."> and </div>
    links_start = aside_content.find(
        '<div class="space-y-2 flex-1 min-h-0 overflow-y-auto pr-1 sidebar-scroll">'
    ) + len(
        '<div class="space-y-2 flex-1 min-h-0 overflow-y-auto pr-1 sidebar-scroll">'
    )
    links_end = aside_content.find("</div>", links_start)
    links = aside_content[links_start:links_end].strip()

new_aside = f"""<!-- DESKTOP LEFT SIDEBAR -->
    <aside class="hidden lg:flex w-80 flex-shrink-0 flex-col gap-4 sticky top-[75px] h-[calc(100vh-95px)] overflow-hidden">
      
      <!-- Card 1: Navigation -->
      <div class="glass-panel rounded-2xl p-4 flex-shrink-0 flex flex-col flex-1 min-h-0">
        <h2 class="text-xs font-mono uppercase font-semibold text-slate-500 dark:text-slate-400 tracking-wider flex items-center justify-between mb-4">
          AGENT NAVIGATION
        </h2>
        <div class="space-y-2 overflow-y-auto pr-1 sidebar-scroll flex-1">
          {links}
        </div>
      </div>

      <!-- Card 2: FLOP Banner -->
      <div class="glass-panel rounded-2xl p-4 flex-shrink-0 flex flex-col gap-3">
        
        <div class="rounded-xl overflow-hidden shadow-sm relative group bg-black p-4 flex items-center justify-center flex-col gap-2 border border-slate-200 dark:border-slate-800">
          <!-- Text-based FLOP logo instead of image to match the screenshot better if needed, or just use the banner -->
          <img src="/static/images/flop-banner.jpeg" alt="Flopii Agent" class="w-full h-auto object-cover rounded" />
        </div>
        
        <div class="flex items-center gap-1.5 text-[#00c2ff] font-mono font-semibold text-[13px] mt-1">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
          </svg>
          <span>FLOP Zero-Trust Verifier</span>
        </div>
        
        <p class="text-slate-600 dark:text-slate-400 text-[11px] leading-relaxed font-sans font-medium">
          Signatures are calculated with <code class="text-slate-800 dark:text-slate-200 font-mono text-[10px]">@noble/ed25519</code> directly in browser memory over <code class="text-slate-800 dark:text-slate-200 font-mono text-[10px]">room|nonce|text</code>.
        </p>

        <div class="mt-2 pt-3 border-t border-slate-200 dark:border-slate-800/80 flex items-center justify-between text-[10px] text-slate-500 font-mono">
          <span>Created by</span>
          <a href="#" class="flex items-center gap-1.5 text-slate-700 dark:text-slate-300 hover:text-cyan-600 dark:hover:text-[#00c2ff] transition-colors font-bold">
            <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"></path></svg>
            FewFineLlama
          </a>
        </div>
      </div>
    </aside>"""

new_html = html[:aside_start] + new_aside + html[aside_end:]

with open("templates/base.html", "w") as f:
    f.write(new_html)
