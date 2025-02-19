from django.utils.timezone import now
from ipaddress import ip_address
from .app_settings import app_settings

class BaseLoggingMixin:
    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        self.log = {
            'request_at': now(),
        }
        return super().initial(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Returns the final response object.
        """
        response = super().finalize_response(request, response, *args, **kwargs)
        user = self._get_user(request)
        self.log.update({
            'remote_addr': self._get_ip_address(request),
            'view': self._get_view_name(request),
            'view_method': self._get_view_method(request),
            'path': self._get_path(request),
            'host': request.get_host(),
            'method': request.method,
            'user': user,
            'user_persistent': user.get_username() if user else 'Anonymous',
            'response_ms': self._get_response_ms(),

        })
        self.handle_log()
        return response

    def handle_log(self):
        raise NotImplementedError

    def _get_ip_address(self, request):
        ipaddr = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if ipaddr:
            ipaddr = ipaddr.split(',')[0]
        else:
            ipaddr = request.META.get('REMOTE_ADDR', None).split(',')[0]

        possibles = (ipaddr.lstrip('[').split(']')[0], ipaddr.split(':')[0])
        for addr in possibles:
            try:
                return str(ip_address(addr))
            except:
                pass
        return ipaddr

    def _get_view_name(self, request):
        method = request.method.lower()
        try:
            attribute = getattr(self, method)
            return type(attribute.__self__).__module__ + '.' + type(attribute.__self__).__name__
        except AttributeError:
            return None

    def _get_view_method(self, request):
        if hasattr(self, 'action'):
            return getattr(self, 'action')
        return request.method.lower()

    def _get_path(self, request):
        return request.path[:app_settings.PATH_LENGTH]

    def _get_user(self, request):
        user = request.user
        if user.is_anonymous:
            return None
        return user

    def _get_response_ms(self):
        pass