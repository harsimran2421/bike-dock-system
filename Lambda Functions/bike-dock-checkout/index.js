var AWS = require("aws-sdk");

var ddb = new AWS.DynamoDB({apiVersion: '2012-10-08'});

var parse = AWS.DynamoDB.Converter.output;

exports.handler = (event, context, callback) => {
    // TODO implement
    console.log("PARAMS---:"+event.params.querystring.email_id+" "+event.params.querystring.RFID_value);
    
    var params = {
        TableName: "users",
        Key:{
            "email_id": {S: event.params.querystring.email_id},
            "RFID_value": {S: event.params.querystring.RFID_value}
        },
    };
    
    
    
    ddb.getItem(params, function(err, data){
        if(err) {
            console.log("Error reading users", err);
        } else {
            console.log("Success reading users",data.Item);

            var dock = parse(data.Item.dock);

            if (dock == 0)
            {
                console.log("No dock assigned");
                callback(null, "No dock assigned");
            }
            else
            {
                console.log("Dock =", dock);
                
                var params1 = {
                    TableName: "users",
                    Key:{
                        "email_id": {S: event.params.querystring.email_id},
                        "RFID_value": {S: event.params.querystring.RFID_value}
                    },
                    UpdateExpression: "set dock = :d, slot = :s",
                    ExpressionAttributeValues:{
                        ":d": {S: "0"},
                        ":s": {S: "0"}
                    }
                };
                
                var params2 = {
                    TableName: "Availability",
                    Key:{
                        "dock": data.Item.dock,
                        "slot": data.Item.slot
                    },
                    UpdateExpression: "set booking = :x",
                    ExpressionAttributeValues:{
                        ":x":{S: "available"}
                    }
                };
            
                ddb.updateItem(params1, function(err, data){
                if (err) {
                    console.log("Error updating users", err);
                } else {
                    console.log("Success updating users");   
                }  
                });

                ddb.updateItem(params2, function(err, data){
                if (err) {
                    console.log("Error updating availability", err);
                } else {
                    console.log("Success updating availability");   
                }
                });
                
                
                var mobile_number = parse(data.Item.mobile_number);
                
                var params_sms = {
                  Message: 'Checkout Confirmed from Dock : '+data.Item.dock.N+" Slot : "+data.Item.slot.N, /* required */
                  PhoneNumber: mobile_number,
                };
                                
                var publishTextPromise = new AWS.SNS({apiVersion: '2010-03-31'}).publish(params_sms).promise();
                                
                publishTextPromise.then(
                  function(data) {
                    console.log("MessageID is " + data.MessageId);
                  }).catch(
                    function(err) {
                    console.error(err, err.stack);
                  });
                
                callback(null, "Checkout Successful");
            }
                
            

        }
    });



};
