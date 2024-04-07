const OpenAI = require('openai');

const openai = new OpenAI({ apiKey: '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', dangerouslyAllowBrowser: true });

const fs = window.require('fs');

let audioElement = new Audio();

async function tts() {
    const response = await openai.audio.speech.create({
      model: 'tts-1',
      voice: 'alloy',
      input: 'こんにちは！ 你好！',
    });
  
    // Assuming the response has a property that gives you access to the MP3 data as an ArrayBuffer
    const buffer = Buffer.from(await response.arrayBuffer());
  
    // Convert the Node.js buffer into an ArrayBuffer for the Blob constructor
    const arrayBuffer = new Uint8Array(buffer).buffer;
  
    // Create a blob from the ArrayBuffer
    const blob = new Blob([arrayBuffer], { type: 'audio/mp3' });
  
    // Create an object URL for the blob
    const audioUrl = URL.createObjectURL(blob);
  
    // Create an audio element and set its source to the object URL
    audioElement = new Audio(audioUrl);
  
    // Play the audio
    audioElement.play();
  
    // Optional: Revoke the object URL after playing to release resources
    audioElement.onended = function() {
      URL.revokeObjectURL(audioUrl);
    };
  }

let noise = new SimplexNoise();
const area = document.getElementById("visualiser");

let audioRecorder;
let audioData = []; // This array will store the recorded audio chunks
let isRecording = false; // A flag to check recording status

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    console.log('MediaDevices API and getUserMedia supported.');
} else {
    console.log('MediaDevices API or getUserMedia not supported in this browser.');
}

// Function to start recording
function startRecording(stream) {
    audioRecorder = new MediaRecorder(stream);
    audioRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
            audioData.push(event.data);
        }
    };
    audioRecorder.onstop = () => {
        // Combine the audio chunks into a single Blob
        let audioBlob = new Blob(audioData, { 'type' : 'audio/wav; codecs=opus' });
        // Do something with the Blob (e.g., create an audio URL for playback)
        // let audioUrl = URL.createObjectURL(audioBlob);
        // console.log('Recording stopped, audio available at:', audioUrl);
        asr(audioBlob);
        // Reset the audio data array for the next recording
        audioData = [];
    };
    audioRecorder.start();
    console.log('Recording started');
}

const { Readable } = require('stream');


async function asr(audioBlob) {
    const arrayBuffer = await audioBlob.arrayBuffer();
    const readableStream = Readable.from(arrayBuffer);
    console.log(readableStream);

    // const transcription = await openai.audio.transcriptions.create({
    //   file: stream,
    //   model: "whisper-1",
    // });
  
    // console.log(transcription.text);
}

let light;

area.addEventListener('click', () => {
    // Get the element you want to check
    const element = document.getElementById('visualiser');

    // Get the computed style of the element
    const computedStyle = window.getComputedStyle(element);

    // Check the value of -webkit-app-region property
    const appRegionValue = computedStyle.getPropertyValue('-webkit-app-region');

    if (appRegionValue !== 'drag' && !isRecording) {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(startRecording)
            .catch((err) => {
                console.error('Could not start recording:', err);
            });
        light.color.setHex(0xccccff);
        console.log(light.color);
        isRecording = true;
    } else {
        if (audioRecorder) {
            audioRecorder.stop();
            console.log('Recording stopped by user');
            light.color.setHex(0x6666ff);
            isRecording = false;
        }
    }
    console.log(audio)
    if (audio.paused) {
        audio.play()
        label.style.display = "none"
    } else {
        audio.pause()
        label.style.display = "flex"
    }

    // tts();
})

async function ocr(audioUrl) {
    const transcription = await openai.audio.transcriptions.create({
      file: fs.createReadStream(audioUrl),
      model: "whisper-1",
    });
  
    console.log(transcription);
}

startVis()

function clearScene() {
    const canvas = area.firstElementChild;
    area.removeChild(canvas);
}

function startVis() {
    const context = new AudioContext();
    const src = context.createMediaElementSource(audioElement);
    // const src = context.createMediaElementSource(audio);
    const analyser = context.createAnalyser();
    src.connect(analyser);
    analyser.connect(context.destination);
    analyser.fftSize = 512;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(80, window.innerWidth / window.innerHeight, 0.1, 100);
    camera.position.z = 60;
    scene.add(camera);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    //   renderer.setClearColor("#ffffff");
    renderer.setClearColor(0x000000, 0);

    area.appendChild(renderer.domElement);
    const geometry = new THREE.IcosahedronGeometry(20, 3);
    const material = new THREE.MeshLambertMaterial({
        color: "#00e6e6",
        wireframe: true
    });
    const sphere = new THREE.Mesh(geometry, material);

    //   const axesHelper = new THREE.AxesHelper( 5 );
    //   scene.add( axesHelper );

    light = new THREE.DirectionalLight("#6666ff");
    light.position.set(0, 50, 100);
    scene.add(light)
    scene.add(sphere)

    window.addEventListener('resize', () => {
        renderer.setSize(window.innerWidth, window.innerHeight);
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
    });

    function render() {
        analyser.getByteFrequencyData(dataArray);

        const lowerHalf = dataArray.slice(0, (dataArray.length / 2) - 1);
        const upperHalf = dataArray.slice((dataArray.length / 2) - 1, dataArray.length - 1);

        const lowerMax = max(lowerHalf);
        const upperAvg = avg(upperHalf);

        const lowerMaxFr = lowerMax / lowerHalf.length;
        const upperAvgFr = upperAvg / upperHalf.length;

        sphere.rotation.x += 0.001;
        sphere.rotation.y += 0.003;
        sphere.rotation.z += 0.005;

        WarpSphere(sphere, modulate(Math.pow(lowerMaxFr, 0.8), 0, 1, 0, 8), modulate(upperAvgFr, 0, 1, 0, 4));
        requestAnimationFrame(render);
        renderer.render(scene, camera)
    }

    function WarpSphere(mesh, bassFr, treFr) {
        mesh.geometry.vertices.forEach(function (vertex, i) {
            var offset = mesh.geometry.parameters.radius;
            var amp = 5;
            var time = window.performance.now();
            vertex.normalize();
            var rf = 0.00001;
            var distance = (offset + bassFr) + noise.noise3D(vertex.x + time * rf * 4, vertex.y + time * rf * 6, vertex.z + time * rf * 7) * amp * treFr * 2;
            vertex.multiplyScalar(distance);
        });
        mesh.geometry.verticesNeedUpdate = true;
        mesh.geometry.normalsNeedUpdate = true;
        mesh.geometry.computeVertexNormals();
        mesh.geometry.computeFaceNormals();
    }
    render()
}

//helper functions
function fractionate(val, minVal, maxVal) {
    return (val - minVal) / (maxVal - minVal);
}

function modulate(val, minVal, maxVal, outMin, outMax) {
    var fr = fractionate(val, minVal, maxVal);
    var delta = outMax - outMin;
    return outMin + (fr * delta);
}

function avg(arr) {
    var total = arr.reduce(function (sum, b) { return sum + b; });
    return (total / arr.length);
}

function max(arr) {
    return arr.reduce(function (a, b) { return Math.max(a, b); })
}
