import React from "react";
import { Link } from "react-router-dom";
import "../css/home.css";

export default function HomePage() {
  return (
    <div className="home-container">
      <div className="overlay">
        <div className="d-flex h-100  mx-auto flex-column">
          <header className="masthead">
            <div className="inner">
              <h3 className="masthead-brand">TabuQuest</h3>
              <nav className="nav nav-masthead justify-content-center">
                <Link className="nav-link active" to="/chat-with-file">
                  Explore
                </Link>
                <Link className="nav-link" to="/services">
                  Service
                </Link>
                <Link className="nav-link" to="/contact">
                  Contact
                </Link>
              </nav>
            </div>
          </header>

          <main role="main" className="inner cover">
            <h1 className="cover-heading">The Table's Secret</h1>
            <p className="lead">
              Let's reveal the secrets hidden within your tables
              <br />
              Dive deep into your tabular data with us
              <br />
              Unlock powerful insights waiting to be discovered
            </p>

            <p className="lead">
              <Link to="/chat-with-file" className="btn explore-btn btn-lg btn-secondary">
                Explore
              </Link>
            </p>
          </main>
        </div>
      </div>
    </div>
  );
}
