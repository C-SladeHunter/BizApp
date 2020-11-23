import Dashboard from "./views/Dashboard.js";
import Stocks from "./views/Stocks.js";
import Crypto from "./views/Crypto.js";
import FAQ from "./views/FAQ.js";


const navigateTo = url => {
    history.pushState(null, null, url);
    router();
};

const router = async () => {
    const routes = [
        //Below is the root path of the webpage, or the 'frontpage' 
        //This may change to memphisbizapp.com later, not exactly sure yet
        { path: "/", view: Dashboard },
         
        //Stocks webpage in the side drawer
        { path: "/stocks", view: Stocks },

        //Crypto webpage in the side drawer
        { path: "/crypto", view: Crypto },

        //FAQ webpage in the side drawer
        { path: "/FAQ", view: FAQ },
    ];

    //testing each route for potential match
    const potentialMatches = routes.map(route => {
        return{
            route: route,
            isMatch: location.pathname === route.path

        };
    });

    let match = potentialMatches.find(potentialMatch => potentialMatch.isMatch);

    //incorrect url extension makes dashboard the default
    if (!match) {
        match = {
            route: routes[0],
            isMatch: true
        };
    }

    const view = new match.route.view();

    document.querySelector("#app").innerHTML = await view.getHtml();

    //console.log(match.route.view());
};

window.addEventListener("popstate", router);

document.addEventListener("DOMContentLoaded", () => {
    document.body.addEventListener("click", e => {
        if(e.target.matches("[data-link]")) {
            e.preventDefault();
            navigateTo(e.target.href);
        }
    });
    
    router();
});