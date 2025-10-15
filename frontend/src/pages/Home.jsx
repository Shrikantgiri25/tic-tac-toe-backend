import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'react-toastify';
import { games } from '../api/api';
import './Home.css';

const Home = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleJoinMatchmaking = async () => {
    setLoading(true);
    try {
      const response = await games.joinMatchmaking();
      toast.success('Match found! Starting game...');
      navigate(`/game/${response.data.id}`);
    } catch {
      toast.error('Failed to find a match. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home-container">
      <div className="home-content">
        <h1>🎮 Multiplayer Tic-Tac-Toe</h1>
        
        {user && (
          <div className="user-stats">
            <h3>Your Stats</h3>
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-value">{user.wins}</div>
                <div className="stat-label">Wins</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{user.losses}</div>
                <div className="stat-label">Losses</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{user.draws}</div>
                <div className="stat-label">Draws</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{user.rating}</div>
                <div className="stat-label">Rating</div>
              </div>
            </div>
          </div>
        )}

        <div className="action-buttons">
          <button
            className="btn-large btn-primary"
            onClick={handleJoinMatchmaking}
            disabled={loading}
          >
            {loading ? 'Finding Match...' : 'Play Now'}
          </button>
          
          <button
            className="btn-large btn-secondary"
            onClick={() => navigate('/leaderboard')}
          >
            View Leaderboard
          </button>
        </div>

        <div className="game-rules">
          <h3>How to Play</h3>
          <ul>
            <li>Click "Play Now" to find an opponent</li>
            <li>Take turns placing X's and O's</li>
            <li>Get three in a row to win</li>
            <li>Earn rating points for wins!</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Home;