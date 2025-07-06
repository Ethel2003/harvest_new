import React from 'react';

interface LineChartData {
  date: string;
  value: number;
}

interface LineChartProps {
  data: LineChartData[];
}

const LineChart: React.FC<LineChartProps> = ({ data }) => {
  const maxValue = Math.max(...data.map(d => d.value));
  const chartHeight = 200;
  const chartWidth = 400;
  const padding = 40;

  const points = data.map((item, index) => {
    const x = (index / (data.length - 1)) * (chartWidth - 2 * padding) + padding;
    const y = chartHeight - padding - ((item.value / maxValue) * (chartHeight - 2 * padding));
    return { x, y, value: item.value, date: item.date };
  });

  const pathData = points.map((point, index) => 
    `${index === 0 ? 'M' : 'L'} ${point.x} ${point.y}`
  ).join(' ');

  return (
    <div className="w-full">
      <svg width="100%" height={chartHeight} viewBox={`0 0 ${chartWidth} ${chartHeight}`} className="overflow-visible">
        {/* Grid lines */}
        {[0, 1, 2, 3, 4, 5].map(i => (
          <line
            key={i}
            x1={padding}
            y1={chartHeight - padding - (i / 5) * (chartHeight - 2 * padding)}
            x2={chartWidth - padding}
            y2={chartHeight - padding - (i / 5) * (chartHeight - 2 * padding)}
            stroke="#f3f4f6"
            strokeWidth="1"
          />
        ))}
        
        {/* Y-axis labels */}
        {[0, 1, 2, 3, 4, 5].map(i => (
          <text
            key={i}
            x={padding - 10}
            y={chartHeight - padding - (i / 5) * (chartHeight - 2 * padding) + 4}
            textAnchor="end"
            className="text-xs fill-gray-500"
          >
            {i}
          </text>
        ))}

        {/* Line */}
        <path
          d={pathData}
          fill="none"
          stroke="#22c55e"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* Points */}
        {points.map((point, index) => (
          <circle
            key={index}
            cx={point.x}
            cy={point.y}
            r="4"
            fill="#22c55e"
            className="hover:r-6 transition-all cursor-pointer"
          />
        ))}

        {/* X-axis labels */}
        {points.map((point, index) => (
          <text
            key={index}
            x={point.x}
            y={chartHeight - 10}
            textAnchor="middle"
            className="text-xs fill-gray-500"
          >
            {point.date}
          </text>
        ))}
      </svg>
    </div>
  );
};

export default LineChart;