function init() {
    console.log("Helle from group membership")

    let node = document.createElement('li')
    node.appendChild(document.createTextNode('Processor created by JS'))

    let list = document.querySelector('ul')
    list.appendChild(node)
    fetchAndDisplayAllProcessors();

}

/**
 * Fetches all the processors either working or crashed, and displays them in the page
 */
function fetchAndDisplayAllProcessors() {
    const url = '/all-processors';
    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            let list = document.querySelector('ul')
            for (let processor of data) {
                let node = document.createElement('li');
                node.appendChild(document.createTextNode(`Processor ${processor.id}, members: ${processor.members}`));
                list.appendChild(node);
            }
        });
}