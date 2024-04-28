from pyscript import document
import radioactivedecay as rd
from radioactivedecay.utils import build_nuclide_string

from js import Uint8Array, File, URL, document
import io
import random

OUTPUT_DIV  = document.querySelector('#output')
INPUT_FIELD = document.querySelector('#nuclide-input')
MODE_BTN = document.querySelector('#mode-btn')

MODES = ['Most probable', 'Manual', 'Simulate']
ELEMENT_NAMES: dict = {"h":["hydrogen","wasserstoff"],"he":["helium"],"li":["lithium"],"be":["beryllium"],"b":["boron","bor"],"c":["carbon","kohlenstoff"],"n":["nitrogen","stickstoff"],"o":["oxygen","sauerstoff"],"f":["fluorine","fluor"],"ne":["neon"],"na":["sodium","natrium"],"mg":["magnesium"],"al":["aluminum","aluminium"],"si":["silicon","silicium"],"p":["phosphorus","phosphor"],"s":["sulfur","schwefel"],"cl":["chlorine","chlor"],"ar":["argon"],"k":["potassium","kalium"],"ca":["calcium"],"sc":["scandium"],"ti":["titanium","titan"],"v":["vanadium"],"cr":["chromium","chrom"],"mn":["manganese","mangan"],"fe":["iron","eisen"],"co":["cobalt"],"ni":["nickel"],"cu":["copper","kupfer"],"zn":["zinc","zink"],"ga":["gallium"],"ge":["germanium"],"as":["arsenic","arsen"],"se":["selenium","selen"],"br":["bromine","brom"],"kr":["krypton"],"rb":["rubidium"],"sr":["strontium"],"y":["yttrium"],"zr":["zirconium"],"nb":["niobium","niob"],"mo":["molybdenum","molybd\u00e4n"],"tc":["technetium"],"ru":["ruthenium"],"rh":["rhodium"],"pd":["palladium"],"ag":["silver","silber"],"cd":["cadmium"],"in":["indium"],"sn":["tin","zinn"],"sb":["antimony","antimon"],"te":["tellurium","tellur"],"i":["iodine","iod"],"xe":["xenon"],"cs":["cesium","caesium"],"ba":["barium"],"la":["lanthanum","lanthan"],"ce":["cerium","cer"],"pr":["praseodymium","praseodym"],"nd":["neodymium","neodym"],"pm":["promethium"],"sm":["samarium"],"eu":["europium"],"gd":["gadolinium"],"tb":["terbium"],"dy":["dysprosium"],"ho":["holmium"],"er":["erbium"],"tm":["thulium"],"yb":["ytterbium"],"lu":["lutetium"],"hf":["hafnium"],"ta":["tantalum","tantal"],"w":["tungsten","wolfram"],"re":["rhenium"],"os":["osmium"],"ir":["iridium","irudium"],"pt":["platinum","platin"],"au":["gold"],"hg":["mercury","quecksilber"],"tl":["thallium"],"pb":["lead","blei"],"bi":["bismuth","bismut"],"po":["polonium"],"at":["astatine","astat"],"rn":["radon"],"fr":["francium"],"ra":["radium"],"ac":["actinium"],"th":["thorium"],"pa":["protactinium"],"u":["uranium","uran"],"np":["neptunium"],"pu":["plutonium"],"am":["americium"],"cm":["curium"],"bk":["berkelium"],"cf":["californium"],"es":["einsteinium"],"fm":["fermium"],"md":["mendelevium"],"no":["nobelium"],"lr":["lawrencium"],"rf":["rutherfordium"],"db":["dubnium"],"sg":["seaborgium"],"bh":["bohrium"],"hs":["hassium"],"mt":["meitnerium"],"ds":["darmstadtium"],"rg":["roentgenium"],"cn":["copernicium"],"nh":["nihonium"],"fl":["flerovium"],"mc":["moscovium"],"lv":["livermorium"],"ts":["tennessine","tenness"],"og":["oganesson"]}

current_mode: int = 0

