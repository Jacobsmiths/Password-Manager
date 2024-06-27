

chrome.runtime.onInstalled.addListener(() => {
  chrome.action.setBadgeText({ text: 'OFF' });
});

chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
  if(message.action === 'fetchUserData') {
    const { username, password } = message.data;
    const url = 'http://localhost:8080/verify_user';
    
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('Server response:', data);
      // Handle the response from the server as needed
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
      // Handle errors appropriately
    });
    const response =  fetch(`http://localhost:8080/verifyUser`); //get_data?username=${username}&password=${password}
    const data =  response.json();

    if (response.ok) {
      chrome.action.setBadgeText({ text: message.text });
    }
  } 
  else if(message === "other"){
    
  }

});

// chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
//   if (message.action === 'fetchData') {
//     const { username, password } = message.data;

    
// });

// function insertCredentials(username, password) {
//   // Logic to insert the credentials into the webpage's form fields
//   const usernameField = document.querySelector('input[name="username"]');
//   const passwordField = document.querySelector('input[name="password"]');

//   if (usernameField && passwordField) {
//     usernameField.value = username;
//     passwordField.value = password;
//   } else {
//     console.error('Username or password field not found');
//   }
// }

// // Handle the data, e.g., insert it into the current tab
// const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
// chrome.scripting.executeScript({
//   target: { tabId: tab.id },
//   function: insertCredentials,
//   args: [data.username, data.password]
// });
// } else {
// console.error('Failed to fetch data:', data.error);
// }
// } catch (error) {
// console.error('Error fetching data:', error);
// }
