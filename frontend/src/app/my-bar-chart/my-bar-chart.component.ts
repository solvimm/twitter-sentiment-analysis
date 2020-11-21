import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-my-bar-chart',
  templateUrl: './my-bar-chart.component.html',
  styleUrls: ['./my-bar-chart.component.css']
})
export class MyBarChartComponent implements OnInit {

  public barChartType = 'bar';
  public barChartLegend = false;

  public barChartOptions = {
    scaleShowVerticalLines: false,
    responsive: true,
    scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }],
        xAxes: [{
            display: true,
            distribution: 'series',
            ticks: {
                autoSkip: false
            }
        }]
      }
  };

  @Input()
  labels: string;

  @Input()
  data: number;

  constructor() { }

  ngOnInit() {
    console.log(this.labels);
    console.log(this.data);
  }

  

}
