'use client'

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'

interface DataPoint {
  name: string
  value: number
}

interface DonutChartProps {
  data: DataPoint[]
  height?: number
  colors?: string[]
  showLegend?: boolean
}

const DEFAULT_COLORS = ['#1A6FE8', '#22C55E', '#F5A623', '#EF4444', '#9CA3AF', '#0B1628']

export default function DonutChart({
  data,
  height = 200,
  colors = DEFAULT_COLORS,
  showLegend = true,
}: DonutChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={55}
          outerRadius={80}
          paddingAngle={3}
          dataKey="value"
        >
          {data.map((_, index) => (
            <Cell key={index} fill={colors[index % colors.length]} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            border: '1px solid #9CA3AF33',
            borderRadius: 6,
            fontSize: 12,
            background: '#fff',
          }}
        />
        {showLegend && (
          <Legend
            iconType="circle"
            iconSize={8}
            wrapperStyle={{ fontSize: 12, color: '#9CA3AF' }}
          />
        )}
      </PieChart>
    </ResponsiveContainer>
  )
}
