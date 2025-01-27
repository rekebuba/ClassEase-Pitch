import React from 'react';
import HomeHeader from './HomeHeader';
import '../styles/HomePage.css';
import '../pages/student/StudentRegistrationForm';
import classEaseImage from '../images/ClassEase-no-slogan.png';

/**
 * Home component renders the main landing page of the ClassEase School website.
 * It includes several sections such as Hero, About Us, Academic Programs, 
 * Latest News & Events, Testimonials, and Footer.
 *
 * Sections:
 * - Hero: Welcomes visitors and provides a call-to-action button for student registration.
 * - About Us: Provides information about the school's mission and environment.
 * - Academic Programs: Details the different educational programs offered by the school.
 * - Latest News & Events: Displays recent news and upcoming events.
 * - Testimonials: Shares feedback from students and parents.
 * - Footer: Contains contact information, quick links, and a newsletter subscription form.
 *
 * @component
 * @example
 * return (
 *   <Home />
 * )
 */
const Home = () => {
  return (
    <>
      <HomeHeader />
      {/* Hero Section */}
      <section id="home" className="hero">
        <img src={classEaseImage} alt="ClassEase Logo" className="hero-image" />
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
        <img src="../images/about-us.jpg" alt="About ClassEase School" className="about-image" />
      </section>

      {/* Academic Programs Section */}
      <section id="academics" className="academics">
        <h2>Academic Programs</h2>
        <div className="program-list">
          <div className="program-item">
            <h3>Primary School</h3>
            <p>We provide a strong foundation for students from Grade 1 to 6, encouraging curiosity and a love for learning.</p>
            <img src="../images/primary-school.jpg" alt="Primary School" className="program-image" />
          </div>
          <div className="program-item">
            <h3>Middle School</h3>
            <p>Building essential skills for students from Grade 7 to 9 with a focus on collaboration and critical thinking.</p>
            <img src="../images/middle-school.jpg" alt="Middle School" className="program-image" />
          </div>
          <div className="program-item">
            <h3>High School</h3>
            <p>Challenging students from Grade 10 to 12 to prepare them for higher education and future careers.</p>
            <img src="../images/high-school.jpg" alt="High School" className="program-image" />
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
            <img src="../images/sports-day.jpg" alt="Annual Sports Day" className="event-image" />
          </div>
          <div className="event-item">
            <h3>Parent-Teacher Meeting</h3>
            <p>Meet with our teachers to discuss the progress of students and their achievements.</p>
            <img src="../images/parent-teacher-meeting.jpg" alt="Parent-Teacher Meeting" className="event-image" />
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="testimonials">
        <h2>What Our Students Say</h2>
        <div className="testimonial-list">
          <div className="testimonial-item">
            <p>&quot;ClassEase School helped me build confidence and prepare for the future. I love it here!&quot;</p>
            <span>- John Doe, Student</span>
          </div>
          <div className="testimonial-item">
            <p>&quot;This school offers a welcoming community and excellent learning resources.&quot;</p>
            <span>- Jane Smith, Parent</span>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer id="contact" className="footer">
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
