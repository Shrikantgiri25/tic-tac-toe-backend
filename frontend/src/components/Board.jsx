import React from 'react';
import Cell from './Cell';
import './Board.css';

const Board = ({ board, onCellClick, disabled }) => {
  const flatBoard = board.flat();

  return (
    <div className="board">
      {flatBoard.map((cell, index) => (
        <Cell
          key={index}
          value={cell}
          index={index}
          onClick={disabled ? () => {} : onCellClick}
        />
      ))}
    </div>
  );
};

export default Board;