from django.utils.timezone import now
from ipaddress import ip_address
from traceback import format_exc
from logging import getLogger
from .app_settings import app_settings
import ast

logger = getLogger(__name__)


class BaseLoggingMixin:
    logging_methods = '__all__'
    sensitive_fields = {}
    CLEANED_SUBSTITUTE = '**********'

    def __init__(self, *args, **kwargs):
        assert isinstance(self.CLEANED_SUBSTITUTE, str), 'CLEANED_SUBSTITUTE must be a String'
        super().__init__(*args, **kwargs)

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        self.log = {
            'requested_at': now(),
        }
        if not getattr(self, 'decode_request_body', app_settings.DECODE_REQUEST_BODY):
            self.log['data'] = ''
        else:
            self.log['data'] = request.data
        return super().initial(request, *args, **kwargs)

    def handle_exception(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        response = super().handle_exception(exc)
        self.log['errors'] = format_exc()
        return response

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Returns the final response object.
        """
        response = super().finalize_response(request, response, *args, **kwargs)
        if self.should_log(request, response):
            user = self._get_user(request)
            if request.stream:
                rendered_content = None
            elif hasattr(response, 'rendered_content'):
                rendered_content = response.rendered_content
            else:
                rendered_content = response.getvalue()
            self.log.update({
                'remote_addr': self._get_ip_address(request),
                'view': self._get_view_name(request),
                'view_methode': self._get_view_method(request),
                'path': self._get_path(request),
                'host': request.get_host(),
                'method': request.method,
                'user': user,
                'user_persistent': user.get_username() if user else 'Anonymous',
                'response_ms': self._get_response_ms(),
                'status_code': response.status_code,
                "query_params": self._clean_data(request.query_params.dict()),
                'response': self._clean_data(rendered_content)
            })
            try:
                self.handle_log()
            except Exception as ex:
                logger.exception("Logging API call raise exception!", ex.args)
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
        response_timedelta = now() - self.log['requested_at']
        response_ms = response_timedelta.total_seconds() * 1000
        return max(int(response_ms), 0)

    def should_log(self, request, response):
        return (
                self.logging_methods == '__all__' or request.method in self.logging_methods
        )

    def _clean_data(self, data):
        if isinstance(data, bytes):
            data = data.decode(errors="Replace")
        if isinstance(data, list):
            return [self._clean_data(_data) for _data in data]

        if isinstance(data, dict):
            SENSITIVE_FIELDS = {'api', 'token', 'key', 'secret', 'password', 'signature'}
            if self.sensitive_fields:
                SENSITIVE_FIELDS = SENSITIVE_FIELDS | {field.lower() for field in self.sensitive_fields}
                for key, value in data.items():
                    try:
                        value = ast.literal_eval(value)
                    except (ValueError, SyntaxError):
                        pass

                    if isinstance(value, (list, dict)):
                        self._clean_data(value)
                    if key.lower() in SENSITIVE_FIELDS:
                        data[key] = self.CLEANED_SUBSTITUTE
        return data
