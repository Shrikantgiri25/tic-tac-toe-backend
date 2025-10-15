import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'react-toastify';
import Board from '../components/Board';
import GameInfo from '../components/GameInfo';
import GameWebSocket from "../api/websocket";
import './Game.css';

const Game = () => {
  const { gameId } = useParams();
  const { user, refreshUser } = useAuth();
  const navigate = useNavigate();
  const [game, setGame] = useState(null);
  const [error, setError] = useState('');
  const wsRef = useRef(null);

  useEffect(() => {
    const ws = new GameWebSocket(gameId, handleWebSocketMessage);
    wsRef.current = ws;

    return () => {
      ws.close();
    };
  }, [gameId]);

  const handleWebSocketMessage = (data) => {
    if (data.type === 'game_state') {
      const newGame = { ...data.game };
      setGame(newGame);

      // Show game status notifications
      if (newGame.status === 'finished') {
        if (newGame.winner) {
          if (newGame.winner.id === user?.id) {
            toast.success('Congratulations! You won!');
          } else {
            toast.info(`Game over! ${newGame.winner.username} won.`);
          }
        } else {
          toast.info('Game ended in a draw!');
        }
        // Refresh user data after game ends to get updated stats
        refreshUser();
      } else if (newGame.status === 'in_progress' && newGame.current_turn?.id === user?.id) {
        toast.info('Your turn!');
      }
    } else if (data.type === 'error') {
      setError(data.message);
      toast.error(data.message);
      setTimeout(() => setError(''), 3000);
    }
  };

  const handleCellClick = (position) => {
    if (!game || game.status !== 'in_progress') return;
    if (game.current_turn?.id !== user?.id) return;

    wsRef.current?.makeMove(position);
  };

  const handlePlayAgain = () => {
    navigate('/');
  };

  if (!game) {
    return <div className="loading-container">Loading game...</div>;
  }

  const isGameOver = game.status === 'finished';
  const canMove = game.status === 'in_progress' && game.current_turn?.id === user?.id;

  return (
    <div className="game-container">
      <GameInfo game={game} currentUser={user} />
      
      {error && <div className="error-banner">{error}</div>}
      
      <Board
        board={game.board_state}
        onCellClick={handleCellClick}
        disabled={!canMove}
      />

      {isGameOver && (
        <div className="game-over-actions">
          <button className="btn-large btn-primary" onClick={handlePlayAgain}>
            Play Again
          </button>
          <button
            className="btn-large btn-secondary"
            onClick={() => navigate('/leaderboard')}
          >
            View Leaderboard
          </button>
        </div>
      )}
    </div>
  );
};

export default Game;