class AppSettings:
    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, default=None):
        from django.conf import settings
        return getattr(settings, self.prefix + name, default)

    @property
    def PATH_LENGTH(self):
        return self._setting(name='PATH_LENGTH', default=200)

    @property
    def DECODE_REQUEST_BODY(self):
        return self._setting('DECODE_REQUEST_BODY', True)


app_settings = AppSettings('DRF_TRACKING_')
