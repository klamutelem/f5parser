/*
This is JS file where we specify all the front end action
*/
/*
----------------------------------------------
Below we have functions related to general layout
----------------------------------------------
*/
function highlightdiv(div){
    div.style.backgroundcolor = "darkblue";
}

/*
----------------------------------------------
Below we have functions related to F5 parser
----------------------------------------------
*/
function autoResize(textarea) {
    textarea.style.height = 'auto'; // Reset height
    textarea.style.height = textarea.scrollHeight + 'px'; // Set height to scrollHeight
}

function submitForm(event){
    event.preventDefault();
    //This is mandatory for some reason :D

    const name = document.getElementById('name').value ;
    const surname = document.getElementById('surname').value ;

    //We extract the values from the HTML form using 

    const data = {
        name: name,
        surname: surname
    };

    fetch('/page1', {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
        })
    .then(response => {
        //console.log("Fetch response received");
        if (response.ok) {
            return response.json(); 
        } else {
            throw new Error('Network response was not ok'); 
        }
    })
    .then(data => console.log(data))
    .catch(error => console.error('There was a problem with the fetch operation:', error));


}

function submitFormAsString(event){
    event.preventDefault();
    const string = document.getElementById('string').value;
    const result = document.getElementById('result');
    

    fetch('LBparse',{
        method: 'POST',
        headers:{
            'Content-type': 'text/plain'
        },
        body: string
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();  // Parse the JSON data
    })
    .then(data => {
        // Step 3: Display the data in HTML
        result.innerHTML = JSON.stringify(data, null, 2);  // Display as formatted JSON
        autoResize(result)
    })

    function submitFormAsJSON(event){
        event.preventDefault();
        const JSONdata = document.getElementById('result').value;
        console.log("YOu are here")
        alert("You have clicked")
    }
}