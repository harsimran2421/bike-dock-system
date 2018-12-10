var AWS = require("aws-sdk");

var ddb = new AWS.DynamoDB({apiVersion: '2012-10-08'});

var parse = AWS.DynamoDB.Converter.output;

exports.handler = (event, context, callback) => {
    // TODO implement
    console.log("PARAMS---:"+event.params.querystring.dock+" "+event.params.querystring.slot);
    var params = {
        TableName: "Availability"
    };
    

    ddb.scan(params, function(err, data) {
      if (err) {
        console.log("Error", err);
      } else {
          console.log("Pika -->",data.Items.dock);
        data.Items.forEach(function(element, index, array) {
            var dock = parse(element.dock);
            var slot = parse(element.slot);
            var booking = parse(element.booking);
          callback(null, JSON.parse( JSON.stringify(data, null, 2)));
        });
      }
    });
    
    

};
