/* add more from: https://gist.github.com/meain/6440b706a97d2dd71574769517e7ed32 */
const LOADING_MESSAGES = [
    'Decay in progress... atoms are feeling flaky today!',
    'Counting down... fingers crossed for a chain reaction!',
    'Loading decay chains... atoms are doing their dance!',
    'Hold tight... atoms are shaking off their electrons!',
    'Decay in progress... atoms are feeling flaky today!',
    'This may take a minute...',
    'Loading radioactive jokes...',
    'Waiting for atoms to finish their transformation...',
    'Fetching some decay rates... they\'re decaying at their own pace',
    'Should have used a compiled language...'
]
var unused_messages = JSON.parse(JSON.stringify(LOADING_MESSAGES));
var label = document.getElementById('loading-message');

function change_loading_message() {
    label.animate(
        {
            opacity: [1,0],
            transform: ['translateY(0)', 'translateY(-.5rem)']
        },
        500
    )
    setTimeout(finish_change_loading_animation, 500)
}

function finish_change_loading_animation() {
    let old_message = label.innerText;
    let new_message = old_message;

    if (unused_messages.length == 0) {
        unused_messages = JSON.parse(JSON.stringify(LOADING_MESSAGES));
    }
    while (new_message == old_message) {
        new_message = unused_messages[Math.floor(Math.random() * unused_messages.length)];
    }
    label.innerText = new_message;
    let index = unused_messages.indexOf(new_message);
    unused_messages.splice(index, 1);
    
    label.animate(
        {
            opacity: [0,1],
            transform: ['translateY(.5rem)', 'translateY(0)'],
            easing: ["ease-in-out", "ease-in-out"]
        },
        500
    )
}

let message_timer = setInterval(change_loading_message, 2800);

var pse_selector = document.getElementById('pse-selector');
var nuclide_input = document.getElementById('nuclide-input');
var pse_btn = document.getElementById('pse-btn');

function hide_pse() { pse_selector.classList.remove('active'); }
function show_pse() { pse_selector.classList.add('active'); }
function select_element(element) { nuclide_input.value = element+'-'; nuclide_input.focus() }

pse_selector.addEventListener('click', hide_pse);
pse_btn.addEventListener('click', show_pse);