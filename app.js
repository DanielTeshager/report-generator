const submit = document.querySelector('#submit');
const sentence = document.querySelector('#sentence');
const category = document.querySelector('#category');
const issues_list = document.querySelector('.issues-list');
const actions_list = document.querySelector('.actions-list');
const form = document.querySelector('form');
const add = document.querySelectorAll('.add');
const remove = document.querySelectorAll('.remove');
const ul = document.querySelectorAll('ul');
const pod = document.querySelector('#pod');
const clear_pod = document.querySelector('#clear-pod');
const sentence_pod = document.querySelector('.sentence-pod');

pod.addEventListener('click', (e) => {
    clicked_element = e.target.parentElement;
    console.log(clicked_element);
    if(clicked_element.className === 'pod-item'){   
        if(sentence_pod.children.length === 0){
            sentence_pod.classList.add('hide');
        } 
     clicked_element.remove();
    }
});

clear_pod.addEventListener('click', (e) => {
    pod.innerHTML = '';
    // add hide to parent element
    sentence_pod.classList.add('hide');
});

issues_list.addEventListener('click', (e) => {
    // get child element text
    actions(e);
});
actions_list.addEventListener('click', (e) => {
    // get child element text
    actions(e);
});
  function actions(e){
    const clicked_element = e.target;
    // check if sentece_pod has class hide

    if (clicked_element.className === 'remove'){
        // console.log(clicked_element.parentElement.id);
        console.log('a', sentence_pod);
       
        clicked_element.parentElement.remove();
        // check if sentence_pod has elements if not hide it
       
    }
    if(clicked_element.className === 'add'){
        console.log(clicked_element.parentNode.children[1].innerText);
        // add to the pod
        if(sentence_pod.classList.contains('hide')){
            sentence_pod.classList.remove('hide');
        }
        pod.innerHTML += `<div class="pod-item">
        <div class="pod-item-text">${clicked_element.parentNode.children[1].innerText}</div>
        <div class="pod-item-remove">
            <i class="fas fa-times"></i>
        </div>
    </div>`;
       
    }

  }



async function postData(url = '', data = {}, method = 'POST') {
    // Default options are marked with *
    const response = await fetch(url, {
      method: method, // *GET, POST, PUT, DELETE, etc.
    //   mode: 'no-cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    //   credentials: 'same-origin', // include, *same-origin, omit
      headers: {
        'Content-Type': 'application/json'
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: Object.keys(data).length > 0 ?  JSON.stringify(data) : null, // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
  }


submit.addEventListener('click', (e) => {

    
   e.preventDefault(); 
    // Example POST method implementation:
  const data = {title: sentence.value, category: category.value};
  postData("http://127.0.0.1:5000/sentences", data, 'POST')
    .then(data => {
        console.log(data);
    });


});

function load(){
    postData('http://127.0.0.1:5000/sentences', '', 'GET')
    .then(data => {
    //   filter category
        populate(data);
        console.log(data)
    //populate the page
    }).catch(err => {
        console.log(err);
    });
    console.log(sentence.value, category.value);
}

function populate(data){
    console.log(data)
    const actions = data.Sentences.filter(sentence => sentence.category ==='Action');
    const issues = data.Sentences.filter(sentence => sentence.category ==='Issue')

    issues_list.innerHTML = issues.map(sentence => `
    <li id='${sentence.id}'>
    <span class='remove'>   <i class="fas fa-times"></i> </span>
    <span>${sentence.title}</span>
    <span class='add'>   <i class="fas fa-plus"></i> </span>
    </li>
    `).join('');
    actions_list.innerHTML = actions.map(sentence => `
    <li id='${sentence.id}'>
    <span class='remove'>   <i class="fas fa-times"></i> </span>
    <span>${sentence.title}</span>
    <span class='add'>   <i class="fas fa-plus"></i> </span>
    </li>
    `).join('');
}