import { Component, Inject, PLATFORM_ID, OnInit } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import * as Highcharts from 'highcharts';
import { HighchartsChartModule } from 'highcharts-angular';
import { ChartsComponent } from '../../charts/charts.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
  imports: [HighchartsChartModule, ChartsComponent]
})
export class DashboardComponent {
  
  }
  

  // aici păstrezi graficele la fel
  

  /* memoryGaugeOptions: Highcharts.Options = {
    chart: { type: 'solidgauge' },
    title: { text: 'Memory Usage' },
    pane: {
      center: ['50%', '85%'],
      size: '100%',
      startAngle: -90,
      endAngle: 90,
      background: [{ backgroundColor: '#EEE', innerRadius: '60%', outerRadius: '100%', shape: 'arc' }]
    },
    yAxis: { min: 0, max: 100, title: { text: 'Memory %' } },
    series: [{ type: 'solidgauge', name: 'Memory', data: [45] }]
  };
  
  storageGaugeOptions: Highcharts.Options = {
    chart: { type: 'solidgauge' },
    title: { text: 'Storage Usage' },
    pane: {
      center: ['50%', '85%'],
      size: '100%',
      startAngle: -90,
      endAngle: 90,
      background: [{ backgroundColor: '#EEE', innerRadius: '60%', outerRadius: '100%', shape: 'arc' }]
    },
    yAxis: { min: 0, max: 100, title: { text: 'Storage %' } },
    series: [{ type: 'solidgauge', name: 'Storage', data: [60] }]
  };
  
  loadAverageOptions: Highcharts.Options = {
    chart: { type: 'line' },
    title: { text: 'Load Average' },
    xAxis: { categories: ['1m', '5m', '15m'] },
    yAxis: { title: { text: 'Load' } },
    series: [{
      type: 'line',
      name: 'Load',
      data: [0.5, 0.7, 0.9]
    }]
  };
  
  cpuFrequencyOptions: Highcharts.Options = {
    chart: { type: 'line' },
    title: { text: 'CPU Frequency' },
    xAxis: { categories: ['Core 1', 'Core 2', 'Core 3', 'Core 4'] },
    yAxis: { title: { text: 'Frequency (GHz)' } },
    series: [{
      type: 'line',
      name: 'Frequency',
      data: [3.4, 3.5, 3.3, 3.6]
    }]
  };
*/

