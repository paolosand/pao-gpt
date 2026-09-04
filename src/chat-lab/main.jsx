import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import ChatLab from './ChatLab.jsx';
import './ChatLab.css';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ChatLab />
  </StrictMode>,
);
