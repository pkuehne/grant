""" Test conversion functions in research.py """

from grant.research.research import convert_html


def test_html_is_stripped():
    """ Check that the html codes are stripped """
    # Given
    html = """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
    <html>
    <head>
        <meta name="qrichtext" content="1" />
        <style type="text/css">
            p, li { white-space: pre-wrap; }
        </style>
    </head>
    <body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;">
        <p>
            Describe your goals for this plan...
        </p>
    </body>
    </html>
    """

    # When
    text = convert_html(html)

    # Then
    print(f">{text}<")
    assert text == "Describe your goals for this plan..."
