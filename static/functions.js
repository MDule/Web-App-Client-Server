function search_db() {

    let index_num = document.getElementById('search-input').value;
    let xhttp = new XMLHttpRequest();
    

    xhttp.onreadystatechange = function () {
        document.getElementById('search-results').innerHTML = this.responseText;
    }

    xhttp.open('GET', 'http://127.0.0.1:8080/?index_num=' + index_num, true)
    xhttp.send();
};


function new_student_db() {

    let name = document.getElementById('name').value;
    let surname = document.getElementById('surname').value;
    let index_num = document.getElementById('index-num').value;
    let gpa = document.getElementById('gpa').value;

    console.log(name, surname, index_num, gpa)

    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function () {
        document.getElementById('new_student_results').innerHTML = this.responseText;
    }

    xhttp.open('POST',
        'http://127.0.0.1:8080/?name=' + name
        + '&surname=' + surname
        + '&index_num=' + index_num
        + '&gpa=' + gpa,
        true);
    xhttp.send();
}