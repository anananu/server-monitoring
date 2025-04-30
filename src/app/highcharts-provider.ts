import { importProvidersFrom } from '@angular/core';
import { HighchartsChartModule } from 'highcharts-angular';

export function provideHighchartsChart() {
  return importProvidersFrom(HighchartsChartModule);
}
