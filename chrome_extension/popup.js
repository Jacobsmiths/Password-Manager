

document.getElementById('userForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    const userData = {username, password};
  
    // Send the user data to the background script
    chrome.runtime.sendMessage({ action: 'fetchData', data: userData });
});



// const path = require('path');

// document.addEventListener('DOMContentLoaded', function() {
//     // creates the save button
//     const saveButton = document.getElementById('save');
//     let masterKey;

//     //creates inputs and adds function for when submit button is clicked
//     saveButton.addEventListener('click', function() {
//         const passwordInput = document.getElementById('password');
//         const usernameInput = document.getElementById('username'); 

//         if(checkUserFileExists(usernameInput)) {
//             log('userExists')
//         }

             
//     //     chrome.storage.sync.set({userPreference: preference}, function() {
//     //     console.log('User preference saved from popup');
//     //   });
//     });

//     function checkUserFileExists(username) {
//         // Check if username input is not empty
//         if (!username) {
//             return false;
//         }
//         // Construct the file name
//         let sanitizedUsername = username.replace(/\s/g, '_');
    
//         // Construct the filename
//         let fileName = `${sanitizedUsername}_data.json`;
//         // Construct the full file path
//         const filePath = `../data/${sanitizedUsername}_data.json`;
    
//         // Check if file exists synchronously (you can also use asynchronous fs.exists() if preferred)
//         try {
//             fs.accessSync(filePath, fs.constants.F_OK);  // Check if file exists
//             return true;  // File exists
//         } catch (err) { return false; }
//     }

//     // async function deriveKey(masterPassword, salt) {
//     //     // Convert the password and salt to Uint8Array
//     //     const enc = new TextEncoder();
//     //     const passwordInBytes = enc.encode(masterPassword);
//     //     const saltInBytes = enc.encode(salt);
    
//     //     // Import the password as a key
//     //     const keyMaterial = await window.crypto.subtle.importKey(
//     //         "raw", 
//     //         passwordInBytes, 
//     //         { name: "PBKDF2" }, 
//     //         false, 
//     //         ["deriveKey"]
//     //     );
    
//     //     // Derive a key using PBKDF2
//     //     const derivedKey = await window.crypto.subtle.deriveKey(
//     //         {
//     //             name: "PBKDF2",
//     //             salt: saltInBytes,
//     //             iterations: 100000,
//     //             hash: "SHA-256"
//     //         },
//     //         keyMaterial,
//     //         { name: "AES-GCM", length: 256 }, // Example usage: deriving an AES-GCM key
//     //         true, // Whether the key is extractable
//     //         ["encrypt", "decrypt"]
//     //     );
    
//     //     // Export the derived key to a raw format
//     //     const rawKey = await window.crypto.subtle.exportKey("raw", derivedKey);
    
//     //     return new Uint8Array(rawKey);
//     // }
    

//     // function sha256Hex(password, salt) {
//     //     var hash = sha256.create();
//     //     hash.update(password+salt);
//     //     hash.hex();

//     //     const hash = crypto.createHash('sha256');
//     //     hash.update(password + salt, 'utf8');
//     //     return hash.digest('hex');
//     // }
  
//     // chrome.storage.sync.get(['userPreference'], function(result) {
//     //   if (result.userPreference) {
//     //     inputField.value = result.userPreference;
//     //   }
//     // });
//   });