document.addEventListener('DOMContentLoaded', function () {
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    var url = tabs[0].url;
    fetch('http://localhost:5000/process-url', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url })
    })
      .then(response => response.json())
      .then(data => {
        // Handle the processed data from the server
        console.log(data.all);
        // Display the processed data on the popup UI
        var a1 = document.getElementById('a1');
        a1.innerHTML = `<p>Website Certificate: ${data.SSL}</p>`
        var a2 = document.getElementById('a2');
        a2.innerHTML = `<p>Cookie Expires On: ${data.Cookie_Expiry_Date}</p>`
        var a3 = document.getElementById('a3');
        a3.innerHTML = ` <p> Safe Browsing: ${data.Google_Safe_Browsing}</p>`
        var a4 = document.getElementById('a4');
        a4.innerHTML = `<p>Users Choice: ${data.Crowd_Status}</p>`
        var a5 = document.getElementById('a5');
        a5.innerHTML = `<p>Privacy Policy(English): ${data.PRE}</p>`
        var a6 = document.getElementById('a6');
        a6.innerHTML = `<p>Privacy Policy(Hindi): ${data.PRH}</p>`
        var a7 = document.getElementById("a7");
        a7.innerHTML = `<p>Regulatory Compliance(English): ${data.RCE}</p>`
        var a8 = document.getElementById('a8');
        a8.innerHTML = `<p>Regulatory Compliance(Hindi): ${data.RCH}</p>`
        /*
        var all = document.getElementById("all");
        all.innerHTML = `<p>ALL:${data.all}</p>`
        */

        // Set progress bar color and width based on progress value
        var progressBar = document.getElementById("progress-value");
        var progressWidth;
        if (data.progress >= 1 && data.progress <= 4) {
          progressBar.className = "progress red";
          progressWidth = (data.progress / 4) * 33.33 + "%";
        } else if (data.progress > 4 && data.progress <= 7) {
          progressBar.className = "progress yellow";
          progressWidth = ((data.progress - 4) / 3) * 33.33 + "%";
        } else if(data.progress == 8){
          progressBar.className = "progress green";
          progressWidth = "80%";
        } else if(data.progress == 9){
          progressBar.className = "progress green";
          progressWidth = "90%";         
        }else if(data.progress == 10){
          progressBar.className = "progress green";
          progressWidth = "100%"; 
        }
        progressBar.style.width = progressWidth;

        // Add event listener to the review submit button
        document.getElementById("review-submit").addEventListener("click", function() {
          var reviewValue = document.querySelector('input[name="review"]:checked').value;
          // Send review value to the backend
          fetch('http://localhost:5000/store-review', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ review: reviewValue })
          })
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            console.log('Review stored successfully:', data);
            // Hide the review container
            document.getElementById("review-container").style.display = "none";
          })
          .catch(error => {
            console.error('Error storing review:', error);
          });
        });

      })
      .catch(error => {
        // Handle errors gracefully
        console.error('Error sending URL to server:', error);
      });
  });
});
