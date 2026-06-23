import { useState, useEffect } from 'react';

export default function ProfileSettings() {
  // Ensure every array is initialized so the map functions never fail
  const [formData, setFormData] = useState({
    name: 'Zubair',
    email: 'zubair@example.com',
    phone: '+91 9833698785',
    summary: 'AWS Certified Solutions Architect and DevOps Engineer...',
    skills: 'AWS, Kubernetes, Docker, Terraform, Python',
    experience: [],
    projects: [],
    academics: []
  });

  const [statusMessage, setStatusMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/profile');
        if (response.ok) {
          const data = await response.json();
          setFormData({
            name: data.name || '',
            email: data.email || '',
            phone: data.phone || '',
            summary: data.summary || '',
            // Handle arrays safely
            skills: data.skills ? data.skills.join(', ') : '',
            experience: data.experience || [],
            projects: data.projects || [],
            academics: data.academics || []
          });
        }
      } catch (error) {
        console.error("Error fetching profile, using defaults.", error);
      }
    };
    fetchProfile();
  }, []);

  const handleBasicChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleArrayChange = (index, field, value, arrayName) => {
    const newArray = [...formData[arrayName]];
    newArray[index][field] = value;
    setFormData({ ...formData, [arrayName]: newArray });
  };

  const addArrayItem = (arrayName, emptyTemplate) => {
    setFormData({ ...formData, [arrayName]: [...formData[arrayName], emptyTemplate] });
  };

  const removeArrayItem = (index, arrayName) => {
    const newArray = formData[arrayName].filter((_, i) => i !== index);
    setFormData({ ...formData, [arrayName]: newArray });
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setStatusMessage('');

    try {
      const payload = {
        ...formData,
        // Convert the comma-separated string back to an array
        skills: formData.skills.split(',').map(s => s.trim()).filter(Boolean),
      };

      const response = await fetch('http://localhost:8000/api/profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error("Failed to save profile");
      setStatusMessage("✅ Profile saved successfully!");
    } catch (error) {
      console.error("Error:", error);
      setStatusMessage("❌ Failed to save profile.");
    } finally {
      setIsLoading(false);
      setTimeout(() => setStatusMessage(''), 3000); 
    }
  };

  return (
    <div className="tracker-container">
      <h2>Master Profile Settings</h2>
      <p style={{textAlign: 'center', marginBottom: '20px'}}>Update your data below.</p>
      
      <form onSubmit={handleSave} className="add-app-form" style={{flexDirection: 'column', gap: '20px', background: 'white'}}>
        
        {/* BASIC INFO */}
        <div style={{display: 'flex', gap: '15px'}}>
          <div className="form-group" style={{flex: 1}}><label>Full Name</label><input type="text" name="name" value={formData.name} onChange={handleBasicChange} required /></div>
          <div className="form-group" style={{flex: 1}}><label>Email</label><input type="email" name="email" value={formData.email} onChange={handleBasicChange} required /></div>
          <div className="form-group" style={{flex: 1}}><label>Phone</label><input type="text" name="phone" value={formData.phone} onChange={handleBasicChange} /></div>
        </div>

        <div className="form-group">
          <label>Professional Summary</label>
          <textarea name="summary" value={formData.summary} onChange={handleBasicChange} rows={3} style={{width: '100%', padding: '10px'}}/>
        </div>

        <div className="form-group">
          <label>Skills (comma separated)</label>
          <textarea name="skills" value={formData.skills} onChange={handleBasicChange} rows={2} style={{width: '100%', padding: '10px'}}/>
        </div>

        {/* DYNAMIC EXPERIENCE */}
        <div className="form-group">
          <label style={{borderBottom: '2px solid #ecf0f1', paddingBottom: '5px', marginBottom: '10px', display: 'block'}}>Professional Experience</label>
          {formData.experience.map((exp, index) => (
            <div key={index} style={{background: '#f8f9fa', padding: '15px', borderRadius: '5px', marginBottom: '10px'}}>
              <div style={{display: 'flex', gap: '10px', marginBottom: '10px'}}>
                <input type="text" placeholder="Company Name" value={exp.company || ''} onChange={(e) => handleArrayChange(index, 'company', e.target.value, 'experience')} style={{flex: 1}}/>
                <input type="text" placeholder="Job Title" value={exp.role || ''} onChange={(e) => handleArrayChange(index, 'role', e.target.value, 'experience')} style={{flex: 1}}/>
              </div>
              <input type="text" placeholder="Duration (e.g., June 2023 - Present)" value={exp.duration || ''} onChange={(e) => handleArrayChange(index, 'duration', e.target.value, 'experience')} style={{marginBottom: '10px', width: '100%'}}/>
              <textarea placeholder="Job Responsibilities (Bullet points)" value={exp.description || ''} onChange={(e) => handleArrayChange(index, 'description', e.target.value, 'experience')} rows={3} style={{width: '100%', padding: '10px'}}/>
              <button type="button" onClick={() => removeArrayItem(index, 'experience')} className="delete-btn" style={{width: 'auto', marginTop: '10px'}}>🗑️ Remove Job</button>
            </div>
          ))}
          <button type="button" onClick={() => addArrayItem('experience', { company: '', role: '', duration: '', description: '' })} style={{background: '#2ecc71', width: 'auto', padding: '10px 15px', border: 'none', color: 'white', borderRadius: '5px', cursor: 'pointer'}}>+ Add Experience</button>
        </div>

        {/* DYNAMIC PROJECTS */}
        <div className="form-group">
          <label style={{borderBottom: '2px solid #ecf0f1', paddingBottom: '5px', marginBottom: '10px', display: 'block'}}>Technical Projects</label>
          {formData.projects.map((proj, index) => (
            <div key={index} style={{background: '#f8f9fa', padding: '15px', borderRadius: '5px', marginBottom: '10px'}}>
              <div style={{display: 'flex', gap: '10px', marginBottom: '10px'}}>
                <input type="text" placeholder="Project Title" value={proj.title || ''} onChange={(e) => handleArrayChange(index, 'title', e.target.value, 'projects')} style={{flex: 1}}/>
                <input type="text" placeholder="Technologies Used" value={proj.technologies || ''} onChange={(e) => handleArrayChange(index, 'technologies', e.target.value, 'projects')} style={{flex: 1}}/>
              </div>
              <textarea placeholder="Project Description" value={proj.description || ''} onChange={(e) => handleArrayChange(index, 'description', e.target.value, 'projects')} rows={3} style={{width: '100%', padding: '10px'}}/>
              <button type="button" onClick={() => removeArrayItem(index, 'projects')} className="delete-btn" style={{width: 'auto', marginTop: '10px'}}>🗑️ Remove Project</button>
            </div>
          ))}
          <button type="button" onClick={() => addArrayItem('projects', { title: '', technologies: '', description: '' })} style={{background: '#2ecc71', width: 'auto', padding: '10px 15px', border: 'none', color: 'white', borderRadius: '5px', cursor: 'pointer'}}>+ Add Project</button>
        </div>

        {/* DYNAMIC ACADEMICS */}
        <div className="form-group">
          <label style={{borderBottom: '2px solid #ecf0f1', paddingBottom: '5px', marginBottom: '10px', display: 'block'}}>Education & Certifications</label>
          {formData.academics.map((edu, index) => (
            <div key={index} style={{background: '#f8f9fa', padding: '15px', borderRadius: '5px', marginBottom: '10px'}}>
              <input type="text" placeholder="Degree / Certification Name" value={edu.degree || ''} onChange={(e) => handleArrayChange(index, 'degree', e.target.value, 'academics')} style={{marginBottom: '10px', width: '100%'}}/>
              <div style={{display: 'flex', gap: '10px'}}>
                <input type="text" placeholder="Institution" value={edu.institution || ''} onChange={(e) => handleArrayChange(index, 'institution', e.target.value, 'academics')} style={{flex: 1}}/>
                <input type="text" placeholder="Year" value={edu.year || ''} onChange={(e) => handleArrayChange(index, 'year', e.target.value, 'academics')} style={{flex: 1}}/>
              </div>
              <button type="button" onClick={() => removeArrayItem(index, 'academics')} className="delete-btn" style={{width: 'auto', marginTop: '10px'}}>🗑️ Remove Education</button>
            </div>
          ))}
          <button type="button" onClick={() => addArrayItem('academics', { degree: '', institution: '', year: '' })} style={{background: '#2ecc71', width: 'auto', padding: '10px 15px', border: 'none', color: 'white', borderRadius: '5px', cursor: 'pointer'}}>+ Add Education</button>
        </div>

        <button type="submit" disabled={isLoading} style={{marginTop: '20px', padding: '15px', width: '100%'}}>
          {isLoading ? 'Saving...' : 'Save Profile to Database'}
        </button>
        {statusMessage && <p className="status-message">{statusMessage}</p>}
      </form>
    </div>
  );
}