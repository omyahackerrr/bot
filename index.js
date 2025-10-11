const express = require('express');
const app = express();
app.get('/', (req, res) => res.send('TeraBox Archive Bot is running.'));
app.listen(process.env.PORT || 3000);

