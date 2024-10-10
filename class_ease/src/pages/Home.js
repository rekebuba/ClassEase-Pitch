import React from 'react';
// import React, { useState } from "react";
import './styles/HomePage.css';
import './StudentRegistrationForm';



const Home = () => {
  return (
    <>
      {/* Header */}
      <header className="header">
        <div className="logo">ClassEase School</div>
        <nav>
          <ul className="nav-links">
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About Us</a></li>
            <li><a href="#admissions">Admissions</a></li>
            <li><a href="#academics">Academics</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </nav>
        <div className="login-btn">
          <a href="/login">Login</a>
        </div>
      </header>

      {/* Hero Section */}
      <section id="home" className="hero">
        <div className="hero-content">
          <h1>Welcome to ClassEase School</h1>
          <p>Empowering students with the knowledge and skills to excel in the modern world.</p>
          <a href="/student/registration" className="cta-btn">Apply Now</a>
        </div>
      </section>

      {/* About Us Section */}
      <section id="about" className="about">
        <h2>About Us</h2>
        <p>
          ClassEase School has been dedicated to providing a rich and rigorous academic program. Our focus is to shape the minds of tomorrow by providing a nurturing, inclusive, and forward-thinking environment.
        </p>
      </section>

      {/* Academic Programs Section */}
      <section id="academics" className="academics">
        <h2>Academic Programs</h2>
        <div className="program-list">
          <div className="program-item">
            <h3>Primary School</h3>
            <p>We provide a strong foundation for students from Grade 1 to 6, encouraging curiosity and a love for learning.</p>
          </div>
          <div className="program-item">
            <h3>Middle School</h3>
            <p>Building essential skills for students from Grade 7 to 9 with a focus on collaboration and critical thinking.</p>
          </div>
          <div className="program-item">
            <h3>High School</h3>
            <p>Challenging students from Grade 10 to 12 to prepare them for higher education and future careers.</p>
          </div>
        </div>
      </section>

      {/* Events and News Section */}
      <section id="events" className="events">
        <h2>Latest News & Events</h2>
        <div className="event-list">
          <div className="event-item">
            <h3>Annual Sports Day</h3>
            <p>Join us for an exciting day of competitions and events on the school campus.</p>
          </div>
          <div className="event-item">
            <h3>Parent-Teacher Meeting</h3>
            <p>Meet with our teachers to discuss the progress of students and their achievements.</p>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="testimonials">
        <h2>What Our Students Say</h2>
        <div className="testimonial-list">
          <div className="testimonial-item">
            <p>"ClassEase School helped me build confidence and prepare for the future. I love it here!"</p>
            <span>- John Doe, Student</span>
          </div>
          <div className="testimonial-item">
            <p>"This school offers a welcoming community and excellent learning resources."</p>
            <span>- Jane Smith, Parent</span>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-about">
            <h3>ClassEase School</h3>
            <p>123 School Street, Education City</p>
            <p>Email: info@classease.edu</p>
            <p>Phone: +123-456-7890</p>
          </div>
          <div className="footer-links">
            <h3>Quick Links</h3>
            <ul>
              <li><a href="#about">About Us</a></li>
              <li><a href="#admissions">Admissions</a></li>
              <li><a href="#academics">Academics</a></li>
              <li><a href="#contact">Contact</a></li>
            </ul>
          </div>
          <div className="footer-subscribe">
            <h3>Subscribe to Our Newsletter</h3>
            <input type="email" placeholder="Enter your email" />
            <button className='subscribe'>Subscribe</button>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2024 ClassEase School. All Rights Reserved.</p>
        </div>
      </footer>
    </>
  );
};

export default Home;
