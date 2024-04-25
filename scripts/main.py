from pyscript import document
import radioactivedecay as rd

OUTPUT_DIV  = document.querySelector('#output')
INPUT_FIELD = document.querySelector('#nuclide-input')

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

def test(event):
    nuclide_name = INPUT_FIELD.value

    try:
        nuc = rd.Nuclide(nuclide_name)
        OUTPUT_DIV.innerHTML = generate_nuclide_card(nuclide_name, nuc)
        OUTPUT_DIV.innerHTML += f'Protons: {nuc.Z}<br>Nucleon: {nuc.A}<br>Halftime: {nuc.half_life("readable")}<br>Progeny: {nuc.progeny()}'
    except ValueError:
        OUTPUT_DIV.innerHTML = 'Invalid Nuclide Name'




# Removing Loading screen
document.querySelector('.loading-screen').classList.remove('active')
document.querySelector('main').classList.add('active')