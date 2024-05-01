"""
Regular expressions
"""

import re


def rgx_email_address(
    *,
    strings: list[str]
) -> list[str]:
    """
    Extract list of unique email addresses from a list of strings.

    Parameters
    ----------
    strings : list[str]
        A list of strings which may contain email addresses.

    Returns
    -------
    matches : list[str]
        A list of strings containing the email addresses in the input list.

    Examples
    --------

    >>> import datasense as ds
    >>> strings = [
    ...     "first email bob.smith@somemail.com send",
    ...     "second email bobsmith13@othermail.com received",
    ...     "third email tom@onemail.com and fourth mail frank@twomail.com"
    ... ]
    >>> matches = ds.rgx_email_address(strings=strings)
    >>> matches # doctest: +NORMALIZE_WHITESPACE
    ['bob.smith@somemail.com',
     'bobsmith13@othermail.com',
     'frank@twomail.com',
     'tom@onemail.com']

     open a file containing email addresses and \n\t

    >>> with open("../tests/mailbox.txt") as f:
    ...     data = f.read()
    >>> strings = data.split("\\n")
    >>> matches = ds.rgx_email_address(strings=strings)
    """
    regex = re.compile(pattern=r"[\w.-]+@[\w.-]+")
    list_of_lists = [re.findall(pattern=regex, string=x) for x in strings]
    list_of_emails = [x for sublist in list_of_lists for x in sublist]
    unique_emails = list(set(list_of_emails))
    matches = [email for email in unique_emails if email]
    matches.sort()
    return matches


def rgx_url(
    *,
    strings: list[str]
) -> list[str]:
    """
    Extract list of unique URLs from a list of strings.

    This is a work-in-progress as I discover more URLs to test.

    Parameters
    ----------
    strings : list[str]
        A list of strings which may contain URLs.

    Returns
    -------
    matches : list[str]
        A list of strings containing URLs in the input list.

    Example
    -------

    >>> import datasense as ds
    >>> strings = [
    ...     "https://www.google.com",
    ...     "https://www.wikipedia.org/",
    ...     "http://www.wikipedia.org/",
    ...     "one https://www.wikipedia.org/ and two http://www.wikipedia.org/",
    ...     "http://localhost:631/jobs/",
    ...     "https://en.wikipedia.org/wiki/Regular_expression#History",
    ...     "www.regexbuddy.com",
    ...     "http://www.regexbuddy.com/index.html",
    ...     "http://www.regexbuddy.com/index.html?source=library",
    ...     "Download RegexBuddy at http://www.regexbuddy.com/download.html",
    ...     "http://10.2.2.1.2/ttxx/txt/gg",
    ...     "file:///home/gilles/downloads/cheat_sheet_finance.pdf"
    ... ]
    >>> matches = ds.rgx_url(strings=strings)
    >>> matches # doctest: +NORMALIZE_WHITESPACE
    ['file:///home/gilles/downloads/cheat_sheet_finance.pdf',
     'http://10.2.2.1.2/ttxx/txt/gg',
     'http://localhost:631/jobs/',
     'http://www.regexbuddy.com/download.html',
     'http://www.regexbuddy.com/index.html',
     'http://www.regexbuddy.com/index.html?source=library',
     'http://www.wikipedia.org/',
     'https://en.wikipedia.org/wiki/Regular_expression#History',
     'https://www.google.com',
     'https://www.wikipedia.org/']
    """
    regex = re.compile(
        r"""
        (?:http|ftp|file)s?:///?
        (?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?(?:\.|/|_))+
        (?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|
        localhost|
        \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|
        \[?[A-F0-9]*:[A-F0-9:]+\]?)
        (?::\d+)?
        (?:/?|[/?]\S+)$
        """,
        flags=re.IGNORECASE | re.VERBOSE
    )
    list_of_lists = [
        re.findall(pattern=regex, string=x)
        for x in strings
    ]
    list_of_urls = [x for sublist in list_of_lists for x in sublist]
    unique_urls = list(set(list_of_urls))
    matches = [url for url in unique_urls if url]
    matches.sort()
    return matches


__all__ = (
    "rgx_email_address",
    "rgx_url",
)
