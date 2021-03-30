#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import os,datetime

#https://stackoverflow.com/questions/4823574/sending-meeting-invitations-with-python 
#https://stackoverflow.com/questions/57141694/why-encode-base64-give-me-typeerror-expected-bytes-like-object-not-nonetype/62255629#62255629

def send_email(attendees, chatroom_url):
  CRLF = "\r\n"
  login = "chatbot9900@gmail.com"
  password = "Chat#9900"
  # attendees = ["chatbot9900@gmail.com", "e.life.hacker@gmail.com"]
  organizer = "ORGANIZER;CN=organiser:mailto:chatbot9900"+CRLF+" @gmail.com"
  fro = "Chatbot9900 <chatbot9900@gmail.com>"

  ddtstart = datetime.datetime.now()
  dtoff = datetime.timedelta(days = 1)
  dur = datetime.timedelta(hours = 1)
  ddtstart = ddtstart +dtoff
  dtend = ddtstart + dur
  dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
  dtstart = ddtstart.strftime("%Y%m%dT%H%M%SZ")
  dtend = dtend.strftime("%Y%m%dT%H%M%SZ")

  description = "DESCRIPTION: test invitation from pyICSParser"+CRLF
  attendee = ""
  for att in attendees:
      attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+att+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
  ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
  ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
  ical+= "UID:FIXMEUID"+dtstamp+CRLF
  ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
  ical+= "SUMMARY:test "+ddtstart.strftime("%Y%m%d @ %H:%M")+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF

  eml_body = "Chatroom url: "+chatroom_url+" \nEmail body visible in the invite of outlook and outlook.com but not google calendar"
  eml_body_bin = "This is the email body in binary - two steps"
  msg = MIMEMultipart('mixed')
  msg['Reply-To']=fro
  msg['Date'] = formatdate(localtime=True)
  msg['Subject'] = "pyICSParser invite"+dtstart
  msg['From'] = fro
  msg['To'] = ",".join(attendees)

  part_email = MIMEText(eml_body,"html")
  part_cal = MIMEText(ical,'calendar;method=REQUEST')

  msgAlternative = MIMEMultipart('alternative')
  msg.attach(msgAlternative)

  ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
  ical_atch.set_payload(ical)
  encoders.encode_base64(ical_atch)
  ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

  eml_atch = MIMEText('', 'plain')
  encoders.encode_base64(eml_atch)
  eml_atch.add_header('Content-Transfer-Encoding', "")

  msgAlternative.attach(part_email)
  msgAlternative.attach(part_cal)

  mailServer = smtplib.SMTP('smtp.gmail.com', 587)
  mailServer.ehlo()
  mailServer.starttls()
  mailServer.ehlo()
  mailServer.login(login, password)
  mailServer.sendmail(fro, attendees, msg.as_string())
  mailServer.close()


# In[ ]:




