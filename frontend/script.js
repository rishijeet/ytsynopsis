let recognition;
let isRecording = false;

document.addEventListener('DOMContentLoaded', () => {
    // Safely get all elements with null checks
    const audioFileInput = document.getElementById('audioFile');
    const audioPlayer = document.getElementById('audioPlayer');
    const convertBtn = document.getElementById('convertBtn');
    const transcriptDiv = document.getElementById('transcript');
    const unsupportedWarning = document.getElementById('unsupportedWarning');
    const startBtn = document.getElementById('startBtn');
    const statusDiv = document.getElementById('status');

    // Verify all required elements exist
    if (!audioFileInput || !audioPlayer || !startBtn || !transcriptDiv || !statusDiv) {
        console.error("Critical elements missing from DOM!");
        return;
    }

    let recognition;
    let isTranscribing = false;
    let fullTranscript = '';
    let audioContext;
    let audioStream;
    let mediaStreamSource;

    // Check for Web Speech API support
    const isSupported = 'webkitSpeechRecognition' in window;
    if (!isSupported) {
        unsupportedWarning.classList.remove('hidden');
        statusDiv.textContent = "Your browser doesn't support live transcription. Try Chrome or Edge.";
    }

    // Initialize UI state
    resetUI();

    // Safe event listener binding
    audioFileInput?.addEventListener('change', handleFileSelect);
    startBtn?.addEventListener('click', toggleTranscription);
    audioPlayer?.addEventListener('play', handleAudioPlay);
    audioPlayer?.addEventListener('ended', handleAudioEnd);
    convertBtn?.addEventListener('click', async () => {
        const audioFile = audioFileInput.files[0];
        if (!audioFile) return;

        transcriptDiv.textContent = 'Processing... (Speak into microphone after starting)';
        convertBtn.disabled = true;

        try {
            if ('webkitSpeechRecognition' in window) {
                // Real transcription using microphone (limitation: can't process files directly)
                await transcribeWithMicrophone();
            } else {
                // Fallback simulation
                await simulateTranscription(audioFile);
            }
        } catch (error) {
            transcriptDiv.textContent = 'Error: ' + error.message;
        } finally {
            convertBtn.disabled = false;
        }
    });

    function handleFileSelect(e) {
        const file = e.target.files[0];
        if (!file || !file.type.startsWith('audio/')) {
            statusDiv.textContent = "Please select a valid audio file (MP3, WAV, etc.)";
            resetUI();
            return;
        }

        audioPlayer.src = URL.createObjectURL(file);
        audioPlayer.classList.remove('hidden');
        startBtn.disabled = false;
        statusDiv.textContent = "File loaded. Click 'Start Transcription' and play the audio.";
    }

    async function toggleTranscription() {
        if (startBtn.textContent === 'Start Transcription') {
            await startTranscription();
        } else {
            stopTranscription();
        }
    }

    async function startTranscription() {
        if (!('webkitSpeechRecognition' in window)) {
            statusDiv.textContent = "Live transcription requires Chrome/Edge.";
            simulateTranscription();
            return;
        }

        // Reset
        fullTranscript = '';
        transcriptDiv.textContent = '';
        isTranscribing = true;
        startBtn.textContent = 'Stop Transcription';
        statusDiv.textContent = "Starting transcription...";

        // Setup audio context
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        
        // Create recognition
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onresult = (event) => {
            let interimTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    fullTranscript += transcript + ' ';
                } else {
                    interimTranscript += transcript;
                }
            }

            transcriptDiv.innerHTML = `
                <strong>Full Transcript:</strong><br>${fullTranscript}
                ${interimTranscript ? `<br><em>Processing:</em> ${interimTranscript}` : ''}
            `;
            transcriptDiv.scrollTop = transcriptDiv.scrollHeight;
        };

        recognition.onerror = (event) => {
            statusDiv.textContent = `Error: ${event.error}`;
            stopTranscription();
        };

        recognition.onend = () => {
            if (isTranscribing) recognition.start();
        };

        recognition.start();
        audioPlayer.play().catch(e => {
            statusDiv.textContent = "Click the play button to start";
        });
    }

    function handleAudioPlay() {
        if (!recognition) return;
        statusDiv.textContent = "Transcribing live audio...";
    }

    function handleAudioEnd() {
        if (!recognition) return;
        statusDiv.textContent = "Audio playback complete. Final transcript below.";
        stopTranscription();
    }

    function stopTranscription() {
        isTranscribing = false;
        startBtn.textContent = 'Start Transcription';
        
        if (recognition) {
            recognition.stop();
            recognition = null;
        }
        
        if (audioContext) {
            audioContext.close();
            audioContext = null;
        }
    }

    function resetUI() {
        startBtn.disabled = true;
        startBtn.textContent = 'Start Transcription';
        audioPlayer.classList.add('hidden');
        audioPlayer.src = '';
        statusDiv.textContent = "Select an audio file to begin";
    }

    function simulateTranscription() {
        isTranscribing = true;
        startBtn.textContent = 'Stop Transcription';
        statusDiv.textContent = "Simulating transcription...";
        
        const phrases = [
            "This is a simulated full transcript.",
            "In a real implementation, you would see:",
            "1. The complete text of your audio file",
            "2. Word-by-word updates as the audio plays",
            "3. Punctuation and formatting",
            "4. Support for multiple languages"
        ];

        let i = 0;
        const interval = setInterval(() => {
            if (!isTranscribing || i >= phrases.length) {
                clearInterval(interval);
                return;
            }

            fullTranscript += phrases[i] + '\n\n';
            transcriptDiv.textContent = fullTranscript;
            transcriptDiv.scrollTop = transcriptDiv.scrollHeight;
            i++;
        }, 1500);
    }

    async function transcribeWithMicrophone() {
        return new Promise((resolve) => {
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.continuous = true;
            recognition.interimResults = true;

            recognition.onresult = (event) => {
                let interimTranscript = '';
                let finalTranscript = '';

                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        finalTranscript += transcript + ' ';
                    } else {
                        interimTranscript += transcript;
                    }
                }

                transcriptDiv.innerHTML = `<strong>Final:</strong> ${finalTranscript}<br><em>Interim:</em> ${interimTranscript}`;
            };

            recognition.onerror = (event) => {
                throw new Error(event.error);
            };

            recognition.onend = () => {
                resolve();
            };

            recognition.start();
        });
    }
});

async function processAudioWithSpeechAPI(audioBuffer) {
    return new Promise((resolve) => {
        if (!('webkitSpeechRecognition' in window)) {
            throw new Error('Web Speech API not supported. Use Chrome or Edge.');
        }

        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.continuous = true;
        recognition.interimResults = false;

        let transcript = '';

        // Mock processing (Web Speech API doesn't support direct file input)
        // In a real app, you'd stream the audio to the API (not trivial)
        setTimeout(() => {
            recognition.onresult = (event) => {
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    transcript += event.results[i][0].transcript + ' ';
                }
            };

            recognition.onend = () => {
                resolve(transcript || "Could not transcribe audio.");
            };

            recognition.start();
        }, 1000);
    });
}
