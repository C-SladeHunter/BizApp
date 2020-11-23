import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor() {
        super();
        this.setTitle("Crypto");
    }

    //I think that the .json files will be set in the return statement below
    async getHtml() {
        return `
                <h1>Crypto</h1>

                <body>
                    <div id ="symbol"></div>
                    <div id="chart"></div>

                    <input type="text" id="userInput"></input>
                    <button onclick="crypto_Graph()">Submit</button>

                </body>
        `;
    }

}