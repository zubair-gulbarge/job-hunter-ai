import { useState, useEffect } from 'react';

const STATUSES = ["Preparing", "Applied", "Interviewing", "Offered", "Rejected"];

export default function ApplicationTracker() {
  const [applications, setApplications] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  // Added "source" to the newApp state
  const [newApp, setNewApp] = useState({ company_name: '', job_title: '', source: '', job_description: 'Manual Entry' });

  const fetchApplications = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/applications');
      if (response.ok) {
        const data = await response.json();
        setApplications(data);
      }
    } catch (error) {
      console.error("Error fetching applications:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchApplications();
  }, []);

  const handleAddApplication = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/applications', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...newApp, status: "Preparing" }),
      });
      if (response.ok) {
        setNewApp({ company_name: '', job_title: '', source: '', job_description: 'Manual Entry' });
        fetchApplications(); 
      }
    } catch (error) {
      console.error("Error adding application:", error);
    }
  };

  const handleStatusChange = async (appId, newStatus) => {
    try {
      const response = await fetch(`http://localhost:8000/api/applications/${appId}/status?new_status=${newStatus}`, { method: 'PUT' });
      if (response.ok) {
        setApplications(prevApps => prevApps.map(app => app._id === appId ? { ...app, status: newStatus } : app));
      }
    } catch (error) {
      console.error("Error updating status:", error);
    }
  };

  // NEW: Delete Functionality
  const handleDelete = async (appId) => {
    if (!window.confirm("Are you sure you want to delete this job?")) return;
    
    try {
      const response = await fetch(`http://localhost:8000/api/applications/${appId}`, { method: 'DELETE' });
      if (response.ok) {
        setApplications(prevApps => prevApps.filter(app => app._id !== appId));
      }
    } catch (error) {
      console.error("Error deleting application:", error);
    }
  };

  // NEW: Filter Logic for Search
  const filteredApps = applications.filter(app => 
    app.company_name.toLowerCase().includes(searchQuery.toLowerCase()) || 
    app.job_title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (isLoading) return <p>Loading your Kanban board...</p>;

  return (
    <div className="tracker-container">
      <h2>Application Tracker</h2>
      
      {/* Search Bar */}
      <input 
        type="text" 
        className="search-bar" 
        placeholder="🔍 Search jobs by company or title..." 
        value={searchQuery} 
        onChange={(e) => setSearchQuery(e.target.value)}
      />
      
      {/* Mini Form to add a new job manually */}
      <form className="add-app-form" onSubmit={handleAddApplication}>
        <input 
          type="text" placeholder="Company Name" required
          value={newApp.company_name} onChange={e => setNewApp({...newApp, company_name: e.target.value})} 
        />
        <input 
          type="text" placeholder="Job Title" required
          value={newApp.job_title} onChange={e => setNewApp({...newApp, job_title: e.target.value})} 
        />
        <input 
          type="text" placeholder="Source (e.g. LinkedIn, Naukri)" required
          value={newApp.source} onChange={e => setNewApp({...newApp, source: e.target.value})} 
        />
        <button type="submit">Add to Board</button>
      </form>

      {/* Kanban Board Columns */}
      <div className="kanban-board">
        {STATUSES.map(status => (
          <div key={status} className="kanban-column">
            <h3>{status} ({filteredApps.filter(app => app.status === status).length})</h3>
            <div className="kanban-cards">
              {filteredApps.filter(app => app.status === status).map(app => (
                <div key={app._id} className="kanban-card">
                  <h4>{app.company_name}</h4>
                  <p>{app.job_title}</p>
                  {/* Source Tag */}
                  <small style={{ color: '#2980b9', fontWeight: 'bold' }}>📍 {app.source || 'Website'}</small>
                  <small>Applied: {new Date(app.applied_date).toLocaleDateString()}</small>
                  
                  <select value={app.status} onChange={(e) => handleStatusChange(app._id, e.target.value)}>
                    {STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
                  </select>

                  {/* Delete Button */}
                  <button className="delete-btn" onClick={() => handleDelete(app._id)}>🗑️ Delete</button>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}