def get_symbol(element_name: str) -> str|None:
    for element in ELEMENT_NAMES.keys():
        if element_name.lower() in ELEMENT_NAMES[element]:
            return element
    return None

def generate_nuclide_card(nuclide_name: str, nuclide: rd.Nuclide) -> str:
    element_symbol: str = nuclide_name.split('-')[0]
    mass: str = nuclide_name.split('-')[1]
    decay_modes: list = nuclide.decay_modes()
    half_time: str = nuclide.half_life('readable')

    visual_type: str = ''
    
    if half_time == 'stable':
        visual_type = 'stable'
    elif len(decay_modes) == 0:
        visual_type = ''
    elif 'α' in decay_modes[0]:
        visual_type = 'alpha'
    elif 'β-' in decay_modes[0]:
        visual_type = 'betam'
    elif 'β+' in decay_modes[0]:
        visual_type = 'betap'

    return f'''
    <div class="nuclide-card {visual_type}">
        <div class="name">
            {element_symbol}<span class="number">{mass}</span>
        </div>
        <span class="time">{half_time}</span>
        <span class="decay">{','.join(decay_modes)}</span>
    </div>'''

def parse_nuclide_input(nuclide_input: str):
    nuclide_input = nuclide_input.lower()

    nuclide_input = nuclide_input.split('-',maxsplit=1)

    if not nuclide_input[0] in list(ELEMENT_NAMES.keys()):
        nuclide_input[0] = get_symbol(nuclide_input[0])
    
    return f'{nuclide_input[0]}-{nuclide_input[1]}'
    
def change_mode(event):
    global current_mode
    current_mode = (current_mode+1) % len(MODES)
    MODE_BTN.innerText = f'Mode: {MODES[current_mode]}'

def generate_image_url():
    bstream = io.BytesIO()

    download_btn = document.querySelector('#plot-download-btn')

    nuclide_name = download_btn.dataset.nuclide
    nuclide = rd.Nuclide(nuclide_name)
    fig, ax = nuclide.plot()
    fig.savefig(bstream)

    js_array = Uint8Array.new(len(bstream.getbuffer().tobytes()))
    js_array.assign(bstream.getbuffer())

    file = File.new([js_array], f'{nuclide_name}-chain.png', {type: 'image/png'})
    url = URL.createObjectURL(file)
    return (url, nuclide_name)

def download_plot(event):
    url, filename = generate_image_url()

    hidden_link = document.createElement('a')
    hidden_link.setAttribute('href', url)
    hidden_link.setAttribute('download', f'{filename}-chain.png')
    hidden_link.click()

def open_plot(event):
    url, filename = generate_image_url()

    hidden_link = document.createElement('a')
    hidden_link.setAttribute('href', url)
    hidden_link.setAttribute('target', '_blank')
    hidden_link.click()

