import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {HttpParams} from "@angular/common/http";
import { CloudData, CloudOptions } from 'angular-tag-cloud-module';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  
    public response;
    
    public sentimentLabels = [];
    public sentimentData = [];
    public sentimentColors = [];
    public sentimentColorsMapping = {"POSITIVE": 'rgba(0, 196, 0, 0.4)', "NEUTRAL": 'rgba(196, 196, 196, 0.4)', "NEGATIVE": 'rgba(255, 0, 0, 0.4)', 'MIXED': 'rgba(128, 64, 0, 0.4)', "UNDEFINED": 'rgba(240, 240, 240, 0.3)', "undefined": 'rgba(240, 240, 240, 0.3)'};
    public sentimentLabelsMapping = {"POSITIVE": 'Positivo', "NEUTRAL": 'Neutro', "NEGATIVE": 'Negativo', 'MIXED': 'Misto',"UNDEFINED": "Indefinido", "undefined": "Indefinido"};

    public peopleLabels = [];
    public peopleData = [];

    public organizationLabels = [];
    public organizationData = [];

    public languageLabels = [];
    public languageData = [];
    public languageColors = [];
    public languageColorsMapping = {"pt": 'rgba(0, 128, 0, 0.4)', "en": 'rgba(255, 0, 0, 0.4)', "fr": 'rgba(0, 0, 255, 0.4)', "es": 'rgba(196, 196, 0, 0.4)', 'de': 'rgba(128, 0, 128, 0.4)', 'it': 'rgba(0, 126, 0, 0.4)', "UNDEFINED": 'rgba(240, 240, 240, 0.3)', "undefined": 'rgba(240, 240, 240, 0.3)'};
    public languageLabelsMapping = {"pt": 'Português', "en": 'Inglês', "fr": 'Francês', "es": 'Espanhol', 'de': 'Alemão', 'it': 'Italiano', "UNDEFINED": "Indefinido", "undefined": "Indefinido"};
    

    cloudOptions: CloudOptions = {
        width: 1,
        height: 1,
        overflow: false,
    };

    cloudData: CloudData[] = [];

    public data_loaded = false;
    public loading = false;

    search_element: string;

  constructor(private http:HttpClient) {
  }

  r = {};

  public getSentiment(){
        const search_type = this.search_element.substring(0, 1);
        const search_key = this.search_element.substring(1);

        if (search_type != '@' && search_type != '#') {
            alert("Para fazer a busca, coloque @, se quiser pesquisar sobre um usuário, ou #, se quer buscar uma #. Por exemplo, utilize @" + this.search_element + " ou #" + this.search_element + " na busca.");
        } else {
            this.loading = true;
            this.data_loaded = false;
            const params = new HttpParams().set('search_key', search_key).set('search_type', search_type);
            this.response = this.http
            .get("https://67v2nzkxpl.execute-api.us-east-1.amazonaws.com/dev/sentiment", {params}).subscribe(data => {
                this.loading = false;
                this.r = data;
                console.log(this.r);

                const sentimentLabelsTmp = Object.keys(this.r["body"]["sentiment"]);
                this.sentimentLabels = [];
                sentimentLabelsTmp.forEach(sentimentLabel => {
                    this.sentimentLabels.push(this.sentimentLabelsMapping[sentimentLabel]);
                });

                this.sentimentData = Object.values(this.r["body"]["sentiment"]);
                var sentimentColorsList = []
                sentimentLabelsTmp.forEach(sentimentLabel => {
                    sentimentColorsList.push(this.sentimentColorsMapping[sentimentLabel]);
                });
                this.sentimentColors = [{backgroundColor: sentimentColorsList}];


                this.peopleLabels = Object.keys(this.r["body"]["entity_people"]);
                this.peopleData = [{data: Object.values(this.r["body"]["entity_people"]), label: 'Menções'}];
                
                /*
                this.peopleLabels = Object.keys(this.r["body"]["entity_people"]);
                const peopleDataTmp = this.r["body"]["entity_people"];

                console.log('starting');
                this.peopleData = [];
                this.peopleLabels.forEach((value, index) => {
                    console.log(value);
                    console.log(peopleDataTmp[value]);
                    let arr = new Array<number>(this.peopleLabels.length);
                    arr[index] = peopleDataTmp[value];
                    this.peopleData.push({data: arr, label: value});
                });
                */

                // this.peopleData = [{data: Object.values(this.r["body"]["entity_people"]), label: 'Menções'}];
                // console.log(Object.values(this.r["body"]["entity_people"]))
                // console.log(this.peopleLabels);
                // console.log(this.peopleData);

                // this.peopleLabels = Object.keys(this.r["body"]["entity_people"]);
                // this.peopleData = [{data: Object.values(this.r["body"]["entity_people"]), label: 'Menções'}];

                this.organizationLabels = Object.keys(this.r["body"]["entity_organization"]);
                this.organizationData = [{data: Object.values(this.r["body"]["entity_organization"]), label: 'Menções'}];
                console.log('test')
                console.log(this.organizationLabels);
                console.log(Object.values(this.r["body"]["entity_organization"]));
                console.log(this.organizationData);
                console.log('end')

                // this.organizationData = [{data: Object.values(this.r["body"]["entity_organization"]), label: 'Menções'}];

                const languageLabelsTmp = Object.keys(this.r["body"]["language"]);

                // this.languageLabels = Object.keys(this.r["body"]["language"]);
                this.languageLabels = [];
                languageLabelsTmp.forEach(languageLabel => {
                    this.languageLabels.push(this.languageLabelsMapping[languageLabel]);
                });

                this.languageData = Object.values(this.r["body"]["language"]);

                var languageColorsList = []
                languageLabelsTmp.forEach(languageLabel => {
                    languageColorsList.push(this.languageColorsMapping[languageLabel]);
                });
                this.languageColors = [{backgroundColor: languageColorsList}];

                const wordCloudTmp = Object.keys(this.r["body"]["words"]);
                this.cloudData = [];
                wordCloudTmp.forEach(word => {
                    this.cloudData.push({text: word, weight: this.r["body"]["words"][word]});
                });

                this.data_loaded = true;
                
            });
        }
  }
  title = 'ngchart';

}

