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
                A necessary tool for any smart investor.
            </p>

        
        `;
    }

}