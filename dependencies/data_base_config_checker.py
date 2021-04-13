class MySQLConfigChecker:
    """
    db connect detail check
    """
    def __init__(self, hostname, username, password, database):

        self.hostname=hostname
        self.username=username
        self.password=password
        self.database=database

    @property
    def hostname(self):
        return self.hostname
    @property
    def username(self):
        return self.username
    @property
    def password(self):
        return self.password
    @property
    def database(self):
        return self.database
    @hostname.setter
    def hostname(self, hostname):
        if hostname:
            self._hostname=hostname
        else:
            raise TypeError('hostname input is error')
    @username.setter
    def username(self, username):
        if username:
            self._username=username
        else:
            raise TypeError('username input is error')
    @password.setter
    def password(self, password):
        if password:
            self._password=password
        else:
            raise TypeError('password input is error')
    @database.setter
    def database(self, database):
        if database:
            self._database=database
        else:
            raise TypeError('database input is error')
