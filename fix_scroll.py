with open("templates/base.html", "r") as f:
    html = f.read()

# 1. Update body to h-screen overflow-hidden
html = html.replace(
    '<body class="min-h-screen', '<body class="h-screen overflow-hidden'
)

# 2. Ensure MAIN APP WRAPPER handles the height constraint
html = html.replace(
    '<div class="flex-1 flex flex-col lg:flex-row max-w-6xl w-full mx-auto p-3.5 sm:p-5 lg:p-6 gap-6 lg:gap-8 justify-center">',
    '<div class="flex-1 flex flex-col lg:flex-row max-w-6xl w-full mx-auto p-3.5 sm:p-5 lg:p-6 gap-6 lg:gap-8 justify-center overflow-hidden">',
)

# 3. Update the sidebar to not be sticky, just a normal flex item that doesn't scroll
html = html.replace(
    '<aside class="hidden lg:flex w-80 flex-shrink-0 flex-col gap-4 sticky top-[85px] h-fit self-start">',
    '<aside class="hidden lg:flex w-80 flex-shrink-0 flex-col gap-4 h-full">',
)

# 4. Update the main feed container to be scrollable
html = html.replace(
    '<main id="feed-container" class="flex-1 flex flex-col min-w-0 w-full gap-5 lg:gap-6 pt-0">',
    '<main id="feed-container" class="flex-1 flex flex-col min-w-0 w-full gap-5 lg:gap-6 pt-0 overflow-y-auto pr-2 custom-scrollbar">',
)

with open("templates/base.html", "w") as f:
    f.write(html)
