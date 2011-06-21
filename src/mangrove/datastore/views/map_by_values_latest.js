function(doc) {
  if (doc.document_type == "Entity") {
    var entity_type = doc.aggregation_paths['_type'];
    var entity_id = doc.id;
    for (k in doc.data){
      value = {};
      key = [entity_type,entity_id,k];
      value["value"] = doc.data[k].value;
      emit(key, value);
    }
  }
}

