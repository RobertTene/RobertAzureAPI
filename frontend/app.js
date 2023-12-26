import express from 'express';
import axios from 'axios';
const app = express();
const port = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files (like HTML, CSS, JS for frontend)
app.use(express.static('public'));

// Example route to trigger provisioning from the frontend
app.post('/provision-vm', async (req, res) => {
    try {
        const orderData = req.body; // Assuming order data is sent in request body
        const response = await axios.post('http://localhost:8000/provision', { order: orderData });
        res.json(response.data);
    } catch (error) {
        console.error('Error in provisioning VM:', error);
        res.status(500).send('Error in provisioning VM');
    }
});

app.listen(port, () => {
    console.log(`Node.js server running at http://localhost:${port}`);
});
