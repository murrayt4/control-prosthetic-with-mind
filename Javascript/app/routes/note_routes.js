var ObjectID = require('mongodb').ObjectID;
var path = require('path');
const exphbs = require('express-handlebars');
//The below methods create routes for various HTTP methods
module.exports = function(app, db) {
// note_routes.js
app.put('/notes/:id', (req, res) => {
    const id = req.params.id;
    const details = { '_id': new ObjectID(id) };
    const note = { text: req.body.body, title: req.body.title };
    db.collection('notes').update(details, note, (err, result) => {
      if (err) {
          res.send({'error':'An error has occurred'});
      } else {
          res.send(note);
      }
    });
  });
app.delete('/notes/:id', (req, res) => {
    const id = req.params.id;
    const details = {'_id': new ObjectID(id) };
    db.collection('notes').remove(details, (err, item) =>{
     if(err){
      res.send({'error':'An error has occurred'});
      } else {
        res.send('Note ' + id + ' deleted!');
      }
    });
  });
/*app.get('/notes', (req, res) => {//figure out how this relates to ajax call
  db.collection('notes').find().toArray( (err, result) => {
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
          "catergory": timearray
         };
         res.send(response);
      }
    });
  });
*/

app.post('/login', (req,res)=> {//Opens second html page after button is submitted

  const login = {FirstName: req.body.firstname, LastName: req.body.lastname};
  db.collection('names').insert(login, (err, result) => {
  if (err) {
    res.send({ 'error': 'An error has occurred' });
  } else {
  // app.engine('handlebars', exphbs({defaultLayout: 'main'}));
  // app.set('view engine', 'handlebars');
   res.sendFile(path.join(__dirname + '../../../views/layouts/display.html'));


   }
  });
});


app.post('/notes', (req, res) => {//Uploads data to mongodb
   //Creates a file that stores data in a variable
   const note = { Time: req.body.time, Userid: req.body.userid, Signal: req.body.signal,
        Blink: req.body.blink, Leftwink: req.body.leftwink, Rightwink: req.body.rightwink,
        Surprise: req.body.surprise, Frown: req.body.frown, Clench: req.body.clench,
        Smile: req.body.smile, MentalAction: req.body.mentalaction, MentalPower: req.body.me$
   db.collection('notes').insert(note, (err, result) => {//Inserts data into database
   if (err) {
   res.send({ 'error': 'An error has occurred' });
   } else {
   res.send(result.ops[0]);
  }
 });
});
};
