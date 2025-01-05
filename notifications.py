# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import logging
#
#
# class NotificationHandler:
#     def __init__(self, notification_type="email", email_config=None, log_file="job_scheduler.log"):
#         self.notification_type = notification_type
#         self.email_config = email_config if email_config else {}
#         self.log_file = log_file
#
#         # Setup logging if necessary
#         self.logger = logging.getLogger('JobScheduler')
#         if self.notification_type == "log":
#             logging.basicConfig(filename=log_file, level=logging.INFO,
#                                 format='%(asctime)s - %(message)s')
#
#     def send_notification(self, message, level="info"):
#         if self.notification_type == "email":
#             self.send_email_notification(message, level)
#         elif self.notification_type == "log":
#             self.log_notification(message, level)
#         elif self.notification_type == "console":
#             self.print_notification(message, level)
#
#     def send_email_notification(self, message, level="info"):
#         try:
#             # Email configuration
#             from_email = self.email_config.get("from_email")
#             to_email = self.email_config.get("to_email")
#             subject = f"Job Notification - {level}"
#
#             # Prepare the message
#             msg = MIMEMultipart()
#             msg['From'] = from_email
#             msg['To'] = to_email
#             msg['Subject'] = subject
#             msg.attach(MIMEText(message, 'plain'))
#
#             # Send the email using SMTP
#             server = smtplib.SMTP(self.email_config.get("smtp_server"))
#             server.starttls()
#             server.login(self.email_config.get("from_email"), self.email_config.get("email_password"))
#             server.sendmail(from_email, to_email, msg.as_string())
#             server.quit()
#
#             print(f"Notification sent to {to_email} via email.")
#         except Exception as e:
#             print(f"Failed to send email notification: {str(e)}")
#
#     def log_notification(self, message, level="info"):
#         if level == "info":
#             self.logger.info(message)
#         elif level == "error":
#             self.logger.error(message)
#         elif level == "warning":
#             self.logger.warning(message)
#
#     def print_notification(self, message, level="info"):
#         print(f"{level.upper()}: {message}")
#
#
# # Example usage of NotificationHandler
# if __name__ == "__main__":
#     # For Email notifications
#     email_config = {
#         "from_email": "your_email@gmail.com",
#         "to_email": "recipient_email@example.com",
#         "smtp_server": "smtp.gmail.com",
#         "email_password": "your_email_password"
#     }
#
#     notification_handler = NotificationHandler(notification_type="email", email_config=email_config)
#     notification_handler.send_notification("This is a test email notification.")
#
#     # For logging notifications
#     notification_handler_log = NotificationHandler(notification_type="log", log_file="scheduler.log")
#     notification_handler_log.send_notification("This is a test log notification.", level="info")
#
#     # For console notifications
#     notification_handler_console = NotificationHandler(notification_type="console")
#     notification_handler_console.send_notification("This is a test console notification.", level="error")
