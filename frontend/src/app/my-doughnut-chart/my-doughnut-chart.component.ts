import { Component, OnInit, Input} from '@angular/core';

@Component({
  selector: 'app-my-doughnut-chart',
  templateUrl: './my-doughnut-chart.component.html',
  styleUrls: ['./my-doughnut-chart.component.css']
})
export class MyDoughnutChartComponent implements OnInit {

  @Input()
  labels: string;

  @Input()
  data: number;

  @Input()
  colors: string;

  constructor() { }

  ngOnInit() {
    
  }

}
