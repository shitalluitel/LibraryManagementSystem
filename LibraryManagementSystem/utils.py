import sys
import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string


def render_pdf(template_name, context, filename, options=None, attachment=False, http_response=True, path=None):
    if http_response:
        response = HttpResponse(content_type='application/pdf')
        if attachment:
            response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
        else:
            response['Content-Disposition'] = 'filename="' + filename + '"'

    # return render(None, template_name, context)
    html_string = render_to_string(template_name, context)

    if options:
        options['quiet'] = ''
        options['encoding'] = 'UTF-8'
        if sys.platform == 'darwin':
            options['zoom'] = 12.5
    else:
        options = {
            'quiet': '',
            'page-size': 'A4',
            'orientation': 'Portrait',
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            'encoding': 'UTF-8',
        }
        if sys.platform == 'darwin':
            options['zoom'] = 12.5

    if http_response:
        pdf = pdfkit.from_string(html_string, None, options=options)
        response.write(pdf)
        return response
    else:
        pdfkit.from_string(html_string, output_path=path, options=options)
