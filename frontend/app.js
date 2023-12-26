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
        const usersApiUrl = 'http://localhost:8080/users';
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


app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
