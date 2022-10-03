import React from 'react';
import HomePage from './components/HomePage.js'
import FPLView from './components/FPLPage.js'
// import TicTacToe from './components/newGamePage.js';

import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<HomePage />}></Route>
        <Route exact path="/myFPLteam" element={<FPLView />}></Route>
      </Routes>
    </Router>
  ); 
}
