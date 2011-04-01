function(key, values, rereduce) {
    var isNull = function(o) {
        return (o === undefined) || (o == null);
    };

    var current = { entity_id : {value: key[0][0][1] } };

    for (value in values) {
        for (index in values[value]) {
            if (isNull(current[index]) || values[value][index].timestamp_for_view > current[index].timestamp_for_view) {
                current[index] = values[value][index];
            }
        }
    }
    return current;
}