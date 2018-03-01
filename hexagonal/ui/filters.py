from hexagonal import app


@app.template_filter('ordinal')
def ordinal(n):
    return "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n if n < 20 else n % 10, "th"))


@app.template_filter('ids')
def ids(l):
    return list(map(lambda x: x.id, l))


HUMANIZE_MAP = {
    'book': 'book',
    'journal_article': 'journal article',
    'av_material': 'A/V material'
}


HUMANIZE_ARTICLE_MAP = {
    'book': 'a',
    'journal_article': 'a',
    'av_material': 'an'
}


@app.template_filter('humanize')
def humanize(v, with_article=False):
    if with_article:
        article = HUMANIZE_ARTICLE_MAP.get(v, '')
        if article:
            return article + ' ' + HUMANIZE_MAP.get(v, v)
        else:
            return HUMANIZE_MAP.get(v, v)
    else:
        return HUMANIZE_MAP.get(v, v)
