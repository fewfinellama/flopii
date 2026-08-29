import re

with open("templates/base_flopscope.html", "r") as f:
    html = f.read()

# Replace <head> logic to include the Jinja title and our css/js
head_end = html.find("</head>")
head_start = html[:head_end]
# We'll just strip out the old styles and keep standard ones
new_head = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>Flopii Agent {% block title %}{% endblock %}</title>
  <meta name="description" content="Flopii Agent Dashboard">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- Use copied Flopscope CSS -->
  <link rel="stylesheet" href="/static/css/style.css">
  <!-- Use Flop Logo as Favicon -->
  <link rel="icon" type="image/jpeg" href="/static/images/flop_logo.jpg">
  
  <script>
        if (localStorage.theme === 'light' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: light)').matches)) {
            document.documentElement.classList.remove('dark')
        } else {
            document.documentElement.classList.add('dark')
        }

        function toggleTheme() {
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.theme = 'light';
            } else {
                document.documentElement.classList.add('dark');
                localStorage.theme = 'dark';
            }
        }
  </script>
</head>
"""

# Now find the body tag and the header. We can just keep the exact header.
body_start_idx = html.find("<body")
main_start_idx = html.find("<!-- MAIN APP WRAPPER -->")
header_html = html[body_start_idx:main_start_idx]

# Replace "FLOPSCOPE" with "FLOPII" in header_html, and "Zero-Trust Verifier" with "Agent Dashboard"
header_html = header_html.replace(
    'FLOP<span class="text-[#00c2ff]">SCOPE</span>',
    'FLOP<span class="text-[#00c2ff]">II</span>',
)
header_html = header_html.replace(
    "$FLOP is food for your AI agent &middot; Zero-Trust Verifier",
    "Autonomous Core Pipeline & Controller",
)
header_html = header_html.replace("<!-- Desktop Global Tooling Controls -->", "")
header_html = re.sub(
    r"<!-- Desktop Global Tooling Controls -->.*?</div>",
    "<!-- Controls removed -->",
    header_html,
    flags=re.DOTALL,
)
header_html = re.sub(
    r'<button id="theme-toggle-btn".*?</button>',
    r"""<button id="theme-toggle-btn" onclick="toggleTheme()" class="btn-interactive p-2 rounded-xl bg-slate-100 dark:bg-slate-900/80 hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 transition-colors shadow-sm" title="Toggle Theme">
        <svg id="theme-sun-icon" class="w-4 h-4 text-amber-400 theme-icon-rotate dark:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
        </svg>
        <svg id="theme-moon-icon" class="w-4 h-4 text-cyan-600 theme-icon-rotate hidden dark:block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
        </svg>
      </button>""",
    header_html,
    flags=re.DOTALL,
)

# Main Wrapper and Sidebar
main_wrapper_html = """
  <!-- MAIN APP WRAPPER -->
  <div class="flex-1 flex flex-col lg:flex-row max-w-[1600px] w-full mx-auto p-3.5 sm:p-5 lg:p-6 gap-5 lg:gap-6">
    <!-- DESKTOP LEFT SIDEBAR -->
    <aside class="hidden lg:flex w-80 flex-shrink-0 flex-col gap-4 sticky top-[75px] h-[calc(100vh-95px)] overflow-hidden">
      <div class="glass-panel rounded-2xl p-4 flex-shrink-0 flex flex-col h-full">
        <h2 class="text-xs font-mono uppercase font-semibold text-slate-500 dark:text-slate-400 tracking-wider flex items-center justify-between mb-4">
          NAVIGATION
        </h2>
        <div class="space-y-2 flex-1 min-h-0 overflow-y-auto pr-1 sidebar-scroll">
          
          <a href="/" class="{% if active_page == 'home' %}border-cyan-200 dark:border-cyan-800 bg-cyan-50 dark:bg-cyan-950/60 text-cyan-700 dark:text-[#00c2ff] shadow-sm{% else %}border-transparent hover:border-slate-200 dark:hover:border-slate-800/80 hover:bg-slate-50 dark:hover:bg-slate-900/60 text-slate-600 dark:text-slate-400{% endif %} flex items-center gap-3 w-full p-3 rounded-xl border transition-all cursor-pointer">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
            <div class="flex-1 min-w-0">
                <div class="font-mono text-sm font-bold truncate">Dashboard</div>
            </div>
          </a>

          <a href="/identity" class="{% if active_page == 'identity' %}border-cyan-200 dark:border-cyan-800 bg-cyan-50 dark:bg-cyan-950/60 text-cyan-700 dark:text-[#00c2ff] shadow-sm{% else %}border-transparent hover:border-slate-200 dark:hover:border-slate-800/80 hover:bg-slate-50 dark:hover:bg-slate-900/60 text-slate-600 dark:text-slate-400{% endif %} flex items-center gap-3 w-full p-3 rounded-xl border transition-all cursor-pointer">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.364 0-1.457.39-2.823 1.07-4"></path></svg>
            <div class="flex-1 min-w-0">
                <div class="font-mono text-sm font-bold truncate">Identity</div>
            </div>
          </a>

          <a href="/settings" class="{% if active_page == 'settings' %}border-cyan-200 dark:border-cyan-800 bg-cyan-50 dark:bg-cyan-950/60 text-cyan-700 dark:text-[#00c2ff] shadow-sm{% else %}border-transparent hover:border-slate-200 dark:hover:border-slate-800/80 hover:bg-slate-50 dark:hover:bg-slate-900/60 text-slate-600 dark:text-slate-400{% endif %} flex items-center gap-3 w-full p-3 rounded-xl border transition-all cursor-pointer">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path></svg>
            <div class="flex-1 min-w-0">
                <div class="font-mono text-sm font-bold truncate">Settings</div>
            </div>
          </a>

          <a href="/logs" class="{% if active_page == 'logs' %}border-cyan-200 dark:border-cyan-800 bg-cyan-50 dark:bg-cyan-950/60 text-cyan-700 dark:text-[#00c2ff] shadow-sm{% else %}border-transparent hover:border-slate-200 dark:hover:border-slate-800/80 hover:bg-slate-50 dark:hover:bg-slate-900/60 text-slate-600 dark:text-slate-400{% endif %} flex items-center gap-3 w-full p-3 rounded-xl border transition-all cursor-pointer">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"></path></svg>
            <div class="flex-1 min-w-0">
                <div class="font-mono text-sm font-bold truncate">Audit Logs</div>
            </div>
          </a>
        </div>
      </div>
    </aside>

    <!-- MAIN FEED CONTAINER -->
    <main id="feed-container" class="flex-1 flex flex-col min-w-0 max-w-full gap-5 lg:gap-6">
        {% block content %}{% endblock %}
    </main>
  </div>
