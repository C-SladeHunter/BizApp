import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor() {
        super();
        this.setTitle("FAQ");
    }

    //I think that the .json files will be set in the return statement below
    async getHtml() {
        return `
            <h1>FAQ</h1>
            <p>
                Frequently asked questions.
                <br>
                <br>1. How do I view stocks?
                <br>Ans: You can access stock options from our stock tab, or see an overview on from dashboard.
                <br>
                <br>2. Can I purchase stocks from the site?
                <br>Ans: No, BizApp does not offer a way to purchase stock options in app.
                <br>
                <br>3. How much is the data updated?
                <br>Ans: The data is updated in real-time. Simply refresh the page for an update on stock option.
                <br>
                <br>4. Why should I trust this data?
                <br>Ans: All analytics that are available on BizApp are published through an API that takes data from
                professional websites many investors use in their day to day.
                <br>
                <br>5. How to use BizApp?
                <br>Ans: There isn't one way to use BizApp. You can view the history of stocks, how well they have performed, real time data, and predictive algorithm that
                may give insight to how a stock may perform going forward. 

            </p>

        
        `;
    }

}