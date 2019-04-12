#!/bin/python

# 
# mail-attachments-archiver
# Author: Enrico Cambiaso
# Email: enrico.cambiaso[at]gmail.com
# GitHub project URL: https://github.com/auino/mail-attachments-archiver
# 

# libraries import
import email, email.header, getpass, imaplib, os, time, re

# --- --- --- --- ---
# CONFIGURATION BEGIN
# --- --- --- --- ---

# IMAP server connection configuration
USER = 'your-mail-username'
PWD = 'your-secret-password'
IMAPSERVER = 'imap.gmail.com'

# allowed senders list (may be configured separately for each directory)
YOUR_MAIL = 'you@yourprovider.com'
ALICE_MAIL = 'alice@herprovider.com'
BOB_MAIL = 'bob@hisprovider.com'

# storage/archive capabilities configuration
MAIL_MAPPINGS = [
	{ 'filter_sender': True, 'senders': [ YOUR_MAIL ], 'add_date': True, 'subject': [ 'TODO', 'TO-DO' ], 'destination': '/media/disk/todo/' },
	{ 'filter_sender': True, 'senders': [ ALICE_MAIL ], 'add_date': True, 'subject': [ 'BACKUP' ], 'destination': '/media/disk/backup_alice/' },
	{ 'filter_sender': True, 'senders': [ BOB_MAIL ], 'add_date': True, 'subject': [ 'BACKUP' ], 'destination': '/media/disk/backup_bob/' },
	{ 'filter_sender': True, 'senders': [ YOUR_MAIL, ALICE_MAIL, BOB_MAIL ], 'add_date': False, 'subject': [ 'DATA' ], 'destination': '/media/disk/data/' },
]

# only consider unread emails?
FILTER_UNREAD_EMAILS = True

# mark emails as read after their attachments have been archived?
MARK_AS_READ = False

# delete emails after their attachments have been archived?
DELETE_EMAIL = True

# if no attachment is found, mark email as read?
MARK_AS_READ_NOATTACHMENTS = False

# if no attachment is found, delete email?
DELETE_EMAIL_NOATTACHMENTS = True

# if no match is found (on MAIL_MAPPINGS), mark email as read?
MARK_AS_READ_NOMATCH = True

# if no match is found (on MAIL_MAPPINGS), delete email?
DELETE_EMAIL_NOMATCH = False

# --- --- --- --- ---
#  CONFIGURATION END
# --- --- --- --- ---

# source: https://stackoverflow.com/questions/12903893/python-imap-utf-8q-in-subject-string
def decode_mime_words(s): return u''.join(word.decode(encoding or 'utf8') if isinstance(word, bytes) else word for word, encoding in email.header.decode_header(s))

# connecting to the IMAP serer
m = imaplib.IMAP4_SSL(IMAPSERVER)
m.login(USER, PWD)
# use m.list() to get all the mailboxes
m.select("INBOX") # here you a can choose a mail box like INBOX instead

# you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
searchstring = 'ALL'
if FILTER_UNREAD_EMAILS: searchstring = 'UNSEEN'
resp, items = m.search(None, searchstring)
items = items[0].split() # getting the mails id
for emailid in items:
	# fetching the mail, "(RFC822)" means "get the whole stuff", but you can ask for headers only, etc
	resp, data = m.fetch(emailid, "(RFC822)")
	# getting the mail content
	email_body = data[0][1]
	# parsing the mail content to get a mail object
	mail = email.message_from_string(email_body)
	# check if any attachments at all
	if mail.get_content_maintype() != 'multipart':
		# marking as read and delete, if necessary
		if MARK_AS_READ_NOATTACHMENTS: m.store(emailid.replace(' ',','),'+FLAGS','\Seen')
		if DELETE_EMAIL_NOATTACHMENTS: m.store(emailid.replace(' ',','),'+FLAGS','\\Deleted')
		continue
	# checking sender
	sender = mail['from'].split()[-1]
	senderaddress = re.sub(r'[<>]','', sender)
	print "<"+str(mail['date'])+"> "+"["+str(mail['from'])+"] :"+str(mail['subject'])
	# check if subject is allowed
	subject = mail['subject']
	outputrule = None
	for el in MAIL_MAPPINGS:
		if el['filter_sender'] and (not (senderaddress.lower() in el['senders'])): continue
		for sj in el['subject']:
			if str(sj).lower() in subject.lower(): outputrule = el
	if outputrule == None: # no match is found
		# marking as read and delete, if necessary
		if MARK_AS_READ_NOMATCH: m.store(emailid.replace(' ',','),'+FLAGS','\Seen')
		if DELETE_EMAIL_NOMATCH: m.store(emailid.replace(' ',','),'+FLAGS','\\Deleted')
		continue
	outputdir = outputrule['destination']
	# we use walk to create a generator so we can iterate on the parts and forget about the recursive headach
	for part in mail.walk():
		# multipart are just containers, so we skip them
		if part.get_content_maintype() == 'multipart':
			# marking as read and delete, if necessary
			if MARK_AS_READ: m.store(emailid.replace(' ',','),'+FLAGS','\Seen')
			if DELETE_EMAIL: m.store(emailid.replace(' ',','),'+FLAGS','\\Deleted')
			continue
		# is this part an attachment?
		if part.get('Content-Disposition') is None:
			# marking as read and delete, if necessary
			if MARK_AS_READ: m.store(emailid.replace(' ',','),'+FLAGS','\Seen')
			if DELETE_EMAIL: m.store(emailid.replace(' ',','),'+FLAGS','\\Deleted')
			continue
		filename = part.get_filename()
		counter = 1
		# if there is no filename, we create one with a counter to avoid duplicates
		if not filename:
			filename = 'part-%03d%s' % (counter, 'bin')
			counter += 1
		# getting mail date
		if outputrule['add_date']:
			d = mail['Date']
			ss = [ ' +', ' -' ]
			for s in ss:
				if s in d: d = d.split(s)[0]
			maildate = time.strftime('%Y%m%d', time.strptime(d, '%a, %d %b %Y %H:%M:%S'))
			filename = maildate+'_'+filename
		filename = decode_mime_words(u''+filename)
		att_path = os.path.join(outputdir, filename)
		# check if output directory exists
		if not os.path.isdir(outputdir): os.makedirs(outputdir)
		# check if its already there
		if not os.path.isfile(att_path):
			print 'Saving to', str(att_path)
			# finally write the stuff
			fp = open(att_path, 'wb')
			fp.write(part.get_payload(decode=True))
			fp.close()
			# marking as read and delete, if necessary
			if MARK_AS_READ: m.store(emailid.replace(' ',','),'+FLAGS','\Seen')
			if DELETE_EMAIL: m.store(emailid.replace(' ',','),'+FLAGS','\\Deleted')
# Expunge the items marked as deleted... (Otherwise it will never be actually deleted)
m.expunge()
# logout
m.logout()
