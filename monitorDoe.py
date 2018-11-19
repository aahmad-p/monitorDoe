import requests
import smtplib
import hashlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

urlPrefix = 'http://www.doe.carleton.ca/Course/4th_year_projects/'
urlSuffix = '.html'

pages = {
    'objectives' : 0xea6c43eded212ee4f45d75039f435bfc,
    'selection' : 0x0cf706e93b35b30c56d906a3eca97d7b,
    'application' : 0x53db8932ac82051f73988e4335b5edb6,
    'proposal' : 0x40057eb436e2afe5ab1a25d79214dbeb,
    'funding' : 0x89aaf9d5efcadc8157f363310941e25c,
    'meetings' : 0x2552db7a33cfe7985978e027a4f1562c,
    'progress' : 0x9225f0c48010b69e81ef1c50d14e4fb5,
    'competition' : 0x0c0134d989a8fa59dd8bb7828e1425b6,
    'oral' : 0x5a10440a4f3b061822af49063a7c8082,
    'poster' : 0x4116b7d267740eb3326dd1ed7d9a82a2,
    'report' : 0xd3ca04b5a16bb92defb34f9969e3c277,
    'overview' : 0x2c6cd13e72c71d4efed9b8a42b5212ab,
    'prerequisites' : 0xcdd97b2d816009431a331877f8013b46,
    'projects' : 0x9b88d4b796a30c8cbb044e281dd30433,
    'CurrentProjectAssignments' : 0xc098aec94870724c9e64c5080b29c735,
    'health' : 0x0270836fa811d1f6b84f21342c450dad,
    'calendar' : 0xf6e271a233f9b434b7938e79b7530619,
    'skills' : 0x319fb1eb0fb68db9cfabdab4c806de88,
    'samples' : 0x3b1bd20510c50637bc90ca4cbe44fee0,
    #'ugrad',
    'faq' : 0xf266cb7cd805170b29ca9539fb7e6c57,
    #'view_submission',
    'contact' : 0x490d0f4e40e08cc5db18a13793bb7a0e,
    'index' : 0x1b09309e8429d7707df949bb4efade5f
    }

# Set email and message properties
fromaddr = 'fromaddr@gmail.com'
toaddr = 'toaddr@gmail.com'

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = 'Upd Server: DOE'
body = 'No changes'

# setup the email server,
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
    
# add my account login name and password,
server.login(fromaddr, 'passhere')

for pg, storedHash in pages.items():
    req = requests.get(urlPrefix + pg + urlSuffix)
    newHash = int( hashlib.md5(req.text.encode()).hexdigest(), 16 )

    #print('\'' + pg + '\'', ':', '0x' + hashedPg.hexdigest() + ',')
    # Send update that page changed
    if storedHash != newHash:
        body = 'S touched it!' + '\n' + 'Page: ' + pg + '\n' + ' New hash: 0x' + format(newHash, 'x')
        msg.attach(MIMEText(body, 'plain'))

        # send the email
        server.send_message(msg, fromaddr, toaddr)
msg.attach(MIMEText(body, 'plain'))
server.send_message(msg, fromaddr, toaddr)
server.quit()