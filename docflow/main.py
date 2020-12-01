from flask import Flask, request, Response

app = Flask(__name__)


@app.route('/DocFlow/DocumentGeneration', methods=['POST'])
def document_generation():
    soup_action = request.headers.get('SOUPAction')
    if soup_action == "http://schemas.it.mts.ru/DocFlow/DocFlow/ServiceContracts/IDocumentGeneration/GenerateDocument":
        return generate_document()


@app.route('/DocFlow/DocumentManagement', methods=['POST'])
def document_management():
    soup_action = request.headers.get('SOUPAction')
    if soup_action == 'http://schemas.it.mts.ru/DocFlow/DocFlow/ServiceContracts/IDocumentManagement/GetFile':
        return get_file()
    else:
        return sign()


def get_file():
    with open('science.pdf', 'rb') as pdf:
        pdf_bytes = pdf.read()
    xml = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">' \
          f'<s:Body> <GenerateBlankDocumentResponse xmlns="http://schemas.it.mts.ru/DocFlow/DocFlow/ServiceContracts">' \
          f'<GenerateBlankDocumentResult xmlns:a="http://schemas.it.mts.ru/DocFlow/DocFlow/Entities" ' \
          f'xmlns:i="http://www.w3.org/2001/XMLSchema-instance"> <a:Code>098cb73b-8c31-4bc1-a43e-cd5da41b1e90</a:Code>' \
          f'<a:PdfBytes>{pdf_bytes}</a:PdfBytes> ' \
          f'</GenerateBlankDocumentResult> </GenerateBlankDocumentResponse> </s:Body></s:Envelope>'
    return Response(xml, mimetype='text/xml')


def sign():
    xml = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">' \
          '<s:Body><SignResponse xmlns="http://schemas.it.mts.ru/DocFlow/DocFlow/ServiceContracts"/>' \
          '</s:Body></s:Envelope>'
    return Response(xml, mimetype='text/xml')


def generate_document():
    with open('science.pdf', 'rb') as pdf:
        pdf_bytes = pdf.read()
    xml = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">' \
          f'<s:Body><GenerateBlankDocumentResponse xmlns="http://schemas.it.mts.ru/DocFlow/DocFlow/ServiceContracts">' \
          f'<GenerateBlankDocumentResult xmlns:a="http://schemas.it.mts.ru/DocFlow/DocFlow/Entities" ' \
          f'xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><a:Code>098cb73b-8c31-4bc1-a43e-cd5da41b1e90</a:Code>' \
          f'<a:PdfBytes>{pdf_bytes}</a:PdfBytes></GenerateBlankDocumentResult>' \
          f' </GenerateBlankDocumentResponse> </s:Body></s:Envelope>'
    return Response(xml, mimetype='text/xml')


if __name__ == "__main__":
    app.run()
