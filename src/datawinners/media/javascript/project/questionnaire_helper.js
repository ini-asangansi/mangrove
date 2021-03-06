//DW is the global name space for DataWinner

DW.instruction_template = {
    "number" :"Answer must be a number.",
    "min_number" :"Answer must be a number. The minimum is %d.",
    "max_number" :"Answer must be a number. The maximum is %d.",
    "range_number" :"Answer must be a number between %d-%d.",
    "text":"Answer must be a word or phrase",
    "max_text":"Answer must be a word or phrase %d characters maximum",
    "date":"Answer must be a date in the following format %s. Example: %s",
    "single_select":"Choose 1 answer from the above list. Example: a",
    "multi_select":"Choose 1 or more answers from the above list. Example: a or ab ",
    "gps":"Answer must be GPS co-ordinates in the following format: xx.xxxx yy.yyyy Example: -18.1324, 27.6547 ",
    "dd.mm.yyyy": "25.12.2011",
    "mm.dd.yyyy": "12.25.2011",
    "mm.yyyy": "12.2011"

}

DW.question = function(question) {
    var defaults = {
        name : "Question",
        code : "code",
        type : "text",
        choices :[
            {text:"", val:""}
        ],
        entity_question_flag : false,
        length_limiter : "length_unlimited",
        length : {
            min : 1,
            max : ""
        },
        range : {
            min : "",
            max : ""
        },
        date_format: "mm.yyyy",
        instruction: "Answer must be a text"
    };

    // Extend will override the default values with the passed values(question), And take the values from defaults when its not present in question
    this.options = $.extend({}, defaults, question);
    this._init();
};


DW.question.prototype = {
    _init : function() {
        var q = this.options;
        this.range_min = ko.observable(q.range.min);

        //This condition required especially because in DB range_max is a mandatory field
        this.range_max = ko.observable(q.range.max);

        this.min_length = ko.observable(q.length.min);
        this.max_length = ko.observable(q.length.max);
        this.title = ko.observable(q.name);
        this.code = ko.observable(q.code);
        this.type = ko.observable(q.type);
        this.choices = ko.observableArray(q.choices);
        this.is_entity_question = ko.observable(q.entity_question_flag);
        this.date_format = ko.observable(q.date_format);
        this.length_limiter = ko.observable(q.length.max ? "length_limited" : "length_unlimited");
        this.instruction = ko.dependentObservable({
            read: function(){
                  if(this.type()=="text"){
                      if (this.max_length()!="")
                          return $.sprintf(DW.instruction_template.max_text, this.max_length());
                      return DW.instruction_template.text;
                  }
                  if (this.type()=="integer"){
                      if(this.range_min() == "" && this.range_max() == "")
                        return DW.instruction_template.number;
                      if(this.range_min()=="")
                        return $.sprintf(DW.instruction_template.max_number, this.range_max());
                      if(this.range_max()=="")
                        return $.sprintf(DW.instruction_template.min_number, this.range_min());
                      return $.sprintf(DW.instruction_template.range_number, this.range_min(), this.range_max());
                  }
                  if(this.type()=="date")
                    return $.sprintf(DW.instruction_template.date, this.date_format(), DW.instruction_template[this.date_format()]);
                  if(this.type()=="geocode")
                    return DW.instruction_template.gps;
                  if(this.type()=="select1")
                    return DW.instruction_template.single_select;
                if(this.type()=="select")
                    return DW.instruction_template.multi_select;

                return "No instruction can be generated"
            },
            owner:this
    });
        this.canBeDeleted = function() {
            return !this.is_entity_question();
        };
        this.isAChoiceTypeQuestion = ko.dependentObservable({
                    read:function() {
                        return this.type() == "select" || this.type() == "select1" ? "choice" : "none";
                    },
                    write:function(value) {
                        this.type(this.type() == "" ? "select" : "select1");
                    },
                    owner: this
                });


    }
};

DW.current_code = "aa";

DW.generateQuestionCode = function() {
    var code = DW.current_code;
    var next_code = DW.current_code;
    var x,y = '';
    if (next_code[1] < 'z') {
        y = String.fromCharCode(next_code[1].charCodeAt() + 1);
        x = next_code[0];
    }
    else {
        x = String.fromCharCode(next_code[0].charCodeAt() + 1);
        y = 'a';
    }
    next_code = x + y;
    DW.current_code = next_code;
    return code
};

