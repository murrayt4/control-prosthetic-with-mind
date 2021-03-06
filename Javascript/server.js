//This is the main file that puts the server online.
//The below constants defines necessary dependencies
const express        = require('express');
const MongoClient    = require('mongodb').MongoClient;
const bodyParser     = require('body-parser');
const db             = require('./config/db');
const app            = express();
const port = 8000;
const path = require('path');
const exphbs = require('express-handlebars');
app.use(bodyParser.urlencoded({ extended: true }));

 MongoClient.connect(db.url, (err, database) => {
 if (err) return console.log(err)
 let mydb = database.db("apipractice")
 require('./app/routes')(app,mydb);
 dbObject = database;

})
// Make sure you add the database name and not the collection name
//Loads the main.handlebars file to the front end, allows files in the public folder to be used
  app.engine('handlebars', exphbs({defaultLayout: 'main'}));
  app.set('view engine', 'handlebars');
  app.use('/public', express.static('public'));
// app.use(express.static(__dirname + '/public'));
 // app.use(express.static(__dirname + '/views'));
//Function to retrieve data to database and format it in JSON format
function getData(responseObj){
   dbObject.collection('notes').find().toArray( (err, result) => {
      if (err) {
        res.send({'error':'An error has occured'});
      } else {
        var timearray = [];
        var blinkarray = [];

        for (i in result){
                var doc = result[i];
                //category array
                var time = doc['Time'];
                var blink = doc['Blink'];
                timearray.push({"label" : time});
                blinkarray.push({"value": blink});
        }

        var dataset = [
          {
            "seriesname" : "Number of Blinks",
            "data" : blinkarray
          }

        ];

        var response = {
          "dataset" : dataset,
          "categories": timearray
         };
         responseObj.json(response);
      }
    });
}
//calls getData function upon HTTP GET request to /notes server
 app.get("/notes", function(req, res){
 getData(res);
 });


// app.get('/', function(req, res) {//request and response opens html file
// res.sendFile(path.join(__dirname + '/index.html'));
// });
//Renders the chart upon opening the server
app.get("/", function(req, res){
 res.render("charts");
 });

app.listen(port, () => {
    console.log('We are live on ' + port);
 });

