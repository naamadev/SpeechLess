import "./Speech.css"
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import useClipboard from "react-use-clipboard";
import {useState} from "react";
import Camera from "./Camera";
import { Link } from 'react-router-dom';
import { Conversion } from "@rsuite/icons";



const Speech = () => {
    const [textToCopy, setTextToCopy] = useState();
    const [isCopied, setCopied] = useClipboard(textToCopy, {
        successDuration:1000
    });

    const startListening = () => SpeechRecognition.startListening({ continuous: true, language: 'en-IN' });
    const { transcript, browserSupportsSpeechRecognition } = useSpeechRecognition();

    if (!browserSupportsSpeechRecognition) {
        return null
    }
    console.log(transcript)
    return (
        <>
            <div className="container">
                <h3>Click on the buttons to start or stop your SpeechRecognition</h3>
                <br/>
                <div className="main-content" onClick={() =>  setTextToCopy(transcript)}>
                    {transcript}
                </div>
                <div className="btn-style">
                    <button class="buttons" onClick={setCopied}>
                        {isCopied ? 'Copied!' : 'Copy to clipboard'}
                    </button>
                    <button class="buttons" onClick={startListening}>Start Listening</button>
                    <button class="buttons" onClick={SpeechRecognition.stopListening}>Stop Listening</button>
                </div>
            </div>
            <Link to="/Camera">
     <span class="link1">Go to Camera recognition</span>
   </Link>
        </>
    );
};

export default Speech;