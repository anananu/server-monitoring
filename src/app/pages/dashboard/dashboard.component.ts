import { Component } from '@angular/core';
import * as Highcharts from 'highcharts';
import HighchartsMore from 'highcharts/highcharts-more';
import SolidGauge from 'highcharts/modules/solid-gauge';

// Activăm modulele suplimentare Highcharts
HighchartsMore(Highcharts);
SolidGauge(Highcharts);

@Component({
  selector: 'app-dashboard',
  standalone: true,
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  Highcharts: typeof Highcharts = Highcharts;

  cpuGaugeOptions: Highcharts.Options = {
    chart: { type: 'solidgauge' },
    title: { text: 'CPU Usage' },
    pane: { center: ['50%', '85%'], size: '100%', startAngle: -90, endAngle: 90, background: [{ backgroundColor: '#EEE', innerRadius: '60%', outerRadius: '100%', shape: 'arc' }]},
    yAxis: { min: 0, max: 100, title: { text: 'CPU %' } },
    series: [{ type: 'solidgauge', name: 'CPU', data: [70] }]
  };

  memoryGaugeOptions: Highcharts.Options = {
    chart: { type: 'solidgauge' },
    title: { text: 'Memory Usage' },
    pane: { center: ['50%', '85%'], size: '100%', startAngle: -90, endAngle: 90, background: [{ backgroundColor: '#EEE', innerRadius: '60%', outerRadius: '100%', shape: 'arc' }]},
    yAxis: { min: 0, max: 100, title: { text: 'Memory %' } },
    series: [{ type: 'solidgauge', name: 'Memory', data: [55] }]
  };

  storageGaugeOptions: Highcharts.Options = {
    chart: { type: 'solidgauge' },
    title: { text: 'Storage Usage' },
    pane: { center: ['50%', '85%'], size: '100%', startAngle: -90, endAngle: 90, background: [{ backgroundColor: '#EEE', innerRadius: '60%', outerRadius: '100%', shape: 'arc' }]},
    yAxis: { min: 0, max: 100, title: { text: 'Storage %' } },
    series: [{ type: 'solidgauge', name: 'Storage', data: [40] }]
  };

  loadAverageOptions: Highcharts.Options = {
    title: { text: 'Load Average (1m, 5m, 15m)' },
    xAxis: { categories: ['10min', '20min', '30min', '40min', '50min', '1h'] },
    yAxis: { title: { text: 'Load' } },
    series: [
      { type: 'area', name: '1 min', data: [0.2, 0.3, 0.4, 0.35, 0.5, 0.6] },
      { type: 'area', name: '5 min', data: [0.1, 0.2, 0.3, 0.3, 0.35, 0.4] },
      { type: 'area', name: '15 min', data: [0.05, 0.1, 0.15, 0.2, 0.25, 0.3] }
    ]
  };

  cpuFrequencyOptions: Highcharts.Options = {
    title: { text: 'CPU Frequency per Core' },
    xAxis: { categories: ['Core 1', 'Core 2', 'Core 3', 'Core 4'] },
    yAxis: { title: { text: 'Frequency (MHz)' } },
    series: [
      { type: 'line', name: 'Core 1', data: [2500, 2600, 2550, 2650] },
      { type: 'line', name: 'Core 2', data: [2400, 2450, 2500, 2550] },
      { type: 'line', name: 'Core 3', data: [2300, 2350, 2400, 2450] },
      { type: 'line', name: 'Core 4', data: [2200, 2250, 2300, 2350] }
    ]
  };
}
