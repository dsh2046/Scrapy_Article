import urllib, urllib2, sys, base64, re, os, subprocess
import ssl
from docx import Document

from docx.shared import Pt
from docx.shared import Inches
from docx.oxml.ns import qn


# host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=vdmNgq7rlDMKkTSiGpbdOx1X&client_secret=WrVz0qotpK9ff7SdUOScQKGHkACgREjd'
# request = urllib2.Request(host)
# request.add_header('Content-Type', 'application/json; charset=UTF-8')
# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE
# response = urllib2.urlopen(request, context=ctx)
# content = response.read()
# if (content):
#     print(content)

# access_token = '24.6aabb65176176cc3bb2e771718126de9.2592000.1501786822.282335-9844511'
# url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token='+access_token
# f=open(r'license.jpg', 'rb')
# img=base64.b64encode(f.read())
# params= {"image": img, "language_type": 'ENG'}
# params = urllib.urlencode(params)
# request = urllib2.Request(url, params)
# request.add_header('Content-Type', 'application/x-www-form-urlencoded')
# response = urllib2.urlopen(request)
# content = response.read()
# if content:
#     first_name = str(eval(content)['words_result'][3]['words']).strip()
#     last_name = str(eval(content)['words_result'][4]['words']).strip()
#     license_number = re.findall(r'\bD.*', str(eval(content)['words_result'][7]['words']))[0]
#
#     document = Document(u'permit1.docx')
#     for paragraph in document.paragraphs:
#         if 'Driver Name' in paragraph.text:
#             paragraph.runs[1].text = first_name + " " + last_name
#         if 'Drivers licence no:' in paragraph.text:
#             paragraph.runs[1].text = license_number
#
#     document.save(u'test.docx')

subprocess.call(["unoconv", "-f", "pdf", "test.docx"])
