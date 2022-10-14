import imaplib, getpass, re, email
import asyncio
import platform
import time
from dotenv import load_dotenv


pattern_uid = re.compile(b'\d+ \(UID (?P<uid>\d+)\)')


def parse_mailbox(data):
    flags, b, c = data.partition(' ')
    separator, b, name = c.partition(' ')
    return (flags, separator.replace('"', ''), name.replace('"', ''))

async def mail_store(imap, mail):
    imap.store(mail, "+FLAGS", "\\Deleted")
    return

async def main():
    try:

        # user credentials 
        my_email = "email@email.com.br" 
        app_generated_password = "password@2015" 

        # initialize IMAP object for Gmail
        imap = imaplib.IMAP4_SSL("imap.outlook.com")  # imap.gmail.com # imap.outlook.com  # "outlook.office365.com",993
        
        # login to gmail with credentials
        print("imap.login = ", imap.login(my_email, app_generated_password))

        # print("imap.select = ", imap.select('INBOX')) 
        # print("imap.select = ", imap.select('teste')) 
        print("imap.select = ", imap.select('"Itens Exclu&AO0-dos"'))  # '[Gmail]/Trash'  # TRASH # [Outlook]/Trash   # \\Deleted

        # #status, messages_id_list = imap.search(None, 'FROM "email.email@email.com.br"')  # email.email@email.com.br # noreply@kaggle.com
        status, messages_id_list = imap.search(None, "ALL")
        print("status = ", status)
        print("len(messages_id_list) = ", len(messages_id_list))

        messages = messages_id_list[0].split(b' ') # #convert the string ids to list of email ids
        print("len(messages) = ", len(messages))

        # print("Deleting mails")
        
        # imap.store("1:*", '+FLAGS', '\\Deleted')  #Flag all Trash as Deleted

        # [imap.store(mail, "+FLAGS", "\\Deleted") for mail in messages] 

        print("asyncio.create_task()")
        tasks = [asyncio.create_task(mail_store(imap=imap, mail=mail)) for mail in messages]
        print("len(tasks) = ", len(tasks))

        print("asyncio.gather()")
        await asyncio.gather(*tasks)

        # # tasks = []
        # count = 1
        # for mail in messages:
        #     # tasks.append(asyncio.create_task(mail_store(imap=imap, mail=mail)))
        #     imap.store(mail, "+FLAGS", "\\Deleted")  # mark the mail as deleted
        #     if  (count % 500) == 0: 
        #         print(count, "mail(s) deleted")
        #     count +=1

        # count = 1
        # for mail in messages:
        #     _, msg = imap.fetch(mail, "(RFC822)") # you can delete the for loop for performance if you have a long list of emails because it is only for printing the SUBJECT of target email to delete
        #     for response in msg:
        #         if isinstance(response, tuple):
        #             msg = email.message_from_bytes(response[1])
        #             subject = decode_header(msg["Subject"])[0][0] # decode the email subject
        #             if isinstance(subject, bytes):
        #                 subject = subject.decode() # if it's a bytes type, decode to str
        #             print(count, " Deleting", subject)
        #     imap.store(mail, "+FLAGS", "\\Deleted") # mark the mail as deleted
        #     count +=1

        # rv, data = imap.list()
        # if rv == 'OK':
        #     for mbox in data:
        #         print("mbox=", mbox)
        #         flags, separator, name = parse_mailbox(bytes.decode(mbox))
                # print("flags=", flags, "separator=", separator, "name=", name)
                # print("name=", name)
                # if 'HasNoChildren' in flags and '2' in name:
                #     name = name.replace('/ Inbox','Inbox')
                #     rv2, data2 = imap.select('"'+name+'"')
                #     print(rv2)
                #     resp, items = imap.search(None, 'All')
                #     # print(items)
                #     email_ids  = items[0].split()
                #     print(email_ids)
                #     print(len(email_ids))
                #     for i in range(0,len(email_ids)):
                #         print('NOUVEAU MESSAGE \n')
                #         print(email_ids[i])
                #         resp, data = imap.fetch(email_ids[i], "(UID)")
                #         rv,sujet = imap.fetch(email_ids[i],("(RFC822)"))
                #         varSubject= ""
            # if result[0] == 'OK':
            #     mov, data = imap.uid('STORE', msg_uid , '+FLAGS', '(\Deleted)')
            #     imap.expunge()

        print("imap.expunge()") # print("All selected mails has been deleted")
        imap.expunge() # delete all the selected messages 

        print("imap.close()")
        imap.close() # close the mailbox

        print("imap.logout()")
        imap.logout() # logout from the server

        '''

        import imaplib
import email

host = 'imap.gmail.com'
username = 'hungrypy@gmail.com'
password = '<your password>'


def get_inbox():
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select("inbox")
    _, search_data = mail.search(None, 'UNSEEN')
    my_message = []
    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
        # print(data[0])
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ['subject', 'to', 'from', 'date']:
            print("{}: {}".format(header, email_message[header]))
            email_data[header] = email_message[header]
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                email_data['body'] = body.decode()
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True)
                email_data['html_body'] = html_body.decode()
        my_message.append(email_data)
    return my_message


if __name__ == "__main__":
    my_inbox = get_inbox()
    print(my_inbox)
# print(search_data)
        
        '''

    except Exception as e:
        print("Erro: ", e)


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop(asyncio.ProactorEventLoop())
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    start = time.time()
    asyncio.run(main()) 
    print("Levou {} segundos para fazer".format(time.time() - start))


# py -3 -m venv .venv

# python -m pip install psutil

# cd c:/Users/chris/Desktop/CMS Python/CMS Teste Email
# .venv\scripts\activate
# python main.py
