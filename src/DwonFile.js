import React, { useState,useEffect } from 'react';
import { SIZE } from 'rsuite/esm/utils/constants';

function FileCreator(props) {

  const [fileName, setFileName] = useState('');
  const [fileContent, setFileContent] = useState('');
  const [content, setContent] = useState("");


  const handleFileNameChange = (event) => {
    setFileName(event.target.value);
  };

  const handleFileContentChange = (event) => {
    setFileContent(event.target.innerText);
  };

  const handleFileCreate = () => {
    const element = document.createElement('a');
    const file = new Blob([fileContent], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = fileName + '.txt';
    document.body.appendChild(element);
    element.click();
  };
  
  useEffect(() => {
    setContent(prevContent => prevContent + ' ' + props.responseText);
  }, [props.responseText]);
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center',position:'absolute',right:'100px',top:'30px'}}>
      <div class="fromCamera"
        contentEditable={true}
        onInput={handleFileContentChange}
        style={{
          border: '1px solid black',
          padding: '10px',
          borderRadius: '5px',
          marginBottom: '20px',
          width: '200px',
          textAlign: 'center',
          height:'400px'
        }}
      >
      {content}
      </div>
      <h5>Create a text file</h5>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: '20px' }}>
        <label htmlFor="fileNameInput">Enter file name:</label>
        <input type="text" id="fileNameInput" value={fileName} onChange={handleFileNameChange} placeholder="Enter file name here" style={{ width: '200px' }} />
      </div>
      <button class="bbb" onClick={handleFileCreate} style={{color:'royalblue', padding: '10px 20px', borderRadius: '5px', fontWeight: 'bold',height:'50px',fontSize:'15px',cursor:'pointer',border:'3px solid royalblue' }}>Save File</button>
    </div>
  );
}

export default FileCreator;