var AWS = require("aws-sdk");

var ddb = new AWS.DynamoDB({apiVersion: '2012-10-08'});

var parse = AWS.DynamoDB.Converter.output;

exports.handler = (event, context, callback) => {
    // TODO implement
    console.log("PARAMS---:"+event.params.querystring.dock+" "+event.params.querystring.slot);
    var params = {
        TableName: "Availability"
    };
    
    //  ddb.getItem(params, function(err, data) {
    //   if (err) {
    //     console.log("Error", err);

    //   } else {
    //       console.log("Booking status ----> ",data.Item.booking);
          
    //       var x = parse(data.Item.booking,String);
          
    //       console.log("x =",x);
          
    //       if(  data.Item.booking == "booked")
    //       {
    //           console.log("Dock is booked");
    //           callback(null, "Dock is booked");
    //       }
    //       else if (x == "available")
    //       {
    //           console.log("Dock is available");
    //           callback(null, "Dock is available");
    //       }
    //       else 
    //       {
    //           console.log("Ho rha hi nhi hai");
    //       }
    //     console.log("Success", data.Item);
    //   // callback(null, JSON.parse( JSON.stringify(data, null, 2)));
    //   }
    // });


    ddb.scan(params, function(err, data) {
      if (err) {
        console.log("Error", err);
      } else {
          console.log("Pika -->",data.Items.dock);
        data.Items.forEach(function(element, index, array) {
            var dock = parse(element.dock);
            var slot = parse(element.slot);
            var booking = parse(element.booking);
          //console.log("Dock :",element.dock," Slot :",slot," Availability: ",booking);
          //console.log(element.dock + " (" + element.slot + ")");
          //callback(null,"Dock :");
          callback(null, JSON.parse( JSON.stringify(data, null, 2)));
        });
      }
    });
    
    // ddb.listTables({Limit: 10}, function(err, data) {
    //   if (err) {
    //     console.log("Error", err.code);
    //   } else {
    //     console.log("Table names are ", data.TableNames);
    //   }
    // });

};
