import express from 'express';
import bodyParser from 'body-parser';
import { diagnose } from './diagnosisModel'; // Assuming you have a diagnosis model

const app = express();
app.use(bodyParser.json());

app.post('/api/diagnose', async (req, res) => {
  const { symptoms } = req.body;

  if (!symptoms || !Array.isArray(symptoms)) {
    return res.status(400).json({ error: 'Symptoms are required and must be an array' });
  }

  try {
    const diagnosisResult = await diagnose(symptoms);
    res.json(diagnosisResult);
  } catch (error) {
    console.error('Error during diagnosis:', error);
    res.status(500).json({ error: 'An error occurred while processing the request' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});