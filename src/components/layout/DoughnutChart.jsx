import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip);

// Function to generate a random percentage between 70 and 100
const getRandomPercentage = () => Math.floor(Math.random() * (90 - 75 + 1)) + 75;

const DoughnutChart = () => {
  const randomPercentage = getRandomPercentage(); // Generate random percentage

  const data = {
    labels: ['CreditWorthiness',],
    datasets: [
      {
        data: [randomPercentage, 100 - randomPercentage], // Show percentage and remaining part
        backgroundColor: ['rgba(34, 139, 34, 0.8)', 'rgba(220, 220, 220, 0.3)'], // Green and light gray
        borderColor: ['rgba(34, 139, 34, 1)', 'rgba(220, 220, 220, 0.3)'], // Matching border colors
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      tooltip: {
        enabled: false, // Disable tooltip for simplicity
      },
    },
    cutout: '80%', // Thin doughnut
  };

  return (
    <div className="chart-container">
      <div className="rotating-chart">
        <Doughnut data={data} options={options} />
      </div>
      <div className="percentage-label">{randomPercentage}/100</div>
      Congratulations! You are Eligible..!
    </div>
  );
};

export default DoughnutChart;
