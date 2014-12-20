from pyquery import PyQuery as pq


"""A quick and dirty scraper for w3c's css properties list.

    TODO: W3c adds category prefixes to their properties,
    so the resulting output is wrong for some attributes.

    These should be stripped off:

    text-text-
    pos-
    font-font-
    nav-
    class-
    gen-

    ...and a few more one offs (see error output in parser for details!)

"""


def strip_all_prefixes(string):
    bad_prefixes = [
        'text-text-',
        'pos-',
        'font-font-',
        'nav-',
        'class-',
        'gen-',
        'tab-'
    ]
    for prefix in bad_prefixes:
        string = string.replace(prefix, '')
    return string


def normalize_w3c_link(url):
    url = strip_all_prefixes(url)
    return '-'.join(url.replace(
        '.asp', '').replace('css3_pr_', '').replace('pr_', '').split('_'))


def load_all_w3c_props(root_url, max_open=None):
    table_class = '.reference.notranslate'
    data = {}
    urls = []
    doc = pq(url=root_url)
    links = pq(doc).find(table_class).find('a')

    def _process(_, selector):
        if selector is not None:
            prop = pq(selector).find('td').eq(0).text().strip()
            if len(prop) > 0:
                return urls.append(prop)
        else:
            return ''

    for k, link in enumerate(links):
        if max_open is not None:
            if k >= max_open:
                break
        url = pq(link).attr('href')
        follow_doc = pq(url='{}/{}'.format(root_url, url))
        pq(follow_doc).find(table_class).find('tr').each(_process)
        # Normalize property from w3c's url structure
        url = normalize_w3c_link(url)
        # Push all current options
        data[url] = {'dropdown': True, 'props': urls}
        # Mutable container, empty it out for reuse
        urls = []
    return data


print load_all_w3c_props('http://www.w3schools.com/cssref/')
