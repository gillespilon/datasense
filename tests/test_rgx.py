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
