Mangrove Exceptions (DRAFT):
============================

This is a very simple framework for defining exceptions/errors specific to the
Mangrove project.  We can expand this list as needed.  Note "MangroveException"
is based on the base "Exception" class.  More specific exceptions are derived
from MangroveException.  The exceptions are defined in
"mangrove/errors/MangroveException.py"


* Exception -->
    - MangroveException  -->
        - DataDictionaryFormatException
        - DataStoreException
        - FormValidationException
        - FieldValidationException
        - TypeException
        - FormBuilderException
        - SMSGatewayException
        - ServiceNotAvailableException
        - MessageAPIException
        - VUMIException
        - AuthenticationException 


Example:
========
The following code example, "validate_age.py", validates the age of a person.
The example illustrates how one might use the Mangrove exception hierarchy.
::
    from errors.MangroveException import FieldValidationException, TypeException

    def validate_age(age):
        if type(age) != int:
            raise TypeException("Age is not a whole number.")
        if not 0 <= age <= 135:
            raise FieldValidationException("Age is not in the acceptable range")
        #If we made it here the validation passed so return None to denote no errors
        return None