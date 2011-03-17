/**
 * Created by .
 * User: apgeorge
 * Date: 3/9/11
 * Time: 12:17 PM
 * To change this template use File | Settings | File Templates.
 */

//map
function(doc) {
  if (doc.type == 'Data_Record2') emit([doc.entity_uuid,doc.field_name], doc);
}
//reduce
function(doc,results,rereduce){
	r = {};
	max = results[0].value;
	min = results[0].value;
	total = 0;
	latest_value = results[0].value;
	latest_timestamp = results[0].updated_at;
	for(i in results){
		d = results[i];
		if (d.value > max) max = d.value;
		if (d.value < min) min = d.value;
		total = total + d.value;
		if (d.updated_at > latest_timestamp){
			latest_value = d.value;
                        latest_timestamp = d.updated_at;
		}

	}
	count = results.length;
	r.max = max;
	r.min = min;
        r.count = count;
        r.sum = total;
	r.avg = r.sum/r.count;
	r.latest_value = latest_value;
        r.latest_timestamp = latest_timestamp;
        return r;
}


//map
function(doc) {
    for (i in doc.attr) {
        field_dict = doc.attr[i];
        if (field_dict.type == "Number")
            emit([doc.namespace, field_dict.field], parseInt(field_dict.value));
    }
}


// including location
function(doc) {
    for (i in doc.attr) {
        field_dict = doc.attr[i];
        if (field_dict.type == "Number") {
            key = [doc.namespace, field_dict.field];
            for (v in doc.location) {
                key.push(doc.location[v]);
            }
            emit(key, parseInt(field_dict.value));
        }
    }
}

// including time and location
function(doc) {
 for(i in doc.attr){
  field_dict = doc.attr[i];
  if (field_dict.type == "Number"){
     key = [doc.namespace, field_dict.field];
     key.push(field_dict.timestamp);
     for (v in doc.location){
        key.push(doc.location[v]);
     }

     emit(key,parseInt(field_dict.value));
  }
 }
}
//reduce

//_stats

function(doc,results,rereduce){
	r = {};
	max = results[0];
	min = results[0];
	total = 0;
	for(i in results){
		d = results[i];
		if (d > max) max = d;
		if (d < min) min = d;
		total = total + d;
	}
	count = results.length;
	r.max = max;
	r.min = min;
        r.count = count;
        r.sum = total;
	r.avg = r.sum/r.count;
	return r;
    if ((doc.type == "Data_Record2") && (doc.field_type == "Number")) {
        for (location in doc.location_path) {
            key = [doc.namespace, doc.field_name];
            date = new Date(doc.event_time)
            var year = date.getFullYear();
            var month = date.getMonth() + 1;
            key.push(location);
            key.push(doc.location_path[location]);
            key.push(year);
            key.push(month);
            emit(key, parseInt(doc.value));
        }
    }
}
//reduce
//_sum

function(doc, results, rereduce) {
    r = {};
    max = results[0];
    min = results[0];
    total = 0;
    for (i in results) {
        d = results[i];
        if (d > max) max = d;
        if (d < min) min = d;
        total = total + d;
    }
    count = results.length;
    r.max = max;
    r.min = min;
    r.count = count;
    r.sum = total;
    r.avg = r.sum / r.count;
    return r;
}
