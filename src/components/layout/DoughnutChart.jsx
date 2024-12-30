import React, { useEffect, useState } from 'react';
import { Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip);

// Function to generate a random percentage between 70 and 100
const getRandomPercentage = () => Math.floor(Math.random() * (100 - 70 + 1)) + 70;

const PercentageDoughnutChart = () => {
  const [rotationClass, setRotationClass] = useState(''); // State for rotation animation
  const randomPercentage = getRandomPercentage(); // Generate random percentage

  const data = {
    labels: [`${randomPercentage}%`], // Display the percentage as a label
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

  useEffect(() => {
    // Trigger the rotation animation on load
    setRotationClass('rotate-once');
    const timer = setTimeout(() => {
      setRotationClass('');
    }, 2000); // Matches animation duration

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className={`chart-container ${rotationClass}`}>
      <Doughnut data={data} options={options} />
      <div className="percentage-label">{randomPercentage}%</div>
    </div>
  );
};

export default PercentageDoughnutChart;
