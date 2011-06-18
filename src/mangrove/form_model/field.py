# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from _collections import defaultdict
from datetime import datetime
from mangrove.datastore.datadict import DataDictType
from mangrove.errors.MangroveException import AnswerTooBigException, AnswerTooSmallException, AnswerTooLongException, AnswerTooShortException, AnswerWrongType, IncorrectDate, GeoCodeFormatException
from mangrove.form_model.validation import NumericConstraint, ConstraintAttributes, TextConstraint, ChoiceConstraint, GeoCodeConstraint
from validate import VdtValueTooBigError, VdtValueTooSmallError, VdtValueTooLongError, VdtValueTooShortError, VdtTypeError


def create_question_from(dictionary, dbm):
    """
     Given a dictionary that defines a question, this would create a field with all the validations that are
     defined on it.
    """
    type = dictionary.get("type")
    name = dictionary.get("name")
    code = dictionary.get("code")
    is_entity_question = dictionary.get("entity_question_flag")
    label_dict = dictionary.get("label")
    label=None
    if label_dict is not None:
        label = label_dict.get(field_attributes.DEFAULT_LANGUAGE)
    ddtype = DataDictType.create_from_json(dictionary.get("ddtype"), dbm)
    if type == field_attributes.TEXT_FIELD:
        return _get_text_field(code, ddtype, dictionary, is_entity_question, label, name)
    elif type == field_attributes.INTEGER_FIELD:
        return _get_integer_field(code, ddtype, dictionary, label, name)
    elif type == field_attributes.DATE_FIELD:
        return _get_date_field(code, ddtype, dictionary, label, name)
    elif type == field_attributes.LOCATION_FIELD:
        return GeoCodeField(name=name, code=code, label=label, ddtype=ddtype)
    elif type == field_attributes.SELECT_FIELD or type == field_attributes.MULTISELECT_FIELD:
        return _get_select_field(code, ddtype, dictionary, label, name, type)
    return None


def field_to_json(object):
    #    assert isinstance(object, Field)
    if isinstance(object, datetime):
        return object.isoformat()
    else:
        return object._to_json_view()


class field_attributes(object):
    '''Constants for referencing standard attributes in questionnaire.'''
    LANGUAGE = "language"
    FIELD_CODE = "code"
    INTEGER_FIELD = "integer"
    TEXT_FIELD = "text"
    SELECT_FIELD = 'select1'
    LOCATION_FIELD = "geocode"
    DATE_FIELD = 'date'
    MULTISELECT_FIELD = 'select'
    DEFAULT_LANGUAGE = "eng"
    ENTITY_QUESTION_FLAG = 'entity_question_flag'
    NAME = "name"


class Field(object):
    NAME = "name"
    LABEL = "label"
    TYPE = "type"
    CODE = "code"
    DDTYPE = "ddtype"
    LANGUAGE = "language"

    _DEFAULT_VALUES = {
        NAME: "",
        TYPE: "",
        CODE: "",
        DDTYPE: None
    }

    _DEFAULT_LANGUAGE_SPECIFIC_VALUES = {
        LABEL: {},
        }

    def __init__(self, **kwargs):
        self._dict = defaultdict(dict)
        assert kwargs.get(self.DDTYPE) is not None
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
    def code(self):
        return self._dict.get(self.CODE)

    @property
    def is_entity_field(self):
        return False

    @property
    def ddtype(self):
        return self._dict.get(self.DDTYPE)

    @property
    def language(self):
        return self._dict.get(self.LANGUAGE) or field_attributes.DEFAULT_LANGUAGE

    def _to_json(self):
        dict = self._dict.copy()
        dict['ddtype'] = dict['ddtype'].to_json()
        return dict

    def _to_json_view(self):
        return self._to_json()

    def add_or_edit_label(self, label, language=None):
        language_to_add = language if language is not None else field_attributes.DEFAULT_LANGUAGE
        self._dict[self.LABEL][language_to_add] = label


class IntegerField(Field):
    RANGE = "range"

    def __init__(self, name, code, label, ddtype, range=None, language=field_attributes.DEFAULT_LANGUAGE):
        Field.__init__(self, type=field_attributes.INTEGER_FIELD, name=name, code=code,
                       label=label, language=language, ddtype=ddtype)

        self.constraint = range if range is not None else NumericConstraint()
        self._dict[self.RANGE] = self.constraint._to_json()

    def validate(self, value):
        try:
            return self.constraint.validate(value)
        except VdtValueTooBigError:
            raise AnswerTooBigException(self._dict[field_attributes.FIELD_CODE], value)
        except VdtValueTooSmallError:
            raise AnswerTooSmallException(self._dict[field_attributes.FIELD_CODE], value)
        except VdtTypeError:
            raise AnswerWrongType(self._dict[field_attributes.FIELD_CODE])

    @property
    def range(self):
        return self._dict.get(self.RANGE)


