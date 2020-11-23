import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor() {
        super();
        this.setTitle("Dashboard");
    }

    async getHtml() {
        return `
            <h1>Welcome to BizApp</h1>
            <p>
                <u><b>My Favorites:</b></u>
                    <br>
                <b>MSFT</b> - Microsoft Corporation
                    <br>
                <b>AAPL</b> - Apple Inc
                    <br>
                <b>GOOG</b> - Alphabet Inc Class C

            </p>

        
        `;
    }

}