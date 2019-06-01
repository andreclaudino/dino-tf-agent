var express = require('express');
var app = express();

app.use(express.static('./'));

app.use('/', express.static('./index.html'))

app.listen(3000, function () {
    console.log('Dino started on port 3000');
});
  