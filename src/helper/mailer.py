from email.mime.text import MIMEText
from subprocess import Popen, PIPE


def send_mail(text: str, title="Error in Mood Light") -> None:
    msg = MIMEText(text)
    msg["From"] = "moodlight@ivolino.de"
    msg["To"] = "ivo@ivolino.de"
    msg["Subject"] = title
    p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)

    p.communicate(msg.as_bytes())
