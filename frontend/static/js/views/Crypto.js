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
            <p>
                Here will be the list of crypto
            </p>

        
        `;
    }

}