import { Component, AfterViewInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import * as Highcharts from 'highcharts';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements AfterViewInit {
  title = 'monitoring-dashboard';
  ngAfterViewInit() {
    Highcharts.chart('container', {
      title: {
        text: 'CPU Usage'
      },
      yAxis: {
        title: {
          text: 'Usage (%)'
        }
      },
      xAxis: {
        categories: ['Core 1', 'Core 2', 'Core 3', 'Core 4']
      },
      series: [{
        type: 'column',
        name: 'Load',
        data: [30, 40, 55, 70]
      }]
    });
  }
}

