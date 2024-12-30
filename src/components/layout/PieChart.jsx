import React from 'react';
import { Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

// Function to generate random values between 30 and 99
const getRandomValues = (count) => {
  return Array.from({ length: count }, () => Math.floor(Math.random() * (99 - 9 + 1)) + 30);
};  

const PieChart = () => {
  const randomData = getRandomValues(3); // Generate 3 random values

  const data = {
    labels: ['Red', 'Blue', 'Yellow'],
    datasets: [
      {
        label: 'Random Dataset',
        data: randomData,
        backgroundColor: [
          'rgba(255, 99, 132, 0.5)',
          'rgba(54, 162, 235, 0.5)',
          'rgba(255, 206, 86, 0.5)'
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)'
        ],
        borderWidth: 1
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false, // Allow precise sizing
    plugins: {
      legend: {
        position: 'top',
      },
      tooltip: {
        enabled: true,
      }
    }
  };

  return (
    <div className="chart-container">
      <div className="rotating-chart">
        <Pie data={data} options={options} />
      </div>
    </div>
  );
};

export default PieChart;
