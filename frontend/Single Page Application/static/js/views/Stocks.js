import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor() {
        super();
        this.setTitle("Stocks");
    }

    //I think that the .json files will be set in the return statement below
    async getHtml() {
        return `
            <h1>Stocks</h1>
            <p>
                Here will be the list of stocks
            </p>

        
        `;
    }

}