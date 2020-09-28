import React from 'react'
import { ResponsivePie } from '@nivo/pie'

function generateHslaColors (saturation, lightness, alpha, amount) {
    let colors = []
    let huedelta = Math.trunc(360 / amount)
  
    for (let i = 0; i < amount; i++) {
      let hue = i * huedelta
      colors.push(`hsla(${hue},${saturation}%,${lightness}%,${alpha})`)
    }
  
    return colors
  }
  

function MyResponsivePie({title,data}) {
      const defs = [
        {
            id: 'dots',
            type: 'patternDots',
            background: 'inherit',
            color: 'rgba(255, 255, 255, 0.3)',
            size: 4,
            padding: 1,
            stagger: true
        },
        {
            id: 'lines',
            type: 'patternLines',
            background: 'inherit',
            color: 'rgba(255, 255, 255, 0.3)',
            rotation: -45,
            lineWidth: 6,
            spacing: 10
        }
    ]

    return (
        <div className="pie-chart">
            <h3 className="chart-title">{title}</h3>
            <div style={{height: 'calc(100% - 4rem)'}}>
        <ResponsivePie
            data={data}
            margin={{ top: 40, right: 0, bottom: 80, left: 80 }}
            innerRadius={0.5}
            padAngle={0.7}
            cornerRadius={3}
            colors={{scheme: 'category10'}}
            borderWidth={1}
            borderColor={{ from: 'color', modifiers: [ [ 'darker', 0.2 ] ] }}
            radialLabelsSkipAngle={10}
            radialLabelsTextXOffset={6}
            radialLabelsTextColor="#333333"
            radialLabelsLinkOffset={0}
            radialLabelsLinkDiagonalLength={16}
            radialLabelsLinkHorizontalLength={24}
            radialLabelsLinkStrokeWidth={1}
            radialLabelsLinkColor={{ from: 'color' }}
            slicesLabelsSkipAngle={10}
            slicesLabelsTextColor="#333333"
            animate={true}
            motionStiffness={90}
            motionDamping={15}
        defs={defs}
        fill={[]}
        legends={[
            {
                anchor: 'top-left',
                direction: 'column',
                translateY: 56,
                itemWidth: 80,
                itemHeight: 18,
                itemTextColor: '#999',
                symbolSize: 12,
                symbolShape: 'circle',
                effects: [
                    {
                        on: 'hover',
                        style: {
                            itemTextColor: '#000'
                        }
                    }
                ]
            }
        ]}
    />
    </div>
</div>)
}

export default MyResponsivePie