async function playAudio(audioUrl) {

    try {
        // Create an AudioContext
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();

        // Fetch the AAC audio data
        const response = await fetch(audioUrl);
        if(!response.ok) {
            throw new Error('Network response was '+response.status);
        }
        const audioData = await response.arrayBuffer();

        // Decode the audio data
        const audioBuffer = await audioContext.decodeAudioData(audioData);

        // Create a buffer source
        const source = audioContext.createBufferSource();
        source.buffer = audioBuffer;

        // Connect the source to the audio context's destination
        source.connect(audioContext.destination);

        // Start playback
        source.start();
    } catch (error) {
        console.error('Error during playback:', error);
    }
}