class DateField(Field):
    DATE_FORMAT = "date_format"

    def __init__(self, name, code, label, date_format, ddtype, language=field_attributes.DEFAULT_LANGUAGE):
        Field.__init__(self, type=field_attributes.DATE_FIELD, name=name, code=code,
                       label=label, language=language, ddtype=ddtype)

        self._dict[self.DATE_FORMAT] = date_format

    def validate(self, value):
        DATE_DICTIONARY = {'mm.yyyy': '%m.%Y', 'dd.mm.yyyy': '%d.%m.%Y', 'mm.dd.yyyy': '%m.%d.%Y'}
        try:
            datetime.strptime(value.strip(), DATE_DICTIONARY.get(self._dict[self.DATE_FORMAT]))
        except ValueError:
            raise IncorrectDate(self._dict.get(field_attributes.FIELD_CODE), value, self._dict.get(self.DATE_FORMAT))
        return value
    
    @property
    def date_format(self):
        return self._dict.get(self.DATE_FORMAT)


class TextField(Field):
    DEFAULT_VALUE = "defaultValue"
    LENGTH = "length"
    ENTITY_QUESTION_FLAG = 'entity_question_flag'

    def __init__(self, name, code, label, ddtype, length=None, defaultValue=None,
                 language=field_attributes.DEFAULT_LANGUAGE, entity_question_flag=False):
        Field.__init__(self, type=field_attributes.TEXT_FIELD, name=name, code=code,
                       label=label, language=language, ddtype=ddtype)
        self._dict[self.DEFAULT_VALUE] = defaultValue if defaultValue is not None else ""
        self.constraint = length if length is not None else TextConstraint()
        self._dict[self.LENGTH] = self.constraint._to_json()
        if entity_question_flag:
            self._dict[self.ENTITY_QUESTION_FLAG] = entity_question_flag

    def validate(self, value):
        try:
            return self.constraint.validate(value)
        except VdtValueTooLongError:
            raise AnswerTooLongException(self._dict[field_attributes.FIELD_CODE], value)
        except VdtValueTooShortError:
            raise AnswerTooShortException(self._dict[field_attributes.FIELD_CODE], value)

    @property
    def is_entity_field(self):
        return self._dict.get(self.ENTITY_QUESTION_FLAG)


class SelectField(Field):
    OPTIONS = "choices"

    def __init__(self, name, code, label, options, ddtype, language=field_attributes.DEFAULT_LANGUAGE,
                 single_select_flag=True):
        assert len(options) > 0
        type = field_attributes.SELECT_FIELD if single_select_flag else field_attributes.MULTISELECT_FIELD
        self.SINGLE_SELECT_FLAG = single_select_flag
        Field.__init__(self, type=type, name=name, code=code,
                       label=label, language=language, ddtype=ddtype)
        self._dict[self.OPTIONS] = []
        valid_choices = self._dict[self.OPTIONS]
        if options is not None:
            for option in options:
                if isinstance(option, tuple):
                    single_language_specific_option = {'text': {language: option[0]}, 'val': option[1]}
                elif isinstance(option, dict):
                    single_language_specific_option = option
                else:
                    single_language_specific_option = {'text': {language: option}}
                valid_choices.append(single_language_specific_option)
        self.constraint = ChoiceConstraint(
            list_of_valid_choices=[each.get('text').get(language) for each in valid_choices],
            single_select_constraint=single_select_flag, code=code)

    SINGLE_SELECT_FLAG = 'single_select_flag'

    def validate(self, value):
        return self.constraint.validate(answer=value)

    @property
    def options(self):
        return self._dict.get(self.OPTIONS)

    def _to_json_view(self):
        dict = self._dict.copy()
        option_list = []
        for option in self.options:
            option_text = option["text"][field_attributes.DEFAULT_LANGUAGE]
            option_list.append({"text": option_text, "val": option.get("val")})
        dict['choices'] = option_list
        dict['ddtype'] = dict['ddtype'].to_json()
        return dict


class GeoCodeField(Field):
    def __init__(self, name, code, label, ddtype, language=field_attributes.DEFAULT_LANGUAGE):
        Field.__init__(self, type=field_attributes.LOCATION_FIELD, name=name, code=code,
                       label=label, language=language, ddtype=ddtype)

    def validate(self, lat_long_string):
        if lat_long_string is None:
            raise GeoCodeFormatException(self.code)
        lat_long = lat_long_string.strip().split()
        if len(lat_long)<2:
            raise GeoCodeFormatException(self.code)
        return GeoCodeConstraint().validate(latitude=lat_long[0], longitude=lat_long[1])




def _get_text_field(code, ddtype, dictionary, is_entity_question, label, name):
    length_dict = dictionary.get("length")
    length = TextConstraint(min=length_dict.get(ConstraintAttributes.MIN),
                            max=length_dict.get(ConstraintAttributes.MAX))
    return TextField(name=name, code=code, label=label, entity_question_flag=is_entity_question,
                     length=length, ddtype=ddtype)


def _get_integer_field(code, ddtype, dictionary, label, name):
    range_dict = dictionary.get("range")
    range = NumericConstraint(min=range_dict.get(ConstraintAttributes.MIN),
                              max=range_dict.get(ConstraintAttributes.MAX))
    return IntegerField(name=name, code=code, label=label, range=range, ddtype=ddtype)


def _get_date_field(code, ddtype, dictionary, label, name):
    date_format = dictionary.get("date_format")
    return DateField(name=name, code=code, label=label, date_format=date_format, ddtype=ddtype)


def _get_select_field(code, ddtype, dictionary, label, name, type):
    choices = dictionary.get("choices")
    single_select = True if type == field_attributes.SELECT_FIELD else False
    return SelectField(name=name, code=code, label=label, options=choices,
                       single_select_flag=single_select, ddtype=ddtype)
