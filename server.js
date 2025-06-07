
const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');

const app = express();
app.use(express.json());
app.use(cors());
app.use(express.static('public'));

app.post('/ask', (req, res) => {
  const question = req.body.question;
  exec(`python knowledge_base.py "${question}"`, (error, stdout) => {
    if (error) return res.status(500).send('Server error.');
    res.send({ answer: stdout.trim() });
  });
});

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});
