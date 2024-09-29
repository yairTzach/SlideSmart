// wait.js
document.addEventListener("DOMContentLoaded", function () {
    // Extract the filename from the URL
    const pathParts = window.location.pathname.split('/');
    const filename = pathParts[pathParts.length - 1]; // Assumes the filename is the last part of the URL

    function checkProcessingStatus() {
        // Make a request to check the processing status
        fetch("/check_status/" + filename)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'complete') {
                    // Enable the start button
                    const startButton = document.getElementById('startButton');
                    startButton.style.pointerEvents = 'auto';  // Enable the button
                    startButton.style.opacity = '1';           // Make the button fully visible
                    // Set the href to include the filename and start at question 1
                    startButton.href = '/questions/' + filename + '/1';

                    // Add event listener for the start button to trigger the countdown
                    startButton.addEventListener('click', function (event) {
                        event.preventDefault();  // Prevent immediate redirect
                        startCountdown(startButton.href);  // Start countdown before redirect
                    });

                } else if (data.status === 'failed') {
                    // Handle failure case, e.g., alert the user
                    alert('Processing failed. Please try again.');
                } else {
                    // If still processing, keep polling every 5 seconds
                    setTimeout(checkProcessingStatus, 5000);
                }
            })
            .catch(error => console.error('Error checking status:', error));
    }

    // Start polling after the page loads
    checkProcessingStatus();

    // Function to start countdown
    function startCountdown(redirectUrl) {
        let countdown = 5;
        const countdownElement = document.createElement('p');
        countdownElement.id = 'countdown';
        countdownElement.textContent = `Starting in: ${countdown}`;
        document.querySelector('.wait-wrapper').appendChild(countdownElement);

        const interval = setInterval(function () {
            countdown--;
            countdownElement.textContent = `Starting in: ${countdown}`;

            if (countdown === 0) {
                clearInterval(interval);
                window.location.href = redirectUrl;  // Redirect after countdown
            }
        }, 1000);
    }
});
