import { Component } from '@angular/core';
import { HighchartsChartModule } from 'highcharts-angular';
import Highcharts from 'highcharts';

@Component({
  selector: 'app-charts',
  imports: [HighchartsChartModule],
  templateUrl: './charts.component.html',
  styleUrl: './charts.component.css'
})
export class ChartsComponent {
  Highcharts: typeof Highcharts = Highcharts;
  
  cpuGaugeOptions: Highcharts.Options = {
      chart: { type: 'solidgauge' },
      title: { text: 'CPU Usage' },
      pane: { 
        center: ['50%', '85%'], 
        size: '100%', 
        startAngle: -90, 
        endAngle: 90, 
        background: [{ backgroundColor: '#EEE', innerRadius: '60%', outerRadius: '100%', shape: 'arc' }]
      },
      yAxis: { min: 0, max: 100, title: { text: 'CPU %' } },
      series: [{ type: 'solidgauge', name: 'CPU', data: [70] }]
    };


}
