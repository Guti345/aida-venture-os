'use client'

import {
  BarChart as RechartsBar,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

interface DataPoint {
  name: string
  value: number
}

interface BarChartProps {
  data: DataPoint[]
  color?: string
  height?: number
  valueFormatter?: (v: number) => string
}

export default function BarChart({
  data,
  color = '#1A6FE8',
  height = 200,
  valueFormatter,
}: BarChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsBar data={data} barSize={28}>
        <CartesianGrid strokeDasharray="3 3" stroke="#9CA3AF20" vertical={false} />
        <XAxis
          dataKey="name"
          tick={{ fontSize: 12, fill: '#9CA3AF' }}
          axisLine={false}
          tickLine={false}
        />
        <YAxis
          tick={{ fontSize: 12, fill: '#9CA3AF' }}
          axisLine={false}
          tickLine={false}
          tickFormatter={valueFormatter}
          width={36}
        />
        <Tooltip
          cursor={{ fill: '#F5F7FA' }}
          contentStyle={{
            border: '1px solid #9CA3AF33',
            borderRadius: 6,
            fontSize: 12,
            background: '#fff',
          }}
          formatter={(value) => {
            const num = typeof value === 'number' ? value : Number(value)
            return valueFormatter ? [valueFormatter(num), ''] : [num, '']
          }}
        />
        <Bar dataKey="value" fill={color} radius={[4, 4, 0, 0]} />
      </RechartsBar>
    </ResponsiveContainer>
  )
}
