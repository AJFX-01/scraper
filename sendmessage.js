require('dotenv').config();
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');


// Get command-line arguments
const args = process.argv.slice(1);
const groupId = process.env.WHATSAPP_GROUP_ID;
const message = args[1];

if (!message) {
    console.error("Error: Group ID and message are required.");
    process.exit(1);
}

// Initialize the client with session management
const client = new Client({
    // authStrategy: new LocalAuth(),
    puppeteer: {
        headless: false, // Runs the browser in headless mode (no UI)
    },
});


client.on('qr', (qr) => {
    console.log('Please scan this QR code to authenticate:');
    qrcode.generate(qr, { small: true });
});

client.on('ready', async () => {
    console.log('Client is ready!');
    try {
        // Send the message to the specified group
        const res = await client.sendMessage(groupId, message);

        if(res) {
            console.log(`Message sent to group: ${groupId}`);
        } else {
            comsole.log('an error occured');
        }
        // process.exit(0); // Exit the script after sending the message
    } catch (err) {
        console.error(`Failed to send message: ${err.message}`);
        process.exit(1);
    }
});

client.on('auth_failure', (msg) => {
    console.error('Authentication failed:', msg);
});

client.on('disconnected', () => {
    console.log('Client was logged out. Please re-scan the QR code.');
    process.exit(1);
});

client.initialize();

// const { Client } = require('whatsapp-web.js');
// const qrcode = require('qrcode-terminal');
// const fs = require('fs');

// const client = new Client({
//     puppeteer: {
//         headless: false, // Runs the browser in headless mode (no UI)
//     },
// });

// client.on('qr', (qr) => {
//     qrcode.generate(qr, { small: true });
// });

// client.on('ready', async () => {
//     console.log('Client is ready!');

//     // Fetch chats and list group names
//     try {
//       // Fetch chats and list group names
//       console.log('Client is ready2!');
//       const chats = await client.getChats();
//       console.log(chats);
//       // fs.write(chats, { small: true }, "chats.json");
//       fs.writeFileSync("chats.json", JSON.stringify(chats), 'utf8');
//       console.log('Client is ready2!');
//       chats.forEach((chat) => {
//           if (chat.isGroup) {
//               console.log(`Group Name: ${chat.name}, Group ID: ${chat.id._serialized}`);
//           }
//       });
//   } catch (error) {
//       console.error('An error occurred while fetching chats:', error);
//   }
// });

// client.initialize();


