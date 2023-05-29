import datasense as ds


def test_rgx_email_address():
    # test for a list of strings
    strings = [
        "third email tom@onemail.com and fourth mail frank@twomail.com",
        "first email bob.smith@somemail.com send",
        "second email bobsmith13@othermail.com received",
        "third email tom@onemail.com and fourth mail frank@twomail.com",
        "second email bobsmith13@othermail.com received",
    ]
    result = ds.rgx_email_address(strings=strings)
    expected = list(set([
        'bob.smith@somemail.com', 'bobsmith13@othermail.com',
        'tom@onemail.com', 'frank@twomail.com'
    ]))
    expected.sort()
    assert result == expected
    # test for a file of strings with \n\t present
    with open('mailbox_string.txt') as f:
        data = f.read()
    strings = data.split("\n")
    result = ds.rgx_email_address(strings=strings)
    with open('mailbox_list.txt') as f:
        data = f.read()
    expected = list(set(data.split("\n")))
    expected = [i for i in expected if i]
    expected.sort()


def test_rgx_url():
    list_strings = [
        "https://www.google.com",
        "https://www.wikipedia.org/",
        "http://www.wikipedia.org/",
        "one https://www.wikipedia.org/ and two http://www.wikipedia.org/",
        "http://localhost:631/jobs/",
        "https://en.wikipedia.org/wiki/Regular_expression#History",
        "www.regexbuddy.com",
        "http://www.regexbuddy.com/index.html",
        "http://www.regexbuddy.com/index.html?source=library",
        "Download RegexBuddy at http://www.regexbuddy.com/download.html",
        "http://10.2.2.1.2/ttxx/txt/gg",
        "file:///home/gilles/downloads/cheat_sheet_finance.pdf"
    ]
    result = ds.rgx_url(strings=list_strings)
    expected = [
        'file:///home/gilles/downloads/cheat_sheet_finance.pdf',
        'http://10.2.2.1.2/ttxx/txt/gg',
        'http://localhost:631/jobs/',
        'http://www.regexbuddy.com/download.html',
        'http://www.regexbuddy.com/index.html',
        'http://www.regexbuddy.com/index.html?source=library',
        'http://www.wikipedia.org/',
        'https://en.wikipedia.org/wiki/Regular_expression#History',
        'https://www.google.com',
        'https://www.wikipedia.org/'
     ]
    assert result == expected
