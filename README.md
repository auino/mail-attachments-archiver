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

#### Behavior configuration ####

The behavior of the program is configured by associating specific senders to specific subjects keywords.
When the program finds an email matching the couple (sender, subject), the attachment is stored on the disk.
It is possible to set up a list of senders associated to a list of subjects.

You can configure a separated list of senders (as in `mail-attachments-archiver.py`, for `YOUR_MAIL`, `ALICE_MAIL` and `BOB_MAIL` parameters, for reuse them), but it is not strictly necessary.

The most important part of the behavior settings is relative to the `MAIL_MAPPINGS` variable content.
Such variable contains a list of rules objects, defined for instance as follows:

```
{
	'filter_sender': True,
	'senders': [ 'me@gmail.com', 'you@gmail.com' ],
	'add_date': True,
	'subject': [ 'GITHUB TEST', 'GITHUB-TEST', 'GITHUBTEST' ],
	'destination': '/media/disk/test/'
}
```

The following attributes are needed:
 * `filter_sender`, specifying if the filter on sender's email address is active/considered or not
 * `senders`, specifying the list of allowed source addresses
 * `add_date`, specifying if the email date (in `YYYYMMDD` format) should be appended to the begin of the filename or not (if enabled, output format is in `20160731_filename.txt` format)
 * `subject`, specifying the subject filter
 * `destination`, specifying the destination directory of attached files

Source address and subject checks are both case insensitive.
Concerning subject check, if the specified subject is found inside of the entire object (not equality comparison), the attachment is store, otherwise not.

#### Additional settings ####

Additional settings may be configured in order to define emails management.
 * `FILTER_UNREAD_EMAILS` specifies if the program should only consider unread emails
 * `MARK_AS_READ` specifies if the program should mark an email as read after its attachments are stored/archived
 * `DELETE_EMAIL` specifies if the program should delete an email as read after its attachments are stored/archived
 * `MARK_AS_READ_NOATTACHMENTS` specifies if the program should mark as read emails without attachments
 * `DELETE_EMAIL_NOATTACHMENTS` specifies if the program should delete emails without attachments
 * `MARK_AS_READ_NOMATCH` specifies if the program should mark as read emails not matching the configured rules
 * `DELETE_EMAIL_NOMATCH` specifies if the program should delete emails not matching the configured rules

### Notes ###

This program is an extended and customized version of a [code snipped found on Stack Overflow](http://stackoverflow.com/questions/10182499/how-do-i-download-only-unread-attachments-from-a-specific-gmail-label).

### Supporters ###

* [sebastianberm](https://github.com/sebastianberm)
* [DeltaLima](https://github.com/DeltaLima)

### Contacts ###

You can find me on Twitter as [@auino](https://twitter.com/auino).