"""

# Replace Mobile Bottom Navigation Bar (if it exists) and add Toast logic
mobile_nav_html = """
  <!-- Mobile Bottom Navigation Bar -->
  <div class="lg:hidden fixed bottom-0 left-0 right-0 mobile-bottom-bar z-50 flex justify-around items-center px-2">
      <a href="/" class="p-3 text-slate-500 dark:text-slate-400 hover:text-[#00c2ff] {% if active_page == 'home' %}text-[#00c2ff] dark:text-[#00c2ff]{% endif %}">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
      </a>
      <a href="/identity" class="p-3 text-slate-500 dark:text-slate-400 hover:text-[#00c2ff] {% if active_page == 'identity' %}text-[#00c2ff] dark:text-[#00c2ff]{% endif %}">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.364 0-1.457.39-2.823 1.07-4"></path></svg>
      </a>
      <a href="/settings" class="p-3 text-slate-500 dark:text-slate-400 hover:text-[#00c2ff] {% if active_page == 'settings' %}text-[#00c2ff] dark:text-[#00c2ff]{% endif %}">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path></svg>
      </a>
      <a href="/logs" class="p-3 text-slate-500 dark:text-slate-400 hover:text-[#00c2ff] {% if active_page == 'logs' %}text-[#00c2ff] dark:text-[#00c2ff]{% endif %}">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"></path></svg>
      </a>
  </div>
"""

toast_html = """
    <!-- Custom Toast Alert Container -->
    <div id="toast-container" class="fixed top-20 right-6 z-50 flex flex-col gap-3 pointer-events-none"></div>

    <script>
        function showToast(message, type = 'success') {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            
            const isSuccess = type === 'success';
            const bgColor = isSuccess ? 'bg-emerald-50 dark:bg-emerald-950/40' : 'bg-rose-50 dark:bg-rose-950/40';
            const borderColor = isSuccess ? 'border-emerald-200 dark:border-emerald-800' : 'border-rose-200 dark:border-rose-800';
            const textColor = isSuccess ? 'text-emerald-700 dark:text-emerald-400' : 'text-rose-700 dark:text-rose-400';
            const icon = isSuccess 
                ? `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`
                : `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>`;

            toast.className = `flex items-center gap-3 p-4 rounded-xl border shadow-xl backdrop-blur-md pointer-events-auto transform transition-all duration-300 translate-y-[-1rem] opacity-0 ${bgColor} ${borderColor} ${textColor}`;
            toast.innerHTML = `${icon} <span class="font-mono font-medium text-sm shadow-sm">${message}</span>`;
            
            container.appendChild(toast);
            
            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    toast.classList.remove('translate-y-[-1rem]', 'opacity-0');
                    toast.classList.add('translate-y-0', 'opacity-100');
                });
            });
            
            setTimeout(() => {
                toast.classList.remove('translate-y-0', 'opacity-100');
                toast.classList.add('translate-y-[-1rem]', 'opacity-0');
                setTimeout(() => toast.remove(), 300);
            }, 3000);
        }
        
        window.alert = function(message) {
            const msg = String(message).toLowerCase();
            if (msg.includes('error') || msg.includes('fail') || msg.includes('incorrect') || msg.includes('invalid')) {
                showToast(message, 'error');
            } else {
                showToast(message, 'success');
            }
        };
    </script>

    <!-- Scripts Block -->
    {% block scripts %}{% endblock %}
</body>
</html>
"""

final_html = new_head + header_html + main_wrapper_html + mobile_nav_html + toast_html

# Swap out the F logo div with the new logo img in header_html
final_html = final_html.replace(
    """<div class="w-10 h-10 sm:w-12 sm:h-12 bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 rounded-xl flex items-center justify-center text-xl sm:text-2xl font-black text-cyan-600 dark:text-[#00c2ff] shadow-sm group-hover:scale-105 group-hover:border-cyan-300 dark:group-hover:border-[#00c2ff] transition-all">
          F
        </div>""",
    """<img src="/static/images/flop_logo.jpg" alt="Flopii Logo" class="w-10 h-10 sm:w-12 sm:h-12 border-2 border-slate-200 dark:border-slate-800 rounded-xl object-cover shadow-sm group-hover:scale-105 group-hover:border-cyan-300 dark:group-hover:border-[#00c2ff] transition-all">""",
)

with open("templates/base.html", "w") as f:
    f.write(final_html)
