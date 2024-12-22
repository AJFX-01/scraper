// const { Client, LocalAuth } = require('whatsapp-web.js');

// // Get command-line arguments
// const args = process.argv.slice(2);
// const groupId = args[0];
// const message = args[1];

// if (!groupId || !message) {
//     console.error("Error: Group ID and message are required.");
//     process.exit(1);
// }

// // Initialize the client with session management
// const client = new Client({
//     authStrategy: new LocalAuth()
// });

// client.on('qr', (qr) => {
//     console.log('Please scan this QR code to authenticate:');
//     const qrcode = require('qrcode-terminal');
//     qrcode.generate(qr, { small: true });
// });

// client.on('ready', async () => {
//     console.log('Client is ready!');
//     try {
//         // Send the message to the specified group
//         await client.sendMessage(groupId, message);
//         console.log(`Message sent to group: ${groupId}`);
//         process.exit(0); // Exit the script after sending the message
//     } catch (err) {
//         console.error(`Failed to send message: ${err.message}`);
//         process.exit(1);
//     }
// });

// client.on('auth_failure', (msg) => {
//     console.error('Authentication failed:', msg);
// });

// client.on('disconnected', () => {
//     console.log('Client was logged out. Please re-scan the QR code.');
//     process.exit(1);
// });

// client.initialize();

const { Client } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const client = new Client({
    puppeteer: {
        headless: true, // Runs the browser in headless mode (no UI)
    },
});

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
});

client.on('ready', async () => {
    console.log('Client is ready!');

    // Fetch chats and list group names
    const chats = await client.getChats();
    chats.forEach((chat) => {
        if (chat.isGroup) {
            console.log(`Group Name: ${chat.name}, Group ID: ${chat.id._serialized}`);
        }
    });
});

client.initialize();


