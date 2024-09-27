import React, { useState, useEffect, useRef } from 'react';
import './CameraGame.css'

const CameraGame = (props) => {
  console.log(props.letter)
  const [stream, setStream] = useState(null);
  const [responseText, setResponseText] = useState('');
  const videoRef = useRef(null);

  useEffect(() => {
    // Get the user's camera stream
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        setStream(stream);
        videoRef.current.srcObject = stream;
        videoRef.current.style.transform = "scaleX(-1)"; // Mirror the video
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

    fetch('http://localhost:5000/process_frame', {
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
          Question()
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
    setTimeout(captureFrame, 100);
  };

  useEffect(() => {
    if (stream) {
      captureFrame();
    }
  }, [stream, captureFrame]);

  function Question()
  {
    if((props.letter)===responseText)
    {
      console.log("correct answer")
      Open()
    }
    else{
      Open_n()
    }
  }
  function Close()
  {
          document.querySelector('.popupg').classList.remove('popupActiveg');
          setResponseText('')
  }
  function Open()
  {
          document.querySelector('.popupg').classList.add('popupActiveg');
  }
  function Close_n()
  {
          document.querySelector('.popupgn').classList.remove('popupActivegn');
          setResponseText('')
  }
  function Open_n()
  {
          document.querySelector('.popupgn').classList.add('popupActivegn');
  }
  return (
    <>
    <div className="container1">
      <div className="video-container1">
        <video ref={videoRef} autoPlay={true} />
      </div>
      {responseText && <p>Response: {responseText}</p>}
     </div>
     <div class="popupg">
     <div style={{display:'flex',flexDirectio:'column'}}>
      <div style={{color: 'green',fontSize:'20px',textAlign:'center',margin:'auto',flex:'1'}}>Correct Answer</div>
      <div class="A" onClick={()=>Close()}>Close</div>
      </div>
    </div>
    <div class="popupgn">
     <div style={{display:'flex',flexDirectio:'column'}}>
      <div style={{color: 'red',fontSize:'20px',textAlign:'center',margin:'auto',flex:'1'}}>UnCorrect Answer</div>
      <div class="An" onClick={()=>Close_n()}>Close</div>
      </div>
    </div>
     </>
  );
};

export default CameraGame 
