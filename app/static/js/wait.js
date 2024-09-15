    // wait.js
    document.addEventListener("DOMContentLoaded", function () {
        // Extract the filename from the URL
        const filename = window.location.pathname.split('/').pop(); // Assumes the filename is passed in the URL

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
                    } else if (data.status === 'failed') {
                        // Handle failure case, e.g., alert the user
                        alert('Processing failed. Please try again.');
                    } else {
                        // If still processing, keep polling every 5 seconds
                        setTimeout(checkProcessingStatus, 25000);
                    }
                })
                .catch(error => console.error('Error checking status:', error));
        }

        // Start polling after the page loads
        checkProcessingStatus();
    });
