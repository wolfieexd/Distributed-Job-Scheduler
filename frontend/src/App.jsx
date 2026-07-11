import React, { useState, useEffect } from 'react';
import { Activity, Server, ListTree, Settings, Plus, LayoutDashboard } from 'lucide-react';
import axios from 'axios';
import './index.css';

const SIDEBAR_ITEMS = [
  { id: 'dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { id: 'queues', icon: ListTree, label: 'Queues' },
  { id: 'workers', icon: Server, label: 'Workers' },
  { id: 'activity', icon: Activity, label: 'Activity' },
  { id: 'settings', icon: Settings, label: 'Settings' }
];

export default function App() {
  const [activeTab, setActiveTab] = useState('queues');
  const [queues, setQueues] = useState([]);
  
  // Dummy data for now, would be replaced by actual API calls
  useEffect(() => {
    setQueues([
      { id: 'q-1', name: 'high-priority', priority: 'P0', concurrency: 10, depth: 154, status: 'active' },
      { id: 'q-2', name: 'default', priority: 'P1', concurrency: 50, depth: 1205, status: 'active' },
      { id: 'q-3', name: 'background-tasks', priority: 'P2', concurrency: 5, depth: 8, status: 'error' }
    ]);
  }, []);

  return (
    <div className="dashboard-layout">
      {/* Sidebar Rail */}
      <nav className="sidebar-rail">
        {SIDEBAR_ITEMS.map(item => {
          const Icon = item.icon;
          return (
            <div 
              key={item.id}
              className={`sidebar-icon ${activeTab === item.id ? 'active' : ''}`}
              onClick={() => setActiveTab(item.id)}
              title={item.label}
            >
              <Icon size={20} />
            </div>
          );
        })}
      </nav>

      {/* Main Content */}
      <main className="main-content">
        <header className="top-bar">
          <h1 className="top-bar-title">Scheduler Pro</h1>
          <button className="action-btn">
            <Plus size={16} />
            New Job
          </button>
        </header>

        <div className="dashboard-container">
          {/* Metrics Row */}
          <div className="metrics-row">
            <div className="glass-card">
              <span className="metric-title">Total Jobs Processed</span>
              <span className="metric-value">1,248,592</span>
            </div>
            <div className="glass-card">
              <span className="metric-title">Active Workers</span>
              <span className="metric-value">42 / 50</span>
            </div>
            <div className="glass-card">
              <span className="metric-title">Failed Jobs (24h)</span>
              <span className="metric-value" style={{ color: 'var(--accent-red)' }}>12</span>
            </div>
          </div>

          {/* Queues Table */}
          <div className="data-table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Queue Name</th>
                  <th>Priority</th>
                  <th>Concurrency Limit</th>
                  <th>Depth</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {queues.map(q => (
                  <tr key={q.id}>
                    <td className="font-mono">{q.name}</td>
                    <td>{q.priority}</td>
                    <td className="font-mono">{q.concurrency}</td>
                    <td className="font-mono">{q.depth}</td>
                    <td>
                      <span className={`status-pill ${q.status === 'active' ? 'status-active' : 'status-error'}`}>
                        {q.status === 'active' ? 'Healthy' : 'Blocked'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