def list_chain(event):
    nuclide_name = parse_nuclide_input(INPUT_FIELD.value)
    OUTPUT_DIV.innerHTML = f'''
    <section class="pre-results">
        <p><i>Searching for {nuclide_name}</i></p>
        <p>Plot Image of entire decay chain:</p>
        <div>
            <button data-nuclide="{nuclide_name}" data-type="download" id="plot-download-btn" class="btn" py-click="download_plot">Download</button>
            <button data-nuclide="{nuclide_name}" data-type="open" id="plot-download-btn" class="btn" py-click="open_plot">Open in new Tab</button>
        </div>
    </section>
    '''
    
    try:
        finished: bool = False
        index: int = 1
        while not finished:
            nuc = rd.Nuclide(nuclide_name)
            OUTPUT_DIV.innerHTML += generate_nuclide_card(build_nuclide_string(nuc.Z, nuc.A, nuc.state), nuc)
            OUTPUT_DIV.innerHTML += f'''
                <div class="extra-info">
                    <b>Number in Chain</b>: {index}<br>
                    <b>Protons</b>: {nuc.Z}<br>
                    <b>Nucleon</b>: {nuc.A}<br>
                    <b>Halftime</b>: {nuc.half_life("readable")}<br>
                    <b>Progeny</b>: {nuc.progeny()}
                </div>
                <hr>
            '''
            nuc.branching_fractions()
            nuc.decay_modes()

            if len(nuc.progeny()) > 0:
                match current_mode:
                    case 0: # Most Probable
                        progeny_index = 0
                    case 1: # Manual
                        # Not implemented
                        progeny_index = 0
                        OUTPUT_DIV.innerHTML += '<b>Manual mode not implemented!</b> <i>Using Most Probable instead</i>:'
                    case 2: # Simulate
                        if len(nuc.progeny()) > 1:
                            progeny_index = -1
                            number = random.random()
                            helper = 0

                            for i, fraction in enumerate(reversed(nuc.branching_fractions())):
                                helper += fraction
                                print(f'{helper=}, {fraction=}')
                                if number <= helper:
                                    progeny_index = len(nuc.branching_fractions()) - 1 - i
                                    break
                            print(f'{number} -> {progeny_index} {nuc.branching_fractions()}')
                            if progeny_index == -1:
                                progeny_index = 0
                                print('Error: Something went wrong')
                        else:
                            progeny_index = 0
                    
                OUTPUT_DIV.innerHTML += f'↓ {nuc.decay_modes()[progeny_index]} ({nuc.branching_fractions()[progeny_index]*100}%)<hr>'
                nuclide_name = nuc.progeny()[0]
                index += 1
            else:
                finished = True
    except ValueError:
        OUTPUT_DIV.innerHTML = 'Invalid Nuclide Name'




# Removing Loading screen
document.querySelector('.loading-screen').classList.remove('active')
document.querySelector('main').classList.add('active')


# Table Generator
table = document.querySelector('#table')
EXTRA_CLASSES = ["d-nonmetal gas", "n-gas gas", "al-metal", "alearth-metal", "metalloid", "patomic-nonmetal", "d-nonmetal gas", "d-nonmetal gas", "d-nonmetal gas", "n-gas gas", "al-metal", "alearth-metal", "pTransition-metal", "metalloid", "patomic-nonmetal", "patomic-nonmetal", "d-nonmetal gas", "n-gas gas", "al-metal", "alearth-metal", "trans", "trans", "trans", "trans", "trans", "trans", "trans", "trans", "trans", "pTransition-metal", "pTransition-metal", "metalloid", "metalloid", "patomic-nonmetal", "d-nonmetal liquid", "n-gas gas", "al-metal", "alearth-metal", "trans", "trans", "trans", "trans", "trans", "trans", "trans", "trans", "trans", "pTransition-metal", "pTransition-metal", "pTransition-metal", "metalloid", "metalloid", "d-nonmetal", "n-gas gas", "al-metal", "alearth-metal", "lan lan-group", "lan lan-group", "lan lan-group", "lan lan-group", "lan lan-group", "lan lan-group", "lan lan-group", "lan lan-group", "lan lan-group", "lan lan-group", "lan lan-group", "lan lan-group", "lan lan-group", "lan lan-group", "lan lan-group", "trans", "trans", "trans", "trans", "trans", "trans", "trans", "trans", "pTransition-metal", "pTransition-metal", "pTransition-metal", "pTransition-metal", "pTransition-metal", "metalloid", "n-gas gas", "al-metal", "alearth-metal", "act act-group", "act act-group", "act act-group", "act act-group", "act act-group", "act act-group", "act act-group", "act act-group", "act act-group", "act act-group", "act act-group", "act act-group", "act act-group", "act act-group", "act act-group", "trans", "trans", "trans", "trans", "trans", "trans", "trans", "trans", "trans", "trans", "trans", "trans", "trans", "trans", "n-gas gas"]
for number, element in enumerate(ELEMENT_NAMES.keys()):
    table.innerHTML += f'''
    <div tabindex='0' class='ele ele-{number+1} {EXTRA_CLASSES[number]}' onclick='select_element("{ELEMENT_NAMES[element][0]}");'> 
        <div class='ele-name' title='{ELEMENT_NAMES[element][0]}'> 
            {element}
        </div> 
    </div> 
    '''