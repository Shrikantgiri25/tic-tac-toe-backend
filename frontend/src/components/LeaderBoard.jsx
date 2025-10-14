import React, { useState, useEffect, useRef, useCallback } from 'react';
import { auth } from '../api/api';
import './Leaderboard.css';

const Leaderboard = () => {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [nextPage, setNextPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const loaderRef = useRef(null);

  const loadLeaderboard = useCallback(async () => {
    if (loading || !hasMore) return;
    setLoading(true);

    try {
      const response = await auth.getLeaderboard(nextPage);
      const data = response.data;
      const newPlayers = data?.results || data || [];

      setPlayers(prevPlayers => {
        const existingIds = new Set(prevPlayers.map(p => p.id));
        const filtered = newPlayers.filter(p => !existingIds.has(p.id));
        return [...prevPlayers, ...filtered];
      });

      setNextPage(prev => (data?.next ? prev + 1 : prev));
      setHasMore(!!data?.next);
    } catch (error) {
      console.error('Error loading leaderboard:', error);
    } finally {
      setLoading(false);
    }
  }, [loading, nextPage, hasMore]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      entries => {
        if (entries[0].isIntersecting && hasMore) {
          loadLeaderboard();
        }
      },
      { threshold: 1.0 }
    );

    const loader = loaderRef.current;
    if (loader) observer.observe(loader);
    return () => {
      if (loader) observer.unobserve(loader);
    };
  }, [loadLeaderboard, hasMore]);

  useEffect(() => {
    loadLeaderboard(); // initial load
  }, []);

  return (
    <div className="leaderboard">
      <h2>🏆 Leaderboard</h2>
      <div className="leaderboard-table">
        <div className="table-header">
          <span className="rank">Rank</span>
          <span className="player">Player</span>
          <span className="stats">W/L/D</span>
          <span className="rating">Rating</span>
        </div>

        {players.map((player, index) => (
          <div key={player.id || index} className="table-row">
            <span className="rank">#{index + 1}</span>
            <span className="player">{player.username}</span>
            <span className="stats">
              {player.wins}/{player.losses}/{player.draws}
            </span>
            <span className="rating">{player.rating}</span>
          </div>
        ))}

        <div ref={loaderRef} className="loading">
          {loading && hasMore ? 'Loading more players...' : hasMore ? '' : '🏁 End of Leaderboard'}
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;
