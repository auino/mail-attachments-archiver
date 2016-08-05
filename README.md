# mail-attachments-archiver
Store mail attachments to file-system

### Description ###

This program is a simple mail client written in Python.
It allows you to automatically archive email attachments in function of predefined rules.

### Installation ###

Clone the repository:

```
git clone https://github.com/auino/mail-attachments-archiver.git
```

### Configuration ###

Edit the `mail-attachments-archiver.py` file content by configuring the program and customizing its behavior.

#### IMAP connection setup ####

Following variables are used and should be configured:
 * `USER`: adopted IMAP username (e.g. `username@gmail.com`)
 * `PWD`: adopted IMAP password
 * `IMAPSERVER` adopted IMAP server (e.g. `imap.gmail.com`)

#### Behavior configuration ####

The behavior of the program is configured by associating specific senders to specific subjects keywords.
When the program finds an email matching the couple (sender, subject), the attachment is stored on the disk.
It is possible to set up a list of senders associated to a list of subjects.
Both the checks are case insensitive.
Concerning subject check, if the specified subject is found inside of the entire object (not equality comparison), the attachment is store, otherwise not.

You can configure a separated list of senders (as in `mail-attachments-archiver.py`, for `YOUR_MAIL`, `ALICE_MAIL` and `BOB_MAIL` parameters, for reuse them), but it is not strictly necessary.

The most important part of the behavior settings is relative to the `MAIL_MAPPINGS` variable content.
Such variable contains a list of rules objects, defined for instance as follows:

```
	{
		'senders': [ 'me@gmail.com', 'you@gmail.com' ],
		'add_date': True,
		'subject': [ 'GITHUB TEST', 'GITHUB-TEST', 'GITHUBTEST' ],
		'destination': '/media/disk/test/'
	}
```

The following attributes are needed:
 * `senders`
 * `add_date`
 * `subject`
 * `destination`

TODO

#### Additional settings ####

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

### Notes ###

This program is an extended and customized version of a [code snipped found on Stack Overflow](http://stackoverflow.com/questions/10182499/how-do-i-download-only-unread-attachments-from-a-specific-gmail-label).

### Contacts ###

You can find me on Twitter as [@auino](https://twitter.com/auino).
