class MangroveException(Exception): pass
class DataDictionaryFormatException(MangroveException):pass
class StoreException(MangroveException):pass
class TypeException(MangroveException):pass
class FieldValidationException(MangroveException):pass
class FormValidationException(MangroveException):pass
class FormBuilderException(MangroveException):pass
class SMSGatewayException(MangroveException):pass
class MessageAPIException(MangroveException):pass
class VUMIException(MangroveException):pass
class AuthenticationException(MangroveException):pass