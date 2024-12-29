import "./LoanAnalysis.css";
import { Footer } from "../components/layout/Footer";

const LoanAnalysis = () => {
  return (
    <section className="analysis-section">
      {/* Navbar */}
      <nav className="adashboard-navbar">
        <div className="dashboard-logo">
          Nano<i className="ri-money-rupee-circle-fill"></i>Rise
        </div>
      </nav>

      {/* Main Analysis Section */}
      <section className="main-analysis d-text">
        <div className="analysis-heading">
          <h1>
            Welcome to our <span>NanoRise Dashboard</span>
          </h1>
          <p>
            Your loan application has been submitted successfully. View your
            personalized loan insights and recommendations instantly!
          </p>
        </div>
      </section>

      {/* Embed Streamlit App
      <iframe
        className="streamlit-embed"
        src="https://creditworthy-customer-view.streamlit.app/?embed=true"
        title="Nano Entrepreneur App"
        frameBorder="0"
        allowFullScreen
        width="100%"
        height="800px"
        style={{ border: "none", marginTop: "20px" }}
        sandbox="allow-scripts allow-same-origin allow-forms"
      ></iframe> */}

      <Footer />
    </section>
  );
};

export default LoanAnalysis;
