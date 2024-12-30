import "./LoanAnalysis.css";
import { Footer } from "../components/layout/Footer";
import PieChart from "../components/layout/PieChart";
import { useNavigate } from "react-router-dom";
import DoughnutChart from "../components/layout/DoughnutChart";


const LoanAnalysis = () => {
  const navigate = useNavigate();

const handleSubmit = () => {
  navigate("/FinanceInsights");
};
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
            Welcome to our <span>Analysis Dashboard</span>
          </h1>
          <p>
            Your loan application has been submitted successfully.
          </p>
          <p> Get your Comprehensive analysis report now!
          </p>
        </div>
        <div className="results">
        <div className="status-container">
          <div className="status-item">
            <span className="status-text">Data from UPI transactions accessed</span>
            <span className="status-tick">✔</span>
          </div>
          <div className="status-item">
            <span className="status-text">Location Images provided are matched</span>
            <span className="status-tick">✔</span>
          </div>
          <div className="status-item">
            <span className="status-text">Feedback form sent to referenced people</span>
            <span className="status-tick">✔</span>
          </div>
          <div className="status-item">
            <span className="status-text">Documents provided are verified</span>
            <span className="status-tick">✔</span>
          </div>
          <div className="status-item">
            <span className="status-text">Credit History has been verified</span>
            <span className="status-tick">✔</span>
          </div>
        </div>
      <DoughnutChart/>
    </div>
        
        
        

        <button
            className="btn"
            onClick={()=>handleSubmit()}
          >
            Next
          </button>
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

<Footer/>  
      
    </section>
  );
};

export default LoanAnalysis;
