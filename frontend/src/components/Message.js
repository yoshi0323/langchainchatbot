import React from 'react';
import './Message.css';

const Message = ({ text, user }) => {
  return (
    <div className={`message ${user ? 'user' : 'bot'}`}>
      <p>{text}</p>
    </div>
  );
};

export default Message;
