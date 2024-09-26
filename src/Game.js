import './Game.css'
import React, { useState, useEffect, useRef } from 'react';
import Camera from './Camera'
import './Camera.css'
import A from './A.png';
import B from './B.png';
import C from './C.png';
import  './SpeechLess (2).png';
import { Link } from 'react-router-dom';
import CameraGame from './CameraGame';
import HomeIcon from './HomeIcon';


export default function Game() {
  const images = [A, B, C];
  const letters = ['A', 'B', 'C'];
  const [imageUrl, setImageUrl] = useState('');
  const [letter, setletter] = useState('');
  const [showImage, setShowImage] = useState(false);

  useEffect(() => {
    if (showImage) {
      const randomIndex = Math.floor(Math.random() * images.length);
      setImageUrl(images[randomIndex]);
      setletter(letters[randomIndex])
      console.log(letters[randomIndex])
    }
  }, [showImage, images]);

  useEffect(() => {
    if (imageUrl) {
      const timer = setTimeout(() => {
        setImageUrl('');
        setShowImage(false);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [imageUrl, setShowImage]);

  const handleButtonClick = () => {
    setShowImage(true);
  };

  return (
    <>
    <img src={require('./SpeechLess (2).png')} alt="SpeechLess" style={{ width: '200px' , height: 'auto', marginBottom: '20px' }} />

    <div class="cg">
      <button class="but" onClick={handleButtonClick}>Show Image</button>
      {imageUrl && (
        <img src={imageUrl} alt="Random image" style={{border:'3px solid royalblue',margin:'5px'}} />
      )}
    </div>

    <div class="dg">
    <CameraGame letter={letter}/>
    {/* <div class="circle">Correct Answer</div> */}
    </div>
    <Link class="link" to={`/${1}`}>
     <span style={{display:'inline-block'}}><HomeIcon/></span>
     <span style={{display:'inline-block'}}>Come back to Home</span>
     </Link>
</>
  );
}