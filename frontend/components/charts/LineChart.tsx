'use client'

import {
  LineChart as RechartsLine,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts'

interface DataPoint {
  date: string
  value: number
}

interface LineChartProps {
  data: DataPoint[]
  color?: string
  height?: number
  valueFormatter?: (v: number) => string
  referenceValue?: number
}

export default function LineChart({
  data,
  color = '#1A6FE8',
  height = 200,
  valueFormatter,
  referenceValue,
}: LineChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsLine data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#9CA3AF20" vertical={false} />
        <XAxis
          dataKey="date"
          tick={{ fontSize: 12, fill: '#9CA3AF' }}
          axisLine={false}
          tickLine={false}
        />
        <YAxis
          tick={{ fontSize: 12, fill: '#9CA3AF' }}
          axisLine={false}
          tickLine={false}
          tickFormatter={valueFormatter}
          width={48}
        />
        <Tooltip
          contentStyle={{
            border: '1px solid #9CA3AF33',
            borderRadius: 6,
            fontSize: 12,
            background: '#fff',
          }}
          formatter={(value) => {
            const num = typeof value === 'number' ? value : Number(value)
            return valueFormatter ? [valueFormatter(num), 'ARR'] : [num, 'ARR']
          }}
        />
        {referenceValue !== undefined && (
          <ReferenceLine
            y={referenceValue}
            stroke="#9CA3AF"
            strokeDasharray="4 4"
            label={{ value: 'P50 mercado', fontSize: 11, fill: '#9CA3AF' }}
          />
        )}
        <Line
          type="monotone"
          dataKey="value"
          stroke={color}
          strokeWidth={2}
          dot={{ r: 3, fill: color, strokeWidth: 0 }}
          activeDot={{ r: 5 }}
        />
      </RechartsLine>
    </ResponsiveContainer>
  )
}
