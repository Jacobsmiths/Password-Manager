
// Function to insert credentials into detected username and password fields
function insertCredentials(username, password) {
    const usernameFields = document.querySelectorAll('input[type="text"], input[type="email"]');
    const passwordFields = document.querySelectorAll('input[type="password"]');
  
    // Insert credentials into username fields
    usernameFields.forEach(field => {
      field.value = username;
    });
  
    // Insert credentials into password fields
    passwordFields.forEach(field => {
      field.value = password;
    });
}
window.addEventListener('load', () => {
    const usernameFields = document.querySelectorAll('input[type="text"], input[type="email"]');
    const passwordFields = document.querySelectorAll('input[type="password"]');
  
    // If username and password fields are found, insert credentials
    if (usernameFields.length > 0 && passwordFields.length > 0) {
      // Replace 'username' and 'password' with actual values or fetch from storage
    //   insertCredentials('username', 'password'); // Example usage
        chrome.runtime.sendMessage({ action: 'fetchData', data: userData });
    }
});



  // Listen for form submissions to capture credentials
// document.addEventListener('submit', (event) => {
//     event.preventDefault(); // Prevent default form submission

//     const form = event.target;
//     const usernameField = form.querySelector('input[type="text"]');
//     const passwordField = form.querySelector('input[type="password"]');

//     if (usernameField && passwordField) {
//         // Capture username and password when the form is submitted
//         const username = usernameField.value;
//         const password = passwordField.value;

//         // Send message to background script to store credentials
//         chrome.runtime.sendMessage({
//             action: 'storeCredentials',
//             username: username,
//             password: password
//         });

//         // Log captured credentials (for demonstration purposes)
//         console.log('Captured credentials:', username, password);
//     }
// });
  
  // Optional: Check for username and password fields on page load
//   window.addEventListener('load', () => {
    // const usernameFields = document.querySelectorAll('input[type="text"], input[type="email"]');
    // const passwordFields = document.querySelectorAll('input[type="password"]');
  
    // // If username and password fields are found, insert credentials
    // if (usernameFields.length > 0 && passwordFields.length > 0) {
    //   // Replace 'username' and 'password' with actual values or fetch from storage
    //   insertCredentials('username', 'password'); // Example usage
    // }
//   });
  