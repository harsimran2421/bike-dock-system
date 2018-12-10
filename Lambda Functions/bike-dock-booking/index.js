var AWS = require("aws-sdk");

var ddb = new AWS.DynamoDB({apiVersion: '2012-10-08'});

var parse = AWS.DynamoDB.Converter.output;

exports.handler = (event, context, callback) => {
    // TODO implement
    console.log("PARAMS---:"+event.params.querystring.email_id+" "+event.params.querystring.RFID_value+" "+event.params.querystring.dock+" "+event.params.querystring.slot);
    
    var params = {
        TableName: "users",
        Key:{
            "email_id": {S: event.params.querystring.email_id},
            "RFID_value": {S: event.params.querystring.RFID_value}
        },
    };
    
    var params0 = {
        TableName: "Availability",
        Key:{
            "dock": {N: event.params.querystring.dock},
            "slot": {N: event.params.querystring.slot}
        },
    };
    
    ddb.getItem(params, function(err, data){
        if(err) {
            console.log("Error reading users", err);
        } else {
            console.log("Success reading users",data.Item);

            var dock = parse(data.Item.dock);

            if (dock != 0)
            {
                console.log("User already checked in");
                callback(null, "User already checked in");
            }
            else
            {
                console.log("Dock =", dock);
                
                
                ddb.getItem(params0, function(err, data){
                    if(err) {
                        console.log("Error reading Availability", err);
                    } else {
                        console.log("Success reading Availability",data.Item);
    
                        var booking = parse(data.Item.booking);
                        
                        console.log("booking staus of dock",booking);
                        
                        if ( booking == "booked")
                        {
                         
                            console.log("Dock not available");
                            callback(null, "Dock not available");
                            
                        }
                        else
                        {
                            
                            var params1 = {
                                TableName: "users",
                                Key:{
                                    "email_id": {S: event.params.querystring.email_id},
                                    "RFID_value": {S: event.params.querystring.RFID_value}
                                },
                                UpdateExpression: "set dock = :d, slot = :s",
                                ExpressionAttributeValues:{
                                    ":d": {N: event.params.querystring.dock},
                                    ":s": {N: event.params.querystring.slot}
                                }
                            };
                            
                            var params2 = {
                                TableName: "Availability",
                                Key:{
                                    "dock": {N: event.params.querystring.dock},
                                    "slot": {N: event.params.querystring.slot}
                                },
                                UpdateExpression: "set booking = :x",
                                ExpressionAttributeValues:{
                                    ":x":{S: "booked"}
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
                            
                            callback(null, "Booking Successful");
                        }
                    }
                });
                
                var mobile_number = parse(data.Item.mobile_number);
                
                var params_sms = {
                  Message: 'Booking Confirmed !!!', /* required */
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
            }
        }
    });
};
