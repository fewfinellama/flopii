with open("core/agent.py", "r") as f:
    code = f.read()

# Replace actual newlines inside those f-strings with \n string literals
code = code.replace(
    'payload = f"FLOPII PULSE | {now}\n"', 'payload = f"FLOPII PULSE | {now}\\n"'
)
code = code.replace(
    "payload += f\"{p['ticker']} ${p['price']:,.2f} ({sign}{p['change_24h']:.2f}%)\n\"",
    "payload += f\"{p['ticker']} ${p['price']:,.2f} ({sign}{p['change_24h']:.2f}%)\\n\"",
)
code = code.replace(
    'payload += f"\nNEWS:\n{summary}"', 'payload += f"\\nNEWS:\\n{summary}"'
)

with open("core/agent.py", "w") as f:
    f.write(code)
