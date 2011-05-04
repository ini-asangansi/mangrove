# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from _collections import defaultdict
from mangrove.form_model.validation import IntegerConstraint, ConstraintAttributes


def field_to_json(object):
    assert isinstance(object ,Field)
    return object._to_json()

class field_attributes(object):

    '''Constants for referencing standard attributes in questionnaire.'''
    LANGUAGE = "language"
    FIELD_CODE = "question_code"
    INTEGER_FIELD = "integer"
    TEXT_FIELD = "text"
    SELECT_FIELD = 'select1'
    DATE_FIELD = 'date'
    MULTISELECT_FIELD = 'select'
    DEFAULT_LANGUAGE = "eng"
    ENTITY_QUESTION_FLAG = 'entity_question_flag'
    NAME = "name"

class Field(object):
    NAME = "name"
    LABEL = "label"
    TYPE = "type"
    QUESTION_CODE = "question_code"

    _DEFAULT_VALUES = {
        NAME: "",
        TYPE: "",
        QUESTION_CODE: "",
    }

    _DEFAULT_LANGUAGE_SPECIFIC_VALUES = {
        LABEL: {},
    }

    def __init__(self, **kwargs):
        self._dict = defaultdict(dict)
        for k, default_value in self._DEFAULT_VALUES.items():
            self._dict[k] = kwargs.get(k, default_value)

        for k, default_langauge_specific_value in self._DEFAULT_LANGUAGE_SPECIFIC_VALUES.items():
            a = kwargs.get(field_attributes.LANGUAGE, field_attributes.DEFAULT_LANGUAGE)
            language_dict = {a: kwargs.get(k)}
            self._dict[k] = language_dict


    @property
    def name(self):
        return self._dict.get(self.NAME)

    @property
    def label(self):
        return self._dict.get(self.LABEL)

    @property
    def type(self):
        return self._dict.get(self.TYPE)

    @property
    def question_code(self):
        return self._dict.get(self.QUESTION_CODE)

    @property
    def is_entity_field(self):
        return False

    def _to_json(self):
        return self._dict

    def add_or_edit_label(self, label, language=None):
        language_to_add = language if language is not None else field_attributes.DEFAULT_LANGUAGE
        self._dict[self.LABEL][language_to_add] = label


class IntegerField(Field):
    RANGE = "range"

    def __init__(self, name, question_code, label, range=None, language=field_attributes.DEFAULT_LANGUAGE):
        Field.__init__(self, type=field_attributes.INTEGER_FIELD, name=name, question_code=question_code,
                          label=label, language=language)
        if range is None:
            range=IntegerConstraint()
        self._dict[self.RANGE] = range._to_json()

    @property
    def range(self):
        return self._dict.get(self.RANGE)


class TextField(Field):
    DEFAULT_VALUE = "defaultValue"
    ENTITY_QUESTION_FLAG = 'entity_question_flag'

    def __init__(self, name, question_code, label, defaultValue=None, language=field_attributes.DEFAULT_LANGUAGE,entity_question_flag=False):
        Field.__init__(self, type=field_attributes.TEXT_FIELD, name=name, question_code=question_code,
                          label=label, language=language)
        self._dict[self.DEFAULT_VALUE] = defaultValue if defaultValue is not None else ""
        if entity_question_flag:
            self._dict[self.ENTITY_QUESTION_FLAG] = entity_question_flag

    @property
    def is_entity_field(self):
        return self._dict.get(self.ENTITY_QUESTION_FLAG)
    

class SelectField(Field):
    OPTIONS = "options"
    SINGLE_SELECT_FLAG = 'single_select_flag'

    def __init__(self, name, question_code, label, options=None, language=field_attributes.DEFAULT_LANGUAGE,single_select_flag=True):
        type = field_attributes.SELECT_FIELD if single_select_flag else field_attributes.MULTISELECT_FIELD
        self.SINGLE_SELECT_FLAG = single_select_flag
        Field.__init__(self, type=type, name=name, question_code=question_code,
                          label=label, language=language)
        self._dict[self.OPTIONS] = []
        if options is not None:
            for option in options:
                if isinstance(option, tuple):
                    single_language_specific_option = {'text': {language: option[0]}, 'val': option[1]}
                elif isinstance(option, dict):
                    single_language_specific_option = option
                else:
                    single_language_specific_option = {'text': {language: option}}
                self._dict[self.OPTIONS].append(single_language_specific_option)

    @property
    def options(self):
        return self._dict.get(self.OPTIONS)



class DateField(Field):
    RANGE = "range"
    FORMAT="format"
    def __init__(self,name, question_code, label,format,range=None,language=field_attributes.DEFAULT_LANGUAGE):
        Field.__init__(self, type=field_attributes.DATE_FIELD, name=name, question_code=question_code,
                          label=label, language=language)

        self._dict[self.RANGE] = range if range is not None else {}
        self._dict[self.FORMAT] = format if format is not None else ""


def create_question_from(dictionary):
    """
     Given a dictionary that defines a question, this would create a field with all the validations that are
     defined on it.
    """
    type = dictionary.get("type")
    name = dictionary.get("name")
    code = dictionary.get("question_code")
    is_entity_question = dictionary.get("entity_question_flag")
    label = dictionary.get("label")
    if type=="text":
        return TextField(name=name,question_code=code, label=label, entity_question_flag=is_entity_question )
    elif type =="integer":
        range_dict = dictionary.get("range")
        range=IntegerConstraint(min=range_dict.get(ConstraintAttributes.MIN),max=range_dict.get(ConstraintAttributes.MAX))
        return IntegerField(name=name,question_code=code, label=label, range = range)
    elif type == "select" or type == "select1":
        choices = dictionary.get("options")
        single_select = True if type=="select1" else False
        return SelectField(name=name,question_code=code, label=label, options=choices, single_select_flag=single_select)
    return None