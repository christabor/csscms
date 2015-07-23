from pyquery import PyQuery as Pq

"""
A quick and dirty scraper for w3c's css properties list.
See css_properties.py for the example output. This is meant to be run once,
except when new properties need to be scraped.
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
    doc = Pq(url=root_url)
    links = Pq(doc).find(table_class).find('a')

    def _process(_, selector):
        if selector is not None:
            prop = Pq(selector).find('td').eq(0).text().strip()
            if len(prop) > 0:
                return urls.append(prop)
        else:
            return ''

    for k, link in enumerate(links):
        if max_open is not None:
            if k >= max_open:
                break
        url = Pq(link).attr('href')
        follow_doc = Pq(url='{}/{}'.format(root_url, url))
        Pq(follow_doc).find(table_class).find('tr').each(_process)
        # Normalize property from w3c's url structure
        url = normalize_w3c_link(url)
        # Push all current options
        data[url] = {'dropdown': True, 'props': urls}
        # Mutable container, empty it out for reuse
        urls = []
    return data


if __name__ == '__main__':
    print(load_all_w3c_props('http://www.w3schools.com/cssref/'))
