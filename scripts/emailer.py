#!/usr/bin/python3.8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from time import strftime
from os import uname
from constants import Constants
from json import load, dump
from time import time

def send(logger, day=1):
    '''send email based on meta.json every {day} taking in consideration logs.log
    '''
    c = Constants()
    files = c.files()
    attached, meta = files["logs.log"], files["meta.json"]
    del(files)

    parser = lambda data:"".join([chr(i) for i in data])
    name = uname()[1]

    with open(meta, "r") as f:
        j = load(f)["sender"]
        last_sent = j["last"]
        to_email = parser(j["t"])
        from_email = parser(j["f"])
        password = parser(j["p"])

    if ( (time() - last_sent) / 86400) < day:
        logger.info(f"No need to send email")
        return

    bodymsg = f"""
        Hi there,

        Here the logs from {name}.

        ***Please DO NOT reply***

        Have a good day!
    """

    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = f'Project_b - Automatic email - from {name} - {strftime("%x")}'
        body = bodymsg
        msg.attach(MIMEText(body, 'plain'))

        ## ATTACHMENT PART OF THE CODE IS HERE
        with open(attached, 'rb+') as f:
            attachment = f.read()
        part = MIMEBase('application', "octet-stream")
        part.set_payload(attachment)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= logs")
        msg.attach(part)


        with smtplib.SMTP('smtp.office365.com', 587) as server: ### put your relevant SMTP here
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(from_email, password)  ### if applicable
            server.send_message(msg)
    except Exception as e:
        logger.error(f"Cannot send email. {e}")
    else:
        with open(attached, 'w+') as f:
            f.truncate()
        with open(meta, "r+") as f:
            j = load(f)
            j["sender"]["last"] = time()
            f.seek(0)
            dump(j, f, indent=1)
        logger.info(f"logs emailed then truncated. meta.json updated")

if __name__ == "__main__":
    l = Constants().logger()
    send(logger=l)
