import { useState } from 'react';
import ProfileSettings from './components/ProfileSettings';
import ApplicationTracker from './components/ApplicationTracker';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('generator');
  
  // New State for the Generator Form
  const [companyName, setCompanyName] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  
  const [isLoading, setIsLoading] = useState(false);

  const handleGenerateResume = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // 1. Generate the PDF
      const pdfResponse = await fetch('http://localhost:8000/api/tailor-resume', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          master_resume: "Use master profile from DB", 
          job_description: jobDescription,
        }),
      });

      if (!pdfResponse.ok) throw new Error("Failed to generate resume");

      // 2. Download the PDF
      const blob = await pdfResponse.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${companyName}_${jobTitle}_Resume.pdf`); // Smarter filename!
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);

      // 3. Auto-save to the Kanban Tracker
      const trackerResponse = await fetch('http://localhost:8000/api/applications', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          company_name: companyName,
          job_title: jobTitle,
          job_description: jobDescription,
          status: "Preparing"
        }),
      });

      if (!trackerResponse.ok) console.error("Failed to sync to tracker");

      // 4. Clear the form and switch to the Tracker tab to show the user their new card!
      setCompanyName('');
      setJobTitle('');
      setJobDescription('');
      setActiveTab('tracker');

    } catch (error) {
      console.error("Error:", error);
      alert("Failed to generate resume.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>Job Hunter AI 🚀</h1>
        <div className="tabs">
          <button className={activeTab === 'generator' ? 'active' : ''} onClick={() => setActiveTab('generator')}>
            PDF Generator
          </button>
          <button className={activeTab === 'profile' ? 'active' : ''} onClick={() => setActiveTab('profile')}>
            Profile Settings
          </button>
          <button className={activeTab === 'tracker' ? 'active' : ''} onClick={() => setActiveTab('tracker')}>
            Job Tracker
          </button>
        </div>
      </header>

      <main>
        {activeTab === 'generator' && (
          <form onSubmit={handleGenerateResume} className="generator-form">
            <p>Enter the job details below. We will generate your tailored PDF and log it to your tracker.</p>
            
            <div className="form-row">
              <input 
                type="text" placeholder="Company Name (e.g. AWS)" required
                value={companyName} onChange={(e) => setCompanyName(e.target.value)}
              />
              <input 
                type="text" placeholder="Job Title (e.g. Cloud Architect)" required
                value={jobTitle} onChange={(e) => setJobTitle(e.target.value)}
              />
            </div>

            <textarea 
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the target Job Description here..."
              rows={8} required
            />
            
            <button type="submit" disabled={isLoading || !jobDescription || !companyName || !jobTitle}>
              {isLoading ? '🤖 Tailoring PDF & Updating Tracker...' : 'Generate & Track'}
            </button>
          </form>
        )}

        {activeTab === 'profile' && <ProfileSettings />}
        {activeTab === 'tracker' && <ApplicationTracker />}
      </main>
    </div>
  );
}

export default App;