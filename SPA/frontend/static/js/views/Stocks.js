import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor() {
        super();
        this.setTitle("Stocks");
    }

    //edit test() funciton name to match stock graph function
    //I think that the .json files will be set in the return statement below
    async getHtml() {
        return `
                        
                    <h1>Stocks</h1>
                    <head>
                    </head>

                    <body>
                        <div id ="symbol"></div>
                        <div id="chart"></div>

                        <input type="text" id="userInput"></input>
                        <button onclick="stock_graph()">Submit</button>

                    </body>

        
        `;
    }

}