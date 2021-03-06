$(document).ready(function() {

     $("#location").autocomplete("/places", {
        minChars: 0,
        max: 12,
        autoFill: true,
        mustMatch: true,
        matchContains: false,
        scrollHeight: 220});

    $.validator.addMethod('regexrule', function(value, element, params) {
        var text = $('#' + element.id).val().trim();
        if (text=="")
            return true;
        var re = new RegExp("^[0-9]+(\-[0-9]+)*$");
        return re.test(text);
    }, "Please enter a valid phone number");

    $.validator.addMethod('gpsrule', function(value, element, params) {
        var codes = $('#' + element.id).val();
        codes = codes.trim();
        if (codes == "")
            return true;
        codes = codes.replace(/\s+/g, " ");
        lat_long = codes.split(' ');

        if (lat_long.length != 2)
            return false;
        return (lat_long[0] > -90 && lat_long[0] < 90)
                && (lat_long[1] > -180 && lat_long[1] < 180);
    }, "Incorrect GPS coordinates. Please resubmit");

    DW.validator = $('#question_form').validate({
        messages:{
            geo_code:{
                required:"Please fill out at least one location field."
            },
            location:{
                required:"Please fill out at least one location field"
            }

        },
        rules:{
            entity_name:{
                required: true
            },

            mobile_number:{
                regexrule:true

            },
            geo_code:{
                required:function(element) {
                    return $("#location").val().trim() == "";
                },
                gpsrule: true
            },
            location:{
                required:function(element) {
                    return $("#geo_code").val().trim() == "";
                }
            },
            short_name:{
                required :true
            }
        },
        wrapper: "span",
        errorPlacement: function(error, element) {
                    offset = element.offset();
                    error.insertAfter(element)
                    error.addClass('error_arrow');  // add a class to the wrapper

        }
});


});