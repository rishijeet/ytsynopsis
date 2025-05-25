// File upload interaction
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const fileName = document.getElementById('fileName');
    const uploadForm = document.getElementById('uploadForm');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.querySelector('.progress-bar');
    const progressText = document.getElementById('progressText');

    // Update filename display
    fileInput.addEventListener('change', function(e) {
        fileName.textContent = e.target.files[0]?.name || 'Choose an MP3 file';
    });

    // AJAX upload with animated progress
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        progressContainer.style.display = 'block';
        progressBar.style.width = '0%';
        progressText.textContent = '0%';

        // Simulate progress (polling)
        const simulateProgress = async () => {
            let progress = 0;
            const interval = setInterval(async () => {
                progress += 5;
                if (progress > 100) progress = 100;
                
                gsap.to(progressBar, {
                    width: `${progress}%`,
                    duration: 0.3,
                    onUpdate: () => {
                        progressText.textContent = `${progress}%`;
                    }
                });

                if (progress === 100) {
                    clearInterval(interval);
                    // Submit the form after progress completes
                    uploadForm.submit();
                }
            }, 300);  // Update every 300ms
        };

        await simulateProgress();
    });

    // Copy transcript to clipboard
    if (document.getElementById('transcriptText')) {
        window.copyToClipboard = function() {
            const transcriptEl = document.getElementById('transcriptText');
            
            // Fallback if innerText doesn't work
            const textToCopy = transcriptEl.innerText || transcriptEl.textContent;
            
            if (!textToCopy || textToCopy.trim() === "Transcription Complete") {
                alert("No transcript text found to copy");
                return;
            }

            navigator.clipboard.writeText(textToCopy)
                .then(() => {
                    const copyBtn = document.querySelector('.copy-btn');
                    const originalHtml = copyBtn.innerHTML;
                    copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                    
                    setTimeout(() => {
                        copyBtn.innerHTML = originalHtml;
                    }, 2000);
                })
                .catch(err => {
                    console.error('Copy failed:', err);
                    // Fallback for browsers that don't support clipboard API
                    const range = document.createRange();
                    range.selectNode(transcriptEl);
                    window.getSelection().removeAllRanges();
                    window.getSelection().addRange(range);
                    document.execCommand('copy');
                    window.getSelection().removeAllRanges();
                    alert('Text copied to clipboard!');
                });
        };
    }
});

function resetProgress() {
    gsap.to(progressBar, {
        width: '0%',
        duration: 0.5
    });
    progressText.textContent = '0%';
}

// Replace the XHR logic with this:
const eventSource = new EventSource('/transcribe');
eventSource.onmessage = function(e) {
    const percent = parseInt(e.data);
    gsap.to(progressBar, {
        width: `${percent}%`,
        duration: 0.3,
        onUpdate: () => {
            progressText.textContent = `${percent}%`;
        }
    });
    if (percent === 100) {
        eventSource.close();
        window.location.href = "/result";  // Redirect when done
    }
};

document.querySelector('form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const youtubeUrl = formData.get('youtube_url');
    
    try {
        // Show loading state
        document.getElementById('progressContainer').style.display = 'block';
        
        const response = await fetch('/transcribe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `youtube_url=${encodeURIComponent(youtubeUrl)}`
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Transcription failed");
        }

        const result = await response.text();
        document.open();
        document.write(result);
        document.close();
        
    } catch (error) {
        console.error('Error:', error);
        showErrorToast(error.message);  // Implement this UI function
    } finally {
        // Hide loading state
        document.getElementById('progressContainer').style.display = 'none';
    }
});

// static/script.js - Ensure proper form encoding
async function submitForm() {
  const formData = new URLSearchParams();
  formData.append('youtube_url', youtubeUrlInput.value);
  
  const response = await fetch('/transcribe', {
    method: 'POST',
    body: formData,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    }
  });
}
