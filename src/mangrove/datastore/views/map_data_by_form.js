function(doc){
    if(!doc.void && doc.document_type == "DataRecord"){
        var time = Date.parse(doc.event_time);
        var short_code = doc.entity_backing_field.short_code;
        var form_code = doc.form_code;
        for (k in doc.data){
            value = {};
            value["value"] = doc.data[k].value;
            value["timestamp"] = time;
            value["short_code"] = short_code
            key = [form_code,short_code,k]
            emit(key,value)
        }
    }
}