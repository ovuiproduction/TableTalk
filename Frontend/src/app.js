// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage'; 
import ChatBot from './components/ChatBot';
import TableTalk from './components/TableTalk';

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/chat-with-file" element={<TableTalk />} />
      </Routes>
    </Router>
  );
}