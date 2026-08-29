with open("templates/base.html", "r") as f:
    html = f.read()

# Revert body
html = html.replace(
    '<body class="h-screen overflow-hidden', '<body class="min-h-screen'
)

# Revert wrapper
html = html.replace(
    '<div class="flex-1 flex flex-col lg:flex-row max-w-6xl w-full mx-auto p-3.5 sm:p-5 lg:p-6 gap-6 lg:gap-8 justify-center overflow-hidden">',
    '<div class="flex-1 flex flex-col lg:flex-row max-w-6xl w-full mx-auto p-3.5 sm:p-5 lg:p-6 gap-6 lg:gap-8 justify-center">',
)

# Revert aside to sticky
html = html.replace(
    '<aside class="hidden lg:flex w-80 flex-shrink-0 flex-col gap-4 h-full">',
    '<aside class="hidden lg:flex w-80 flex-shrink-0 flex-col gap-4 sticky top-[85px] self-start">',
)

# Revert main container
html = html.replace(
    '<main id="feed-container" class="flex-1 flex flex-col min-w-0 w-full gap-5 lg:gap-6 pt-0 overflow-y-auto pr-2 sidebar-scroll">',
    '<main id="feed-container" class="flex-1 flex flex-col min-w-0 w-full gap-5 lg:gap-6 pt-0">',
)

with open("templates/base.html", "w") as f:
    f.write(html)
