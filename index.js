require('dotenv').config();
const { Client } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const bodyParser = require('body-parser');

const client = new Client({
    puppeteer: {
        headless: true,
    },
});

const app = express();
app.use(bodyParser.json());

const groupId = process.env.WHATSAPP_GROUP_ID;
const PORT = process.env.PORT;


// Generate QR Code
client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
});

// Ready event
client.on('ready', () => {
    console.log('WhatsApp Client is ready!');
});

// Endpoint to receive messages from Python
app.post('/send', async (req, res) => {
    const { message } = req.body; // Replace with your group's ID

    try {
        await client.sendMessage(groupId, message);
        console.log('Message sent:', message);
        res.status(200).send('Message sent successfully');
    } catch (error) {
        console.error('Error sending message:', error);
        res.status(500).send('Error sending message');
    }
});

// Start the Express server
app.listen(PORT, () => {
    console.log(`Node.js server is running on port ${PORT}`);
});

// Initialize WhatsApp client
client.initialize();
