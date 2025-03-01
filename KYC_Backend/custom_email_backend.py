from django.core.mail.backends.smtp import EmailBackend

class CustomEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False
        try:
            self.connection = self.connection_class(self.host, self.port, timeout=self.timeout)
            self.connection.ehlo()
            if self.use_tls:
                # Override the starttls method to avoid passing unexpected arguments
                self.connection.starttls()  # Removed `keyfile` and `certfile` arguments
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception:
            if not self.fail_silently:
                raise
            return False
