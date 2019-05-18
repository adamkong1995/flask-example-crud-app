import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd

from flaskr import key


def send(to, cc, tosends):
    login = key.EMAIL_USERNAME
    password = key.EMAIL_PASSWORD
    sender_email = key.EMAIL_SENDER

    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = to
    message["Cc"] = cc

    subject = "Project Update - "

    html = """\
    <html>
        <body>
            <font face="Courier New, Courier">
                <p>
    """
    data = pd.read_json(tosends, orient="records")
    projects = data[['deal_id', 'name', 'group_name', 'country', 'dealSize', 'encounteredDate', 'strategy']].drop_duplicates()

    for index, row in projects.iterrows():
        subject = subject + '{} '.format(row['name'])
        html = html + """<b>{}</b><br>
                        Group: {}<br>
                        Country: {}<br>
                        Size: {}<br>
                        EncounteredDate: {}<br>
                        Instrument: {}<br>
                        <br>
                        Update(s):<br>
                    """.format(row['name'], row['group_name'], row['country'], row['dealSize'], row['encounteredDate'], row['strategy'])

        deal_id = row['deal_id']
        updates = data.query('deal_id == @deal_id')[['update_content']].values.tolist()

        for update in updates:
            html = html + update[0] + "<br><br>"

    html = html + """\
                </p>
            </font>
        </body>
    </html>
    """

    message["Subject"] = subject

    part1 = MIMEText(html, "html")
    message.attach(part1)

    allAddress = to + '; ' + cc

    with smtplib.SMTP(key.EMAIL_SMTP_HOST, key.EMAIL_SMTP_PORT) as server:
        server.login(login, password)
        server.sendmail(sender_email, allAddress.split(";"), message.as_string())
