import PyPDF2
import io
import requests


def report_reader(report_pdf):

    try:
        url = report_pdf
        response = requests.get(url)

        pdf_file = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        if pdf_reader.isEncrypted:
            pdf_reader.decrypt("")
            page_obj = pdf_reader.getPage(0)
            page_text = page_obj.extractText().upper()

            word_vicroad = 'VICROADS'
            word_melway = 'MELWAY'

            text_location = page_text.find(word_vicroad)

            if text_location == -1:
                text_location = page_text.find(word_melway)
                text_to_split = page_text[text_location:text_location + 30]
                text_to_split = (' '.join(text_to_split.split())).split(' ')
                if text_to_split[2][2].isdigit() is True:
                    output_text = text_to_split[0] + ' ' + text_to_split[1] + ' ' + text_to_split[2][0:3]
                    return output_text
                if text_to_split[2][2].isdigit() is False:
                    output_text = text_to_split[0] + ' ' + text_to_split[1] + ' ' + text_to_split[2][0:2]
                    return output_text

            elif text_location != -1:
                text_to_split = page_text[text_location:text_location + 32]
                text_to_split = (' '.join(text_to_split.split())).split(' ')
                if text_to_split[2][2].isdigit() is True:
                    output_text = text_to_split[0] + ' ' + text_to_split[1] + ' ' + text_to_split[2][0:3]
                    return output_text
                if text_to_split[2][2].isdigit() is False:
                    output_text = text_to_split[0] + ' ' + text_to_split[1] + ' ' + text_to_split[2][0:2]
                    return output_text

    except Exception as e:
        print("Error: Unable to detect map reference, property report may not include one.")
        # Map will fail to load if no return value is given, returns empty map ref field instead.
        return ''
        # print(e)
        pass
