# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8


##Variables
QUESTIONNAIRE_CODE = "questionnaire_code"
DEFAULT_QUESTION = "default_question"
QUESTION = "question"
QUESTIONS = "questions"
CODE = "code"
TYPE = "type"
MIN = "min"
MAX = "max"
DATE_FORMAT = "date_format"
CHOICE = "choice"
ALLOWED_CHOICE = "allowed_choice"
NUMBER = "number"
WORD = "word"
DATE = "date"
LIST_OF_CHOICES = "list_of_choices"
DD_MM_YYYY = "dd.mm.yyyy"
MM_DD_YYYY = "mm.dd.yyyy"
MM_YYYY = "mm.yyyy"
ONLY_ONE_ANSWER = "only_one_answer"
MULTIPLE_ANSWERS = "multiple_answers"
ERROR_MSG = "message"
SUCCESS_MSG = "message"

QUESTIONNAIRE_DATA = {QUESTIONNAIRE_CODE : "WPS01",
                      DEFAULT_QUESTION : {QUESTION : "What are you reporting?", CODE:"WID", MIN : "1", MAX : "10"},
                      QUESTIONS : [{QUESTION : "Water Level", CODE:"WL", TYPE: NUMBER, MIN : "1", MAX : "10"},
                                  {QUESTION : "Date of report", CODE:"DR", TYPE: DATE, CODE:"WID", DATE_FORMAT : DD_MM_YYYY},
                                  {QUESTION : "Color of Water", CODE:"WC", TYPE: LIST_OF_CHOICES,
                                   CHOICE : ["LIGHT RED", "LIGHT YELLOW", "DARK YELLOW"],
                                   ALLOWED_CHOICE : ONLY_ONE_ANSWER},
                                  {QUESTION : "Water point admin name", CODE:"WAN", TYPE: WORD, MIN : "3", MAX: "10"},
                                  {QUESTION : "Bacterias in water", CODE:"WC", TYPE: LIST_OF_CHOICES,
                                   CHOICE : ["Aquificae", "Bacteroids", "Chlorobia"],
                                   ALLOWED_CHOICE : MULTIPLE_ANSWERS}],
                      SUCCESS_MSG: ""}

