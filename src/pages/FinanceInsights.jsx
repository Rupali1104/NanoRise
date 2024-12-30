import "./LoanAnalysis.css";
import { Footer } from "../components/layout/Footer";
import "./FinanceInsights.css";


const FinanceInsights = () => {
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
            Get your <span>Finance Insights</span> Using AI
          </h1>
          <p>
            View your personalized loan insights and recommendations instantly!
          </p>
        </div>

        {/* Financial Insights */}
        <div className="financial-insights">
          <h2>AI-Powered Financial Insights</h2>
          
          {/* Financial Health Analysis */}
          <div className="financial-analysis">
            <h3>Financial Health Analysis</h3>
            <h4>Income and Expense Analysis</h4>
            <ul>
              <li>Your income to expense ratio is 5.61, indicating strong financial health</li>
              <li>Average transaction size: ₹2,750.00</li>
              <li>Net cashflow: ₹152,000.00 (positive)</li>
            </ul>
          </div>

          {/* Strengths */}
          <div className="strengths">
            <h4>Strengths</h4>
            <ul>
              <li>Strong income stability</li>
              <li>Opportunity to build business resilience</li>
            </ul>
          </div>

          {/* Areas for Improvement */}
          <div className="areas-for-improvement">
            <h4>Areas for Improvement</h4>
            <ul>
              <li>Focus on transaction discipline</li>
              <li>Strong growth trajectory</li>
            </ul>
          </div>

          {/* Recommendations */}
          <div className="recommendations">
            <h4>Recommendations</h4>
            <ol>
              <li>Maintain strong income streams</li>
              <li>Continue maintaining healthy reserves</li>
              <li>Maintain current expense management</li>
              <li>Focus on consistent transactions</li>
            </ol>
          </div>

          {/* Financial Management Tips */}
          <aside className="financial-tips">
            <h4>💡 Financial Management Tips</h4>
            <ul>
              <li>Maintain consistent income streams</li>
              <li>Control and minimize unnecessary expenses</li>
              <li>Build an emergency fund</li>
              <li>Invest in business growth</li>
              <li>Regularly review financial performance</li>
            </ul>
          </aside>
        </div>
      </section>

      <Footer />
    </section>
  );
};

export default FinanceInsights;

