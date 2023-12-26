const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const port = 3000;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, '/views'));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
    res.render('index');
});

app.get('/users', async (req, res) => {
    try {
        const usersApiUrl = 'http://localhost:8000/users';
        const response = await axios.get(usersApiUrl);
        const users = response.data;

        res.render('users', { users });
    } catch (error) {
        console.error('Error fetching users:', error);
        res.status(500).send('Error fetching user data');
    }
});

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

app.get('/orders', async (req, res) => {
    try {
        // Replace 'http://localhost:8000/orders' with the actual URL of your FastAPI server
        const ordersApiUrl = 'http://localhost:8000/orders';
        const response = await axios.get(ordersApiUrl);
        const orders = response.data;

        // Render the orders page with the fetched data
        res.render('orders', { orders });
    } catch (error) {
        console.error('Error fetching orders:', error);
        res.status(500).send('Error fetching orders');
    }
});


app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
