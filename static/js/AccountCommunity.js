let communityNav = document.getElementsByClassName("nav-link");
let allCommunity = document.getElementsByClassName("all-community")[0];
let myCommunity = document.getElementsByClassName("my-community")[0];

for (let i = 0; i < communityNav.length; i++) {
    communityNav[i].addEventListener("click", function() {
        this.classList.add("active");
        if (this.classList.contains("all-item")) {
            allCommunity.style.display = 'block';
            myCommunity.style.display = 'none';
        } else {
            allCommunity.style.display = 'none';
            myCommunity.style.display = 'block';
        }
        for (let j = 0; j < communityNav.length; j++) {
            if (communityNav[j] !== this) {
                communityNav[j].classList.toggle("active");
            }
        }
    });
}