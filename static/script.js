/**
 * Handles the event when the start button is clicked, wraps the user typed data and
 * sends to the backend
 */
function startButtonOnclick() {
    console.log("Start clicked");
    const url = '/init'
    let numProcessors = document.getElementById('num_processors').value;
    let maxClockSyncError = document.getElementById('clock_sync_error').value;
    let broadcastDelay = document.getElementById('broadcast_delay').value;
    let datagramDelay = document.getElementById('datagram_delay').value;
    let checkInPeriod = document.getElementById('check_in_period').value;

    if (!isCheckInPeriodValid(maxClockSyncError, broadcastDelay, datagramDelay, checkInPeriod)) {
        alert('Error !!! Check in period is too small');
    } else {
        let data = {
            num_processors: numProcessors,
            max_clock_sync_error: maxClockSyncError,
            broadcast_delay: broadcastDelay,
            datagram_delay: datagramDelay,
            check_in_period: checkInPeriod
        }
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        }).then((response) => {
            if (response.status !== 200) {
                alert(`Request return status error!!! Status:${response.status}`);
            } else {
                fetchAndDisplayAllProcessors(true);
            }
        });
    }
}

function crashButtonOnClick() {
    console.log('crash clicked');
    const url = '/crash'
    let selected = document.getElementById('crash_processor').value.toString();
    let id = selected.substring(10, selected.length);

    let data = {processor_id: id}

    fetch(url, {
        method: 'POST',
        headers : {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    }).then((response) => {
        if (response.status !== 200) {
            alert('Crash failed');
        } else {
            fetchAndDisplayAllProcessors(true);
        }
    });
}

var timeout = undefined;

function init() {
    fetchAndDisplayAllProcessors(true);
}

/**
 * Fetches all the processors either working or crashed, and displays them in the page
 */
function fetchAndDisplayAllProcessors(updateAll) {
    if (timeout !== undefined) {
        clearTimeout(timeout);
    }
    updateDate();
    const url = '/all-processors';
    fetch(url).then((response) => {
            if (response.status === 200) {
                response.json().then((data) => {
                    updateProcessor(data, updateAll);
                    timeout = setTimeout(() => fetchAndDisplayAllProcessors(false), 1000);
                });
            }
    });
}

/**
 * Updates the timer displays on the page every second
 */
function updateDate() {
    let d = new Date();
    let dateElement = document.getElementById('current_time');
    dateElement.textContent = d.toString();
}

/**
 * Updates the processors displayed in the page
 * @param data
 * @param updateAll
 */
function updateProcessor(data, updateAll) {
    let list = document.querySelector('ul')
    let selectElement = document.getElementById('crash_processor')

    removeAllChildNodes(list);
    if (updateAll) {
        removeAllOptions(selectElement);
    }

    for (let processor of data) {
        let node = document.createElement('li');
        node.appendChild(document.createTextNode(
            `Processor ${processor.id}, 
                                status: ${processor.status}, 
                                members: ${processor.members}`));
        list.appendChild(node);

        if (updateAll) {
            let option = document.createElement('option');
            option.text = `Processor ${processor.id}`;
            selectElement.add(option);
        }
    }
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function removeAllOptions(selectElement) {
    let L = selectElement.options.length - 1;
    for (let i = L; i >= 0; i--) {
        selectElement.remove(i);
    }
}

/**
 * Returns true if the check in period is a valid value
 */
function isCheckInPeriodValid(maxClockSyncError, broadcastDelay, datagramDelay, checkInPeriod) {
    return checkInPeriod >= maxClockSyncError + broadcastDelay;
}