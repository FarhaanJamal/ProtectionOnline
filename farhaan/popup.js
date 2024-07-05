document.addEventListener('DOMContentLoaded', function () {

  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    var currentTab = tabs[0];
    var url = currentTab.url;


    var reviewSubmitButton = document.getElementById('review-submit');
  if (reviewSubmitButton) {
    console.log('Review submit button found');
    reviewSubmitButton.addEventListener('click', function () {
      submitReview();
    });
  } else {
    console.error('Review submit button not found');
  }

    // Send the URL to the Flask backend
    fetch('http://localhost:5000/receive_url', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: url }),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Response from server:', data);

        // Retrieve each variable from the Flask backend
        fetch('http://localhost:5000/get_sslc')
        .then(response => response.json())
        .then(sslcData => {
          var sslcStatus = sslcData.SSLC;
          var sslHeading = document.getElementById('sslHeading');
          var sslTextContainer = document.getElementById('sslText');
    
          // Display text in different colors based on the status
          if (sslcStatus === 0) {
            sslTextContainer.textContent = ' Valid';
            sslTextContainer.style.color = 'green';
          } else if (sslcStatus === 1) {
            sslTextContainer.textContent = ' Warning';
            sslTextContainer.style.color = 'orange';
          } else if (sslcStatus === 2) {
            sslTextContainer.textContent = ' Invalid';
            sslTextContainer.style.color = 'red';
          } else {
            sslTextContainer.textContent = ' Unknown Status';
            sslTextContainer.style.color = 'black';  // Set default color for unknown status
          }
        })
        .catch(error => {
          console.error('Error fetching SSL Certification status:', error);
        });
          fetch('http://localhost:5000/get_safe_browsing_status')
    .then(response => response.json())
    .then(safeBrowsingStatusData => {
      var safeBrowsingStatus = safeBrowsingStatusData.Google_Safe_Browsing_Status;
      var safeBrowsingHeading = document.getElementById('safeBrowsingHeading');
      var safeBrowsingTextContainer = document.getElementById('safeBrowsingText');

      // Display text in different colors based on the status
      if (safeBrowsingStatus === 0) {
        safeBrowsingTextContainer.textContent = ' Safe';
        safeBrowsingTextContainer.style.color = 'green';
      } else if (safeBrowsingStatus === 1) {
        safeBrowsingTextContainer.textContent = ' Warning';
        safeBrowsingTextContainer.style.color = 'orange';
      } else if (safeBrowsingStatus === 2) {
        safeBrowsingTextContainer.textContent = ' Unsafe';
        safeBrowsingTextContainer.style.color = 'red';
      } else {
        safeBrowsingTextContainer.textContent = ' Unknown Status';
        safeBrowsingTextContainer.style.color = 'black';  // Set default color for unknown status
      }
    })
    .catch(error => {
      console.error('Error fetching Google Safe Browsing status:', error);
    });

        // fetch('http://localhost:5000/get_blacklist')
        //   .then(response => response.json())
        //   .then(blacklistData => {
        //     document.getElementById('blacklist').textContent = `Blacklist or Not: ${blacklistData.Blacklist_or_not}`;
        //   })
        //   .catch(error => {
        //     console.error('Error fetching Blacklist:', error);
        //   });
        
        fetch('http://localhost:5000/expiry')
          .then(response => response.json())
          .then(expiryData => {
            document.getElementById('expiry').textContent = `Cookie Expires On: ${expiryData.Expiry}`;
          })
          .catch(error => {
            console.error('Error fetching Blacklist:', error);
          });

          fetch('http://localhost:5000/get_crowd_source_info')
          .then(response => response.json())
          .then(crowdSourceInfoData => {
            var crowdSourceInfoContainer = document.getElementById('crowd-source-info');
            if (crowdSourceInfoContainer) {
              crowdSourceInfoContainer.textContent = `Crowd Source Voting: ${crowdSourceInfoData.crowd_source_info}`;
            }
          })
          .catch(error => {
            console.error('Error fetching crowd_source_info:', error);
          });

    // Fetch and update progress information
    fetch('http://localhost:5000/get_progress')
      .then(response => response.json())
      .then(progressData => {
        var progressBar = document.getElementById('progress-value');
        var progress = progressData.progress;

        progressBar.style.width = (progress * 10) + '%';

        progressBar.className = 'progress';
        if (progress < 4) {
          progressBar.classList.add('red');
        } else if (progress >= 4 && progress < 7) {
          progressBar.classList.add('yellow');
        } else {
          progressBar.classList.add('green');
        }
      })
      .catch(error => {
        console.error('Error fetching progress:', error);
      });
  });
});
function submitReview() {
  // Get the selected review value
  var reviewValue = document.querySelector('input[name="review"]:checked');
  if (reviewValue) {
    // Send the selected review to the Flask backend
    fetch('http://localhost:5000/submit_review', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ review: reviewValue.value }),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Review submitted:', data);

        // Hide the review container after submission
        var reviewContainer = document.getElementById('review-container');
        if (reviewContainer) {
          reviewContainer.style.display = 'none';
        }
      })
      .catch(error => {
        console.error('Error submitting review:', error);
      });
  } else {
    console.error('No review selected');
  }
}
fetch('http://localhost:5000/get_privacy')
    .then(response => response.json())
    .then(privacyData => {
      var privacyTextContainer = document.getElementById('privacy-text');
      privacyTextContainer.textContent = privacyData.Privacy;
    })
    .catch(error => {
      console.error('Error fetching Privacy information:', error);
    });
  // Fetch and update reg_text information
  fetch('http://localhost:5000/get_reg_text')
    .then(response => response.json())
    .then(regTextData => {
      var regTextContainer = document.getElementById('reg-text');
      if (regTextContainer) {
        regTextContainer.textContent = ` ${regTextData.reg_text}`;
      }
    })
    .catch(error => {
      console.error('Error fetching reg_text:', error);
    });
});