/**
 * Voice Recorder for Fikra - Ideas Store
 * Uses the MediaRecorder Web API to record audio and attach it to the form.
 */

(function() {
    'use strict';

    let mediaRecorder = null;
    let audioChunks = [];
    let audioBlob = null;
    let timerInterval = null;
    let startTime = null;

    // DOM Elements
    const btnRecord = document.getElementById('btn-record');
    const recIcon = document.getElementById('rec-icon');
    const recText = document.getElementById('rec-text');
    const recIndicator = document.getElementById('rec-indicator');
    const recTimer = document.getElementById('rec-timer');
    const voicePlayback = document.getElementById('voice-playback');
    const voiceAudio = document.getElementById('voice-audio');
    const btnRemoveVoice = document.getElementById('btn-remove-voice');
    const voiceFileInput = document.getElementById('voice-file-input');
    const ideaForm = document.getElementById('idea-form');

    if (!btnRecord) return; // Guard — only run on pages with the recorder

    // Check for MediaRecorder support
    const isRecordingSupported = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia && window.MediaRecorder);

    if (!isRecordingSupported) {
        btnRecord.innerHTML = '<span class="text-sm text-stone-400">🎙️ Upload audio file</span>';
        btnRecord.onclick = function() {
            voiceFileInput.click();
        };
        voiceFileInput.classList.remove('hidden');
        voiceFileInput.style.display = 'none';
        voiceFileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                const url = URL.createObjectURL(this.files[0]);
                voiceAudio.src = url;
                voicePlayback.classList.remove('hidden');
                btnRemoveVoice.classList.remove('hidden');
            }
        });
        return;
    }

    let isRecording = false;

    btnRecord.addEventListener('click', async function() {
        if (!isRecording) {
            await startRecording();
        } else {
            stopRecording();
        }
    });

    async function startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    sampleRate: 44100
                }
            });

            // Determine supported MIME type
            let mimeType = 'audio/webm;codecs=opus';
            if (!MediaRecorder.isTypeSupported(mimeType)) {
                mimeType = 'audio/webm';
            }
            if (!MediaRecorder.isTypeSupported(mimeType)) {
                mimeType = 'audio/ogg;codecs=opus';
            }
            if (!MediaRecorder.isTypeSupported(mimeType)) {
                mimeType = ''; // Fallback to default
            }

            const options = mimeType ? { mimeType } : {};
            mediaRecorder = new MediaRecorder(stream, options);
            audioChunks = [];

            mediaRecorder.ondataavailable = function(event) {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = function() {
                const finalMimeType = mediaRecorder.mimeType || 'audio/webm';
                audioBlob = new Blob(audioChunks, { type: finalMimeType });
                const audioUrl = URL.createObjectURL(audioBlob);
                voiceAudio.src = audioUrl;
                voicePlayback.classList.remove('hidden');
                btnRemoveVoice.classList.remove('hidden');

                // Stop all tracks
                stream.getTracks().forEach(track => track.stop());
            };

            mediaRecorder.start(100); // Collect data every 100ms
            isRecording = true;

            // Update UI
            recIcon.textContent = '⏹️';
            recText.textContent = getTranslation('stop');
            btnRecord.classList.add('bg-red-50', 'border-red-300', 'text-red-600');
            btnRecord.classList.remove('bg-sand-100', 'border-sand-300', 'text-stone-600');
            recIndicator.classList.remove('hidden');
            recIndicator.classList.add('flex');

            // Start timer
            startTime = Date.now();
            timerInterval = setInterval(updateTimer, 1000);

        } catch (err) {
            console.error('Microphone access denied:', err);
            alert(getTranslation('micError'));
        }
    }

    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
        }
        isRecording = false;

        // Update UI
        recIcon.textContent = '🎙️';
        recText.textContent = getTranslation('reRecord');
        btnRecord.classList.remove('bg-red-50', 'border-red-300', 'text-red-600');
        btnRecord.classList.add('bg-sand-100', 'border-sand-300', 'text-stone-600');
        recIndicator.classList.add('hidden');
        recIndicator.classList.remove('flex');

        // Stop timer
        clearInterval(timerInterval);
    }

    function updateTimer() {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        recTimer.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }

    // Remove voice
    if (btnRemoveVoice) {
        btnRemoveVoice.addEventListener('click', function() {
            audioBlob = null;
            audioChunks = [];
            voiceAudio.src = '';
            voicePlayback.classList.add('hidden');
            btnRemoveVoice.classList.add('hidden');
            recIcon.textContent = '🎙️';
            recText.textContent = getTranslation('record');
            voiceFileInput.value = '';
        });
    }

    // Attach audio blob to form on submit
    if (ideaForm) {
        ideaForm.addEventListener('submit', function(e) {
            if (audioBlob) {
                // Create a File from the blob and attach it
                const extension = audioBlob.type.includes('ogg') ? 'ogg' : 'webm';
                const audioFile = new File(
                    [audioBlob],
                    `voice_note_${Date.now()}.${extension}`,
                    { type: audioBlob.type }
                );

                // Create a DataTransfer to set the file input
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(audioFile);
                voiceFileInput.files = dataTransfer.files;
            }
        });
    }

    // Translation helper
    function getTranslation(key) {
        const lang = document.documentElement.lang || 'ar';
        const translations = {
            record: { ar: 'تسجيل', en: 'Record' },
            stop: { ar: 'إيقاف', en: 'Stop' },
            reRecord: { ar: 'إعادة التسجيل', en: 'Re-record' },
            micError: {
                ar: 'لم يتم السماح بالوصول إلى الميكروفون. يرجى السماح بالوصول من إعدادات المتصفح.',
                en: 'Microphone access denied. Please allow access from browser settings.'
            }
        };
        return (translations[key] && translations[key][lang]) || translations[key]?.en || key;
    }

})();
