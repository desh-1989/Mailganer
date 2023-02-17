let mailTitles = document.getElementsByClassName("mail-title");
let Mails = document.getElementsByClassName("mail-body");
let myCommunity = document.getElementsByClassName("my-community")[0];

mailTitles[0].classList.add("active")
Mails[0].classList.add("active")

for (let i = 0; i < mailTitles.length; i++) {
    mailTitles[i].addEventListener("click", function() {
        this.classList.add("active");
        for (let j = 0; j < mailTitles.length; j++) {
            if (mailTitles[j].id !== this.id) {
                mailTitles[j].classList.remove("active");
            }
        }
        for (let k = 0; k < Mails.length; k++) {
            if (Mails[k].id.split('-')[1] !== this.id.split('-')[1]) {
                Mails[k].classList.remove("active");
            } else {
                Mails[k].classList.add("active");
            }
        }
    });
}
