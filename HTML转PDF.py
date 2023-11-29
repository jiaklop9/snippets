#!/usr/bin/env python3
# -*- coding: utf8 -*-

import pdfkit


def main():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HTML to PDF</title>
    </head>
    <body>
        <h1>Hello, PDF!</h1>
        <p>This is a simple HTML content.</p>
    </body>
    </html>
    """

    with open('input.html', 'w') as f:
        f.write(html_content)

    config = pdfkit.configuration(wkhtmltopdf=r'D:\HTMLToPdf\bin\wkhtmltopdf.exe')
    pdfkit.from_file('input.html', 'output.pdf', configuration=config)

    print("PDF conversion complete.")


if __name__ == '__main__':
    main()
