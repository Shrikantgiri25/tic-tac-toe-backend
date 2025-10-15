import React from 'react';
import './GameInfo.css';

const GameInfo = ({ game, currentUser }) => {
  if (!game) return null;

  const isPlayer1 = currentUser?.id === game.player1?.id;
  const isMyTurn = game.current_turn?.id === currentUser?.id;
  const mySymbol = isPlayer1 ? 'X' : 'O';

  return (
    <div className="game-info">
      <div className="players">
        <div className={`player ${isPlayer1 ? 'me' : ''}`}>
          <span className="symbol">X</span>
          <span className="username">{game.player1?.username}</span>
          {isPlayer1 && <span className="badge">You</span>}
        </div>
        
        <div className="vs">VS</div>
        
        <div className={`player ${!isPlayer1 ? 'me' : ''}`}>
          <span className="symbol">O</span>
          <span className="username">
            {game.player2?.username || 'Waiting...'}
          </span>
          {!isPlayer1 && game.player2 && <span className="badge">You</span>}
        </div>
      </div>

      {game.status === 'waiting' && (
        <div className="status waiting">
          Waiting for opponent to join...
        </div>
      )}

      {game.status === 'in_progress' && (
        <div className={`status ${isMyTurn ? 'your-turn' : 'opponent-turn'}`}>
          {isMyTurn ? "Your turn!" : `${game.current_turn?.username}'s turn`}
        </div>
      )}

      {game.status === 'finished' && (
        <div className="status finished">
          {game.result === 'draw' && 'Game ended in a draw!'}
          {game.winner?.id === currentUser?.id && 'You won! 🎉'}
          {game.winner && game.winner.id !== currentUser?.id && 
            `${game.winner.username} won!`}
        </div>
      )}
    </div>
  );
};

export default GameInfo;