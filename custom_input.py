try:
    import questionary
    _vprompt=1
except ImportError:
    _vprompt=0

def my_input(query):
    if _vprompt:
        return questionary.text(query).ask()
    else:
        return input(query+" ")

def my_select(query, options):
    if _vprompt:
        return questionary.select(
            query,
            choices=options
        ).ask()
    else:
        txt = f"{query} ({', '.join(options)}) "
        return input(txt)

def my_confirm(query):
    if _vprompt:
        return questionary.confirm(query, default=False, auto_enter=False).ask()
    else:
        reply = my_input(query)
        reply = reply.lower()[0]
        return reply[0] == "y"

