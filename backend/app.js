const express = require('express');
const tf = require('@tensorflow/tfjs-node');  // Use @tensorflow/tfjs-node for better performance
const path = require('path');
const app = express();
const PORT = 5000;
const cors = require('cors');
app.use('/models', express.static(path.join(__dirname, 'models')));


app.use(express.json());

app.use(cors({
    origin: 'https://5173-neeraj10122004-medihelp-44vvu9arfl4.ws-us117.gitpod.io',
    credentials: true,
}));

// Serve model files statically
app.use('/models', express.static(path.join(__dirname, 'models')));

app.post('/submit', async (req, res) => {
  const { matrix } = req.body;
  console.log('Received Matrix:', matrix);

  // Flatten the matrix to a 1D array
  const flattenedArray = matrix.flat();
  console.log('Flattened Matrix:', flattenedArray);
  console.log(flattenedArray.length);

  try {
    // Load the model (change path if serving from static directory)
    const model = await tf.loadLayersModel('http://localhost:5000/models/model.json');


    // Ensure tensor shape matches model input requirements
    const inputTensor = tf.tensor(flattenedArray, [1, flattenedArray.length]);  // Adjust as per model's expected shape

    // Make predictions
    const predictions = model.predict(inputTensor);

    // Convert predictions to JavaScript array
    const predictionsArray = predictions.arraySync(); 

    // Send predictions as JSON response
    res.json({ predictions: predictionsArray });

  } catch (error) {
    console.error('Error during prediction:', error);
    res.status(500).json({ error: 'An error occurred while processing your request.' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
