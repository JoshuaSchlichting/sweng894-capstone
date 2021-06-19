/*!
    * Start Bootstrap - SB Admin v7.0.1 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2021 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

function getJwtHeader(){
    return 'Bearer: ' + localStorage.getItem('jwt');
}

function parseJwt (token) {
    if(localStorage.jwt == "null") return;
    try{
        var base64Url = token.split('.')[1];
        var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
    }catch(err){
        console.log("An error occurred while attempting to parase a JWT!!!");
        console.log(err);
        return null;
    }

    return JSON.parse(jsonPayload);
};

function getJwt(){
    return localStorage.jwt;
}

function getUserName(){
    let jwtObj = parseJwt(getJwt());
    return jwtObj.username;
}

function getUserType(){
    let jwtObj = parseJwt(getJwt());
    return jwtObj.userType;
}

function getUserIsAdmin(){
    let jwtObj = parseJwt(getJwt());
    return jwtObj.userType == 'admin';
}

function displayElement(elementId, makeVisible=true){
    document.getElementById(elementId).style.visibility = (makeVisible ? 'visible' : 'hidden');
}


$(document).ready(function(){
    let token = parseJwt(getJwt());
    if (getUserIsAdmin()){
        displayElement('adminPanelBtn');
    }

    if (token.username){
        displayElement('loginBtn', makeVisible=false);
        document.getElementById('username').innerText = token.username;
        displayElement('loggedInPrompt');
    }else{
        displayElement('loggedInPrompt', makeVisible=false);
        displayElement('loginBtn');
    }


})


$('#logoutBtn').click(function(){
    localStorage.setItem('jwt', null);
    window.location = "/"
})

$('#loginBtn').click(function(){
    window.location = "/login"
})
