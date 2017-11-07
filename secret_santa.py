from os import listdir
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import pprint
import random
import smtplib

username = "me@example.com"
password = "password"
from_email = 'SecretSanta@example.com'

smtp = smtplib.SMTP()
smtp.connect('mail.google.com')
smtp.login(username, password)

random.seed(a=12, version=2)

def send_email(draw):
    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Secret Santa Draw'
    msgRoot['From'] = from_email
    msgRoot['To'] = draw["to_email"]

    create_email(msgRoot, draw["to_name"], draw["gift_big"], draw["gift_small"])

    smtp.sendmail(from_email, draw["to_email"], msgRoot.as_string())

def create_email(msgRoot, giver_name, recipient_name_big, recipient_name_small):
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)

    text = open('templ/index.html')

    text = text.read()
    text = text.replace("{{giver_name}}", giver_name)
    text = text.replace("{{recipient_name_big}}", recipient_name_big)
    text = text.replace("{{recipient_name_small}}", recipient_name_small)



    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText(text, 'html')
    msgAlternative.attach(msgText)

    # This example assumes the image is in the current directory
    for image in listdir("templ/images"):
        filename = "templ/images/" + image
        cidname = '<' + image + '>'
        fp = open(filename, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', cidname)
        msgRoot.attach(msgImage)
    

def shuffle_list(some_list, other_match=None):
    randomized_list = some_list[:]
    if other_match is None:
        other_match = [-1]*len(some_list)

    while True:
        random.shuffle(randomized_list)
        for a, b, c in zip(some_list, randomized_list, other_match):
            if a == b or b == c:
                break
        else:
            return randomized_list

def generate_draw(participants):
    n = len(participants)
    big = set(range(n))
    small = set(range(n))
    
    big = shuffle_list(list(range(n)))
    small = shuffle_list(list(range(n)), big)

    draw = []

    for i in range(n):
        # print(participants[i][0])
        # print("\tBig: ", participants[big[i]][0])
        # print("\tSmall: ", participants[small[i]][0])
        draw.append({
            "to_email": participants[i][1],
            "to_name": participants[i][0],
            "gift_big": participants[big[i]][0],
            "gift_small": participants[small[i]][0],
        })

    return draw

participants = [
    ("Person 1", "person1@example.com"),
    ("Person 2", "person2@example.com"),
]

draw = generate_draw(participants)

for tdraw in draw:
    send_email(tdraw)

smtp.quit()