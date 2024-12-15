const express = require('express');
const app = express();
const PORT = 5000;

app.use(express.json());

app.post('/submit', (req, res) => {
  const { matrix } = req.body;
  console.log('Received Matrix:', matrix);
  res.json({ message: 'Matrix received successfully!' });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
