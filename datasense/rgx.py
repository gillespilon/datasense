"""
Regular expressions
"""

from typing import List
import re


def rgx_email_address(
    *,
    strings: List[str]
) -> List[str]:
    """
    Extract list of unique email addresses from a list of strings.

    Parameters
    ----------
    strings : List[str]
        A list of strings which may contain email addresses.

    Returns
    -------
    matches : List[str]
        A list of strings containing the email addresses found in the input
        list.

    Examples
    --------
    Example 1
    >>> import datasense as ds
    >>> strings = [
    >>>     "first email bob.smith@somemail.com send",
    >>>     "second email bobsmith13@othermail.com received",
    >>>     "third email tom@onemail.com and fourth mail frank@twomail.com"
    >>> ]
    >>> matches = ds.rgx_email_address(strings=strings)
    >>> print(matches)
    [
        'bob.smith@somemail.com', 'bobsmith13@othermail.com',
        'tom@onemail.com', 'frank@twomail.com'
    ]

    Example 2
    # open a file containing email addresses and \n\t
    >>> with open('mailbox.txt') as f:
    >>>     data = f.read()
    >>> strings = data.split("\n")
    >>> matches = ds.rgx_email_address(strings=strings)
    >>> print(matches)
    """
    # pattern = r"[\w.-]+@[\w.-]+"
    pattern = re.compile(r"[\w.-]+@[\w.-]+")
    list_of_lists = [re.findall(pattern=pattern, string=x) for x in strings]
    list_of_emails = [x for sublist in list_of_lists for x in sublist]
    unique_emails = list(set(list_of_emails))
    matches = [email for email in unique_emails if email]
    matches.sort()
    return matches


__all__ = (
    "rgx_email_address",
)
