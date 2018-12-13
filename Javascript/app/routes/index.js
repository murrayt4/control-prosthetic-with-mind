const noteRoutes = require('./note_routes');
//const serverRoutes = require('../../server');
module.exports = function(app, db) {
  noteRoutes(app, db);
  //serverRoutes(app, db);
  // Other route groups could go here, in the future
};
