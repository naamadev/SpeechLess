//זה הקוד של פריים אחד
import React, { useState, useEffect, useRef } from 'react';
import './Camera.css'
import './SpeechLess (1).png';
import { Link } from 'react-router-dom';
import HomeIcon from './HomeIcon';
import DwonFile from './DwonFile';

const Camera = (props) => {
  const [stream, setStream] = useState(null);
  const [responseText, setResponseText] = useState('');
  const videoRef = useRef(null);

  useEffect(() => {
    // Get the user's camera stream
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        setStream(stream);
        videoRef.current.srcObject = stream;
        videoRef.current.style.transform = "scaleX(-1)";
      })
      .catch((error) => console.error(error));
  }, []);

  const captureFrame = async () => {
    // Capture a frame from the video stream
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    canvas.getContext('2d').drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/jpeg', 0.8);
    //console.log(dataURL)
    

    //Send the frame to the server
    // try {
    //   const response = await axios.post('http://localhost:5000/process_frames', JSON.stringify(dataURL));
    //   setPrediction(response.data.prediction);
    //   setResponseText(response.data.response_text);
    // } catch (error) {
    //   console.error(error);
    // }

    fetch('http://localhost:5000/process_frames', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({dataURL})
    })
    .then(response => {
      if (response.ok) {
        // Parse the response object and display the predicted label
        response.json().then(data => {
          console.log(data.label);
          setResponseText(data.label)
        });
      } else {
        // There was an error authenticating the user
        console.log('Error');
      }
    })
    .catch(error => {
      console.error('Error', error);
    });

    // Set a timeout of 2 seconds before capturing the next frame
    setTimeout(captureFrame, 1000);
  };

  useEffect(() => {
    if (stream) {
      captureFrame();
    }
  }, [stream, captureFrame]);

  return (
    <>
      <img class="cameraimage" src={require('./SpeechLess (2).png')} alt="SpeechLess" style={{ width: '200px' , height: 'auto', marginBottom: '20px' ,position:'absolute' }} />
      <div className="container" >
        <div className="video-container">
          <video ref={videoRef} autoPlay={true} />
        </div>
      </div>
      <Link class="link1" to={`/${1}`}>
        <span style={{display:'inline-block'}}><HomeIcon/></span>
        <span style={{display:'inline-block'}}>Come back to Home</span>
      </Link>
      <Link to="/speech">
     <span class="link2">Go to Speech recognition</span>
   </Link>
      {responseText && <p>Response: {responseText}</p>}
      <DwonFile responseText={responseText}/>
    </>
  );
};

export default Camera;