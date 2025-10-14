import React from 'react';
import './Cell.css';

const Cell = ({ value, onClick, index }) => {
  return (
    <button
      className={`cell ${value ? 'filled' : ''}`}
      onClick={() => onClick(index)}
      disabled={value !== null && value !== undefined}
    >
      {value || ''}
    </button>
  );
};

export default Cell;