function startButtonOnclick() {
    console.log("Start clicked");
    const url = '/init-processors'
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
                fetchAndDisplayAllProcessors();
            }
        });
    }
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
            let selectElement = document.getElementById('crash_processor')

            removeAllChildNodes(list);
            removeAllOptions(selectElement);

            for (let processor of data) {
                let node = document.createElement('li');
                node.appendChild(document.createTextNode(`Processor ${processor.id}, members: ${processor.members}`));
                list.appendChild(node);

                let option = document.createElement('option');
                option.text = `Processor ${processor.id}`;
                selectElement.add(option);
            }
        });
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function removeAllOptions(selectElement) {
    let L = selectElement.options.length - 1;
    for(let i = L; i >= 0; i--) {
        selectElement.remove(i);
    }
}

/**
 * Returns true if the check in period is a valid value
 */
function isCheckInPeriodValid(maxClockSyncError, broadcastDelay, datagramDelay, checkInPeriod) {
    return checkInPeriod >= maxClockSyncError + broadcastDelay;
}