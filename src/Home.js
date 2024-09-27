import React from 'react';
import { Link, useParams } from 'react-router-dom';
import './Home.css'
import './Popup.css'
import Popup from './Popup';
import { useState } from 'react';


export default function Home() {

    const [send, setSend] = useState('');
  
    const handleSend = (data) => {
      setSend(data);
    }

   let {code}=useParams();
   let c='true';
    if(code===1)
        c='false'

    return(
    <>
    <div>
    <div className='image'>
    <img src={require('./SpeechLess (2).png')} alt="SpeechLess" style={{ width: '200px' , height: 'auto',left:'0px',flex:'0.5',margin:'0px 900px 0px 0px' }} />
    <h2 style={{color:'black'}} class="send">{send}</h2>
    <h1 style={{color:'black'}}>Welcome to Speechless</h1>
    <h3>our way to communicate</h3>
    <img src={require('./Home.png')} alt="Home" style={{ width: '900px' , height: 'auto', marginBottom:'0px auto',flex:'5' }} />
    </div>
    <div className={c}>
    <Popup onSend={handleSend} />
    </div>
    </div>
    <div class="main">
    <Link class="link3" to='/detection'>Go to detection</Link>
    <Link class="link3" to='/learn'>I want to learn</Link>
    {/* <Audio/> */}
    </div>
    </>
    );
}
