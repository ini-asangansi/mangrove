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

