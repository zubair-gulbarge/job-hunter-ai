import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App Component', () => {
  it('renders the Job Hunter AI header', () => {
    render(<App />);
    // Checks if the main header is present on the screen
    const headerElement = screen.getByText(/Job Hunter AI/i);
    expect(headerElement).toBeDefined();
  });

  it('renders the three navigation tabs', () => {
    render(<App />);
    expect(screen.getByText('PDF Generator')).toBeDefined();
    expect(screen.getByText('Profile Settings')).toBeDefined();
    expect(screen.getByText('Job Tracker')).toBeDefined();
  });
});