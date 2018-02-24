from hexagonal import app


@app.template_filter('ordinal')
def ordinal(n):
    return "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n if n < 20 else n % 10, "th"))


@app.template_filter('ids')
def ids(l):
    return list(map(lambda x: x.id, l))
