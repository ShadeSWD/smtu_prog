import xml.etree.ElementTree as ElT

head = '<?xml version="1.0" encoding="utf-8"?>\n'


def xml_builder(n_idn, n_date_and_time, n_text, n_sender, n_answered, n_comments):
    question = ElT.Element('Question')
    idn = ElT.SubElement(question, 'Idn')
    date_time = ElT.SubElement(question, 'Time')
    text = ElT.SubElement(question, 'Text')
    sender = ElT.SubElement(question, 'Sender')
    status = ElT.SubElement(question, 'Status')
    comments = ElT.SubElement(question, 'Comments')

    idn.text = n_idn
    date_time.text = n_date_and_time
    text.text = n_text
    sender.text = n_sender
    status.text = n_answered

    data = ElT.tostring(question, encoding='unicode')

    return data

