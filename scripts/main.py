from pyscript import document
import radioactivedecay as rd
from radioactivedecay.utils import build_nuclide_string

from js import Uint8Array, File, URL, document
import io


OUTPUT_DIV  = document.querySelector('#output')
INPUT_FIELD = document.querySelector('#nuclide-input')
MODE_BTN = document.querySelector('#mode-btn')

MODES = ['Most probable', 'Manual', 'Random']
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

def generate_image(event):
    bstream = io.BytesIO()

    download_btn = document.querySelector('#plot-download-btn')


    nuclide = rd.Nuclide(download_btn.dataset.nuclide)
    fig, ax = nuclide.plot()
    fig.savefig(bstream)

    js_array = Uint8Array.new(len(bstream.getbuffer().tobytes()))
    js_array.assign(bstream.getbuffer())

    file = File.new([js_array], 'chain.png', {type: 'image/png'})
    url = URL.createObjectURL(file)

    hidden_link = document.createElement('a')
    hidden_link.setAttribute('download', 'chain.png')
    hidden_link.setAttribute('href', url)
    hidden_link.click()

def list_chain(event):
    nuclide_name = parse_nuclide_input(INPUT_FIELD.value)
    OUTPUT_DIV.innerHTML = f'''
    <section class="pre-results">
        <p><i>Searching for {nuclide_name}</i></p>
        <button data-nuclide="{nuclide_name}" id="plot-download-btn" class="btn" py-click="generate_image">Download Plot of entire decay chain</button>
    </section>
    '''
    

    try:
        finished: bool = False
        index: int = 1
        while not finished:
            nuc = rd.Nuclide(nuclide_name)
            OUTPUT_DIV.innerHTML += generate_nuclide_card(build_nuclide_string(nuc.Z, nuc.A, nuc.state), nuc)
            OUTPUT_DIV.innerHTML += f'Number in Chain: {index}<br>Protons: {nuc.Z}<br>Nucleon: {nuc.A}<br>Halftime: {nuc.half_life("readable")}<br>Progeny: {nuc.progeny()}<hr>'

            if len(nuc.progeny()) > 0:
                nuclide_name = nuc.progeny()[0]
                index += 1
            else:
                finished = True
    except ValueError:
        OUTPUT_DIV.innerHTML = 'Invalid Nuclide Name'




# Removing Loading screen
document.querySelector('.loading-screen').classList.remove('active')
document.querySelector('main').classList.add('active')