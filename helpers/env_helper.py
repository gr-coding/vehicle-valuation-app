class EnvHelper:

    @staticmethod
    def url_resolver(env):
        """Returns env urls"""
        if env == "prod":
            return "https://motor.confused.com"
