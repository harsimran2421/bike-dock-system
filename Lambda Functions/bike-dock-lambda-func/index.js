var AWS = require("aws-sdk");

var ddb = new AWS.DynamoDB({apiVersion: '2012-10-08'});


exports.handler = (event, context, callback) => {
    // TODO implement
    console.log("PARAMS---:"+event.params.querystring.email_id+" "+event.params.querystring.RFID_value);
    var params = {
        TableName: "users",
        Key:{
            "email_id": {S: event.params.querystring.email_id},
            "RFID_value": {S: event.params.querystring.RFID_value}
        }
    };
    
     ddb.getItem(params, function(err, data) {
      if (err) {
        callback(null, "User not found");
        console.log("Error", err);
      } else {
          if(data.Item == undefined)
          {
            console.log("User not found");
            callback(null, "User not found");
          }
          else
          {
            console.log("Login Successful");
            callback(null, "Login Successful");
          }
      }
    });


};
