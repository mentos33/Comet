from urlparse import urlparse


import sqlerrors
from web import web

def scan(url):
    """scan multiple websites with multi processing"""
    print url
    vulnerables = []
    results = {}  # store scanned results

    result = __sqli(url)
    results[url] = result
    
    if result[0] == True:
        vulnerables.append((url, result[1]))
    print vulnerables
    return vulnerables



def __single_arg(param_i, queries, payload, domain):
    param_str = ""
    for param_i_add in xrange(len(queries)):
        if param_i_add == param_i:
            param_str += queries[param_i]+payload
        else:
            param_str += queries[param_i_add]
        if param_i_add<len(queries)-1:param_str += "&"
    website = domain + "?" + param_str
    return website


def __sqli(url):
    """check SQL injection vulnerability"""

    print ("scanning {}".format(url))

    domain = url.split("?")[0]  # domain with path without queries
    queries = urlparse(url).query.split("&")
    # no queries in url
    if not any(queries):
        print "" # move cursor to new line
        return False, None
    payloads = ("'", "')", "';", '"', '")', '";', '`', '`)', '`;', '\\', "%27", "%%2727", "%25%27", "%60", "%5C")
    for payload in payloads:
        # website = domain + "?" + ("&".join([param + payload for param in queries]))
        for param_i in xrange(len(queries)):
            website = __single_arg(param_i, queries, payload, domain)
            source = web.gethtml(website)
            if source:
                vulnerable, db = sqlerrors.check(source)
                if vulnerable and db != None:
                    print "" # move cursor to new line
                    std.showsign(website+" vulnerable")
                    return True, db

    print ""  # move cursor to new line
    return False, None
