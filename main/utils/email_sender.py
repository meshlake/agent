import smtplib
from email.mime.text import MIMEText
import logging

class EmailSender:
    
    def __init__(self):
        self.sender_email = '1947822757@qq.com'
        self.password = 'xeixgydmojzfbceg'
        self.smtp_server = 'smtp.qq.com'
        self.smtp_port = 587

    def send_email(self, receiver_email, subject, body):
        # 创建邮件对象
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = receiver_email

        # 连接到SMTP服务器
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            logging.info(f"Connecting to {self.smtp_server}:{self.smtp_port}...")
            # 开启TLS加密
            server.starttls()

            logging.info(f"Logging in as {self.sender_email}...")
            # 登录到发件人邮箱
            server.login(self.sender_email, self.password)  # 使用应用专用密码更为安全

            logging.info(f"Sending email to {receiver_email}...")
            # 发送邮件
            server.sendmail(self.sender_email, receiver_email, msg.as_string())