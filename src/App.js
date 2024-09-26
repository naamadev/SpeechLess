import logo from './logo.svg';
import './App.css';
import React from 'react';
import  './SpeechLess (2).png';
import  './Home.png';
import "rsuite/dist/rsuite.min.css";
import Popup from './Popup'
import styled, { keyframes } from 'styled-components';
import { bounce } from 'react-animations';
import {Route, Routes} from 'react-router-dom';
import Home from './Home';
import Camera from './Camera';
import Game from './Game';
import Speech from './Speech';

const App = () => {
  const bounceAnimation = keyframes`${bounce}`;
  const BouncyDiv = styled.div`animation: 1s ${bounceAnimation};`;
  return (
    <Routes>
      <Route path="/speech" element={<Speech></Speech>} />
      <Route path="/camera" element={<Camera></Camera>} />
      <Route path='/:code?' element={<Home></Home>}></Route>
      <Route path='/detection' element={<Camera></Camera>}></Route>
      <Route path='/learn' element={<Game></Game>}></Route>
    </Routes>
  );
}

export default App;
